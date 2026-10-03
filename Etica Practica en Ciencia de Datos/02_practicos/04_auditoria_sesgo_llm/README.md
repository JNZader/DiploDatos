# Auditoría agnóstica de sesgo (LLM-as-judge)

Metodología: `METODOLOGIA.md`. Código: un factor, templates YAML, modelo OpenAI-compatible.

```bash
python3 -m unittest tests.test_audit_sesgo -v
python3 audit_sesgo.py generate -c config.example.yaml --dataset dataset.json
# apunta model.base_url a LM Studio / vLLM / gateway
python3 audit_sesgo.py run -c config.example.yaml --dataset dataset.json --results results.json
python3 audit_sesgo.py analyze -c config.example.yaml --results results.json
```

YAML necesita PyYAML. El `run` no se testea en CI (red).
