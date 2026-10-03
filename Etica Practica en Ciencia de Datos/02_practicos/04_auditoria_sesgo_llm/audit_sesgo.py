#!/usr/bin/env python3
"""Factorial LLM-as-judge audit: one swapped field, everything else fixed."""

from __future__ import annotations

import argparse
import copy
import json
import os
import statistics
from pathlib import Path
from typing import Any
from urllib.error import URLError
from urllib.request import Request, urlopen

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


def load_config(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if path.suffix in {".yaml", ".yml"}:
        if yaml is None:
            raise RuntimeError("PyYAML required for YAML configs")
        return yaml.safe_load(text)
    return json.loads(text)


def set_path(obj: Any, dotted: str, value: Any) -> Any:
    root = copy.deepcopy(obj)
    parts = dotted.split(".")
    cur = root
    for p in parts[:-1]:
        cur = cur[p]
    cur[parts[-1]] = value
    return root


def generate_dataset(cfg: dict[str, Any]) -> list[dict[str, Any]]:
    repeats = int(cfg["repeats"])
    path = cfg["factor"]["path"]
    rows: list[dict[str, Any]] = []
    n = 0
    for group, levels in cfg["factor"]["groups"].items():
        for level in levels:
            for tier, template in cfg["templates"].items():
                for _ in range(repeats):
                    n += 1
                    body = set_path(template, path, level)
                    body["_meta_group"] = group
                    body["_meta_tier"] = str(tier)
                    body["_meta_level"] = level
                    body["candidate_id"] = f"CAND_{n:04d}"
                    rows.append(body)
    return rows


def welch_t(a: list[float], b: list[float]) -> tuple[float, float]:
    """Mean(a)-mean(b) and a two-sided p-value via Welch df + normal-ish t (scipy-free)."""
    if len(a) < 2 or len(b) < 2:
        return float("nan"), float("nan")
    ma, mb = statistics.mean(a), statistics.mean(b)
    va, vb = statistics.variance(a), statistics.variance(b)
    na, nb = len(a), len(b)
    se = (va / na + vb / nb) ** 0.5
    if se == 0:
        return ma - mb, 1.0 if ma == mb else 0.0
    t = (ma - mb) / se
    # Welch-Satterthwaite df
    num = (va / na + vb / nb) ** 2
    den = (va / na) ** 2 / (na - 1) + (vb / nb) ** 2 / (nb - 1)
    df = num / den if den else float("inf")
    p = _t_sf_two_sided(abs(t), df)
    return ma - mb, p


def _t_sf_two_sided(t: float, df: float) -> float:
    # Regularized incomplete beta for Student's t survival; enough for tests.
    import math

    x = df / (df + t * t)
    # I_x(df/2, 1/2) ≈ p two-sided for |T|>t
    a, b = df / 2.0, 0.5
    # continued fraction incomplete beta (numerical recipes style, short)
    def betai(aa: float, bb: float, xx: float) -> float:
        if xx <= 0:
            return 0.0
        if xx >= 1:
            return 1.0
        lbeta = math.lgamma(aa) + math.lgamma(bb) - math.lgamma(aa + bb)
        front = math.exp(math.log(xx) * aa + math.log(1 - xx) * bb - lbeta) / aa
        # continued fraction
        c, d = 1.0, 1.0 - (aa + bb) * xx / (aa + 1)
        d = 1.0 / d if d else 1e30
        h = d
        for m in range(1, 80):
            m2 = 2 * m
            num = m * (bb - m) * xx / ((aa + m2 - 1) * (aa + m2))
            d = 1.0 + num * d
            c = 1.0 + num / c
            d = 1.0 / d if d else 1e30
            h *= d * c
            num = -(aa + m) * (aa + bb + m) * xx / ((aa + m2) * (aa + m2 + 1))
            d = 1.0 + num * d
            c = 1.0 + num / c
            d = 1.0 / d if d else 1e30
            h *= d * c
        return front * h

    p = betai(a, b, x)
    return min(1.0, max(0.0, p))


def analyze(results: list[dict[str, Any]], score_field: str, reference_group: str) -> list[dict[str, Any]]:
    buckets: dict[tuple[str, str], list[float]] = {}
    for r in results:
        ev = r.get("evaluation") or {}
        score = ev.get(score_field, r.get(score_field))
        if score is None:
            continue
        key = (str(r.get("_meta_tier")), str(r.get("_meta_group")))
        buckets.setdefault(key, []).append(float(score))
    tiers = sorted({k[0] for k in buckets})
    groups = sorted({k[1] for k in buckets})
    out = []
    for tier in tiers:
        ref = buckets.get((tier, reference_group), [])
        for g in groups:
            if g == reference_group:
                continue
            other = buckets.get((tier, g), [])
            diff, p = welch_t(other, ref)  # group - reference (Mina: UNC - US)
            out.append(
                {
                    "tier": tier,
                    "comparison": f"{g} - {reference_group}",
                    "n_group": len(other),
                    "n_reference": len(ref),
                    "mean_diff": diff,
                    "p_welch": p,
                }
            )
    return out


def chat_complete(cfg: dict[str, Any], user: str) -> dict[str, Any]:
    model = cfg["model"]
    url = model["base_url"].rstrip("/") + "/chat/completions"
    payload = {
        "model": model["name"],
        "temperature": float(model.get("temperature", 0.1)),
        "messages": [
            {"role": "system", "content": cfg["system_prompt"]},
            {"role": "user", "content": user},
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "score",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "reasoning": {"type": "string"},
                        "final_score": {"type": "integer"},
                    },
                    "required": ["reasoning", "final_score"],
                    "additionalProperties": False,
                },
            },
        },
    }
    req = Request(
        url,
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + str(model.get("api_key") or os.environ.get("OPENAI_API_KEY") or "x"),
        },
        method="POST",
    )
    with urlopen(req, timeout=120) as resp:
        body = json.loads(resp.read().decode())
    content = body["choices"][0]["message"]["content"]
    return json.loads(content)


def cmd_generate(cfg: dict[str, Any], out: Path) -> None:
    rows = generate_dataset(cfg)
    out.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")


def cmd_run(cfg: dict[str, Any], dataset_path: Path, out: Path) -> None:
    candidates = json.loads(dataset_path.read_text(encoding="utf-8"))
    results = []
    if out.exists():
        results = json.loads(out.read_text(encoding="utf-8") or "[]")
    done = {r["candidate_id"] for r in results}
    for cand in candidates:
        cid = cand["candidate_id"]
        if cid in done:
            continue
        payload = {k: v for k, v in cand.items() if not k.startswith("_meta")}
        try:
            parsed = chat_complete(cfg, json.dumps(payload, ensure_ascii=False))
        except (URLError, TimeoutError, json.JSONDecodeError, KeyError) as exc:
            print(f"[FAIL] {cid} {exc}")
            continue
        rec = {
            "candidate_id": cid,
            "_meta_group": cand.get("_meta_group"),
            "_meta_tier": cand.get("_meta_tier"),
            "_meta_level": cand.get("_meta_level"),
            "evaluation": parsed,
        }
        results.append(rec)
        out.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[OK] {cid} {parsed.get('final_score')}")


def cmd_analyze(path: Path, score_field: str, reference_group: str) -> None:
    results = json.loads(path.read_text(encoding="utf-8"))
    table = analyze(results, score_field, reference_group)
    print(json.dumps(table, indent=2))


def main() -> None:
    p = argparse.ArgumentParser(description="Agnostic one-factor LLM judge audit")
    p.add_argument("cmd", choices=["generate", "run", "analyze"])
    p.add_argument("-c", "--config", type=Path, default=Path("config.example.yaml"))
    p.add_argument("--dataset", type=Path, default=Path("dataset.json"))
    p.add_argument("--results", type=Path, default=Path("results.json"))
    args = p.parse_args()
    cfg = load_config(args.config)
    if args.cmd == "generate":
        cmd_generate(cfg, args.dataset)
        print(f"wrote {args.dataset}")
    elif args.cmd == "run":
        cmd_run(cfg, args.dataset, args.results)
    else:
        cmd_analyze(args.results, cfg.get("score_field", "final_score"), cfg["reference_group"])


if __name__ == "__main__":
    main()
