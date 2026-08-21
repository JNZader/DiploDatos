# Guía de estudio DiploDatos–SAIJ

Este directorio contiene el lector de la guía consolidada de DiploDatos aplicada al caso SAIJ. El sitio se publica en <https://jnzader.github.io/DiploDatos/> mediante el flujo de GitHub Pages del repositorio.

## Recorrido rápido

1. Cree el entorno e instale las dependencias fijadas.
2. Ejecute las pruebas; validan las nueve páginas comprometidas sin necesitar la fuente canónica local.
3. Construya el sitio en modo estricto.
4. Use el servidor local cuando quiera leer o revisar cambios.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m unittest discover -s tests -v
NO_MKDOCS_2_WARNING=1 .venv/bin/mkdocs build --strict
.venv/bin/mkdocs serve
```

MathJax 3.2.2 está incluido en `docs/assets/vendor/mathjax/`. La lectura y la publicación no descargan scripts ni hojas de estilo de terceros; los enlaces de referencia del contenido pueden apuntar a sitios externos.

## Fuente comprometida y verificación

| Elemento | Propósito |
| --- | --- |
| Nueve páginas Markdown | Conservan, en orden, cada byte de la guía verificada. |
| `source-manifest.json` | Registra hash, conteos y correspondencia de cada página sin rutas absolutas. |
| `tests/test_sync_guide.py` | Reconstruye las páginas comprometidas y verifica hash, palabras, líneas, encabezados y manifiesto. |
| `scripts/sync_guide.py` | Regenera el contenido solo cuando se dispone de una fuente canónica autorizada. |

La verificación habitual no lee `Mentoria Jurisprudencia/**` ni ningún archivo externo a este directorio. La fuente canónica solo es necesaria para regenerar las páginas:

```bash
.venv/bin/python scripts/sync_guide.py --source "$CANONICAL_GUIDE"
```

La herramienta detiene la generación si falta un límite, aparece duplicado, cambia el orden canónico o no coinciden el hash y los conteos esperados.

## Publicación

El flujo `/.github/workflows/pages.yml` se activa manualmente o ante cambios relevantes en `main`. Prueba y construye únicamente este lector, sube solo el sitio generado y lo despliega mediante el entorno protegido `github-pages`; después realiza una comprobación HTTP acotada.

Videos, PDF, notebooks, datasets, originales del curso y datos personales quedan fuera del artefacto publicado.
