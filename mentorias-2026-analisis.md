# Análisis de Mentorías DiploDatos 2026 — Selección estratégica para perfil de IA/Backend

> **Fecha:** 2026-06-26
> **Autor del análisis:** Javier (JNZader) + asistente
> **Objetivo:** Elegir 5 mentorías (de 18) que potencien un perfil de **ingeniería de IA + backend**, priorizando **metodologías y tecnologías** por encima del tema. Más proyectos complementarios para reforzar cada una.
> **Fuente oficial:** https://sites.google.com/unc.edu.ar/mentorias-diplodatos-2026/inicio

---

## 0. Perfil de referencia (contra qué se evalúa)

Arquitecto backend / ingeniería de IA. Stack y fortalezas:

- **Lenguajes/frameworks:** Go, TypeScript, Angular/React, Next.js.
- **Datos/infra:** PostgreSQL, RLS, multi-tenant SaaS, Docker, CI/CD, testing.
- **IA-engineering:** RAG, embeddings, vector indexes (pgvector/HNSW), LLM orchestration, multi-agente, evaluación de LLMs (LLM-as-judge), prompt engineering.
- **Metodología:** Clean/Hexagonal architecture, SDD (spec-driven development), code generation.

**Lente de evaluación:** no importa el dominio del dato; importa (1) qué metodología/tecnología nueva o de frontera ofrece, (2) cuánto apalanca lo que YA sé, (3) cuánto me **diferencia** del resto de la cohorte (que serán data scientists puros).

**Dato estructural:** en 4 años (2022–2025) la diplo NUNCA tocó MLOps, agentes, LLMs ni vector DBs. Todo fue DS/ML clásico. Por lo tanto, traiga la mentoría que traiga, llego con un stack que el programa históricamente no vio. La ventaja es estructural.

---

## 1. Metodología del análisis (3 lentes)

El análisis se construyó en capas, cada una corrigiendo sesgos de la anterior:

1. **Lente 1 — Descripción oficial:** las 18 subpáginas del Google Sites (título, metodología declarada, stack, entregables, datos).
2. **Lente 2 — Código real de los repos:** inspección con `gh` de la estructura, `README.md` y `requirements.txt` de los repos. **Reveló cosas que la descripción escondía** (ej.: M17 es un sistema con Postgres/Docker/tests; M03 tiene `requirements.txt` vacío = greenfield).
3. **Lente 3 — Historial 2022–2025:** cruce contra 4 años de mentorías previas para detectar **linajes** (temas recurrentes = madurez/bajo riesgo) y **rarezas** (metodologías que casi no aparecen = mayor diferenciación).

**Cobertura de verificación:**
- Las 18 descripciones: ✅ leídas.
- Repos de las 5 finalistas: ✅ inspeccionados a fondo (M02 no tiene repo, es Google Sheets).
- Repos de las 13 descartadas: ✅ inspeccionados para confirmar que no se escapó ninguna joya (M09 dio 404, no verificable; M05/M11 sin repo).
- Historial 2022–2025: ✅ cruzado a nivel título/dominio.

---

## 2. Las 18 mentorías de 2026 (mapa completo)

| # | Título | Dominio | Nota perfil |
|---|--------|---------|-------------|
| M01 | El Factor D10S: abandono escolar | Educación / tabular ML | Descartada (boosting redundante con M06) |
| M02 | DataLab CONICET: ciencia en Córdoba | Research analytics / **redes** | **TOP 5** |
| M03 | Clasificación de Jurisprudencia Argentina | **NLP / semantic search / RAG** | **TOP 5 — #1** |
| M04 | Predicciones en el Espacio (satélites/desechos) | Tabular ML | Descartada |
| M05 | Clasificación clientes telco (reclamos) | Clustering | Descartada |
| M06 | Ciencia de Datos aplicada al Fútbol | **ML avanzado (boosting/SHAP)** | **TOP 5** |
| M07 | Industria del gaming en PC (Steam) | Tabular ML | Descartada |
| M08 | Detección de fraude bancario | Clasificación | Descartada |
| M09 | Impacto Global de la IA | ML sobre datos sintéticos | Descartada (repo 404) |
| M10 | Cobertura terrestre en salares (SalarIA) | **Geoespacial / teledetección** | Descartada (fuera de lane) |
| M11 | Actividad eléctrica atmosférica | Random Forest / radar | Descartada |
| M12 | Regímenes de mercado financiero | **Series temporales** | **TOP 5** |
| M13 | Rendimiento académico / riesgo temprano | Tabular ML | Descartada |
| M14 | Riesgo de diabetes (ENFR 2018) | Tabular ML salud | Descartada |
| M15 | Centollas en el Canal Beagle | Clustering | Descartada |
| M16 | Inventarios Forestales (biomasa) | Geoespacial / tabular | Descartada |
| M17 | Detección de ofertas hoteleras | **Anomaly detection + sistema desplegable** | **TOP 5 — #2** |
| M18 | Carrito en Black Friday | Tabular ML retail | Descartada |

---

## 3. TOP 5 — Análisis profundo

### 🥇 #1 — M03: Jurisprudencia (NLP + Buscador Semántico)

- **Mentor:** Adrián Zelaya — [LinkedIn](https://www.linkedin.com/in/adrian-zelaya/)
- **Repo:** https://github.com/adrian-alejandro/mentoria-diplodatos-2026-clasificacion-y-busqueda-textos-legales
- **Datos:** HuggingFace `marianbasti/jurisprudencia-Argentina-SAIJ` (miles de fallos del SAIJ) + dataset auxiliar de PDFs/DOCs/HTMLs CRUDOS a extraer.

**Qué se construye:** pipeline NLP completo que termina en un **motor de búsqueda semántico**. Recorrido: BoW → TF-IDF → **embeddings** → retrieval por query en lenguaje natural. El README declara textualmente que sienta *"la base técnica y conceptual sobre la cual escalar hacia un sistema RAG"*.

**Stack/metodología (TP por TP):**
- TP1: EDA dual (estructurado: distribución por fuero, desbalance, sesgo temporal / texto: longitud, vocabulario, n-gramas, términos por fuero).
- TP2: lematización, normalización, y **representación numérica comparada** (BoW vs TF-IDF vs embeddings).
- TP3: (a) clustering no-supervisado de tópicos latentes; (b) clasificación supervisada multi-modelo (¿predecir el fuero leyendo solo el sumario?); (c) **motor de búsqueda semántico** vía embeddings.

**Evidencia de repo:** `requirements.txt` **VACÍO** = greenfield total. Repo mínimo (muestra + notebook de descarga + notebook de extracción de texto). Máxima libertad, mínimo scaffolding. Ideal para quien trae su propia sofisticación de RAG.

**Conexión con el perfil:** DIRECTA. Apalanca `rag-advanced`, `embedding-strategies`, `vector-index-tuning`. Es continuidad pura de la trayectoria de IA-engineering.

**Historial (lente 3):** es la **cima de una línea de 4 años** de NLP de textos legales:
- 2022 M21 "Búsqueda y Recomendación para Textos Legales"
- 2023 M13 "Clasificador de Pliegos con PLN" + M11 "Detección de Plagio"
- 2024 NLP en foros/redes (M07, M13)
- 2025 M05 tweets + M18 "Lectura Distante de Canciones"
- **2026 M03 = la PRIMERA en dar el salto a búsqueda semántica + RAG.** En 4 años nadie construyó un sistema de retrieval con embeddings.

**Nota: 10/10.** Tema con pedigrí + frontera tecnológica + skills más raras justo ahí.

---

### 🥈 #2 — M17: Detección de Ofertas Hoteleras (Sistema desplegable)

- **Mentor:** Martín Rodríguez Núñez (ID90Travel, industria real)
- **Repo:** https://github.com/martinid90/id90-hotel-deals-analysis
- **Datos:** búsquedas históricas reales 2024+2025 (~600MB, Google Drive) + `destination_with_nearest.csv` (~26.000 ciudades).

**Qué se construye:** sistema que decide si un precio es **ganga real, normal o inflado** mediante detección de anomalías sobre datos históricos.

**Stack/metodología (TP por TP):**
- TP1: definición de "mercado" (geografía, día, estacionalidad, categoría, duración) → segmentos homogéneos.
- TP2: **normalización** (`precio_total / (noches × habitaciones × personas)`), feature engineering de contexto, auditoría de calidad.
- TP3: detección de precios anómalos con enfoque libre (estadístico/supervisado/no-supervisado/híbrido), con el desafío de **diseñar métricas SIN labels externos** + análisis de sensibilidad.

**Evidencia de repo (EL HALLAZGO CLAVE):** NO es un notebook, es un **sistema de software**:
```
app.py · pipeline_build_baselines.py · test_system.py · Dockerfile
config.py · auxiliary_functions.py
requirements: streamlit · psycopg2-binary (Postgres) · pandas · numpy · scipy · python-dotenv
```
Es el ÚNICO de los 5 con estructura de ingeniería real: app desplegable, conexión a DB, tests, contenedor. El mentor ya dejó una baseline estadística como referencia (honesto sobre sus límites).

**Conexión con el perfil:** tus skills backend (Postgres/Docker/tests/diseño de sistema) aplican DIRECTO. Es donde más **destacás sobre la cohorte**, que entregará notebooks.

**Historial:** linaje de detección de anomalías (2022 M02 despachos de combustible, 2022 M12 fraude tarjetas) + empresas reales recurrentes. Pero la estructura de software desplegable es **rara incluso históricamente**.

**Nota: 9/10 (puesto 2 para el perfil).**

---

### 🥉 #3 — M06: Ciencia de Datos aplicada al Fútbol (ML avanzado)

- **Mentor:** Guillermo F. Alonso — [LinkedIn](https://www.linkedin.com/in/ingalonso/)
- **Repo:** https://github.com/guillealonso/futbol-ciencia-datos-2026
- **Datos:** Wyscout 2017/18 — **3.251.294 eventos · 1.941 partidos · 4.299 jugadores · 142 equipos**, en Parquet columnar.

**Qué se construye:** el pipeline de ML **más sofisticado de las 18**. Frameworks industria: **VAEP, xT, SPADL** (socceraction).

**Stack/metodología (TP por TP):**
- TP1: shot maps, heat maps, redes de pases, radares, **xG baseline con regresión logística**.
- TP2: conversión Wyscout → **SPADL** con socceraction, outliers, feature engineering, normalización por posición/minutos.
- TP3: **xT + VAEP completos**, **XGBoost + LightGBM con cross-validation por partido** (anti-leakage), **SHAP**, **K-Means + UMAP**, scouting con **cosine similarity**.

**Evidencia de repo:** mejor ingeniería DS de las 5. `requirements.txt` PINNEADO (`scikit-learn 1.8.0`, `socceraction 1.5.3`, `mplsoccer`, `pyarrow`). README grado profesional (badges, citas académicas Decroos 2019 / Singh 2019). **Caveat:** solo está publicado el notebook P1 (EDA); `xgboost`/`lightgbm` aún NO están en requirements — el boosting llega en TP3 (todavía no subido).

**Conexión con el perfil:** llena el **gap de modelado ML serio** con lo más vendible del mercado (gradient boosting + SHAP + CV bien hecha). El core de ML no es tu lane, pero es el certificado de "sé modelar de verdad".

**Historial:** ya corrió en 2025 (M12 "Métricas Avanzadas en el Fútbol"). Tema maduro, 2º año, bajo riesgo.

**Nota: 9/10 (diversificación).**

---

### #4 — M02: DataLab CONICET (Análisis de Redes)

- **Mentora:** Alfonsina Szpeiner (15 años gestionando datos en CONICET).
- **Repo:** ninguno — datos en Google Sheets (muestra anonimizada, 42 unidades ejecutoras de Córdoba).

**Qué se construye:** caracterización de perfiles institucionales del CONICET Córdoba para informar política científica (marco ODS).

**Stack/metodología (TP por TP):**
- TP1: exploración (SIGEVA/SIGERH), estadística descriptiva, visualizaciones.
- TP2: curación, **one-hot encoding**, series temporales, combinación multi-año.
- TP3: clustering sobre categóricas, **método del codo**, word clouds, y — el diferencial — **redes de co-ocurrencia de investigadores**.

**Conexión con el perfil:** apuesta de **diversificación metodológica pura**. El **análisis de redes / grafos** es lo ÚNICO genuinamente nuevo en la caja (transferible a dependencias de código, knowledge graphs, recomendación). Datos administrativos REALES.

**Historial:** corrió en 2025 (M08 "Quiénes son los científicos del CONICET"). Linaje histórico = analítica descriptiva → es la más "soft" técnicamente. Entra al top 5 exclusivamente por el ángulo de redes.

**Nota: 6.5/10 (comodín por metodología única).**

---

### #5 — M12: Regímenes de Mercado Financiero (Series Temporales)

- **Mentor:** Francisco Michati — [LinkedIn](https://www.linkedin.com/in/francisco-michati/)
- **Repo:** https://github.com/FranciscoMichati/MentoriasDiplodatos2026-RegimenesFinancieros
- **Datos:** 9 activos de Yahoo Finance (SPY, QQQ, IWM, TLT, IEF, LQD, GLD, DBC, ^VIX) desde feb-2006.

**Qué se construye:** identificación de regímenes de mercado (calma/estrés/transición). Excluye explícitamente predicción de precios y trading.

**Stack/metodología (TP por TP):**
- TP1: series de precio/volumen, retornos diarios, crisis históricas (2008, COVID).
- TP2: **volatilidad rolling, retornos acumulados, correlaciones rolling**, matriz de correlación, **PCA** opcional.
- TP3: clustering **K-means** de regímenes (validado contra crisis) + clasificación (asignación a cluster vs. supervisado: logística baseline, RF opcional).

**Evidencia de repo:** stack vainilla sin pins (`yfinance, pandas, numpy, matplotlib, seaborn, scikit-learn`). Templates limpios (TP1/TP2/TP3). Prolijo y didáctico, cero sorpresas técnicas.

**Conexión con el perfil:** suma **series temporales** (herramienta nueva, transferible a métricas/logs/telemetría). Poco más.

**Historial (CAVEAT IMPORTANTE):** finanzas/series temporales es **el tema MÁS trillado** de la diplo — aparece TODOS los años, varias veces (2022 cripto/sentiment/fintech, 2023 score crediticio/NLP trading, 2024 series financieras/inflación, 2025 churn finanzas/offers). Templates maduros, pero **el menos diferenciador**: muchos egresados ya hicieron finanzas.

**Nota: 7/10 técnicamente, pero baja al #5 por ser el camino más transitado.**

---

## 4. Verificación de las 13 descartadas (anti-sesgo de fuente)

El triage 18→5 inicial usó solo descripciones. Para cerrar la grieta, se inspeccionaron los repos de las descartadas. **Resultado: ninguna desplaza al top 5.**

| Mentoría | Repo — hallazgo real | Veredicto |
|----------|----------------------|-----------|
| M01 Abandono | `requirements`: xgboost+lightgbm, estructura prolija (`deliverables/`, `src/`) | Boosting redundante con M06 |
| M04 Space Debris | Dockerfile + docker-compose + polars + `src/get_data.py` | Higiene de ing. PERO dataset trivial (262 obj), `requirements`=1 línea |
| M07 Steam | `parser.py` + docs, sin requirements | Bare |
| M08 Fraude | 3 notebooks | Estándar |
| M09 IA Impact | **404 — no verificable** (datos sintéticos según descripción) | No confirmado |
| M10 SalarIA | **Geoespacial real:** Sentinel-2, rasters .tif, GeoJSON | Modalidad nueva (CV satelital) pero fuera de lane |
| M14 Diabetes | solo README | Vacío |
| M15 Centollas | solo README | Vacío |
| M16 Bosques | 2 Excels, cero código | Vacío |
| M18 Black Friday | 3 archivos .docx (Word) | Vacío |
| M05 / M11 | sin repo (solo Drive) | No inspeccionable, descripción estándar |

**Menciones de honor (no ganan):** M04 (Docker/polars pero datos de juguete), M01 (mejor higiene de repo pero boosting redundante), M10 (única con modalidad nueva: teledetección/CV, pero lejos del lane).

**Pendiente:** reintentar M09 si publican el repo.

---

## 5. RANKING FINAL (3 lentes consolidadas)

| # | Mentoría | Eje que cubre | Por qué |
|---|----------|---------------|---------|
| **1** | **M03 Juris** | Continuidad IA/RAG | Cima de línea 4 años + 1er RAG de la historia de la diplo + skills más raras |
| **2** | **M17 Hoteles** | Ingeniería de software | Único sistema desplegable (Postgres/Docker/tests); destaco sobre la cohorte |
| **3** | **M06 Fútbol** | Gap de modelado ML | Boosting+SHAP+UMAP, mejor ingeniería DS, tema maduro |
| **4** | **M02 CONICET** | Metodología nueva (grafos) | Análisis de redes = lo único genuinamente nuevo en la caja |
| **5** | **M12 Finanzas** | Series temporales | Sólida pero el tema más trillado = menos diferenciador |

---

## 6. Proyectos complementarios por mentoría

> **Concepto:** la mentoría da el core de ciencia de datos; los proyectos paralelos son la capa de ingeniería que la cohorte NO sabe hacer. Notebook + sistema que lo sirve = portfolio diferenciado.

### M03 Juris — TECHO MÁS ALTO de complementación
- **A — RAG productivo de jurisprudencia:** embeddings → **pgvector**/Qdrant + **reranking** + capa de generación LLM con citas. Servicio FastAPI/Go, Dockerizado. (Apalanca `rag-advanced`, `vector-index-tuning`.)
- **B — Harness de evaluación + chat UI:** **LLM-as-judge** midiendo recall@k, MRR, faithfulness (`llm-evaluation`) + UI Next.js/React para chatear contra el corpus.

### M17 Hoteles — Alto
- **A — API de scoring real:** reemplazar Streamlit por servicio Go/FastAPI con endpoint en tiempo real, esquema Postgres, Docker, CI/CD.
- **B — Monitoreo + data drift:** detección de drift en distribuciones de precio + dashboard de métricas y alertas.

### M06 Fútbol — Medio-alto
- **A — MLOps del pipeline:** API de inferencia + **MLflow** (registry) + **DVC** (datos versionados); notebook → pipeline reproducible.
- **B — Dashboard de scouting:** web app React sobre el motor de cosine-similarity ("reemplazantes funcionales") con radares/heatmaps.

### M02 CONICET — Medio
- **A — Graph DB real:** cargar la red en **Neo4j**, queries de centralidad/comunidades (Louvain)/caminos.
- **B — Explorador interactivo:** web app React + sigma.js/d3 para navegar la red.

### M12 Finanzas — Medio-bajo
- **A — Ingesta + clasificación en vivo:** yfinance → **TimescaleDB**/Postgres → clasificador de régimen → dashboard del régimen actual.
- **B — Harness de backtesting:** validación sistemática del clasificador contra crisis históricas, reporte automatizado.

### Veredicto de complementación
**M03 es la de mayor techo, por lejos.** La mentoría da lo difícil (corpus + embeddings) y deja abierto TODO el stack de producción RAG — exactamente la frontera del perfil. Mentoría + proyectos paralelos se ENCASTRAN. **M17 es la escolta** perfecta para lucir el músculo de arquitecto de software.

---

## 7. Orden de inscripción (CONFIRMADO: el orden importa)

**Mecánica de asignación:** si se exceden los cupos por mentoría, un algoritmo desempata, pero **se respeta el orden elegido** siempre que haya lugar. Es un esquema por preferencias → ordenar por preferencia REAL es lo óptimo (no conviene "guardar" lo que querés para abajo).

**Golpe de suerte:** la preferencia real coincide con la jugada táctica. M03 (el #1) es de los temas MENOS demandados (NLP legal suena árido), así que hay alta probabilidad de conseguirlo. El riesgo de saturación es M06 (fútbol, tema vistoso) — por eso está bien que vaya 3º, detrás de dos nichos seguros (M03, M17).

**ORDEN FINAL RECOMENDADO:**

| Pos | Mentoría | Lógica |
|-----|----------|--------|
| 1 | **M03 Juris** | Máxima preferencia + baja demanda → casi seguro la consigue |
| 2 | **M17 Hoteles** | 2ª preferencia + demanda media-baja → seguro |
| 3 | **M06 Fútbol** | La quiere, pero MAYOR riesgo de saturación → bien detrás de 2 nichos |
| 4 | **M02 CONICET** | Nicho, baja demanda → red de seguridad |
| 5 | **M12 Finanzas** | Trillada pero cupos amplios → fallback aceptable |

**Clave:** las dos primeras (M03, M17) son las menos peleadas Y las que más potencian el perfil. No hay tradeoff entre "lo que quiero" y "lo que voy a conseguir".

## 8. Extrapolación del conocimiento (rubros donde aplica)

> **Concepto clave:** no se aprende "jurisprudencia" ni "hoteles". Se aprenden dos **primitivas de ingeniería de IA** que aplican en todos lados. El dominio es la excusa; la técnica es lo que queda.

- **M03 = "Búsqueda/preguntas sobre un corpus de texto"** → embeddings, retrieval semántico, clasificación de documentos, RAG. Universal: toda industria tiene montañas de texto que nadie puede leer entero.
- **M17 = "¿Esto es normal, justo o anómalo?"** → detección de anomalías sin labels, scoring de transacciones, pricing, segmentación. Universal: toda industria tiene datos transaccionales y necesita detectar lo raro.

**Entre las dos cubren las DOS grandes familias de ML aplicado en la industria:** texto/LLM por un lado, scoring/anomalías transaccionales por el otro.

### M03 (RAG / búsqueda semántica) — rubros

| Rubro | Caso de uso concreto |
|-------|---------------------|
| Legaltech | Análisis de contratos, due diligence, compliance (dominio madre) |
| Healthtech | Búsqueda en historias clínicas, papers médicos, guías de tratamiento |
| Customer support | Bots sobre knowledge base → deflección de tickets |
| E-commerce | Búsqueda semántica de productos |
| Banca/Fintech | Búsqueda en normativa, análisis de documentos KYC/AML |
| Seguros | Lectura de pólizas, procesamiento de siniestros |
| RRHH/Recruiting | Matching CV↔vacante por embeddings, búsqueda en base de talentos |
| Enterprise (interno) | Buscador inteligente sobre Confluence/Notion/Drive |

Patrón único: corpus grande de texto + gente que necesita encontrar/preguntar. Se cambian los fallos del SAIJ por contratos/papers/tickets y el 90% del pipeline es idéntico.

### M17 (anomalías / pricing / scoring) — rubros

| Rubro | Caso de uso concreto |
|-------|---------------------|
| Fintech/Banca | Detección de fraude en transacciones (primo directo), AML |
| Ciberseguridad | Detección de intrusiones, comportamiento anómalo de usuarios (UEBA) |
| IoT/Industria 4.0 | Mantenimiento predictivo, fallas de sensores por telemetría anómala |
| Energía/Utilities | Fraude eléctrico (NTL), consumo anómalo |
| Retail/E-commerce | Dynamic pricing, precios mal cargados, monitoreo de competencia |
| Adtech/Marketing | Fraude en clicks, tráfico de bots |
| Seguros | Fraude en claims |
| **Observability/DevOps** 🔥 | Anomaly detection en métricas/logs/latencias de sistemas |

**Observability/DevOps conecta DIRECTO con el perfil backend:** detectar un spike anómalo de latencia o un patrón raro en logs es el MISMO problema matemático que detectar un precio anómalo de hotel (anomaly detection sin labels sobre series/transacciones). M17 da la capa de ML para automatizar lo que hoy se hace mirando dashboards a mano.

### La jugada estratégica (el combo)

1. **M03 → empleabilidad en la ola de IA generativa / RAG** (donde está la demanda HOY).
2. **M17 → empleabilidad en ML clásico de scoring/fraude/anomalías** (pan de cada día de fintech, ciber, industria).
3. **El perfil backend permite DESPLEGAR las dos.** La mayoría de DS hace el notebook y ahí muere. Acá: modelo + sistema que lo sirve en producción.

→ Perfil raro: **el que entiende el ML Y lo lleva a producción.** Cruces de mayor valor para este perfil específico:
- **Legaltech / enterprise-search con RAG** (M03 + RAG ya instalado).
- **Observability / anti-fraude con anomaly detection** (M17 + backend).

## 9. Aplicación directa a biogas-platform (verificado en código)

**Hallazgo:** biogas-platform-develop YA tiene el esqueleto de ambas primitivas en `monorepo/apps/ml-service/`. M03/M17 no son hipotéticos: son el conocimiento profundo para hacer buenos esos componentes hoy básicos.

### M17 (anomalías) → ya existe, embrionario
- `apps/ml-service/app/models/anomaly_detector.py` — **Ensemble Isolation Forest (60%) + LSTM Autoencoder (40%)**: anomalías puntuales + temporales por reconstruction error. ES M17 sobre telemetría de planta.
- `apps/ml-service/app/models/failure_predictor.py` — Random Forest por equipo, predice falla 7/14 días + RUL, con `TimeSeriesSplit`. Mantenimiento predictivo.
- **Upgrade concreto:** `apps/backend/internal/featureflags/tank_alerts.go` usa umbral ESTÁTICO (`NearFullThresholdPct: 0.90`). M17 permite pasar de alarmas de umbral fijo → detección de anomalías ADAPTATIVA (aprender lo normal por planta).

### M03 (NLP/RAG) → ya existe, embrionario
- `apps/ml-service/app/datasets/sibia_intents.py` — asistente **SIBIA**: 700+ ejemplos en español, 7 intents (DIAGNOSTIC, QUERY_DATA, ALERT_CHECK, PREDICT, CONFIGURE, HELP, CHITCHAT). Clasificación de texto = TP3 de M03.
- `apps/ml-service/app/datasets/text_to_sql.py` — NL→SQL sobre `sensor_readings, plants, alerts, equipment, maintenance_orders, digestate_records`. RAG sobre schema aplica directo.
- **Oportunidad RAG:** los intents DIAGNOSTIC ("¿por qué bajó la producción ayer?") requieren recuperar y razonar sobre `historical-reports` + sensores → eso es RAG. M03 es el cimiento para que SIBIA pase de clasificar la pregunta a RESPONDERLA.

### Sinergia (oportunidad FUTURA)
La mentoría = R&D (técnica rigurosa en entorno controlado); biogas = futuro campo de aplicación. El hueco (anomaly_detector, SIBIA) ya está en el código esperando.

### Caveat honesto (CRÍTICO)
**biogas todavía NO está en producción.** Recién va a arrancar el data entry; los sistemas aún no son productivos. Por eso hay `data/generator.py` (datos SINTÉTICOS) y no hay telemetría histórica real. El cuello de botella no es solo "DB vacía" (forecasting #20) — es que el sistema entero todavía no está vivo. La técnica de M03/M17 aplica perfecto, pero la aplicación real es FUTURA: depende de que biogas entre en producción y se acumulen datos.

## 10. Formulario de inscripción (estrategia)

**Archivo:** `~/Descargas/Elección de Proyectos de Mentorias.html` (Google Form).
**Campos:** Apellido y nombre · Email · Opción 1–5 (ranking) · "Me interesan los 16 proyectos" (fallback) · Comentarios (texto libre).

**Opciones a cargar (en orden):** 1) M03  2) M17  3) M06  4) M02  5) M12.

**Comentarios (estrategia):** título EXACTO ("Técnico Universitario en Desarrollo de Software", NO Ingeniero). La experiencia con RAG es **experimental, no productiva** — contar la historia real (lo implementó en gentleman-guardian-angel, no funcionó para code review, volvió a DB+paginación) y usarla como MOTIVACIÓN para la mentoría. Anomaly detection = interés teórico (biogas no probado). Saludo cálido + cierre amable. Sin coloquialismos ("laburo"). Para una mentoría, "probé, choqué con límites, quiero aprender bien" > "ya lo domino".

**Evidencia verificada:** repo `JNZader-Vault/gentleman-guardian-angel` (GGA = herramienta OPEN SOURCE de otro, Javier CONTRIBUYÓ; su herramienta propia es **ghagga**, distinta). Ramas `feature/02-semantic`, `feature/03-rag`, `feature/04-hebbiana` + `upstream-pr/02-semantic-rag`, `upstream-pr/03-hebbiana` con `lib/{embeddings,semantic,rag,hebbiana}.sh` + tests — NO mergeadas a main (experimental, aporte upstream). Implementado en Shell.

**DECISIÓN sobre ghagga en el comentario:** NO incluirla — no aporta a la narrativa (el experimento de GGA ya carga el mensaje "probé RAG, vi límites, quiero aprenderlo bien") y suma chapa + largo. El comentario menciona SOLO el aporte OSS a GGA.

**ghagga — estado real (verificado 4vr — Haiku/Sonnet/Opus + Codex, unánime; guardado para CV/web, NO para el comentario):** tool PROPIA, publicada en npm v3.1.0 (MIT, TS strict, 424 tests, CI, web ghagga.javierzader.com). Code review con IA: 5 estrategias de orquestación (incl. consenso multi-agente), 17 tools de análisis estático, y memoria persistente RAG (persist→retrieve→inject) CABLEADA Y ACTIVA — pero vía full-text search (Postgres tsvector / SQLite FTS5 BM25), NO embeddings. La búsqueda semántica/vectorial está en la arquitectura (`packages/core/src/embed.ts`, columna `embedding`, hybrid query en `packages/db/src/queries.ts`) pero NINGÚN provider concreto enchufado → siempre degrada a keyword. Detalle file:line en engram `ghagga/rag-memory-real-state`.

**Texto FINAL (honesto + saludo):**

> ¡Hola! ¿Cómo están?
>
> Soy Técnico Universitario en Desarrollo de Software, orientado a backend (Go, TypeScript, PostgreSQL, Docker). Vengo explorando de forma práctica la IA aplicada: experimenté con RAG y embeddings —incluso con aprendizaje hebbiano— como aporte a Gentleman Guardian Angel, una herramienta open source de code review. Ese experimento me sirvió para entender de primera mano dónde RAG aporta y dónde no.
>
> Además, hoy estoy trabajando en una plataforma de monitoreo de plantas de biogás donde necesito aplicar de lleno estos dos enfoques: detección de anomalías sobre datos de sensores y un asistente en lenguaje natural para operarios. Estoy implementando esas piezas, pero quiero ganar fundamentos más sólidos para hacerlo bien — y justamente por eso me interesan estos dos proyectos:
>
> M03 (Jurisprudencia): quiero profundizar en serio el pipeline NLP → embeddings → búsqueda semántica —un caso donde RAG sí encaja de lleno— y aprender a evaluarlo con rigor (calidad de recuperación, reranking).
>
> M17 (Ofertas hoteleras): la detección de anomalías sin etiquetas se alinea directo con lo que necesito en la plataforma; además, que el proyecto ya tenga estructura de sistema desplegable (Postgres/Docker) encaja con mi perfil de desarrollo de software.
>
> Mi plan es complementar la mentoría con proyectos propios para llevar lo aprendido a nivel producción. Sé que normalmente se asigna un proyecto por persona, pero como M03 y M17 son muy complementarias —y en mi caso convergen en un mismo proyecto real—, si hubiera alguna posibilidad de participar en ambas (aunque sea en una como colaborador), me interesaría mucho.
>
> ¡Muchas gracias! Saludos.

## 11. Decisiones abiertas / próximos pasos

- [ ] Reintentar inspección del repo **M09** (dio 404).
- [ ] (Idea) Proyecto-puente M17 ↔ observabilidad de sistemas (terreno natural del perfil backend).
- [ ] (Idea) Aplicar M03/M17 a biogas: upgrade `tank_alerts` estático→adaptativo; RAG para SIBIA diagnóstico.
- [ ] Asegurar ingesta de datos históricos reales en biogas (unblocker de todo el ML real).
- [ ] Elegir 1–2 proyectos complementarios de M03 para arrancar en paralelo a la mentoría.
- [ ] (Opcional) Validar si interesa el ángulo geoespacial/CV de M10 antes de cerrar definitivamente.

---

## 12. Apéndice A — Dossier técnico M17 (exploración exhaustiva del repo)

> Exploración del repo `martinid90/id90-hotel-deals-analysis` con 3 agentes en paralelo (README 71KB + todo el código + notebook). Verificado con file:línea. Estado: v3.0.0 (enero 2026).

### Qué es
ID90Travel vende hoteles a empleados de aerolíneas con tarifas preferenciales. Problema: el usuario no sabe si un precio es ganga. El sistema clasifica cada precio en `Deal / Good Price / Normal Price / Expensive / Very Expensive`, relativo a la historia del propio destino (no hay escala global).

### Datos
- ~2.5M registros/año × 2 años (2024-2025), CSVs ~200-300MB, de un DWH PostgreSQL (`analytic.customer_shopping_model` + `hotel_city_location`, filtro `type='HOTELS'`).
- CLAVE: cada fila NO es un hotel — es el resumen estadístico de TODOS los hoteles de esa búsqueda (`avg_price_average`, `count_repeated`=demanda, `avg_hotel_count`=oferta).
- 17 columnas originales + 7 derivadas. ~26.000 nombres de ciudad → ~50-100 mercados canónicos vía `destination_with_nearest.csv` (15.989 refs). Tras expansión por noche: ~10.7M observaciones diarias.

### Metodología (baseline del mentor)
Unidad de análisis: `destino × mes × semana-del-mes × bucket-de-precio` → 635.022 baselines.
1. Normaliza precio: `total / (noches × habitaciones × personas)` (multiplicativa, corregida en v3 desde aditiva).
2. Segmenta por percentiles p25/p75 en buckets `low/medium/high`.
3. Z-score contra media histórica **ponderada por `count_repeated`**: `z = (precio_std − mean) / std`.
4. Clasifica por umbrales de z (Deal z<-1.0 ... Very Expensive z≥1.0) + Relative Price Index (`precio/mediana`).
5. Niveles de confianza (high/medium/low), fallback a baseline general, mínimo 30 obs, std dinámica mínima (mean×0.10).

### Arquitectura (terreno backend de Javier)
```
DWH Postgres → query_historicos.py → CSVs → pipeline_build_baselines.py (11 pasos)
→ outputs/*.csv (market_baselines 52MB/635k filas, price_distribution, bucket_summary) → app.py (Streamlit)
```
Dockerizado (python:3.10-slim, healthcheck, EXPOSE 8501), psycopg2, separación limpia config/lógica/UI, vectorización (`numpy.repeat` 1000x), logging estructurado.

### Desafío central = M17 puro
Detección de anomalías SIN etiquetas. Pregunta abierta del mentor: "sin labels externos de 'esto era una oferta real', ¿cómo evaluás que el algoritmo funciona?".

### Qué queda abierto para el mentoreado (extensiones §16)
El mentor dice explícito: repo = inspiración, NO solución. Deja para construir:
- Clasificación multi-clase (RF/XGBoost/LightGBM) — desbalance (Deal≈5%), alta cardinalidad de destino.
- Regresión sobre z-score continuo.
- Series temporales de precio (Prophet/ARIMA/LSTM).
- Clasificación binaria calibrada a negocio (umbral por costo de falsos positivos).

### 🎯 Hallazgos de ingeniería (la palanca de Javier sobre la cohorte)
| Hallazgo | Severidad | file:línea | Oportunidad |
|----------|-----------|-----------|-------------|
| Tests ROTOS — llaman `calcular_total_std` (no existe), labels español vs inglés, ~3/7 clases fallan | 🔴 Crítico | `test_system.py:24,79,241` | Arreglar = victoria rápida y visible |
| Mean ponderado pero std SIN ponderar | 🟠 Alto | `auxiliary_functions.py:697-716` | Sesgo estadístico real en el z-score |
| `iloc[0]` arbitrario en fallback de bucket | 🟠 Alto | `auxiliary_functions.py:353-359` | Bug de correctitud |
| `mkdir` side-effect en import | 🟡 Medio | `config.py:39-41` | Anti-patrón que rompe tests |
| Estandarización duplicada app vs auxiliary | 🟡 Bajo | `app.py:323-328` | Mantenimiento divergente |
| 77% contextos baja confianza (data sparsity) | — | — | Gran problema abierto del dominio |
| Clasificación a nivel de mercado, NO de hotel individual | — | — | Limitación más profunda a atacar |

**Conclusión:** mientras la cohorte pelea con el notebook, Javier puede sumar modelado + arreglar tests + corregir el bug del std + productizar (API real en vez de Streamlit, CI/CD). Confirma con evidencia que "ya tiene estructura de sistema desplegable encaja con mi perfil" es 100% cierto.

---

## 13. Apéndice B — Dossier técnico M03 (reconocimiento dataset + plan RAG)

> Exploración del repo `adrian-alejandro/...textos-legales` (greenfield, requirements vacío) + dataset HF `marianbasti/jurisprudencia-Argentina-SAIJ` + análisis de la muestra real (8.748 registros). Verificado.

### El dataset
- HF `marianbasti/jurisprudencia-Argentina-SAIJ`: ~2.5GB, español, Apache 2.0, 100K-1M registros, split único `train`. Se baja con `snapshot_download`. Muestra 1% en `datos/dataset_sample.jsonl.gz`.
- Dos fuentes: (1) ESTRUCTURADA = jsonl de sumarios + metadata; (2) NO-ESTRUCTURADA opcional = PDFs/DOCs/HTML crudos de fallos completos, extraídos con `unstructured[all-docs]` + chardet + BeautifulSoup (notebook `extracción-texto.ipynb`).

### 🔴 Gotchas verificados (la ventaja de conocerlos antes)
1. **Viewer de HF ROTO** (CastError — schema mismatch, columnas no coinciden). No se puede explorar online; bajar raw + parsear.
2. **~44% filas son plantillas vacías**: de 8.748 muestra, solo 4.851 con contenido real. 1ª fila = ejemplo con todo None → filtrar.
3. **Campos prometidos vacíos**: `tipo-fallo`=100% NULL, `texto-completo`=0%, `hechos`=0%, `sintesis`=1%. Señal real = `sumario` + `texto` + `materia` (de 70+ campos).
4. **Etiquetas sucias**: `materia` mezcla `CIVIL - COMERCIAL` / `CIVIL-COMERCIAL` / `COMERCIAL` como distintas; tribunal con códigos duplicados (`CS CS`, `S S S`). Normalizar = el TP2.
5. **Markup HTML crudo** en sumarios: `[[p]]`, `[[r uuid:...]]` → limpiar.
6. **Textos CORTOS**: sumario mediana 82 chars; texto mediana 525, máx 6.694. Son resúmenes, no fallos completos (esos están en los PDFs crudos aparte).

### Distribución real (muestra)
- `materia` (etiqueta de clasificación): PROCESAL 684 · PENAL 527 · LABORAL 483 · CIVIL 459 · CIVIL-COMERCIAL 419 · ADMINISTRATIVO 288 · CONSTITUCIONAL 205 · COMERCIAL 202... → desbalanceada + categorías a fusionar.
- `provincia`: CABA 2.312 · Buenos Aires 785 · Santa Fe 397... → sesgo geográfico.

### Plan de ataque RAG (conecta con perfil de Javier)
- **Fase 1 — Curación (TP1/TP2):** filtrar plantillas → normalizar `materia` → limpiar markup → corpus = `sumario` limpio + `texto`.
- **Fase 2 — Clasificación supervisada** (`materia` desde texto): baseline TF-IDF + LogReg/LinearSVC → luego embeddings + clasificador. Métrica F1-macro (desbalance) + matriz de confusión (CIVIL vs COMERCIAL).
- **Fase 3 — Buscador semántico (su fuerte):** embeddings ES (`multilingual-e5-large` o `BAAI/bge-m3`); vector store FAISS en notebook → **pgvector** en proyecto propio; **búsqueda híbrida BM25 + semántica** (diferenciador, lo vio en ghagga); evaluación retrieval (recall@k, MRR, nDCG + LLM-as-judge) → responde la research question jerga-técnica-vs-coloquial del mentor.
- **Fase 4 — Productización (proyecto complementario):** pgvector + reranking + generación con citas + UI. Excede la mentoría = portfolio.

---

*Informe generado a partir de: 18 descripciones oficiales + repos de las 5 finalistas + repos de 10/13 descartadas + historial DiploDatos 2022–2025 + dossiers exhaustivos M17 y M03.*
