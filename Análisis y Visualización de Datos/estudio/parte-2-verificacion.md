# Segunda parte: "Análisis y Visualización de Datos", con material externo

**Esta es la continuación de** `analisis-y-visualizacion-apunte-de-estudio.md` y `analisis-y-visualizacion-guia-de-implementacion.md` (las clases de Análisis y Visualización de Datos, primera materia obligatoria de la Diplomatura en Ciencia de Datos de FAMAF UNC, cohorte 2026, dictadas por Georgina Flesia y Karim Nemer en cuatro encuentros: 27 y 28 de marzo y 10 y 11 de abril de 2026). Esos archivos resumen lo que dice la materia. Esta segunda parte suma material externo para verificar lo que en el apunte quedó "para verificar" o "dudoso", respaldar con fuentes las correcciones que ya marqué, corregir errores míos de la primera parte, sumar bibliografía y discutir el enfoque de la materia (tests de hipótesis frecuentistas, p contra α) contra la alternativa más fuerte, con un benchmark real sobre la encuesta de Sysarmy 2026. Revisé todo el 03/10/2026 y solo cito páginas que abrí (las que solo vi en un buscador las marco así). Conflictos de interés: los marco donde aparecen; los más importantes son la CESSI (cámara empresaria del software, autora del dato de empleo), CrowdFlower y Anaconda (venden herramientas de datos y son autoras de las cifras de "tiempo limpiando"), Kruschke (defiende su propio método, BEST) y los autores de dabest y PyMC (escriben sobre sus herramientas).

> Cómo leer esto: cuando digo "la materia" o "las docentes" me refiero a lo que dicen Georgina y Karim en las clases. Las marcas de tiempo usan la etiqueta de cada grabación del apunte (C1P1 es la clase 1, parte 1, y así hasta C4P2; V01 a V05 son los videos de apoyo) y llevan al minuto exacto en la grabación. Cuando digo "sugerencia" es una idea mía que combina fuentes, no algo que diga una fuente puntual. El código lo corrí en el box el 03/10/2026 con Python 3.13, scipy 1.18.1, pandas 3.0.6, numpy 2.2.4 y matplotlib 3.11.2 (los mismos de la guía), y la parte bayesiana en un entorno aparte con PyMC 6.3.2, ArviZ 1.3.0 y dabest 2025.10.20 (que traen scipy 1.15.3 y pandas 2.2.3), siempre contra `sysarmy_survey_2026_processed.csv` del repositorio de la materia. Los tiempos son de una CPU del box, sin GPU.

---

## Checklist actualizado (curso + mejoras)

1. Abrí las notebooks desde el repositorio público `DiploDatos/AnalisisyVisualizacion` (rama `master`, README "2026") y, si un link de la filmina da 404, cambiá 2025 por 2026 en la URL.
2. Confirmá las fechas de los dos entregables en el aula virtual: no están en ninguna página pública; el calendario oficial solo confirma que la materia ocupó el 27 y 28 de marzo y el 10 y 11 de abril, y que la siguiente arrancó el 24 de abril.
3. Leé el CSV procesado con `pd.read_csv(URL)`, mirá `shape`, `dtypes`, faltantes y `describe()`, y recodificá género desde las categorías reales de 2026 (`"Hombre Cis"`, `"Mujer Cis"`).
4. Documentá cada corte de filas y por qué; si querés imitar a OpenQube, que publica el análisis oficial de la encuesta, usá cercos de rango intercuartílico separados para sueldos dolarizados y no dolarizados y descartá sueldos menores a medio salario mínimo.
5. Para outliers usá los cercos de Tukey como los define el NIST: 1,5 IQR desde los cuartiles para atípicos "leves" y 3 IQR para "extremos"; no uses el "2,5 × Q3" del notebook 02.
6. Reportá media y mediana juntas y, para sueldos, preferí la mediana y el IQR, como hace OpenQube.
7. Usá Welch (`ttest_ind(..., equal_var=False)`) por defecto para comparar dos grupos independientes, y el t apareado si las dos medidas son de la misma persona (bruto y neto).
8. Sabé que scipy usa siempre la distribución t para el p valor del t test, con cualquier cantidad de grados de libertad; no hay un cambio a la normal "arriba de 100".
9. Si las colas son pesadas, probá además el t recortado de Yuen (`ttest_ind(..., trim=0.2)`) o un test de permutación (`method=stats.PermutationMethod()`), que scipy ya trae.
10. Interpretá el intervalo de confianza como la tasa de acierto del procedimiento, no como "95% de probabilidad de que μ esté adentro"; esa lectura es el error más común incluso entre investigadores (Hoekstra y otros, 2014).
11. Compará el p valor bilateral de scipy con α = 0,05, no con 0,025, y fijá `alternative` según H1 antes de mirar los datos.
12. No reportes solo "significativo": seguí a la ASA (2016) y poné el tamaño del efecto con su intervalo (diferencia de medias, cociente de medianas, g de Hedges) junto al p valor.
13. Usá Wilcoxon de rangos con signo para una muestra o muestras apareadas y Mann Whitney para dos muestras independientes; es al revés de como quedó en la tabla de la clase.
14. Si un ANOVA rechaza, hacé un post hoc (Tukey HSD, `scipy.stats.tukey_hsd`); no repitas t tests de a pares sin corrección.
15. Para comparar varios clasificadores sobre varios datasets, usá Friedman con su post hoc (Demšar, 2006): compara rangos promedio, no "el de menor variabilidad".
16. Para la brecha de género, condicioná por seniority: el cociente de medianas baja de 1,23 en general a 1,00, 1,12 y 1,15 dentro de Junior, Semi Senior y Senior, porque hay proporcionalmente más mujeres junior.
17. Si usás bootstrap, preferí BCa o percentil con muestras de al menos 30 por grupo: con 10 por grupo, el percentil cubrió el 90% en vez del 95% en mi simulación, y Welch el 95%.
18. En los gráficos, codificá lo importante como posición sobre una escala común (Cleveland y McGill, 1984), mostrá la distribución además del resumen (Anscombe, Datasaurus) y usá ejes desde 0 en barras y paletas aptas para daltonismo.
19. Verificá que la notebook del grupo corra de principio a fin antes de entregar.

---

## Versión completa

### 1. Los datos del curso, verificados

Todo lo que en el apunte o la guía quedó "para verificar" o "dudoso", más las correcciones a mis propios archivos.

| Afirmación | Resultado | Matiz | Fuente |
|---|---|---|---|
| Fechas de las clases 3 y 4: "10/04/2026, para verificar" y "11/04/2026, para verificar" (tabla de videos del apunte) | Sí (corrijo mi apunte: ya no está "para verificar") | El calendario de la cohorte 2026 pone Análisis y Visualización de Datos el 27 y 28 de marzo y el 10 y 11 de abril, y Análisis Exploratorio y Curación el 24 y 25 de abril y el 8 y 9 de mayo. La cohorte va del 27 de marzo al 5 de diciembre; las optativas, del 21 de agosto al 14 de noviembre. El sitio aclara que "este cronograma puede ajustarse". | [Calendario de la diplomatura](https://diplodatos.famaf.unc.edu.ar/calendar/) |
| Fechas de los entregables: apertura 10/04, cierre tentativo 24/04, parte 2 desde el 17/04, cierre a confirmar por Carolina Chavero C2P1 2:22, C4P2 1:52:27 | No verificable | No están en el calendario, ni en la FAQ, ni en el folleto PDF, ni en el repo. El cierre tentativo del 24/04 coincide con el comienzo de la materia siguiente en el calendario oficial. La FAQ dice que todos los prácticos son grupales, que hay que aprobarlos y que las devoluciones se hacen por Meet. Confirmalas en el aula virtual. | [Calendario](https://diplodatos.famaf.unc.edu.ar/calendar/), [sitio de la diplomatura](https://diplodatos.famaf.unc.edu.ar/), repo clonado |
| Karim Nemer: "ingeniero en sistemas (UTN), doctor en ingeniería con mención en electrónica", en un centro de la UTN FRC que la transcripción llama "CPIE" (módulo 0 del apunte) C1P1 12:14 | En parte (corrijo mi apunte) | Karim es **mujer**: el CIII la lista como "Dra.Ing. Karim Nemer Pelliza, Prof. Adjunta interina, Investigadora categoría C" y el sitio de la diplomatura como "Ing. en Sistemas de Información, Doctora en Ingeniería". Donde mi apunte dice "ingeniero", "doctor" o "él" refiriéndose a Karim, leé "ingeniera", "doctora" y "ella" (la transcripción automática dice "ingeniero" y "doctor", y yo lo copié sin verificar). El centro es el **CIII**, Centro de Investigación en Informática para la Ingeniería de la UTN FRC, y su página de docencia lista "Análisis y Visualización de datos. Dra. Karim Nemer Pelliza" en la diplomatura. La "mención en electrónica" no la pude confirmar. Además, en la línea de "para verificar" del módulo 0 escribí "él lo describe": quien la presenta es Georgina. | [CIII, personal](https://ciii.frc.utn.edu.ar/ciii/personal/), [CIII, docencia](https://ciii.frc.utn.edu.ar/ciii/docencia/), [sitio de la diplomatura](https://diplodatos.famaf.unc.edu.ar/) |
| Georgina Flesia, "coordinadora de la diplomatura desde 2022" (apunte) C1P1 7:14 | En parte (corrijo mi apunte) | Ella dice que tomó la coordinación en 2022 C1P1 11:41 y que "Carolina, Laura y yo hemos sido las coordinadoras". En 2026 la coordinadora es Carolina Chavero, según el sitio. Su posdoc en Stanford con Donoho sí se confirma: su ficha de la FCE UNC dice "Stanford University 2000 2002, Computational Mathematics". | [Sitio de la diplomatura](https://diplodatos.famaf.unc.edu.ar/), [ficha de Georgina Flesia en la FCE UNC](https://graduados.eco.unc.edu.ar/es/27-institucional/docentes/1160-dra-georgina-flesia) |
| "Alrededor de 60.000 programadores en Argentina" C2P1 1:33:36 | No | El último informe del Observatorio de la CESSI (OPSSI, primer trimestre de 2026) cuenta 162.391 puestos de trabajo registrados en el sector software y "más de 65.000" puestos nuevos en diez años; el de octubre de 2025, 159.257 puestos y "60.537 nuevos puestos de trabajo en los últimos 10 años". El 60.000 se parece al crecimiento de diez años, no al total. Ojo: son puestos registrados de todo el sector, no solo programadores, y no cuentan freelancers ni a quienes trabajan para afuera. Conflicto de interés: la CESSI es la cámara empresaria del sector. Dato de control interesante: el mismo informe da un salario promedio registrado de $3.738.000 en marzo de 2026, cerca de la media del bruto de Sysarmy (3,88 M). | [Informe OPSSI del primer trimestre de 2026 (PDF, julio de 2026)](https://cessi.org.ar/wp-content/uploads/2026/07/OPSSI-Reporte-Industria-Software-1er.-trim.-2026.pdf); el de octubre de 2025 lo leí en PDF pero ya no figura en la [página del OPSSI](https://www.cessi.org.ar/opssi/) |
| "El 60% del tiempo limpiando" C1P1 52:46 y "casi el 25%" C3P1 1:24:49 | En parte | Las dos cifras existen, de encuestas distintas. CrowdFlower 2016: "Cleaning and organizing data: 60%", más 19% juntando datos, y el 57% dice que es lo que menos disfruta. Anaconda 2020: carga 19%, limpieza 26%, visualización 21%, selección de modelo 11%, entrenamiento 12%, despliegue 11%. El famoso "80%" sale de sumar limpieza y recolección de CrowdFlower 2016; Leigh Dodds lo llama "a bullshit statistic" y muestra que otras encuestas dan cifras muy distintas (CrowdFlower 2017, 51%; Kaggle 2018, alrededor de 11% juntando y 15% limpiando). Son encuestas voluntarias, como la de Sysarmy. Conflicto de interés: CrowdFlower vendía etiquetado y limpieza de datos y Anaconda vende herramientas. | [Informe CrowdFlower 2016 (PDF)](https://www2.cs.uh.edu/~ceick/UDM/CFDS16.pdf), [Anaconda State of Data Science 2020 (PDF)](https://know.anaconda.com/rs/387-XNW-688/images/Anaconda-SODS-Report-2020-Final.pdf), [Leigh Dodds (2020)](https://blog.ldodds.com/2020/01/31/do-data-scientists-spend-80-of-their-time-cleaning-data-turns-out-no/) |
| La tabacalera que "podaba a todos los que tenían cáncer" para mostrar que el cigarrillo no lo causaba ("lo hizo Malboro") C3P1 1:11:14 | En parte | Que la industria tabacalera fabricó duda científica está documentado: Brandt (2012) muestra que desde diciembre de 1953, con la agencia Hill & Knowlton y el Tobacco Industry Research Committee, el objetivo fue "to build and broadcast a major scientific controversy" y que "aggressively solicited a small group of doubters". R. A. Fisher, el padre de los tests de significación, discutió la causalidad (correlación no es causalidad) y trabajó como consultor de las tabacaleras. Pero no encontré ninguna fuente de una "poda" de casos de cáncer como técnica, ni de que fuera Marlboro en particular. Usala como ejemplo de conflicto de interés, no de recorte de datos. | [Brandt (2012), AJPH, PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC3490543/), [Wikipedia, Ronald Fisher](https://en.wikipedia.org/wiki/Ronald_Fisher) |
| "Arriba de 100 personas ya tengo una distribución normal" C2P2 37:31 y "si no hay normalidad necesito más de 100" C3P2 56:24 | No como regla | No hay un n mágico. Para la binomial, OpenIntro usa la condición de éxito y fracaso (np y n(1 − p) de al menos 10), que depende de p. Para la media, depende de la asimetría: con datos exponenciales la asimetría de x̄ baja como 2/√n (0,60 con n = 10 y 0,20 con n = 100 en mi g07). Con los sueldos de Sysarmy (asimetría 1,71), Welch con 10 por grupo ya cubrió el 95,2% en mi simulación de la sección 6. | [OpenIntro Statistics](https://www.openintro.org/book/os/), mis scripts `g07_tcl_ic.py` y `bench_sim.py` |
| "Si los grados de libertad pasan de 100, Python usa el test normal" C4P2 19:39 | No | La documentación de `ttest_ind` (scipy 1.18) dice que "by default, the p-value is determined by comparing the t-statistic of the observed data against a theoretical t-distribution", y el código usa la t con sus grados de libertad siempre. Con muchos grados de libertad la t y la normal casi coinciden, por eso la confusión. | [scipy.stats.ttest_ind](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html) |
| "El promedio de tres exponenciales no tiene nada" C3P1 2:00:21 | No | La suma de k exponenciales independientes con la misma tasa es Erlang(k), un caso especial de la Gamma; el promedio de tres es Gamma(3, escala θ/3). En el box, 100.000 promedios de tres Exp(1) contra Gamma(3, 1/3): Kolmogorov Smirnov D = 0,0028, p = 0,40 (no se distinguen). Lo que quiso decir es que todavía no es normal. | [Wikipedia, Erlang distribution](https://en.wikipedia.org/wiki/Erlang_distribution), [Wikipedia, Exponential distribution](https://en.wikipedia.org/wiki/Exponential_distribution), `bench_estratos.py` |
| El pivote "−2 log(X/σ) ~ chi cuadrado con 2 grados de libertad" para la exponencial C4P1 49:23 | No (como lo dije en el apunte) | Wikipedia lista "Exp(1/2) = χ²₂" y que si T es la suma de n exponenciales de tasa λ, "2λT ~ χ²₂ₙ". Para una sola X de media θ, 2X/θ ~ χ²₂, como puse en el apunte. | [Wikipedia, Exponential distribution](https://en.wikipedia.org/wiki/Exponential_distribution) |
| Friedman "elige el método que tiene menor variabilidad" C4P1 1:56:52 | No | Demšar (2006, JMLR) define Friedman como "the non-parametric equivalent of the repeated-measures ANOVA. It ranks the algorithms for each data set separately" y compara los rangos promedio. Recomienda "the Wilcoxon signed ranks test for comparison of two classifiers and the Friedman test with the corresponding post-hoc tests" para varios. La filmina de C4P1 1:55:03 lleva el mismo título que el paper, así que es ese. | [Demšar (2006), JMLR 7:1 a 30](https://jmlr.org/papers/v7/demsar06a.html) |
| La jerarquía de "escala común alineada" C4P2 1:35:05 | Sí | Es Cleveland y McGill (1984, JASA 79(387):531 a 554): 1, posición sobre una escala común; 2, posición sobre escalas no alineadas; 3, longitud, dirección, ángulo; 4, área; 5, volumen y curvatura; 6, sombreado y saturación. Proponen gráficos de puntos en lugar de tortas y barras apiladas: "radical surgery on these popular graphs is needed". | [Cleveland y McGill (1984), PDF](https://www.dsciclass.org/dsci310/Notes/Cleveland_McGill_EPT.pdf) (la página de Taylor & Francis no cargó) |
| El blog "El arte de medir", que no cargó en clase (el apunte lo ubica en C4P2 57:26) | En parte (corrijo la marca de tiempo) | La mención está en C4P2 59:43. Era el blog de El Arte de Medir, una consultora española de analítica de datos (dirigida por Gemma Muñoz) que compró Ibermática en 2021. El dominio `elartedemedir.com` hoy no responde (curl sin respuesta el 03/10/2026), lo que explica que no cargara; el Internet Archive tiene el blog guardado hasta mayo de 2024, con una categoría "Visualización". | [Relación Cliente (2021)](https://www.relacioncliente.es/ibermatica-compra-el-arte-de-medir/), [blog en el Internet Archive (mayo de 2024)](http://web.archive.org/web/20240521022035/https://elartedemedir.com/blog/) |
| "Los estudios observacionales son el 90% de los estudios que hay" C3P1 1:46:34 | No verificable | No da fuente y no encontré una que lo mida para todas las disciplinas. | |
| "Para dar vuelta la media y la mediana tenés que cortar más del 50% de los datos" C3P1 1:10:07 | En parte (sin cambios) | Ya lo había verificado en el box: con el bruto alcanza con cortar en 3 millones, que deja afuera el 57%; depende de la distribución. | `g04_descriptiva.py` |
| Outliers del boxplot "por encima de unos 7,5 millones" C2P2 1:11:12 | No (sin cambios) | El bigote superior (Q3 + 1,5 IQR) está en 9,1 millones; ya verificado en el box. | `g04_descriptiva.py` |
| La varianza de las medias "es 0,01" con 1000 repeticiones de 200 C3P2 12:00 | No verificable | Depende de los parámetros que usó en vivo. Con media 1, la varianza de x̄ es 1/n: 0,005 con n = 200 y 0,01 con n = 100 (mi g07 da 0,01000 con n = 100). Fijate además que la varianza depende de n, no de las 1000 repeticiones, que es justamente la corrección del TCL. | `g07_tcl_ic.py` |
| La forma cuadrática "con la matriz de correlación" C3P1 40:53 y la covarianza "con otra formulita" para categóricas C3P1 49:46 | No (sin cambios) | La forma es (x − μ)ᵀ Σ⁻¹ (x − μ) con la inversa de la covarianza. Para dos nominales, scipy ofrece la V de Cramér, la T de Tschuprow y el coeficiente de contingencia en `scipy.stats.contingency.association` ("degree of association between two nominal variables"). | [scipy.stats.contingency.association](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.contingency.association.html) |
| "Esto está al revés" al mostrar la regla del p valor C4P2 4:25 | Resuelto por la transcripción | Karim lee "si ese p valor es más chico que el alfa, esto está al revés" y enseguida dice la regla correcta: "es más chico que alfa, rechazamos la hipótesis nula. Si es más grande que el alfa, no rechazamos". O sea, la filmina tenía la desigualdad invertida y ella la corrige en voz alta. | Transcripción de C4P2 |

### 2. Nombres y dudas de la transcripción, resueltos

| En la transcripción o el apunte | Es | Fuente |
|---|---|---|
| "Cristian Carbelino", el profesor que puso un baseline en la competencia de Kaggle cuando Georgina "era profesora de seguimiento" C4P1 29:08 | **Cristian Cardellino**. Su página dice que es doctor (2018) en aprendizaje automático y procesamiento de lenguaje, profesor adjunto en FAMAF UNC, que "taught Supervised Machine Learning and Deep Learning" en la diplomatura e investiga en Mercado Libre. La página de Aprendizaje Profundo de la diplomatura lo lista como docente junto a Milagro Teruel y Mauricio Mazuecos. Su LinkedIn (solo visto en el buscador) dice instructor de 2018 a 2021. | [Cardellino, About (Medium)](https://medium.com/@crscardellino/about), [Aprendizaje Profundo en el sitio de la diplomatura](https://diplodatos.famaf.unc.edu.ar/) |
| "CPIE" C1P1 12:14 | **CIII**, Centro de Investigación en Informática para la Ingeniería, UTN Facultad Regional Córdoba. | [CIII, personal](https://ciii.frc.utn.edu.ar/ciii/personal/) |
| "OpenCube", "pentium" (el análisis de la encuesta) | **OpenQube**, que publica el análisis oficial de cada encuesta de Sysarmy en `sueldos.openqube.io`. | [OpenQube, encuesta 2026.01](https://sueldos.openqube.io/encuesta-sueldos-2026.01/), [post de Sysarmy](https://sysarmy.com/blog/posts/resultados-de-la-encuesta-de-sueldos-2026-1/) |
| "50 años de data science", de "David Donho" C1P1 31:20 | **David Donoho, "50 Years of Data Science"** (versión 1.00 del 18/09/2015, publicada en 2017 en el Journal of Computational and Graphical Statistics). Arranca con el llamado de Tukey en "The Future of Data Analysis" (1962). | [Donoho (2015), PDF](https://courses.csail.mit.edu/18.337/2015/docs/50YearsDataScience.pdf) |
| "Otro paper de data science from 1963 al 2012", de autor que no se entiende (dudoso en el apunte) C1P1 31:54 | **Rafael C. Alvarado, "Data Science from 1963 to 2012"** (arXiv 2311.03292, 2023). Rastrea el término hasta el Data Sciences Laboratory de la Fuerza Aérea de Estados Unidos en los años sesenta y llega hasta el "sexiest job" de Harvard Business Review en 2012; critica que Donoho se concentre en un período corto. | [arXiv 2311.03292](https://arxiv.org/abs/2311.03292) |
| "Laura Alemani", también coordinadora C1P1 7:14 | **Laura Alonso Alemany**, docente de la diplomatura según el sitio. | [Sitio de la diplomatura](https://diplodatos.famaf.unc.edu.ar/) |
| El paper de "comparaciones de clasificadores con múltiples datasets" C4P1 1:55:03 | **Janez Demšar (2006)**, "Statistical Comparisons of Classifiers over Multiple Data Sets", JMLR 7:1 a 30. | [JMLR](https://jmlr.org/papers/v7/demsar06a.html) |
| La jerarquía de canales visuales C4P2 1:35:05 | **Cleveland y McGill (1984)**, "Graphical Perception: Theory, Experimentation, and Application to the Development of Graphical Methods", JASA 79(387). | [PDF](https://www.dsciclass.org/dsci310/Notes/Cleveland_McGill_EPT.pdf) |
| El "blog del arte de Medir" C4P2 59:43 | Blog de **El Arte de Medir**, consultora española de analítica comprada por Ibermática (hoy dentro de Ayesa, según el propio sitio archivado). | [Internet Archive](http://web.archive.org/web/20240521022035/https://elartedemedir.com/blog/) |

### 3. Las correcciones de la clase, con fuentes

En el apunte marqué estas correcciones con mis simulaciones; acá les sumo una fuente autorizada a cada una.

#### 3.1 Teorema central del límite: lo que importa es n, no la cantidad de repeticiones

**Qué dice la fuente.** Ante la pregunta de Valeria, Karim dice que "el TCL dice que la media se comporta como normal cuando tu número de repeticiones es alto" y compara 10 repeticiones de muestras de 20.000 con 20.000 repeticiones de muestras de 10 C3P2 6:44. Georgina escribe la estandarización dividiendo por la esperanza C3P1 1:56:49 y dice que la densidad de la media "crece en dispersión" C3P1 1:59:13.

**Qué suma el material externo.** OpenIntro presenta el TCL con dos condiciones, independencia y tamaño de muestra suficiente según la asimetría de los datos (sección 5.1 en el libro; para proporciones, la condición de éxito y fracaso). Nada habla de repeticiones: m es un artificio de la simulación para dibujar el histograma. Mi g07 lo muestra: con 10 repeticiones de n = 20.000 la asimetría empírica de x̄ sale −0,56 por puro ruido de tener 10 puntos, y con 1000 repeticiones del mismo n, −0,03 (la teórica es 2/√n = 0,014). La varianza de x̄ es σ²/n, así que la dispersión baja, y se estandariza con (x̄ − μ)/(σ/√n).

**Cómo implementarlo.**

```python
# tcl_n_vs_m.py: la forma de x̄ depende de n; m solo afina el dibujo
import numpy as np
from scipy import stats
rng = np.random.default_rng(0)
for n, m in [(10, 20_000), (100, 20_000), (20_000, 10)]:
    xbar = rng.exponential(1, (m, n)).mean(1)
    print(n, m, "asimetría de x̄:", round(stats.skew(xbar), 3), "teórica:", round(2 / np.sqrt(n), 3))
```

#### 3.2 El intervalo de confianza: tasa de acierto del método, no probabilidad del parámetro

**Qué dice la fuente.** Georgina lo explica bien ("el método falla una vez en 20") C3P2 40:29, pero Karim lo interpreta como "con una chance del 95% el verdadero valor del parámetro va a estar dentro de estos rangos" C3P2 1:20:30. Y ante el intervalo (650.632; 945.583) de la brecha, una alumna dice "no hay mucha diferencia" y queda sin corregir C3P2 1:28:35.

**Qué suma el material externo.**
- El NIST: "if the same population is sampled on numerous occasions and interval estimates are made on each occasion, the resulting intervals would bracket the true population parameter in approximately 95 % of the cases".
- Hoekstra, Morey, Rouder y Wagenmakers (2014) dieron seis afirmaciones falsas sobre un IC a 120 investigadores, 442 estudiantes de primer año y 34 de maestría: en promedio aceptaron 3,51 (estudiantes), 3,24 (maestría) y 3,45 (investigadores). Una de las falsas es exactamente la de la clase: "There is a 95% probability that the true mean lies between…". O sea, el error de Karim es el error típico de la gente que sabe estadística, no de principiante.
- Morey y otros (publicado en 2015 en Psychonomic Bulletin & Review) llaman a esa lectura "Fundamental Confidence Fallacy" y suman otras dos: creer que el ancho del IC mide siempre la precisión y que los valores de adentro son "los probables". Citan a Neyman (1937): sobre un intervalo ya calculado, "the answer is obviously in the negative". Para ellos, si querés esa interpretación, necesitás un intervalo bayesiano (de credibilidad); vuelvo a esto en el análisis adversario.

**Cómo implementarlo.** En el entregable escribí, por ejemplo: "Con un procedimiento que acierta el 95% de las veces, la diferencia de medias del bruto entre varones cis y mujeres cis que responden la encuesta está entre 651 mil y 946 mil pesos. El intervalo no incluye el 0." Y si querés decir "95% de probabilidad", hacé el análisis bayesiano de la sección 5 y decilo sobre el intervalo de credibilidad, aclarando la previa.

#### 3.3 Wilcoxon contra Mann Whitney

**Qué dice la fuente.** "Mann Whitney para una población y Wilcoxon para más de una" C4P1 1:59:12, y antes "para el de dos grupos Wilcoxon" C4P1 1:52:48.

**Qué suma el material externo.** scipy define `wilcoxon` para "related paired samples" y lo llama la versión no paramétrica del t apareado, y `mannwhitneyu` para "two independent samples". Demšar (2006) lo usa así: Wilcoxon de rangos con signo como "a non-parametric alternative to the paired t-test" (por ejemplo, dos clasificadores evaluados en los mismos datasets).

**Cómo implementarlo.** Bruto contra neto de la misma persona: `stats.wilcoxon(bruto - neto)`. Varones contra mujeres: `stats.mannwhitneyu(h, m)`. Ojo que Mann Whitney no compara medianas salvo que las dos distribuciones tengan la misma forma; compara si un valor de un grupo tiende a ser mayor que uno del otro.

#### 3.4 Errores de tipo I y II, y qué es α

**Qué dice la fuente.** Georgina define el error de tipo I como "tendría que haber rechazado y no rechacé" y se corrige C4P1 1:04:39, C4P1 1:05:46. Karim define α como "la probabilidad de equivocarnos cuando aceptemos que no hay cambios" C4P2 3:51. Y aparece "un 0,14 de error no está bueno" para un p valor C4P2 18:31.

**Qué suma el material externo.** El NIST: "α = 0.05 implies that the null hypothesis is rejected 5 % of the time when it is in fact true"; el riesgo de no rechazar una H0 falsa, β, "is not chosen by the user but is determined… by the magnitude of the real discrepancy", y baja α sube β. La ASA (2016), principio 2: "P-values do not measure the probability that the studied hypothesis is true". Mi g08 da 4,76% de rechazos en 5000 tests con H0 cierta, y la simulación de la sección 6, entre 4,3% y 5,6% según el test y el n.

**Cómo implementarlo.** Escribí la tabla de 2 × 2 (decisión contra realidad) en el informe, fijá α antes de mirar y, si te piden β, elegí una alternativa concreta (como las lámparas de 5000 contra 5200 horas) y calculala con `statsmodels.stats.power` o simulando.

#### 3.5 ANOVA y comparaciones de a pares

**Qué dice la fuente.** A la pregunta de si el test se hace dos a dos, Karim responde "sí, se hacen todos contra todos" C4P2 34:06; y llama "bilateral" al ANOVA C4P2 31:56.

**Qué suma el material externo.** El NIST lo dice casi con las mismas palabras: "Doing pairwise comparison procedures over and over again for all possible pairs will not, in general, work. This is because the overall significance level is not as specified for a single pair comparison", y presenta el F del ANOVA como "a preliminary test". OpenIntro dedica un apartado de la sección 7.5 a las comparaciones múltiples después del ANOVA. scipy trae `tukey_hsd`, pensado para después de `f_oneway`. Para varios clasificadores sobre varios datasets, Demšar recomienda Friedman con su post hoc (Nemenyi) y los diagramas de diferencia crítica.

**Cómo implementarlo.**

```python
# anova_posthoc.py: F global y después Tukey HSD (LabTAT del notebook 05)
import pandas as pd
from scipy import stats
lab = pd.read_csv("/workspace/yt/ayvd_repo/LabTAT.csv")
grupos = [lab[c].dropna() for c in lab.columns]
print(stats.f_oneway(*grupos))   # ¿alguna media difiere?
print(stats.tukey_hsd(*grupos))  # ¿cuáles? (en la guía: todos salvo Laboratorio 1 contra 2)
```

#### 3.6 Outliers: 1,5 y 3 rangos intercuartílicos

**Qué dice la fuente.** Georgina dice "fuera de tres veces el rango intercuartílico uno tiene datos atípicos" C2P2 9:12 y dibuja los bigotes en 1,5 IQR C2P2 14:13; el notebook 02 y V04 usan "2,5 × Q3" V04 3:52.

**Qué suma el material externo.** El NIST define cercos internos en Q1 − 1,5·IQ y Q3 + 1,5·IQ y externos en Q1 − 3·IQ y Q3 + 3·IQ: "A point beyond an inner fence on either side is considered a mild outlier. A point beyond an outer fence is considered an extreme outlier." O sea, las dos cifras de Georgina son correctas, para dos niveles distintos. El "2,5 × Q3" no aparece en ninguna fuente. OpenQube, que publica el análisis oficial de la encuesta, usa justamente el método del rango intercuartílico, por separado para sueldos dolarizados y no dolarizados, y además saca los sueldos menores a medio salario mínimo porque el cerco inferior da negativo (sección 8).

**Cómo implementarlo.** En la guía, Tukey 1,5 IQR marca 202 filas del bruto y el "2,5 × Q3" 61. Reportá los dos cercos y decidí con criterio de dominio, como pidió Karim C3P1 1:24:49.

#### 3.7 scipy y la t "arriba de 100 grados de libertad"

**Qué dice la fuente.** "Si los grados de libertad pasan de 100, Python usa el test normal" C4P2 19:39.

**Qué suma el material externo.** La documentación de `ttest_ind` en scipy 1.18 dice que el p valor sale de "a theoretical t-distribution" por defecto, y que desde la versión 1.15 se puede pedir `method=PermutationMethod(...)` o `MonteCarloMethod(...)`. También trae `trim`, el t recortado de Yuen, "recommended if the underlying distribution is long-tailed or contaminated with outliers". Ninguna opción cambia a la normal según los grados de libertad. Con df = 1943 (la brecha), el cuantil 0,975 de la t es 1,961 y el de la normal 1,960: por eso parece lo mismo.

**Cómo implementarlo.** `stats.ttest_ind(h, m, equal_var=False, trim=0.2)` para Yuen, y `stats.ttest_ind(h, m, method=stats.PermutationMethod(n_resamples=9999))` para la versión por permutación. Delacre, Lakens y Leys (2017) recomiendan usar Welch por defecto en lugar de Student porque "the assumption of equal variances will seldom hold" y Student "can be severely biased" cuando no se cumple.

### 4. El p valor según la ASA, y qué cambia en el entregable

**Qué dice la fuente.** La materia enseña la receta de Neyman Pearson (H0, H1, α, estadístico, región de rechazo) y el p valor como información adicional ("¿por cuánto no estoy rechazando?") C4P2 5:29, y la pregunta del entregable es binaria: "¿las mujeres cobran menos que los hombres?" C4P2 45:37.

**Qué suma el material externo.**
- La declaración de la ASA (Wasserstein y Lazar, 2016) da seis principios: (1) el p valor puede indicar cuán incompatibles son los datos con un modelo; (2) no mide la probabilidad de que la hipótesis sea cierta; (3) las decisiones no deberían basarse solo en si pasa un umbral; (4) hay que reportar todo con transparencia; (5) no mide el tamaño del efecto ni su importancia; (6) solo, no es una buena medida de evidencia.
- El editorial de 2019 (Wasserstein, Schirm y Lazar, "Moving to a World Beyond 'p < 0.05'") va más lejos, con una sección titulada "Don't Say 'Statistically Significant'", y resume la propuesta en ATOM: "Accept uncertainty. Be thoughtful, open, and modest."
- Ho y otros (2019, Nature Methods), los autores de dabest, proponen "estimation graphics": mostrar los datos y la distribución bootstrap de la diferencia en lugar de un asterisco. Declaran no tener conflictos de interés, pero escriben sobre su herramienta.
- Cumming (2014, "The New Statistics: Why and How", Psychological Science) pide pasar de los tests a la estimación: tamaños de efecto, intervalos y metaanálisis.

**Cómo implementarlo (sugerencia).** Contestá la pregunta del entregable con el test que pide la materia y agregá tres cosas: el tamaño (diferencia de medias con su IC, cociente de medianas con su IC bootstrap y g de Hedges), el mismo análisis por seniority y una frase sobre a quién representa la muestra. La sección 5 tiene todos los números.

### 5. Benchmark: la brecha de género con cuatro métodos

**La pregunta.** La del entregable, sobre el bruto mensual de la encuesta 2026: varones cis (n = 3.861) contra mujeres cis (n = 983). La materia la contesta con Welch y un p valor. Acá la contesto también con un test de permutación, intervalos bootstrap, estadística de estimación con dabest y un modelo bayesiano (BEST de Kruschke en PyMC), con los mismos datos y midiendo tiempos.

```python
# bench_brecha.py (resumen; corre en el entorno de la guía, scipy 1.18.1)
import time, numpy as np, pandas as pd
from scipy import stats
df = pd.read_csv("/workspace/yt/ayvd_repo/sysarmy_survey_2026_processed.csv")
g = df.profile_gender.map({"Hombre Cis": "V", "Mujer Cis": "M"})
h = df.loc[g == "V", "salary_monthly_BRUTO"].to_numpy(float)
m = df.loc[g == "M", "salary_monthly_BRUTO"].to_numpy(float)
dmean = lambda a, b, axis=-1: np.mean(a, axis=axis) - np.mean(b, axis=axis)
dmed = lambda a, b, axis=-1: np.median(a, axis=axis) - np.median(b, axis=axis)

t0 = time.perf_counter(); w = stats.ttest_ind(h, m, equal_var=False)       # 1. Welch
print(w, w.confidence_interval(), time.perf_counter() - t0)
for f in (dmean, dmed):                                                      # 2. Permutación
    r = stats.permutation_test((h, m), f, n_resamples=10_000, vectorized=True, batch=500, random_state=1)
    print(r.statistic, r.pvalue)
for f, met in [(dmean, "percentile"), (dmean, "BCa"), (dmed, "percentile")]: # 3. Bootstrap
    b = stats.bootstrap((h, m), f, n_resamples=10_000, vectorized=True, method=met, batch=500, random_state=1)
    print(met, b.confidence_interval, b.standard_error)
```

```python
# bench_bayes.py (resumen; entorno aparte con PyMC 6.3.2). BEST: t de Student por grupo,
# previas vagas como en Kruschke (2013), sueldos en millones de pesos
import numpy as np, pymc as pm
def best(h, m):
    y = np.r_[h, m]; mu0, s0 = y.mean(), y.std()
    with pm.Model():
        mu = pm.Normal("mu", mu0, 1000 * s0, shape=2)
        sd = pm.Uniform("sd", s0 / 1000, s0 * 1000, shape=2)
        nu = pm.Exponential("nu_m1", 1 / 29) + 1
        pm.StudentT("yh", nu=nu, mu=mu[0], sigma=sd[0], observed=h)
        pm.StudentT("ym", nu=nu, mu=mu[1], sigma=sd[1], observed=m)
        idata = pm.sample(2000, tune=1000, chains=4, random_seed=1)
    d = (idata.posterior["mu"][..., 0] - idata.posterior["mu"][..., 1]).values.ravel()
    return d.mean(), np.percentile(d, [2.5, 97.5]), (d > 0).mean()  # el script completo da el HDI
```

dabest lo corrí con `dabest.load(d, x="g", y="bruto_M", idx=("Mujer cis", "Varón cis"), resamples=5000)` y pedí `mean_diff`, `median_diff` y `hedges_g`.

**Resultados (muestra completa).**

| Método | Qué estima | Estimación | Intervalo 95% | p o probabilidad | Tiempo |
|---|---|---|---|---|---|
| Welch (scipy) | Diferencia de medias | 798.107 | (650.632; 945.583) | p = 1,3 × 10⁻²⁵ bilateral; t = 10,61; df = 1.943 | 0,0013 s |
| Permutación, 10.000 (scipy) | Diferencia de medias | 798.107 | | p = 0,0002, el mínimo posible con 10.000 permutaciones (1/10.001) | 1,0 s |
| Permutación, 10.000 (scipy) | Diferencia de medianas | 650.941 | | p = 0,0002 | 1,5 s |
| Bootstrap percentil, 10.000 (scipy) | Diferencia de medias | 798.107 | (650.531; 940.776) | error estándar 74.612 | 0,36 s |
| Bootstrap BCa, 10.000 (scipy) | Diferencia de medias | 798.107 | (648.540; 938.531) | | 0,44 s |
| Bootstrap percentil, 10.000 (scipy) | Diferencia de medianas | 650.941 | (500.000; 811.000) | | 0,93 s |
| dabest, 5.000, BCa | Diferencia de medias | 798.107 | (648.562; 942.151) | p de permutación menor a 1/5.000 (dabest lo muestra como 0) | 5,9 s para los tres efectos, más unos 7 s de compilar numba la primera vez |
| dabest | Diferencia de medianas | 650.941 | (476.000; 800.000) | dabest avisa que BCa con la mediana puede estar sesgado | (incluido) |
| dabest | g de Hedges | 0,323 | (0,263; 0,379) | | (incluido) |
| BEST, PyMC, escala original | Centro de una t con ν ≈ 3,3 (robusto) | 643 mil | HDI (523 mil; 770 mil) | P(diferencia > 0) = 1,000; r̂ = 1,00 | 4,5 s de muestreo |
| BEST, PyMC, logaritmo del bruto | Cociente de centros | 1,228 | HDI (1,178; 1,280) | P(cociente > 1) = 1,000; ν ≈ 13,8 | 3,4 s de muestreo |
| Cociente de medianas (descriptivo) | Cociente de medianas | 1,232 (3.450.941 / 2.800.000) | | | |

El script bayesiano completo (importar PyMC, compilar y ajustar tres modelos) tardó 12,3 s de reloj. El gráfico de Gardner Altman de dabest con 4.844 puntos avisa que no puede ubicar el 88% de los puntos en el enjambre; con muestras así de grandes conviene cambiar el enjambre por una distribución.

**Qué muestra.**
- **Con la muestra completa, todos dicen lo mismo.** La diferencia de medias es unos 800 mil pesos con un intervalo de 650 mil a 940 mil según el método; Welch, el bootstrap percentil, el BCa y dabest coinciden en los primeros dos dígitos. El p de permutación no puede bajar de 1/10.001, así que "p = 0,0002" no significa que la evidencia sea más débil que la de Welch, sino que se terminó la resolución.
- **El estimando cambia más que el método.** La media difiere en 798 mil, la mediana en 651 mil, el centro robusto de BEST en 643 mil. BEST estima ν ≈ 3,3 (colas muy pesadas), y con eso su μ se comporta como un centro robusto, cerca de la mediana. No es que Bayes "dé otro resultado": contesta otra pregunta. Elegí el estimando antes de elegir el método.
- **En escala relativa, todos convergen en un 23%.** Cociente de medianas 1,232; cociente bayesiano en logaritmos 1,228 (1,178 a 1,280); g de Hedges 0,32, un efecto "chico a mediano" en la escala de Cohen.
- **El tiempo no es un argumento con estos tamaños.** Lo más lento (BEST) tarda segundos; el costo real del enfoque bayesiano es instalar PyMC y explicar las previas, no la CPU.

**Con poca muestra, la historia cambia.** Saqué al azar 30 varones y 30 mujeres (semilla 7):

| Método | Estimación | Intervalo 95% | Lectura |
|---|---|---|---|
| Welch | 0,779 M | (−0,615; 2,172) | p = 0,27: no se rechaza |
| BEST | 0,381 M | HDI (−0,892; 1,815) | P(diferencia > 0) = 0,70 |

Welch dice "no rechazo", que muchos leen mal como "no hay diferencia". BEST dice "70% de probabilidad de que los varones ganen más, con mucha incertidumbre", que es lo que la gente quiere decir, pero solo vale con las previas y la verosimilitud elegidas (y su centro robusto, 0,38, no es la diferencia de medias, 0,78). Ninguno de los dos sirve para afirmar nada con 30 y 30: los dos intervalos van de −0,9 a 2 millones.

**La brecha dentro de cada seniority** (`bench_estratos.py`, Welch más cociente de medianas con bootstrap percentil de 5.000):

| Seniority | n varones / mujeres | Diferencia de medias (M) | IC 95% Welch | p | Cociente de medianas | IC 95% bootstrap |
|---|---|---|---|---|---|---|
| Junior | 368 / 155 | 0,173 | (−0,024; 0,370) | 0,085 | 1,000 | (0,928; 1,102) |
| Semi Senior | 1.123 / 360 | 0,381 | (0,216; 0,546) | 6,6 × 10⁻⁶ | 1,120 | (1,064; 1,217) |
| Senior | 2.370 / 468 | 0,687 | (0,459; 0,916) | 5,3 × 10⁻⁹ | 1,149 | (1,028; 1,205) |

El cociente general (1,23) es mayor que el de cada grupo (1,00 a 1,15) porque el 15,8% de las mujeres que responden son junior contra el 9,5% de los varones, y el 47,6% son senior contra el 61,4%. Parte de la brecha general es de composición; la que queda dentro de Semi Senior y Senior sigue siendo clara. Esto es lo que pidió Georgina con "mirar condicionales" C4P1 44:21, y es más importante que la elección entre Welch, permutación o Bayes. Tampoco es causal: faltan rol, tecnología, horas, provincia y dolarización.

### 6. ¿Cuándo alcanza la t? Simulación con la encuesta como población

Para ver qué método se equivoca menos con muestras chicas, tomé la encuesta como si fuera la población (la diferencia "verdadera" de medias es 0,798 M) y saqué 4.000 pares de muestras de cada tamaño. Medí la cobertura de los intervalos de 95% (Welch y bootstrap percentil con 2.000 remuestreos) y, mezclando los dos grupos para que H0 sea cierta, la tasa de falsos positivos de Welch, de la permutación (2.000) y de Mann Whitney.

```python
# bench_sim.py (resumen)
for n in [10, 30, 100]:
    for _ in range(4000):                       # cobertura
        h, m = rng.choice(H, n, replace=False), rng.choice(M, n, replace=False)
        ci = stats.ttest_ind(h, m, equal_var=False).confidence_interval()
        bh = rng.choice(h, (2000, n)).mean(1) - rng.choice(m, (2000, n)).mean(1)
        lo, hi = np.percentile(bh, [2.5, 97.5])
    for _ in range(4000):                       # error de tipo I: los dos de la misma población
        a, b = rng.choice(P, n, replace=False), rng.choice(P, n, replace=False)
        # Welch, Mann Whitney y permutación de la diferencia de medias, p < 0,05
```

| n por grupo | Cobertura Welch | Cobertura bootstrap percentil | Ancho medio Welch / bootstrap (M) | Error de tipo I Welch / permutación / Mann Whitney | Tiempo |
|---|---|---|---|---|---|
| 10 | 0,952 | **0,902** | 4,24 / 3,67 | 0,044 / 0,056 / 0,049 | 12 s |
| 30 | 0,952 | 0,937 | 2,35 / 2,25 | 0,044 / 0,047 / 0,043 | 16 s |
| 100 | 0,964 | 0,962 | 1,28 / 1,26 | 0,049 / 0,050 / 0,047 | 44 s |

Con 4.000 repeticiones, el error de Monte Carlo de una proporción cerca de 0,95 es de unos ±0,7 puntos. Lecturas:
- **Welch funciona desde n = 10 con estos sueldos** (asimetría 1,71). El "necesito más de 100" de la clase es demasiado conservador para la media de una diferencia de grupos parecidos.
- **El bootstrap percentil es el que falla con muestras chicas**: con 10 por grupo cubre el 90%, porque la distribución bootstrap es demasiado angosta con pocos datos. Es un recordatorio de que el bootstrap no es magia y que sus intervalos son aproximados.
- **Los tres tests controlan el error de tipo I cerca del 5%.** La permutación queda un poco arriba con n = 10 (5,6%, a menos de dos errores de Monte Carlo).
- **Con n = 100 los dos intervalos cubren de más (96%)** porque saco sin reposición 100 de 983 mujeres: la población es finita y el factor de corrección (√(1 − 100/983) ≈ 0,95) achica la variabilidad real. Una primera corrida con 1.000 repeticiones había dado 0,944, dentro de su error de ±1,4 puntos.

### 7. Visualización: de Cleveland y McGill a Datasaurus

**Qué dice la fuente.** La materia muestra la jerarquía de escala común C4P2 1:35:05, las trampas del eje truncado y del gráfico de torta, y pide un solo mensaje claro.

**Qué suma el material externo.**
- **Cleveland y McGill (1984)** midieron con experimentos la precisión con que la gente lee cada canal: posición sobre escala común primero, después posición en escalas no alineadas, longitud, dirección y ángulo, área, volumen y curvatura, y al final sombreado y saturación. De ahí sale preferir puntos o barras a tortas y burbujas. Proponen "dot charts" y piden "radical surgery" para tortas y barras apiladas.
- **Anscombe (1973)**: cuatro conjuntos de 11 puntos con estadísticos casi idénticos y gráficos muy distintos, armados para contrarrestar la idea de que "numerical calculations are exact, but graphs are rough".
- **Datasaurus Dozen** (Matejka y Fitzmaurice, Autodesk Research, CHI 2017, inspirado en el Datasaurus original de Alberto Cairo): un método de recocido simulado que genera conjuntos con los mismos estadísticos y formas arbitrarias (un dinosaurio, una estrella, círculos). Es el argumento a favor de mostrar la distribución y no solo la media con una barra de error, como en el "dynamite plot" de la guía.
- **Tyler Vigen, Spurious Correlations**: correlaciones absurdas entre series (con la leyenda "correlation is not causation"), útiles para la clase de causalidad.

**Cómo implementarlo.** En el gráfico final de la brecha, usá puntos o boxplots por seniority y género sobre una escala común, mostrá la distribución (boxen, violín o histogramas en paneles), anotá la diferencia con su intervalo y evitá la torta. Para los datasets de Anscombe, `seaborn.load_dataset("anscombe")` los trae listos.

### 8. La encuesta de Sysarmy: cómo se limpia y a quién representa

**Qué dice la fuente.** La materia insiste en que la encuesta es voluntaria y no es una muestra aleatoria: Ω son "los que contestaron la encuesta" C2P1 1:03:16, un alumno cuenta que "circula por la web" y llega a cualquiera C2P1 1:43:02, y Georgina pregunta si el 80% de Buenos Aires es real o es que "el registro no se enteró" C2P1 1:54:06.

**Qué suma el material externo.**
- **Participación.** Sysarmy dice que la edición 2026.1 tuvo 5.074 participantes y que 4.939 respuestas (97%) entraron al análisis. El CSV procesado de la materia tiene exactamente esas 4.939 filas, con bruto entre 200.000 y 20.000.000 pesos.
- **La metodología de OpenQube**, que publica el análisis oficial, admite la subjetividad ("¿Quieren decir que existe subjetividad en este reporte? Así es") y explica sus pasos: usa la mediana del salario bruto ("suele estar levemente por debajo del valor promedio"); descarta outliers con el método del rango intercuartílico por separado para sueldos dolarizados y no dolarizados ("es muy posible que existan salarios reales que hayan quedado fuera"); elimina los sueldos menores a medio salario mínimo porque el cerco inferior da negativo; ajusta las series por el IPC del INDEC; y marca en gris las medianas "no confiables", aquellas cuyo intervalo de confianza del 95% es más ancho que el 50% de la mediana.
- **Seniority.** OpenQube agrupa por años de experiencia: semi senior "de 2 años inclusive hasta 5 años" y senior "desde 5 años inclusive". En el CSV de la materia, `work_seniority` corta distinto: Junior hasta 2 años, Semi Senior de 3 a 5 y Senior desde 6. Si comparás tus números con los de OpenQube, no van a coincidir exactamente por eso.
- **Lo que no dice.** La metodología no habla de autoselección ni de ponderación: nadie corrige que el 50% de las respuestas venga de CABA y el 21,5% de la provincia de Buenos Aires. El dato de control externo más cercano es el salario promedio registrado del sector software según OPSSI ($3.738.000 en marzo de 2026), parecido a la media del bruto en la encuesta (3.876.029), aunque miden poblaciones distintas (empleo registrado de todo el sector contra quienes responden).

**Cómo implementarlo.** En el informe, escribí una oración de alcance ("los resultados describen a quienes respondieron la encuesta 2026.1; no es una muestra aleatoria del sector") y, si querés comparar con OpenQube, aplicá sus mismos filtros y su definición de seniority.

### 9. Libros y documentación: qué sacar de cada uno

- **OpenIntro Statistics** (gratis, con PDF): la mejor referencia para las condiciones del TCL, la condición de éxito y fracaso, el ANOVA con comparaciones múltiples y un apartado sobre por qué se usa 0,05. Sus laboratorios están en R.
- **Think Stats, tercera edición** (Allen Downey, versión online gratis con notebooks): "an introduction to Probability and Statistics for Python programmers", con pandas y simulación; es el más cercano al estilo de la materia. Tiene links de afiliado para la versión impresa.
- **Fundamentals of Data Visualization** (Claus Wilke, gratis en la web): estéticas, escalas, color, proporciones, incertidumbre; ejemplos en R (ggplot2) pero los principios se aplican igual en seaborn.
- **Data Visualization: A Practical Introduction** (Kieran Healy): la web tiene el borrador completo de la segunda edición (marzo de 2026), que va a publicar Princeton University Press; también en R.
- **The Visual Display of Quantitative Information** (Edward Tufte, 1983, segunda edición 2001, 197 páginas): el clásico de la relación tinta y datos, los "small multiples" y la detección del engaño gráfico. **No es gratis**: se compra en Graphics Press.
- **Storytelling with Data** (Cole Nussbaumer Knaflic): los libros **son pagos**; el sitio tiene recursos y un blog gratis. Bueno para la parte de "un solo mensaje".
- **Documentación de seaborn 0.13.2** (la del entorno de la guía) y **de matplotlib 3.11.2**: la guía de usuario de seaborn explica `errorbar`, los `stat` de `histplot` y la interfaz `seaborn.objects`; la de matplotlib, figuras, ejes y `savefig`.

### 10. Correcciones a mis archivos de la primera parte

Para tenerlas juntas (todas están también en la tabla de la sección 1):

1. **Karim Nemer es mujer**: Dra. Ing., profesora adjunta e investigadora del CIII (UTN FRC). En el módulo 0 del apunte, "ingeniero en sistemas", "doctor en ingeniería" y "él" deberían ser "ingeniera", "doctora" y "ella"; y quien la describe en C1P1 12:14 es Georgina, no ella misma.
2. **"CPIE" es el CIII**, Centro de Investigación en Informática para la Ingeniería: se va el "para verificar".
3. **Las fechas de C3 y C4 (10/04 y 11/04) están confirmadas** por el calendario oficial: se va el "para verificar" de la tabla de videos.
4. **Georgina tomó la coordinación en 2022**, pero en 2026 la coordinadora es Carolina Chavero; "coordinadora desde 2022" en presente es impreciso.
5. **El blog "El arte de medir" se menciona en C4P2 59:43**, no en 57:26 como puse.
6. **Los dos papers de C1P1 están identificados**: Donoho, "50 Years of Data Science", y Alvarado, "Data Science from 1963 to 2012"; el "dudoso" sobre el autor queda resuelto.
7. **Friedman, Cardellino, OpenQube, Cleveland y McGill y la suma de exponenciales** pasan de "dudoso" o "para verificar" a resueltos con fuente (secciones 1 y 2).

## Críticas y límites

- **Un solo dataset y una sola pregunta.** El benchmark compara métodos sobre la brecha de género del bruto 2026. Con otra variable (por ejemplo, proporciones o datos con ceros) el ranking de métodos podría cambiar.
- **La encuesta es autoseleccionada.** Todo lo que estimo describe a quienes respondieron. La simulación de la sección 6 usa la propia encuesta como "población", así que dice qué método anda mejor con distribuciones como esta, no cuál es la brecha real del sector.
- **El modelo bayesiano usa las previas vagas de Kruschke.** Con muchos datos casi no importan; con 30 y 30 sí, y no probé previas informativas. La submuestra de 30 y 30 es una sola extracción (semilla 7): sirve para ilustrar, no para generalizar.
- **El p de permutación tiene resolución limitada** (1/10.001 con 10.000 permutaciones), y BCa sobre la mediana no terminó en varios minutos con scipy (lo corté); dabest lo calcula pero avisa que puede estar sesgado.
- **Entornos.** La parte bayesiana corre en un entorno aparte con versiones más viejas de scipy y pandas (las que pide PyMC 6.3.2 y dabest); lo frecuentista, con las mismas versiones de la guía. Instalar PyMC en el entorno de la guía bajaba pandas, numpy y scipy; lo revertí y volví a correr los scripts g00 a g09 con salidas idénticas.
- **Conflictos de interés.** La CESSI es la cámara del sector y produce el dato de empleo; CrowdFlower y Anaconda venden herramientas para el trabajo cuyo peso miden; Kruschke defiende su propio método; Ho y otros escriben sobre dabest (declaran no tener intereses en competencia); la documentación de PyMC, scipy, seaborn y matplotlib la escriben sus autores; Allen Downey usa links de afiliado; Tufte y Storytelling with Data venden sus libros y cursos. La ASA y el NIST no venden nada de lo que recomiendan.
- **Afirmaciones que no pude cerrar:** las fechas de los entregables (solo en el aula virtual), la "mención en electrónica" del doctorado de Karim, el "90% de estudios observacionales", la "poda" de casos de cáncer y que fuera Marlboro, y los parámetros con los que Karim obtuvo una varianza de 0,01.
- **Leí con curl** (texto o PDF con `pdftotext`): el calendario, el folleto y la página de Aprendizaje Profundo de la diplomatura; las páginas del CIII; los PDF de Demšar, Cleveland y McGill, CrowdFlower 2016, Anaconda 2020, los dos informes OPSSI, la declaración de la ASA, Wasserstein y otros (2019), Hoekstra y otros (2014), Kruschke (2013) y Donoho (2015); Brandt en PMC; Wikipedia (Ronald Fisher, Erlang, Exponential distribution, Bootstrapping, Anscombe's quartet) en texto crudo; las páginas del NIST; la documentación de scipy (`wilcoxon`, `mannwhitneyu`, `tukey_hsd`, `friedmanchisquare`, `bootstrap`, `permutation_test`, `contingency.association`); Think Stats, Wilke, Healy, Tufte, Storytelling with Data, seaborn y matplotlib; la ficha de Georgina en la FCE; arXiv de Alvarado; Nature Methods (Ho y otros); Autodesk Research; Cumming en SAGE; dabest; PyMC (BEST); Delacre y otros; Tyler Vigen; el post de Sysarmy; la nota de Relación Cliente y el blog archivado de El Arte de Medir. La metodología de OpenQube la saqué del paquete JavaScript del sitio, porque la página es una aplicación que no muestra texto sin navegador.
- **Abrí con el lector web:** el inicio del sitio de la diplomatura, la página de Demšar en JMLR, la de Cardellino en Medium, el post de Leigh Dodds, la de `ttest_ind` en scipy, la de OpenIntro y el paper de Morey y otros en Springer.
- **Solo vi en resultados de búsqueda:** el LinkedIn de Cardellino, la ficha de Karim en el repositorio de la UTN, Stolley (1991) "When genius errs" sobre Fisher y el tabaco, y el post de Sysarmy en LinkedIn que bromea con "confundir mediana con media".
- **No cargaron:** Taylor & Francis (Cleveland y McGill, la ASA y el editorial de 2019; los leí en copias PDF), la nota de Gil Press en Forbes (vacía), PubMed (403), APA PsycNet (Kruschke), Project Euclid (Efron, 1979) y `elartedemedir.com` (sin respuesta).

## Análisis adversario

> Cómo leer esto: acá discuto el enfoque de la materia contra la alternativa más fuerte que encontré, con la mejor versión posible de esa alternativa. No es una crítica a las docentes: una materia de cuatro encuentros tiene que elegir, y esto sirve para que sepas qué elegirías vos en un trabajo real.

**La tesis.** La materia enseña inferencia frecuentista con tests de hipótesis: plantear H0 y H1, fijar α, calcular un estadístico z, t o de Welch, y rechazar si p < α. El intervalo de confianza aparece, pero la pregunta del entregable es binaria ("¿las mujeres cobran menos que los hombres?") y la respuesta esperada es "rechazo" o "no rechazo".

### La alternativa más fuerte: estimación (la "New Statistics"), con remuestreo como motor

Consideré tres alternativas. **El remuestreo** (permutación y bootstrap) cambia cómo se calcula el p o el intervalo, pero no la lógica: en mi benchmark da los mismos números que Welch, así que lo trato como herramienta, no como enfoque rival. **El análisis bayesiano** (BEST de Kruschke, PyMC) es el más distinto: da probabilidades directas sobre el efecto, pero exige previas, otra librería y otra forma de explicar. **La estimación** cambia la pregunta de "¿hay diferencia?" a "¿cuánto, y con cuánta incertidumbre?", usando tamaños de efecto con intervalos, y con bootstrap cuando no hay fórmula. Elegí la estimación porque es la que más respaldo institucional tiene (la ASA, Nature Methods, Psychological Science), porque se hace con las mismas herramientas de la materia (scipy ya devuelve el intervalo) y porque mi benchmark muestra que lo que cambia la conclusión es el estimando y el condicionamiento, que es justo lo que la estimación pone en primer plano. Bayes queda como extensión para muestras chicas, y lo uso en el híbrido.

### La alternativa en su mejor versión

**Quién la defiende.** Geoff Cumming ("The New Statistics: Why and How", 2014); la ASA en su declaración de 2016 y el editorial de 2019, que pide dejar de decir "statistically significant"; Ho y otros (2019) con dabest y los "estimation graphics"; Kruschke (2013), que también pone la estimación en el centro (su título es "Bayesian estimation supersedes the t test"); Efron, con el bootstrap, como motor para cualquier estadístico. Conflictos de interés: Ho y otros y Kruschke promueven sus propias herramientas.

**Qué evidencia la respalda.**
- La ASA, principio 5: el p valor "does not measure the size of an effect or the importance of a result". En la brecha, p = 1,3 × 10⁻²⁵ no dice si la diferencia es de 2% o de 23%; el intervalo (651 mil a 946 mil pesos), el cociente de medianas (1,23) y g = 0,32 sí.
- Con n grande cualquier diferencia "da significativa": con 4.844 personas, un efecto chico a mediano produce un p de 10⁻²⁵. La decisión binaria no agrega información; el tamaño sí.
- Con n chico, la estimación evita el error de leer "no rechazo" como "no hay diferencia": en la submuestra de 30 y 30, Welch da p = 0,27, pero el intervalo (−0,6 a 2,2 millones) muestra que no sabemos casi nada.
- La estimación lleva naturalmente a preguntar "¿cuánto, dentro de cada grupo?", y ahí aparece lo más importante del análisis: el cociente baja de 1,23 a 1,00, 1,12 y 1,15 por seniority.
- Es barata: Welch con su intervalo tarda 1 ms, el bootstrap 0,4 s, y dabest hace el gráfico de estimación en una línea.

**Qué evidencia la contradice.**
- **Los intervalos también se malinterpretan.** Hoekstra y otros (2014): los investigadores aceptan en promedio 3,45 de 6 afirmaciones falsas sobre un IC. Cambiar el p por el IC no arregla la interpretación por sí solo.
- **La teoría de los IC no da lo que la estimación promete.** Morey y otros sostienen que el ancho de un IC no siempre mide la precisión ni sus valores son "los plausibles", y que para esa lectura hace falta un intervalo bayesiano. Citan además un comentario de Morey, Rouder y otros (2014) a Cumming titulado "Why hypothesis tests are essential for psychological science" (lo vi citado, no lo abrí).
- **El bootstrap no es gratis en calidad.** En mi simulación, el percentil con 10 por grupo cubre el 90% en vez del 95%, peor que Welch; BCa sobre la mediana se colgó en scipy y dabest avisa que puede estar sesgado.
- **A veces hay que decidir.** En control de calidad o en un test A/B con regla fija, lo que importa es controlar la tasa de errores de las decisiones, que es exactamente lo que da el marco de Neyman Pearson (el NIST presenta los tests como "a mechanism for making quantitative decisions").

### Comparación directa

| Criterio | A: tests de hipótesis (la materia) | B: estimación con remuestreo | C: Bayes (BEST), la otra candidata |
|---|---|---|---|
| Costo | Ninguno: scipy, 1 ms | Casi ninguno: el IC de Welch sale gratis; bootstrap 0,4 a 1 s; dabest unos 6 s | Instalar PyMC; 3 a 5 s por modelo, 12 s el script completo |
| — | Baja en la receta, alta en la interpretación (p, α, β) | Baja; hay que elegir el estimando y el tipo de intervalo | Media a alta: previas, verosimilitud, diagnóstico de cadenas |
| Tiempo hasta valor | Inmediato para un sí o no | Inmediato para "cuánto" | Un rato más; inmediato si ya tenés la plantilla |
| Riesgo | Leer "no rechazo" como "no hay efecto"; efectos triviales "significativos" con n grande | Interpretar el IC como probabilidad; bootstrap con n chico | Previas mal elegidas; estimar otra cosa sin darte cuenta (el centro robusto de la t no es la media) |
| Madurez | Total | Alta: scipy (`bootstrap`, `permutation_test`), dabest | Alta: PyMC, ArviZ |
| Evidencia | Neyman Pearson, NIST; mi simulación: Welch cubre el 95% desde n = 10 y controla el error de tipo I | ASA 2016 y 2019, Cumming, Ho y otros; mi benchmark | Kruschke (2013), Morey y otros; mi benchmark |
| Contexto donde rinde | Decisiones con regla fija; protocolos que exigen p | Informes, comparaciones de grupos, estadísticos sin fórmula | Muestras chicas, información previa, preguntas tipo "¿qué probabilidad hay de que la brecha supere el 10%?" |

### Dónde gana la alternativa

- **En la pregunta del entregable leída en serio.** "¿Las mujeres cobran menos?" tiene una respuesta trivial con 4.844 respuestas; la interesante es "¿cuánto menos, y dónde?", y esa solo la contesta la estimación (23% en general, 0 en Junior, 12% a 15% en Semi Senior y Senior).
- **En la comunicación.** "Entre 651 mil y 946 mil pesos" se entiende; "p = 1,3 × 10⁻²⁵" no.
- **Con estadísticos sin fórmula cerrada**: el cociente de medianas con su intervalo bootstrap (1,06 a 1,22 en Semi Senior) no tiene un test de la materia que lo dé.

### Dónde pierde

- **Con muestras muy chicas y bootstrap percentil**: Welch es mejor (95% contra 90% de cobertura con 10 por grupo).
- **Cuando hay que decidir con una tasa de error conocida** (control de calidad, A/B): el marco de la materia es el adecuado.
- **En la interpretación**: si no se aprende bien qué es un IC, se cambia un error por otro (Hoekstra; Morey).
- **En la evaluación de la materia**, que pide el test, α y la región de rechazo: la estimación se suma, no reemplaza.

### Cómo decidir

**Elegí A (test de hipótesis) si…**
- la consigna o el cliente pide una decisión sí o no con una tasa de error controlada (control de calidad, test A/B con regla fijada de antemano);
- seguís un protocolo que exige p valor y α, como el entregable;
- hacés muchas comparaciones y necesitás controlar el error global (ANOVA con post hoc, Friedman con su post hoc);
- la muestra es chica y el estadístico es una media: Welch se porta bien desde 10 por grupo en mi simulación.

**Elegí B (estimación con remuestreo) si…**
- la pregunta real es "cuánto" y no "si hay";
- la muestra es grande y cualquier diferencia da un p minúsculo;
- el estadístico no tiene fórmula (cociente de medianas, percentiles, diferencias de proporciones raras) y tenés al menos unos 30 por grupo para el bootstrap;
- vas a comunicar a gente que no es estadística.

**Y C (Bayes) si** tenés pocos datos, información previa defendible o necesitás una probabilidad directa sobre un umbral de negocio.

**Un híbrido posible (sugerencia).** Para el entregable y para cualquier comparación de grupos: (1) definí antes el estimando, por ejemplo diferencia de medias del bruto y cociente de medianas; (2) hacé el test que pide la materia (Welch de una cola, α = 0,05) y reportá el p; (3) reportá el intervalo de Welch de la diferencia y, si hay colas pesadas, también el de Yuen (`trim=0.2`) y un p de permutación como control; (4) calculá el cociente de medianas con un intervalo bootstrap (BCa o percentil, con 30 o más por grupo) y la g de Hedges; (5) repetí todo por seniority y mostralo en una tabla y un gráfico sobre escala común; (6) en subgrupos chicos (por ejemplo, las identidades no binarias, con 22 respuestas), usá BEST con previas documentadas y reportá la probabilidad de que la brecha supere un umbral que tenga sentido, por ejemplo 10%; y (7) escribí la conclusión en magnitud y con el alcance de la muestra. Los scripts `bench_brecha.py`, `bench_estratos.py` y `bench_bayes.py` hacen cada paso.

**Veredicto.** En estos datos los cuatro métodos coinciden: la brecha media es de unos 800 mil pesos (23% en medianas) con cualquier método, y el tiempo de cómputo no decide nada. Lo que cambia la conclusión es qué estimás (media, mediana o centro robusto) y si condicionás por seniority. Por eso me quedo con B como forma de reportar, sin abandonar A: el test que pide la materia contesta el sí o no, y el intervalo, el cociente y la tabla por seniority contestan lo que importa. Bayes vale la pena cuando la muestra es chica o hay que decidir sobre un umbral.

## Material para seguir

**Para el entregable, en este orden**
- [scipy.stats.ttest_ind](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html): Welch, `alternative`, `trim` (Yuen), `method` (permutación) y `confidence_interval()`.
- [scipy.stats.bootstrap](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html) y [scipy.stats.permutation_test](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.permutation_test.html): intervalos y p para cualquier estadístico, sin instalar nada.
- [Metodología de OpenQube, encuesta 2026.01](https://sueldos.openqube.io/encuesta-sueldos-2026.01/): cómo limpia los sueldos el análisis oficial; buscá la sección "Metodología".
- [NIST e-Handbook, capítulo 7.1](https://www.itl.nist.gov/div898/handbook/prc/section1/prc13.htm): tests, errores, intervalos y outliers explicados por una agencia de estándares.
- [Calendario de la diplomatura](https://diplodatos.famaf.unc.edu.ar/calendar/): para ubicar las materias; las fechas de entrega, en el aula virtual.

**Estadística e inferencia**
- [OpenIntro Statistics](https://www.openintro.org/book/os/): libro gratis con PDF; TCL, condiciones, ANOVA y comparaciones múltiples.
- [Think Stats, tercera edición](https://greenteapress.com/wp/think-stats-3e/): estadística para programadores de Python, gratis online y con notebooks.
- [Delacre, Lakens y Leys (2017)](https://rips-irsp.com/articles/10.5334/irsp.82): por qué usar Welch por defecto.
- [Demšar (2006), JMLR](https://jmlr.org/papers/v7/demsar06a.html): Wilcoxon y Friedman para comparar clasificadores, para las materias de aprendizaje automático.
- [Wikipedia, Bootstrapping (statistics)](https://en.wikipedia.org/wiki/Bootstrapping_%28statistics%29): punto de entrada con la referencia a Efron (1979).

**p valores, intervalos y estimación**
- [Declaración de la ASA sobre p valores (2016), PDF](https://www.amstat.org/asa/files/pdfs/p-valuestatement.pdf): los seis principios en dos páginas.
- [Wasserstein, Schirm y Lazar (2019), PDF](https://www.unh.edu/halelab/ANFS933/papers/2019_Wasserstein.pdf): "Moving to a World Beyond 'p < 0.05'", con el ATOM.
- [Hoekstra y otros (2014), PDF](https://www.ejwagenmakers.com/inpress/HoekstraEtAlPBR.pdf): cuánto se malinterpretan los IC, con el cuestionario para hacerte a vos mismo.
- [Morey y otros, The fallacy of placing confidence in confidence intervals](https://link.springer.com/article/10.3758/s13423-015-0947-8): la crítica más dura a la estimación con IC, en acceso abierto.
- [Cumming (2014), The New Statistics](https://journals.sagepub.com/doi/10.1177/0956797613504966): el manifiesto de la estimación.
- [Ho y otros (2019), Nature Methods](https://www.nature.com/articles/s41592-019-0470-3) y [dabest](https://acclab.github.io/DABEST-python/): gráficos de estimación (escriben sobre su herramienta).

**Bayes**
- [Kruschke (2013), Bayesian Estimation Supersedes the t Test, PDF](https://joseph.research.mcgill.ca/courses/EPIB-682/Kruschke2013.pdf): el modelo BEST que usé (lo defiende su autor).
- [PyMC, ejemplo BEST](https://www.pymc.io/projects/examples/en/latest/case_studies/BEST.html): el mismo modelo en Python, listo para copiar.

**Visualización**
- [Cleveland y McGill (1984), PDF](https://www.dsciclass.org/dsci310/Notes/Cleveland_McGill_EPT.pdf): la jerarquía de canales visuales, con los experimentos.
- [Wilke, Fundamentals of Data Visualization](https://clauswilke.com/dataviz/): libro gratis, el mejor complemento de la clase de visualización.
- [Healy, Data Visualization](https://socviz.co/): borrador completo de la segunda edición (en R).
- [Tufte, The Visual Display of Quantitative Information](https://www.edwardtufte.com/book/the-visual-display-of-quantitative-information/): el clásico (pago).
- [Storytelling with Data](https://www.storytellingwithdata.com/books): para la parte de "un solo mensaje" (libros pagos, blog gratis).
- [Guía de usuario de seaborn](https://seaborn.pydata.org/tutorial.html) y [de matplotlib](https://matplotlib.org/stable/users/index.html): las versiones que usa la guía.
- [Same Stats, Different Graphs (Datasaurus Dozen)](https://www.research.autodesk.com/publications/same-stats-different-graphs/) y [el cuarteto de Anscombe](https://en.wikipedia.org/wiki/Anscombe%27s_quartet): por qué graficar siempre.
- [Tyler Vigen, Spurious Correlations](https://www.tylervigen.com/spurious-correlations): correlación no es causalidad, con humor.

**Contexto de lo que se dijo en clase**
- [Brandt (2012), AJPH](https://pmc.ncbi.nlm.nih.gov/articles/PMC3490543/): cómo la industria tabacalera fabricó la duda científica.
- [Leigh Dodds (2020)](https://blog.ldodds.com/2020/01/31/do-data-scientists-spend-80-of-their-time-cleaning-data-turns-out-no/): de dónde sale el "80% del tiempo limpiando datos".
- [Informe OPSSI del primer trimestre de 2026](https://cessi.org.ar/wp-content/uploads/2026/07/OPSSI-Reporte-Industria-Software-1er.-trim.-2026.pdf): empleo y salarios registrados del sector (lo publica la cámara empresaria).
- [Donoho, 50 Years of Data Science](https://courses.csail.mit.edu/18.337/2015/docs/50YearsDataScience.pdf) y [Alvarado, Data Science from 1963 to 2012](https://arxiv.org/abs/2311.03292): los dos papers de la primera clase.
