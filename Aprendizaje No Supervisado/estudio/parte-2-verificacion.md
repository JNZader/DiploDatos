# Segunda parte: "Aprendizaje No Supervisado", con material externo

**Esta es la continuación de** `aprendizaje-no-supervisado-apunte-de-estudio.md` y `aprendizaje-no-supervisado-guia-de-implementacion.md` (las clases de la materia Aprendizaje No Supervisado de la diplomatura en ciencia de datos de FAMAF UNC, cohorte 2026, dictadas por Laura Alonso Alemany y Georgina Flesia en cuatro encuentros: 24 y 25 de julio y 7 y 8 de agosto de 2026). Esos archivos resumen lo que dice la materia. Esta segunda parte suma material externo para verificar lo que en el apunte quedó "para verificar" o "dudoso", respaldar con fuentes las correcciones que ya marqué, proponer mejoras concretas para el trabajo especial sobre FIFA y para el trabajo real, medir con datos reales cuánto rinden los métodos de la materia y marcar dónde el enfoque tiene límites. Revisé todo el 02/10/2026. Solo cito páginas que abrí; cuando una página no cargó en el lector web y la leí con `curl` desde el box, lo digo, y cuando solo vi un resultado de búsqueda, también.

> Cómo leer esto: cuando digo "la materia" o "las docentes" me refiero a lo que dicen Laura y Georgina en las clases. Las marcas de tiempo usan la etiqueta de cada grabación del apunte (C1P1 es la clase 1, parte 1, y así hasta C4P2) y llevan al minuto exacto en la grabación. Cuando digo "sugerencia" es una idea mía que combina fuentes, no algo que diga una fuente puntual. Todo el código lo corrí en el box el 02/10/2026 con scikit-learn 1.9.1, umap-learn 0.5.12, NumPy 2.5.3, mlxtend 0.25 y networkx 3.7, sobre el archivo FIFA 2019 que la diplomatura publica en su GitHub. Marco los conflictos de interés donde importan: hay una herramienta recomendada en clase que firma la propia docente (pysentimiento), varias documentaciones las escriben los autores de la herramienta que recomiendan (UMAP, HDBSCAN, BERTopic, Snorkel), y algunas fuentes sobre empresas son comunicados o notas de esas mismas empresas (IBM con Banco Galicia, Cloudflare, Meta, Anthropic).

---

## Checklist actualizado (curso + mejoras)

1. Para el trabajo especial usá el dataset de Kaggle "EA Sports FC 24 complete player dataset" de Stefano Leone: trae los datos del modo carrera desde FIFA 15 hasta FC 24, con 109 atributos por jugador y licencia CC0, y los nombres de columnas llevan un prefijo por tipo de habilidad (la consigna de 2022 ya lo avisaba), así que revisá `df.columns` antes de copiar código de clase.
2. Si no podés entrar a Kaggle, el GitHub público de la diplomatura (DiploDatos/AprendizajeNOSupervisado) tiene los archivos FIFA 2018 y FIFA 2019 que se usaron en clase en distintas ediciones, sin necesidad de cuenta.
3. Escalá antes de agrupar con `StandardScaler` o `MinMaxScaler`, que trabajan por columna; no uses `Normalizer` para escalar variables, porque lleva cada **fila** (cada jugador) a norma 1.
4. No elijas K con la inercia más baja: la inercia siempre baja cuando sube K; usala para comparar corridas con el mismo K, y para elegir K mirá el codo junto con silueta, BIC (en mezclas de gaussianas) y la estabilidad.
5. Corré K-means con varias inicializaciones (`n_init`) y con `init="k-means++"`, que es el valor por defecto: el algoritmo siempre converge, pero a un mínimo local que depende del punto de partida.
6. Usá `MiniBatchKMeans` solo cuando tengas muchos datos y te importe el tiempo: optimiza el mismo objetivo con submuestras y da resultados "generalmente solo un poco peores", no evita mínimos locales.
7. Si querés otra distancia que no sea la euclídea, no la busques en `KMeans` (no tiene parámetro de métrica): usá `AgglomerativeClustering` con `metric` y `linkage="average"` o `"complete"`, DBSCAN o HDBSCAN, que aceptan otras métricas o distancias precalculadas.
8. Cuando compares agrupamientos con los testigos, recordá que el ARI va de -0,5 a 1 y puede ser negativo; 0 es lo que da el azar.
9. No te quedes con una sola métrica interna: en mis pruebas con FIFA, la silueta más alta (0,56) la saca un agrupamiento trivial de dos grupos, arqueros contra el resto, que tiene un ARI de apenas 0,19 contra las posiciones.
10. No uses un umbral fijo de silueta (por ejemplo, "menos de 0,4 es malo") como regla: no es una regla de scikit-learn y depende de la dimensión, del escalado y de la pregunta.
11. Si usás Yellowbrick, sabé que la segunda curva verde de `KElbowVisualizer` es el tiempo de ajuste de cada K (se apaga con `timings=False`), no una medida de calidad; y que Yellowbrick 1.5 falla con scikit-learn 1.9.1, así que en tu máquina puede romperse aunque en Colab funcione.
12. No uses t-SNE para agrupar: el paper original lo presenta como técnica de visualización, y la guía de Distill muestra que los tamaños de los grupos en el gráfico no significan nada, que las distancias entre grupos pueden no significar nada y que el ruido puro puede parecer agrupado con perplejidad baja.
13. Si agrupás sobre UMAP, seguí la receta de la documentación de UMAP: `min_dist=0.0`, `n_neighbors` más alto que para visualizar, más de dos componentes y un método por densidad como HDBSCAN; y sabé que UMAP también puede inventar cortes ("false tears") dentro de un grupo real.
14. En FIFA, UMAP no es una mejora segura: en mis pruebas sube el ARI de K-means (de 0,36 a 0,39 con todos los jugadores) pero baja el de la mezcla de gaussianas (de 0,41 a 0,37), y agrega entre 13 y 20 segundos de cómputo por corrida, cuando agrupar los datos escalados tarda de 0,04 a 2 segundos.
15. Si probás HDBSCAN (`sklearn.cluster.HDBSCAN`, desde la versión 1.3), sabé que en FIFA con todos los jugadores siempre separa arqueros contra el resto, y que con jugadores de campo puede mandar a ruido la mayoría de los puntos si no reducís la dimensión antes.
16. Si tenés testigos (posiciones), probá también la alternativa supervisada barata: con 50 jugadores etiquetados de 6.000, una regresión logística llega a un ARI de 0,48 contra las posiciones, más que el mejor clustering que medí (0,41).
17. Para elegir K por estabilidad, agrupá dos submuestras distintas, compará las etiquetas que asignan al conjunto completo con el ARI y quedate con los K estables; el código está en la sección 6.
18. En reglas de asociación, recordá que el lift es confianza dividida por el soporte del consecuente (no una probabilidad) y que la convicción vale infinito cuando la confianza es 1.
19. Para conjuntos de ítems grandes, usá `fpgrowth` de mlxtend en lugar de `apriori`: da los mismos conjuntos frecuentes sin generar candidatos.
20. Para comunidades en grafos, preferí Leiden a Louvain cuando puedas: Traag, Waltman y van Eck muestran que Louvain puede dar comunidades mal conectadas y hasta desconectadas.
21. Si hacés recomendación con clics, compras o reproducciones (no con puntajes), leé sobre retroalimentación implícita (Hu, Koren y Volinsky, 2008) y usá una librería pensada para eso, como `implicit`.
22. Cuando cites historia, citá bien: Apriori es de Agrawal y Srikant (1994), LDA de Blei, Ng y Jordan (2003), t-SNE de van der Maaten y Hinton (2008), UMAP de McInnes, Healy y Melville (2018), HITS de Kleinberg (1999) y la anécdota de los pañales y la cerveza viene de un estudio de 1992 que nunca cambió una góndola.

---

## Versión completa

### 1. Los datos del curso, verificados

Las docentes avisan varias veces que algunas cosas las cuentan de memoria. Las revisé y las ordené de la corrección que más cambia el práctico a la que menos. "Sí" quiere decir que la fuente lo confirma, "En parte" que es correcto con matices importantes, "No" que la fuente lo contradice, "Desactualizado" que fue cierto pero ya no lo es, y "No verificable" que no encontré una fuente primaria que lo confirme o lo niegue.

| Afirmación | Resultado | Matiz | Fuente |
|---|---|---|---|
| "El que tiene la inercia más chica me permite decidir que este K es mejor que otro K" C2P1 52:25 | No | La guía de scikit-learn dice que la inercia "is not a normalized metric: we just know that lower values are better and zero is optimal", y que supone grupos convexos e isotrópicos. Como cada K nuevo puede partir un grupo, la inercia baja siempre al subir K (con K igual a la cantidad de puntos vale 0). Sirve para comparar corridas con el mismo K; para elegir K hace falta el codo, la silueta, BIC o la estabilidad. | [scikit-learn, guía de clustering](https://scikit-learn.org/stable/modules/clustering.html) |
| "Las métricas van entre 0 y 1" C2P2 52:11 | No | El ARI "is bounded below by -0.5 for especially discordant clusterings"; 1 es acuerdo perfecto y el azar da cerca de 0. La silueta va de -1 a 1. La medida V sí va de 0 a 1. Lo comprobé en el box con un caso armado que da -0,5. | [scikit-learn, adjusted_rand_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.adjusted_rand_score.html) |
| `Normalizer` sirve para escalar las variables ("normalizar... vector con norma uno") C1P2 1:34:07 | No | La documentación: "Normalize samples individually to unit norm. Each sample (i.e. each row of the data matrix)... is rescaled independently of other samples". Normaliza jugadores, no columnas. Para variables usá `StandardScaler` o `MinMaxScaler`. | [scikit-learn, Normalizer](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.Normalizer.html) |
| "K-means está adaptado a muchísimas distancias" C1P2 2:02:09 | En parte (en teoría) / No (en scikit-learn) | Hay variantes con otras distancias (K-medoids, K-means esférico con coseno), pero `KMeans` de scikit-learn no tiene parámetro de métrica: lo comprobé en el box. La tabla de la guía lista su geometría como "Distances between points", y reserva "Any pairwise distance" y "non Euclidean distances" para el jerárquico aglomerativo. | [scikit-learn, guía de clustering](https://scikit-learn.org/stable/modules/clustering.html) |
| K-means "teóricamente con cualquier partición inicial encuentra la óptima" C1P2 1:59:16 | No | "Given enough time, K-means will always converge, however this may be to a local minimum. This is highly dependent on the initialization of the centroids." Por eso existen `n_init` y la inicialización k-means++. Ella misma agrega que "no ocurre en la vida", pero no es un problema práctico: tampoco ocurre en la teoría. | [scikit-learn, guía de clustering](https://scikit-learn.org/stable/modules/clustering.html) |
| `MiniBatchKMeans` es "para evitar mínimo local" C2P1 19:58 | No | Es para velocidad: "uses mini-batches to reduce the computation time, while still attempting to optimise the same objective function", y sus resultados son "generally only slightly worse than the standard algorithm". | [scikit-learn, guía de clustering](https://scikit-learn.org/stable/modules/clustering.html) |
| "El paper de t-SNE te dice no lo uses para clustering" C3P2 38:22 | En parte | Busqué "cluster" en todo el paper (JMLR 9, 2008, leído con `curl`): no hay una advertencia así. Sí lo presenta como técnica "for visualizing" y, en "Weaknesses", dice que no es obvio cómo funciona para reducción de dimensión general (a más de tres dimensiones). Además, su "early exaggeration" hace que "the natural clusters in the data tend to form tight widely separated clusters in the map": separa grupos a propósito. La advertencia explícita está en Distill (ver la sección 5). | [van der Maaten y Hinton, JMLR 2008](https://www.jmlr.org/papers/volume9/vandermaaten08a/vandermaaten08a.pdf); [Wattenberg, Viégas y Johnson, Distill 2016](https://distill.pub/2016/misread-tsne/) |
| UMAP "sí permite" K-means sobre la proyección C3P2 38:32 | En parte | La documentación de UMAP dedica una página a usarlo antes de agrupar, pero con cuidados: dice que UMAP, como t-SNE, "does not completely preserve density" y "can also create false tears in clusters", y recomienda `min_dist=0.0`, más vecinos y HDBSCAN en lugar de K-means. | [UMAP, Using UMAP for Clustering](https://umap-learn.readthedocs.io/en/latest/clustering.html) |
| "PCA si algo tiene es que eficiente no es, es muy costoso; UMAP y t-SNE mucho más rápidos" C3P1 1:12:11 | No | En el box, sobre los dígitos de scikit-learn (1.797 imágenes de 64 píxeles): PCA tardó 0,003 s, t-SNE 2,3 s y UMAP unos 13 s. En el benchmark de la sección 4, UMAP sobre 6.000 jugadores tardó entre 13 y 20 s. PCA es una descomposición en valores singulares; es lo más barato de los tres. | Medición propia (sección 4) |
| UMAP "es la que salió antes que" t-SNE C3P1 1:11:07 | No | t-SNE es de 2008 (JMLR) y UMAP de febrero de 2018 (arXiv 1802.03426, McInnes, Healy y Melville). | [arXiv 1802.03426](https://arxiv.org/abs/1802.03426); [JMLR 2008](https://www.jmlr.org/papers/volume9/vandermaaten08a/vandermaaten08a.pdf) |
| La segunda curva de `KElbowVisualizer` es un "estimador de fit" C2P2 41:01 | No | La documentación: "The KElbowVisualizer also displays the amount of time to train the clustering model per K as a dashed green line, but is can be hidden by setting timings=False". Es tiempo, no calidad. | [Yellowbrick, Elbow Method](https://www.scikit-yb.org/en/latest/api/cluster/elbow.html) |
| El enlace promedio es el "promedio de la distancia más baja" C2P2 23:17 | No | "Average linkage minimizes the average of the distances between all observations of pairs of clusters." Es el promedio de todas las distancias entre pares, no de las mínimas. | [scikit-learn, guía de clustering](https://scikit-learn.org/stable/modules/clustering.html) |
| "Cuando el valor medio [de la silueta] baja de 0,4 no es un buen cluster" C2P1 1:01:42 | No verificable como regla | No está en scikit-learn y no encontré una fuente primaria abierta que fije ese umbral. Mi benchmark muestra por qué es peligroso: el agrupamiento con mejor silueta en FIFA (0,56) es el trivial de arqueros contra el resto, con ARI 0,19. | Medición propia (sección 4) |
| Mean shift con bandwidth 6 da error "no encuentra ningún punto, pruebe otra estrategia"; "usualmente el bandwidth es 0,5 o 0,7" C2P1 1:28:51 | En parte | El mensaje existe en el código de scikit-learn 1.9.1: "No point was within bandwidth=%f of any seed. Try a different seeding strategy or increase the bandwidth" (lo vi en `_mean_shift.py`). Pero no hay un bandwidth usual: depende de la escala de los datos, y la guía dice que se puede estimar con `estimate_bandwidth`, que se llama sola si no lo fijás. | [scikit-learn, guía de clustering](https://scikit-learn.org/stable/modules/clustering.html) |
| "Miren en scikit-learn el uso de Dirichlet" para elegir K con un prior infinito C3P1 39:00 | Sí, con un matiz | Está en `BayesianGaussianMixture`, no en K-means: `weight_concentration_prior_type` vale `'dirichlet_process'` por defecto, y el modelo apaga componentes que no necesita. | [scikit-learn, BayesianGaussianMixture](https://scikit-learn.org/stable/modules/generated/sklearn.mixture.BayesianGaussianMixture.html) |
| LDA "es la tesis de Andrew Ng, el de Coursera, el del premio Turing" C3P1 37:50 | No | El paper es de David M. Blei, Andrew Y. Ng y Michael I. Jordan (JMLR 3, 993 a 1022, 2003); Blei firma primero. La lista oficial de ganadores del premio Turing por año no incluye a Andrew Ng (sí a Hinton, LeCun y Bengio, por ejemplo). | [Blei, Ng y Jordan, JMLR 2003](https://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf); [ACM, ganadores del Turing por año](https://amturing.acm.org/byyear.cfm) |
| "La matriz de covarianza a veces no es definida positiva y tengo que hacer un cálculo aproximado" C3P2 0:49 | En parte | Toda matriz de covarianza es semidefinida positiva; puede tener autovalores 0 (variables colineales), y PCA funciona igual: lo comprobé en el box con una columna que es suma de otras dos. Lo que sí puede pasar es que, con más variables que observaciones, la estimación sea singular. scikit-learn calcula PCA con SVD sobre los datos centrados, sin invertir nada. | Comprobación propia |
| Apriori fue "publicado en el 93" C4P2 5:54, C4P2 39:19 | En parte | Apriori es de Agrawal y Srikant, "Fast Algorithms for Mining Association Rules", VLDB 1994. En 1993 Agrawal, Imielinski y Swami habían planteado el problema de las reglas de asociación (SIGMOD 1993, citado como referencia 4 en el paper de 1994). | [Agrawal y Srikant, VLDB 1994](https://www.vldb.org/conf/1994/P487.PDF) (leído con `curl`) |
| El lift es "la probabilidad de que esa regla haya sido por casualidad", "básicamente la información mutua" C4P2 35:58 | No | Lift = confianza / soporte del consecuente = P(X,Y) / (P(X) P(Y)); vale 1 si hay independencia y puede ser mayor que 1. No es una probabilidad. Su logaritmo es la información mutua puntual. La documentación de mlxtend también define la convicción, que vale "inf" cuando la confianza es 1. Lo comprobé en el box. | [mlxtend, association_rules](https://rasbt.github.io/mlxtend/user_guide/frequent_patterns/association_rules/) |
| La poda por soporte "es la única optimización que se puede hacer" C4P2 40:22 | No | FP-Growth (Han, Pei, Yin y Mao) encuentra los mismos conjuntos frecuentes "without candidate generation" con un árbol de patrones frecuentes; mlxtend lo trae como `fpgrowth`. Comprobé en el box que da los mismos conjuntos que `apriori`. | [mlxtend, fpgrowth](https://rasbt.github.io/mlxtend/user_guide/frequent_patterns/fpgrowth/) |
| Hubs y authorities "es la base del algoritmo PageRank" C4P2 1:08:29 | No | Hubs y authorities es HITS, de Jon Kleinberg ("Authoritative Sources in a Hyperlinked Environment", 1999 en JACM). PageRank es de Brin y Page ("The Anatomy of a Large-Scale Hypertextual Web Search Engine", 1998). Son contemporáneos y distintos. networkx trae los dos (`hits` y `pagerank`). | [Kleinberg, PDF](https://www.cs.cornell.edu/home/kleinber/auth.pdf); [Brin y Page, Stanford](http://infolab.stanford.edu/~backrub/google.html) |
| Enron "era una petrolera" y los correos salieron porque "el juez pidió los correos" en un juicio de acreedores C1P1 42:26, C4P2 49:58, C4P2 51:05 | No | La página del dataset en CMU dice que los correos "originally made public, and posted to the web, by the Federal Energy Regulatory Commission during its investigation", y que después los compró Leslie Kaelbling (MIT). La FERC regula energía: Enron era una empresa de energía y comercialización de gas y electricidad. | [Enron Email Dataset, CMU](https://www.cs.cmu.edu/~enron/) |
| Arthur Andersen "desapareció"; "una de las Big Four es la estructura de Andersen" C4P2 49:58 | En parte | Fue condenada por obstrucción de la justicia el 15/06/2002 y entregó sus licencias de contador el 31/08/2002, lo que en la práctica la sacó del negocio. La Corte Suprema anuló la condena por unanimidad el 31/05/2005 (Arthur Andersen LLP v. United States), pero ya no tenía a quién volver: quedaban unos 200 empleados de 28.000. Ninguna Big Four "es" Andersen: sus oficinas y socios se repartieron entre KPMG, Ernst & Young, Deloitte & Touche y Grant Thornton. Accenture salió de Andersen Consulting, que se separó antes (2000 y 2001). | [Wikipedia, Arthur Andersen](https://en.wikipedia.org/wiki/Arthur_Andersen) (leído con `curl`, con sus citas a CNN, CBC, WSJ y The Guardian; la nota del New York Times de 2005 no cargó) |
| Premio Netflix "hace 20 años", un millón de dólares C4P2 1:20:47 | Sí | Arrancó en 2006 y se entregó el 21/09/2009 a BellKor's Pragmatic Chaos (AT&T Research, Big Chaos y Pragmatic Theory), que empató en el test privado con The Ensemble y ganó por entregar 10 minutos antes. Mejora de al menos 10% sobre Cinematch. Lo que suma a lo de Laura ("Netflix no es solo collaborative filtering"): el blog técnico de Netflix dice que la ganancia de precisión de la solución ganadora "did not seem to justify the engineering effort needed to bring them into a production environment". | [Wired, 21/09/2009](https://www.wired.com/2009/09/bellkors-pragmatic-chaos-wins-1-million-netflix-prize/); [Netflix TechBlog, 2012](https://netflixtechblog.com/netflix-recommendations-beyond-the-5-stars-part-1-55838468f429) (leído con `curl`) |
| Pañales y cerveza, "años 80, creo"; "esto es ciencia ficción, en la realidad no pasaba" C1P1 26:13, C1P1 40:10 | En parte | Forbes (06/04/1998, "Birth of a legend") cuenta que Thomas Blischok, de NCR, hizo en 1992 un estudio para Osco Drugs y encontró pañales y cerveza juntos entre las 5 y las 7 de la tarde, y que Osco nunca movió las góndolas ("Nope"). Un correo de 2000 publicado en KDnuggets (Tom Fawcett, citando a Lounette Dyer vía Ronny Kohavi) dice que el ejemplo se inventó para material de ventas de NCR y "never supported in any data". Es de 1992, no de los 80; el hallazgo existe en el relato de Blischok, pero la acción comercial nunca pasó. Laura tiene razón en lo importante. | [Forbes, 1998](https://www.forbes.com/forbes/1998/0406/6107128a.html); [KDnuggets 00:13](https://www.kdnuggets.com/news/2000/n13/23i.html) |
| XGBoost "es un método de ensamble que no está basado en boosting" C4P1 1:11:54 | No | El paper se llama "XGBoost: A Scalable Tree Boosting System" (Chen y Guestrin, 2016). Es gradient boosting de árboles. | [arXiv 1603.02754](https://arxiv.org/abs/1603.02754) |
| "Estos algoritmos de aprendizaje semisupervisado no están para nada [en scikit-learn], hay que programarlos" C4P1 1:20:14 | No | scikit-learn tiene `sklearn.semi_supervised` con `SelfTrainingClassifier` (basado en Yarowsky, el mismo autor que cita Laura), `LabelPropagation` y `LabelSpreading`; los no etiquetados se marcan con -1. Co-training y ladder networks sí hay que programarlos. | [scikit-learn, Semi-supervised learning](https://scikit-learn.org/stable/modules/semi_supervised.html) |
| Las ladder networks son "muy viejitas", del libro de 2006 de Bing Liu C4P1 1:42:02 | No | "Semi-Supervised Learning with Ladder Networks" es de Rasmus, Valpola, Honkala, Berglund y Raiko, julio de 2015, y se basa en la ladder network de Valpola (2015). | [arXiv 1507.02672](https://arxiv.org/abs/1507.02672) |
| "No se puede hacer aprendizaje automático sin ejemplos negativos, es un resultado teórico" C4P1 1:44:49 | En parte | Elkan y Noto (KDD 2008) muestran que con positivos y no etiquetados se puede aprender un clasificador bajo el supuesto "selected completely at random" (los positivos etiquetados son una muestra al azar de todos los positivos). Sin ese tipo de supuesto, sí hace falta información sobre los negativos. | [Elkan y Noto, PDF](https://cseweb.ucsd.edu/~elkan/posonly.pdf) (leído con `curl`; la página de ACM pidió verificación) |
| En co-training "la asunción es que los cercanos tienen la misma etiqueta" C4P1 1:14:04 | No | Blum y Mitchell (COLT 1998) parten de "two distinct views of each example": dos conjuntos de rasgos, cada uno suficiente para clasificar. La de cercanía es la asunción de suavidad o de clusters de otros métodos. | [Blum y Mitchell, PDF](https://www.cs.cmu.edu/~avrim/Papers/cotrain.pdf) |
| BERT fue "el primer modelo de lenguaje con todas las letras: le escribías y seguía escribiendo" C4P1 14:37 | No | BERT (Devlin y otros, octubre de 2018) es un codificador bidireccional "designed to pre-train deep bidirectional representations" con palabras enmascaradas; no genera texto de corrido. El que sigue escribiendo es GPT (OpenAI, también de 2018). | [arXiv 1810.04805](https://arxiv.org/abs/1810.04805) |
| "A los 15 días de salir ChatGPT, Bloomberg comentó que tenía su propio modelo" C4P1 10:07 | No | El paper de BloombergGPT (50.000 millones de parámetros, 363.000 millones de tokens de datos financieros) se subió a arXiv el 30/03/2023, cuatro meses después de ChatGPT (30/11/2022). No encontré un anuncio anterior. | [arXiv 2303.17564](https://arxiv.org/abs/2303.17564) |
| "La valoración de Nvidia bajó 20%, la mayor caída de la bolsa de la historia en términos absolutos" C4P1 32:36 | En parte | CNBC (27/01/2025): la acción cayó 17% y la empresa perdió cerca de 600.000 millones de dólares de capitalización, "the biggest drop ever for a U.S. company" en un día. La cifra es 17%, no 20%. | [CNBC, 27/01/2025](https://www.cnbc.com/2025/01/27/nvidia-sheds-almost-600-billion-in-market-cap-biggest-drop-ever.html) (leído con `curl`) |
| Tras la filtración de Llama, "la comunidad de software libre en una semana desarrolló la cuantización" C4P1 34:18 | En parte | La cuantización de modelos grandes es anterior: LLM.int8() se subió a arXiv el 15/08/2022 y GPTQ el 31/10/2022. Lo que la comunidad hizo rápido fue llevarla a modelos abiertos en máquinas comunes; llama.cpp hoy documenta cuantización entera de 1,5 a 8 bits. El "en una semana" no lo verifiqué. | [arXiv 2208.07339](https://arxiv.org/abs/2208.07339); [arXiv 2210.17323](https://arxiv.org/abs/2210.17323); [llama.cpp](https://github.com/ggml-org/llama.cpp) |
| "Desde los años 50 sabíamos que una red podía modelar prácticamente todos los problemas, el problema era entrenarla" C3P2 1:00:07 | No | El perceptrón de los 50 tenía una sola capa y no podía, por ejemplo, con XOR. Los resultados de aproximación universal para redes de una capa oculta son de Cybenko (1989) y Hornik (1991). No pude abrir las páginas de las revistas (Springer pidió verificación y ScienceDirect devolvió una página vacía), así que los dejo como referencia sin link. | Sin página abierta |
| Cloudflare se cayó por un archivo de features para identificar robots que generó un módulo de ML y salió "del doble de tamaño"; "menos de 12 horas" C3P1 18:25 | Sí, con matices | El post de Matthew Prince: el 18/11/2025 a las 11:20 UTC (08:20 ART), un cambio de permisos en una base de datos hizo que se escribieran entradas repetidas en el "feature file" del sistema Bot Management, que "doubled in size". Bot Management incluye "a machine learning model" que puntúa cada pedido. El tráfico se normalizó a las 14:30 UTC (11:30 ART) y todo a las 17:06 UTC (14:06 ART): menos de seis horas. El archivo no lo generó el modelo: lo arma un proceso que consulta esa base de datos. Conflicto de interés: es el informe de la propia empresa. | [Cloudflare Blog, 18/11/2025](https://blog.cloudflare.com/18-november-2025-outage/) |
| Cloudflare "es una empresa alemana, si no recuerdo mal" C3P1 21:43 | No | Su página institucional lista la sede central en San Francisco (101 Townsend St.). | [Cloudflare, About](https://www.cloudflare.com/about-overview/) |
| Los datos personales "no deberían salir de jurisdicción argentina" según la ley de protección de datos C3P1 12:25 | En parte | El artículo 12 de la Ley 25.326 prohíbe transferir datos personales "con países u organismos internacionales o supranacionales, que no propocionen niveles de protección adecuados", con excepciones (colaboración judicial, datos médicos, transferencias bancarias, tratados y otras). No es una prohibición general de usar servidores afuera. | [Ley 25.326, InfoLEG](https://servicios.infoleg.gob.ar/infolegInternet/anexos/60000-64999/64790/norma.htm) |
| "Meta tiene los mensajes de Instagram y Facebook, que nunca tuvo encriptación punto a punto" C3P2 1:03:41 | En parte y desactualizado | Messenger y Facebook tienen cifrado de extremo a extremo por defecto desde el 06/12/2023 (anuncio de Meta). Instagram lo tuvo como opción por chat y lo quitó el 08/05/2026: la BBC informa que Meta lo anunció cambiando sus términos en marzo y que ahora Instagram puede acceder al contenido de los mensajes directos. Para Instagram la frase de Laura hoy es casi cierta; para Messenger, no. Conflicto de interés: el anuncio de 2023 es de Meta. | [Meta, 06/12/2023](https://about.fb.com/news/2023/12/default-end-to-end-encryption-on-messenger/); [BBC, 08/05/2026](https://www.bbc.com/news/articles/clypzxl3lvqo) |
| ICLR 2026 se hizo en Río C3P2 46:05 | Sí | Del 23 al 27 de abril de 2026, en Riocentro, Río de Janeiro. | [ICLR 2026](https://iclr.cc/Conferences/2026) |

**Lo más importante para corregir en el apunte.** Las correcciones que cambian lo que harías en el trabajo especial son cinco: la inercia no elige K, el ARI puede ser negativo, `Normalizer` no escala columnas, `KMeans` solo usa distancia euclídea y la silueta alta no garantiza grupos útiles (en FIFA premia separar arqueros). Las de historia (Apriori, LDA, HITS, BERT, ladder networks) no cambian el código pero sí lo que escribís en un informe.

### 2. Nombres y dudas de la transcripción, resueltos

| En la transcripción o el apunte | Resultado | Cómo lo resolví |
|---|---|---|
| Docentes: Laura y Georgina (solo nombres de pila) | Confirmado: Laura Alonso Alemany y Georgina Flesia | La página del equipo docente de la diplomatura lista a Laura Alonso Alemany (doctora en Ciencia Cognitiva y del Lenguaje) y a Georgina Flesia (doctora en Matemática, FAMAF UNC), junto con Carolina Chavero (doctora en Astronomía, coordinadora), Ariel Mauricio Wolfmann, Diego González Dondo, Karim Alejandra Nemer Pelliza, Vanesa Meinardi y José Ignacio Robledo, y en mentorías a Luis Biedma y Yanina Iberra. [Diplodatos, equipo docente](https://diplodatos.famaf.unc.edu.ar/equipo-docente/) |
| "Valeria Rulloni" como docente de la materia | De una edición anterior (2022), no de 2026 | La página propia de la materia todavía dice "Equipo Docente: Valeria Rulloni, Laura Alonso Alemany", pero su consigna pide `players_22.csv` de Kaggle, o sea que es la de 2022. El README del GitHub de la materia dice lo mismo. Rulloni no figura en la página actual del equipo docente, y en las grabaciones de 2026 no aparece. [Página de la materia](https://diplodatos.famaf.unc.edu.ar/metodologia-y-modalidad-de-cursado/materias-obligatorias/materia-aprendizaje-no-supervisado/); [GitHub DiploDatos/AprendizajeNOSupervisado](https://github.com/DiploDatos/AprendizajeNOSupervisado) |
| Carolina, la coordinadora, astrónoma C1P1 2:55; "Vietma", coordinador de mentorías C1P1 1:08:15 | Confirmado: Carolina Chavero y Luis Biedma | Página del equipo docente (ver la primera fila). |
| Damián, que da la optativa de cálculo distribuido (sin apellido) C3P1 6:52 | Muy probable: Damián Barsotti | El GitLab de FAMAF tiene el repositorio "Damián Barsotti / diplodatos_bigdata", de la materia "Programación Distribuida sobre Grandes Volúmenes de Datos" de la diplomatura, que coincide con "cálculo distribuido". Un sitio de optativas de 2020 lo lista como docente (solo lo vi en un resultado de búsqueda). No confirmé que la dé en 2026: la página de optativas de la diplomatura cargó sin la lista. [GitLab FAMAF, diplodatos_bigdata](https://git.cs.famaf.unc.edu.ar/dbarsotti/diplodatos_bigdata) |
| "SECAT", el centro de cómputo de la UNC, "gratis para investigadores, contratable" C3P1 6:52 | En parte | Es el CCAD (Centro de Computación de Alto Desempeño). Su página de servicios ofrece horas de cómputo a investigadores de instituciones del Sistema Científico Nacional, por pedido por correo al director con descripción del proyecto, y un Comité Científico evalúa la pertinencia y la disponibilidad. O sea: sin costo para investigadores, pero no automático. Solo en resultados de búsqueda vi el convenio con CONICET de abril de 2023 ("acceso abierto y gratuito"), el tarifario para terceros y que el CCAD ofrece JupyterHub y un chat con modelos locales. Para un estudiante de la diplomatura sin cargo de investigación, no hay un acceso documentado. [CCAD, servicios](https://supercomputo.unc.edu.ar/servicios/) |
| "La UNC tiene un convenio con Amazon Web Services para docencia, 100 dólares de crédito por alumno" C3P1 11:16 | Desactualizado o no verificable | Los 100 dólares coinciden con el viejo AWS Educate: el blog de AWS de 2015 anunciaba 100 dólares en créditos para estudiantes de instituciones miembro (35 si no). Una actualización del 21/02/2023 en ese mismo post dice que AWS Educate "no longer offers grants to institutions or to educators" y que las herramientas para docentes pasaron a AWS Academy. Solo en búsqueda vi que el Campus Norte de la UNC se sumó a AWS Academy (cursos y laboratorios en la nube), pero nada sobre 100 dólares por alumno hoy. Preguntá en el aula virtual antes de contar con esos créditos. [AWS News Blog, AWS Educate](https://aws.amazon.com/blogs/aws/aws-educate-credits-training-content-and-collaboration-for-students-educators/) |
| Banco Galicia trabaja con IBM, con detección por grafos de accesos raros a cuentas C3P1 14:01 | En parte | La relación con IBM está confirmada: ITSitio (07/08/2023) cuenta décadas de alianza, el primer homebanking argentino hecho con IBM y el asistente Gala sobre IBM Watson Assistant. La detección por grafos de accesos raros no la encontré en ninguna fuente pública. Conflicto de interés: la nota tiene tono de comunicado de IBM. [ITSitio, 07/08/2023](https://www.itsitio.com/ar/banco-galicia-e-ibm-una-alianza-estrategica/) |
| pysentimiento, "de un estudiante suyo" C4P2 57:18 | En parte, y con conflicto de interés | El paper (arXiv 2106.09462) lo firman Juan Manuel Pérez (ICC, CONICET y UBA), Mariela Rajngewerc (FAMAF UNC y CONICET), Juan Carlos Giudici, Damián A. Furman (UBA), Franco Luque (FAMAF UNC), **Laura Alonso Alemany** (FAMAF UNC) y María Vanina Martínez (IIIA CSIC). La primera versión la firmaban Pérez, Giudici y Luque. O sea: Laura es coautora; que Pérez haya sido su estudiante no lo verifiqué. Recomendar una herramienta propia no está mal, pero conviene saberlo. [arXiv 2106.09462](https://arxiv.org/abs/2106.09462) |
| "El FIFA 24 de Kaggle trae archivos 24, 23, 22, 21" C1P2 1:10:05, C2P2 38:16; "datos del link de Kaggle con 2015 a 2023" C3P2 4:00 | Identificado | El candidato que encaja con todo es "EA Sports FC 24 complete player dataset" de Stefano Leone: datos del modo carrera de FIFA 15 a FC 24, actualizaciones del 10/09/2015 al 22/09/2023, 109 atributos por jugador, extraídos de sofifa.com, licencia CC0. El mismo autor publicó el de FIFA 22 que pedía la consigna de 2022. [Kaggle, EA Sports FC 24](https://www.kaggle.com/datasets/stefanoleone992/ea-sports-fc-24-complete-player-dataset) |
| "Fable", modelos de Anthropic "que se ponen y se sacan" por riesgo de ciberataques C4P1 24:42 | Confirmado el nombre; el resto en parte | La página de Anthropic lista "Claude Fable 5" (anunciado el 09/06/2026), "Claude Fable 5 access unavailable" (12/06/2026), "Claude Fable 5 is rolling out" (01/07/2026, "Access to Claude Fable 5 has been restored") y "Claude Fable 5.1" (01/09/2026). La página no dice por qué se cortó el acceso en junio. Lo que sí dicen la página y el centro de ayuda: Fable trae salvaguardas que desvían consultas de ciberseguridad ofensiva y de biología a modelos Opus, y los modelos "Mythos-class (like Mythos Preview)" solo se dieron a socios elegidos. Conflicto de interés: todo es de Anthropic. [Anthropic, Claude Fable](https://www.anthropic.com/claude/fable); [Centro de ayuda de Claude](https://support.claude.com/en/articles/15363606-why-claude-switched-models-in-your-conversation-with-fable-5-or-fable-5-1) |
| Kimi "1,2 teras", "tres veces más grande que Kimi K3" C4P1 11:47 | En parte | Kimi K2 (Moonshot AI) es una mezcla de expertos de 1 billón (1T) de parámetros totales y 32.000 millones activos por token, según su ficha en Hugging Face. Kimi K3 existe: su README en GitHub lista 2,8T totales y 104.000 millones activos. La relación es al revés de lo transcripto: K3 es unas 2,8 veces K2. [Hugging Face, Kimi-K2-Base](https://huggingface.co/moonshotai/Kimi-K2-Base); [GitHub, Kimi-K3 README](https://raw.githubusercontent.com/MoonshotAI/Kimi-K3/main/README.md) (leído con `curl`) |
| Georgina: con distribuciones esféricas "hay cuatro parámetros para la matriz de covarianza" C4P1 1:17:28 | Hipótesis | Una covarianza esférica tiene un solo parámetro por componente. Lo más probable es que hablara de los cuatro tipos de covarianza de `GaussianMixture` (`full`, `tied`, `diag`, `spherical`). No lo puedo confirmar sin la imagen de la clase. |
| "Lisa", "Elena Nova" | Sin resolver | No encontré nada que los aclare; los dejo como dudosos en el apunte. |

### 3. El dataset del trabajo especial: qué bajar y cómo leerlo

**Qué dice la fuente.** El trabajo especial es clustering sobre FIFA 24 de Kaggle C1P2 1:10:05, con un exploratorio que revise nombres de variables, cantidad y etiquetas de testigos C2P2 38:16. Georgina aclara que el archivo trae varias ediciones y que el FIFA 2018 reducido de clase está en el GitHub de la diplomatura "para no perderlo" C3P2 4:00.

**Qué suma el material externo.**
- El dataset de Kaggle más probable es el de Stefano Leone (ver la tabla anterior). Bajarlo pide una cuenta de Kaggle.
- El GitHub de la materia es público y no pide cuenta. Tiene `2024/Fifa2019/data2019.csv` (18.207 jugadores, 89 columnas), varios archivos de FIFA 2018 y una carpeta `2024/2025` con `male_players.csv` y un archivo de jugadores de junio de 2025. El archivo de 2025 está guardado con Git LFS y no lo pude bajar entero desde el box; el de 2019 sí.
- La consigna de 2022 (que sigue en la página de la materia) pide seis puntos que se parecen mucho a los de 2026: exploratorio, pares de variables, dos técnicas de clustering con hiperparámetros justificados, evaluación, la pregunta de si escalaste y por qué, y una proyección para visualizar o preprocesar. Sirve como guía de lo que se espera.

**Cómo implementarlo.** Este código lee el FIFA 2019 del GitHub, arma los testigos de posición en cuatro grupos y deja las 34 habilidades listas para agrupar. Es el que usé en el benchmark de la sección 4:

```python
import pandas as pd
from sklearn.preprocessing import StandardScaler

URL = ("https://raw.githubusercontent.com/DiploDatos/AprendizajeNOSupervisado/"
       "master/2024/Fifa2019/data2019.csv")
d = pd.read_csv(URL)
habilidades = list(d.loc[:, "Crossing":"GKReflexes"].columns)   # 34 columnas
d = d.dropna(subset=habilidades + ["Position"])

grupo = {"GK": "GK"}
grupo |= {p: "DEF" for p in ["CB", "LCB", "RCB", "LB", "RB", "LWB", "RWB"]}
grupo |= {p: "MID" for p in ["CM", "LCM", "RCM", "CDM", "LDM", "RDM",
                             "CAM", "LAM", "RAM", "LM", "RM"]}
grupo |= {p: "FWD" for p in ["ST", "LS", "RS", "CF", "LF", "RF", "LW", "RW"]}
d["testigo"] = d["Position"].map(grupo)

X = StandardScaler().fit_transform(d[habilidades])   # por columna, no Normalizer
print(d.shape, d["testigo"].value_counts().to_dict())
```

En FC 24 los nombres de las columnas cambian: llevan un prefijo por tipo de habilidad (en clase se vio el prefijo "attacking" C1P2 1:10:05) y las posiciones pueden venir como lista. Mirá `df.columns` y la columna de posiciones, y adaptá el mapeo antes de copiar este código.

**Sugerencia.** Antes de agrupar, decidí y escribí qué querés que salga: "tipos de jugador de campo" no es lo mismo que "arqueros contra el resto". La mayoría de los métodos, si dejás a los arqueros, gastan un grupo en separarlos (la sección 4 lo muestra con números).

### 4. Benchmark: los cinco métodos de la materia, con y sin UMAP, contra testigos reales

**Qué dice la fuente.** La materia compara K-means, mezclas de gaussianas, mean shift, DBSCAN y jerárquicos con métricas internas y externas contra testigos C2P2 49:58, y Georgina comenta que K-means sobre PCA sin escalar llega a una métrica de cerca de 0,41 contra los testigos C2P2 52:11. Laura propone agrupar sobre la proyección C3P2 38:32 y Georgina aclara que ella no lo hace: de 40 dimensiones a 2 "es demasiado" C3P2 38:32.

**Qué suma el material externo.** La documentación de UMAP muestra en MNIST que UMAP más HDBSCAN recupera casi perfecto los dígitos donde K-means falla, y que HDBSCAN solo sobre PCA da un ARI de 0,05 porque manda muchos puntos a ruido. Pero MNIST es justamente el tipo de dato (una variedad de baja dimensión en un espacio de 784 píxeles) donde UMAP brilla. La página de comparación de scikit-learn avisa que su intuición con datos de juguete "might not apply to very high dimensional data". Hacía falta medir en FIFA.

**Cómo lo medí.** Tomé 6.000 jugadores al azar del FIFA 2019 (tres semillas: 0, 1 y 2), escalé las 34 habilidades con `StandardScaler` y corrí cinco métodos en dos espacios: los datos escalados y una proyección UMAP de 10 componentes con `n_neighbors=30` y `min_dist=0.0` (la receta de la documentación de UMAP). K-means, mezcla de gaussianas (covarianza completa) y Ward recibieron el K verdadero. DBSCAN usó `min_samples` igual al doble de la dimensión y `eps` en el percentil 90 de la distancia al vecino número `min_samples`. HDBSCAN usó `min_cluster_size=50`. El ARI y la medida V se calculan contra los testigos de posición, contando el ruido como un grupo más; la silueta se calcula siempre en el espacio escalado original (sin el ruido), para que sea comparable entre espacios. El tiempo incluye UMAP cuando corresponde. Repetí todo en dos versiones del problema, y en los dígitos de scikit-learn como control:

- **FIFA, todos (4 testigos):** arqueros, defensores, mediocampistas y delanteros.
- **FIFA, de campo (3 testigos):** sin arqueros y sin las 5 habilidades de arquero.
- **Dígitos (10 testigos):** 2.000 imágenes de 8x8 de `load_digits`.

Promedios de tres semillas:

| Datos | Espacio | Método | ARI | Medida V | Silueta | Grupos | Ruido | Segundos |
|---|---|---|---|---|---|---|---|---|
| FIFA todos | Escalado | K-means | 0,355 | 0,494 | 0,254 | 4 | 0% | 1,0 |
| FIFA todos | Escalado | Mezcla de gaussianas | **0,410** | **0,569** | 0,195 | 4 | 0% | 2,0 |
| FIFA todos | Escalado | Ward | 0,368 | 0,510 | 0,226 | 4 | 0% | 1,3 |
| FIFA todos | Escalado | DBSCAN | 0,190 | 0,421 | **0,556** | 2 | 0,5% | 0,1 |
| FIFA todos | Escalado | HDBSCAN | 0,190 | 0,430 | 0,555 | 2 | 0% | 1,4 |
| FIFA todos | UMAP 10 | K-means | 0,388 | 0,547 | 0,235 | 4 | 0% | 20,0 |
| FIFA todos | UMAP 10 | Mezcla de gaussianas | 0,373 | 0,557 | 0,226 | 4 | 0% | 20,0 |
| FIFA todos | UMAP 10 | Ward | 0,379 | 0,542 | 0,226 | 4 | 0% | 20,7 |
| FIFA todos | UMAP 10 | DBSCAN | 0,329 | 0,517 | 0,349 | 2,7 | 1,1% | 20,0 |
| FIFA todos | UMAP 10 | HDBSCAN | 0,190 | 0,430 | 0,555 | 2 | 0% | 20,2 |
| FIFA campo | Escalado | K-means | 0,261 | 0,298 | 0,207 | 3 | 0% | 0,04 |
| FIFA campo | Escalado | Mezcla de gaussianas | **0,352** | **0,424** | 0,132 | 3 | 0% | 1,0 |
| FIFA campo | Escalado | Ward | 0,255 | 0,277 | 0,160 | 3 | 0% | 1,2 |
| FIFA campo | Escalado | DBSCAN | 0,001 | 0,002 | (1 grupo) | 1 | 0,7% | 0,1 |
| FIFA campo | Escalado | HDBSCAN | 0,000 | 0,000 | (todo ruido) | 0 | 100% | 1,4 |
| FIFA campo | UMAP 10 | K-means | 0,318 | 0,387 | 0,182 | 3 | 0% | 13,7 |
| FIFA campo | UMAP 10 | Mezcla de gaussianas | 0,300 | 0,388 | 0,179 | 3 | 0% | 13,8 |
| FIFA campo | UMAP 10 | Ward | 0,300 | 0,370 | 0,181 | 3 | 0% | 14,7 |
| FIFA campo | UMAP 10 | DBSCAN | 0,104 | 0,133 | 0,183 | 1,3 | 0,9% | 13,7 |
| FIFA campo | UMAP 10 | HDBSCAN | 0,256 | 0,333 | 0,150 | 3,7 | 18,4% | 14,0 |
| Dígitos | Escalado | K-means | 0,531 | 0,672 | 0,148 | 10 | 0% | 0,06 |
| Dígitos | Escalado | Mezcla de gaussianas | 0,501 | 0,652 | 0,129 | 10 | 0% | 5,0 |
| Dígitos | Escalado | Ward | 0,664 | 0,796 | 0,125 | 10 | 0% | 0,08 |
| Dígitos | Escalado | DBSCAN | 0,000 | 0,009 | (1 grupo) | 1 | 2,5% | 0,1 |
| Dígitos | Escalado | HDBSCAN | 0,028 | 0,218 | 0,398 | 3 | 86,2% | 0,2 |
| Dígitos | UMAP 10 | K-means | 0,802 | 0,865 | 0,116 | 10 | 0% | 7,1 |
| Dígitos | UMAP 10 | Mezcla de gaussianas | 0,780 | 0,856 | 0,116 | 10 | 0% | 7,1 |
| Dígitos | UMAP 10 | Ward | 0,816 | **0,873** | 0,111 | 10 | 0% | 7,0 |
| Dígitos | UMAP 10 | DBSCAN | **0,840** | 0,871 | 0,130 | 12,3 | 4,0% | 7,0 |
| Dígitos | UMAP 10 | HDBSCAN | 0,805 | 0,862 | 0,121 | 10 | 2,3% | 7,0 |

La variación entre semillas es chica (desvío del ARI de 0,03 o menos) salvo en DBSCAN sobre UMAP (0,12 en FIFA todos y 0,18 en FIFA campo), que es inestable con estos parámetros.

**Lo que muestran los números.**
1. **En FIFA, el mejor método es el más clásico.** La mezcla de gaussianas sobre los datos escalados gana en las dos versiones (ARI 0,41 y 0,35). UMAP mejora a K-means y a Ward, pero empeora a la mezcla de gaussianas, y agrega entre 13 y 20 segundos por corrida, cuando agrupar los datos escalados tarda de 0,04 a 2 segundos.
2. **La silueta premia lo trivial.** En FIFA con todos, DBSCAN y HDBSCAN encuentran dos grupos (arqueros contra el resto) con silueta 0,56, el doble que cualquier método con cuatro grupos, y ARI 0,19. Si elegís por silueta, elegís lo que ya sabías. Es el mismo efecto que se vio en clase C2P2 42:40.
3. **HDBSCAN no es mágico en datos tabulares.** Sobre los datos escalados de campo, con `min_cluster_size=50`, manda todo a ruido. Sobre UMAP, en FIFA todos separa arqueros contra el resto con cualquier configuración que probé (`min_cluster_size` de 25, 100 y 300, con `min_samples` 5 o por defecto). En FIFA campo, con `min_cluster_size=100`, deja 7% de ruido y llega a un ARI de 0,31 (0,35 sin contar el ruido): cerca de K-means sobre UMAP, no mejor.
4. **En los dígitos, UMAP cambia todo.** Todos los métodos pasan de un ARI de 0,5 a 0,66 a uno de 0,78 a 0,84, y DBSCAN y HDBSCAN pasan de inservibles a los mejores. Es el caso que muestra la documentación de UMAP, y se reproduce.
5. **Las posiciones no son grupos naturales de las habilidades.** Ningún método pasa de 0,41 en FIFA. Un lateral que ataca se parece más a un extremo que a un central, y el testigo dice "defensor". Esto no es un defecto del clustering: es que la pregunta "¿salen las posiciones?" no es la misma que "¿qué tipos de jugador hay?".

**La línea de base supervisada.** Como hay testigos, medí también qué pasa si etiquetás unos pocos jugadores al azar y entrenás un clasificador (mismos 6.000 jugadores, tres semillas; el ARI se mide sobre los no etiquetados):

| Datos | Etiquetas | Regresión logística (ARI / V) | `LabelSpreading` (ARI / V) |
|---|---|---|---|
| FIFA todos | 20 | 0,340 / 0,441 | 0,267 / 0,381 |
| FIFA todos | 50 | **0,479** / 0,569 | 0,416 / 0,513 |
| FIFA todos | 200 | **0,605** / 0,641 | 0,475 / 0,558 |
| FIFA campo | 20 | 0,358 / 0,361 | 0,254 / 0,297 |
| FIFA campo | 50 | **0,477** / 0,456 | 0,344 / 0,346 |
| FIFA campo | 200 | **0,540** / 0,502 | 0,394 / 0,386 |

Con 50 etiquetas (menos del 1% de los datos), la regresión logística supera al mejor clustering en las dos versiones; con 20 ya empata en FIFA campo. Esto alimenta el análisis adversario.

**Cómo implementarlo.** El núcleo del benchmark (el script completo, con las tres semillas y los tres conjuntos de datos, sigue el mismo esquema):

```python
import numpy as np, umap
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN, HDBSCAN
from sklearn.mixture import GaussianMixture
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import adjusted_rand_score, v_measure_score, silhouette_score

def comparar(Xs, y, k, semilla=0):
    U = umap.UMAP(n_components=10, n_neighbors=30, min_dist=0.0,
                  random_state=semilla).fit_transform(Xs)
    for espacio, Z in [("escalado", Xs), ("UMAP10", U)]:
        ms = 2 * Z.shape[1]
        kd = np.sort(NearestNeighbors(n_neighbors=ms).fit(Z).kneighbors(Z)[0][:, -1])
        metodos = {
            "KMeans": KMeans(k, n_init=10, random_state=semilla),
            "GMM": GaussianMixture(k, covariance_type="full", random_state=semilla),
            "Ward": AgglomerativeClustering(k, linkage="ward"),
            "DBSCAN": DBSCAN(eps=float(np.percentile(kd, 90)), min_samples=ms),
            "HDBSCAN": HDBSCAN(min_cluster_size=50),
        }
        for nombre, m in metodos.items():
            lab = m.fit_predict(Z)
            ok = lab != -1                       # sin ruido para la silueta
            n = len(set(lab[ok]))
            sil = silhouette_score(Xs[ok], lab[ok]) if n > 1 else float("nan")
            print(f"{espacio:9} {nombre:8} ARI={adjusted_rand_score(y, lab):.3f} "
                  f"V={v_measure_score(y, lab):.3f} sil={sil:.3f} grupos={n} "
                  f"ruido={1 - ok.mean():.1%}")

# con X e y de la sección 3, sobre una muestra de 6.000 jugadores
rng = np.random.default_rng(0)
idx = rng.choice(len(X), 6000, replace=False)
comparar(X[idx], d["testigo"].values[idx], k=4)
```

Ward sobre 18.000 jugadores necesita mucha memoria (guarda distancias entre todos los pares); por eso trabajé con 6.000.

**Sugerencia.** Para el informe del trabajo especial, reportá siempre tres cosas por método: una métrica externa contra testigos (ARI o V), una interna (silueta) y la cantidad de grupos y de ruido. Si la interna y la externa no coinciden, eso es un hallazgo, no un error: decí qué grupos premia cada una.

### 5. t-SNE y UMAP: para mirar, y con cuidado para agrupar

**Qué dice la fuente.** Laura dice que el paper de t-SNE desaconseja usarlo para agrupar y que UMAP sí permite K-means sobre la proyección C3P2 38:22, C3P2 38:32. Georgina prefiere no agrupar sobre proyecciones: "las proyecciones cambian los datos" C3P1 1:35:07.

**Qué suma el material externo.**
- **El paper de t-SNE** (van der Maaten y Hinton, JMLR 2008) lo presenta como técnica para visualizar, y reconoce como debilidad que no es obvio cómo funciona fuera de 2 o 3 dimensiones. No trae una advertencia explícita contra agrupar, pero explica que la "early exaggeration" hace que los grupos naturales formen "tight widely separated clusters in the map". O sea: el gráfico exagera la separación a propósito.
- **"How to Use t-SNE Effectively"** (Wattenberg, Viégas y Johnson, Distill, 2016) es la advertencia que Laura recuerda. Sus títulos son el resumen: "Those hyperparameters really matter", "Cluster sizes in a t-SNE plot mean nothing", "Distances between clusters might not mean anything" y "Random noise doesn't always look random" (500 puntos gaussianos en 100 dimensiones con perplejidad 2 "seems to show dramatic clusters"). Recomienda mirar varias perplejidades e iterar hasta que el gráfico se estabilice. Conflicto de interés menor: los autores eran de Google Brain y Google Cloud, sin producto en juego.
- **La documentación de UMAP** tiene una página entera, "Using UMAP for Clustering". Reconoce los mismos riesgos ("UMAP, like t-SNE, does not completely preserve density" y "can also create false tears in clusters, resulting in a finer clustering than is necessarily present in the data") y aun así da razones para usarlo antes de agrupar, con una receta: `min_dist=0.0`, `n_neighbors` más alto (30 en su ejemplo) y HDBSCAN. Conflicto de interés: la escribe Leland McInnes, autor de UMAP y coautor de la librería hdbscan.

**Cómo implementarlo.** Si vas a agrupar sobre UMAP, hacelo así, y compará siempre contra el mismo método sobre los datos escalados (mi benchmark muestra que en FIFA no siempre gana):

```python
import umap
from sklearn.cluster import HDBSCAN

Z = umap.UMAP(n_neighbors=30, min_dist=0.0, n_components=10,
              random_state=0).fit_transform(X)        # para agrupar
Z2 = umap.UMAP(random_state=0).fit_transform(X)        # aparte, solo para el gráfico
lab = HDBSCAN(min_cluster_size=100).fit_predict(Z)
```

**Sugerencia.** Usá la proyección de 2 dimensiones solo para pintar los grupos que encontraste en otro espacio. Si un grupo solo aparece en el gráfico de t-SNE, sospechá de él hasta que lo veas en los datos originales (por ejemplo, con las medias de las habilidades por grupo).

### 6. Elegir K por estabilidad

**Qué dice la fuente.** La materia elige K con el codo de la inercia, la silueta y, en mezclas de gaussianas, con BIC y AIC C3P1 39:00, y discute por qué 3 y no 2 C2P2 42:40.

**Qué suma el material externo.** Ben-Hur, Elisseeff y Guyon (Pacific Symposium on Biocomputing, 2002) proponen medir "the stability of clustering solutions obtained by perturbing the data": si un K refleja estructura real, agrupar submuestras distintas debería dar particiones parecidas. Von Luxburg ("Clustering Stability: An Overview", 2010) resume la teoría: es un método popular para elegir K ("one chooses the number of clusters such that the corresponding clustering results are 'most stable'") y sus garantías son técnicas y limitadas; por ejemplo, un K puede ser estable porque el algoritmo siempre cae en la misma solución mala.

**Cómo implementarlo.** Agrupo dos submuestras distintas de 3.000 jugadores de campo, cada una con su K-means, les pido que etiqueten a todos los jugadores y comparo las dos etiquetas con el ARI (10 repeticiones por K):

```python
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score

rng = np.random.default_rng(0)
for k in range(2, 9):
    aris = []
    for b in range(10):
        i = rng.choice(len(X), 3000, replace=False)
        j = rng.choice(len(X), 3000, replace=False)
        a = KMeans(k, n_init=5, random_state=b).fit(X[i])
        c = KMeans(k, n_init=5, random_state=b + 100).fit(X[j])
        aris.append(adjusted_rand_score(a.predict(X), c.predict(X)))
    print(k, round(np.mean(aris), 3), round(np.std(aris), 3))
```

En FIFA de campo (sin arqueros) dio:

| K | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|
| ARI medio entre submuestras | 0,929 | 0,929 | 0,813 | 0,797 | 0,705 | 0,699 | 0,657 |
| Desvío | 0,040 | 0,029 | 0,096 | 0,125 | 0,127 | 0,157 | 0,123 |

K = 2 y K = 3 son igual de estables, y K = 3 lo es con menos desvío; de 4 en adelante la partición cambia según la muestra. Coincide con los tres testigos (defensores, mediocampistas y delanteros), aunque el ARI contra ellos sea solo 0,26.

**Sugerencia.** En el informe, mostrá la curva de estabilidad junto al codo y la silueta. Si las tres apuntan al mismo K, tenés un argumento fuerte; si no, decí cuál elegiste y por qué.

### 7. HDBSCAN y el ruido como respuesta válida

**Qué dice la fuente.** La materia ve DBSCAN, con sus puntos núcleo, borde y ruido, y menciona OPTICS y DENCLUE como variantes por densidad.

**Qué suma el material externo.** HDBSCAN (Campello, Moulavi y Sander, PAKDD 2013) está en scikit-learn desde la versión 1.3 como `sklearn.cluster.HDBSCAN`. La documentación lo describe como DBSCAN "over varying epsilon values" que integra el resultado para encontrar el agrupamiento más estable, lo que le permite "find clusters of varying densities (unlike DBSCAN), and be more robust to parameter selection". El parámetro principal es `min_cluster_size` (por defecto 5). Ojo: la documentación avisa que su `min_samples` vale uno más que el de la librería hdbscan para dar los mismos resultados. La documentación de UMAP muestra la otra cara: en MNIST, sobre los puntos que HDBSCAN se anima a agrupar, el ARI es 0,998, pero contando el ruido como grupo cae a 0,05.

**Cómo implementarlo.**

```python
from sklearn.cluster import HDBSCAN
from sklearn.metrics import adjusted_rand_score

hdb = HDBSCAN(min_cluster_size=100).fit(Z)      # Z: UMAP de 10 componentes
lab = hdb.labels_
ok = lab != -1
print("ruido:", 1 - ok.mean())
print("ARI con ruido:", adjusted_rand_score(y, lab))
print("ARI sin ruido:", adjusted_rand_score(y[ok], lab[ok]))   # reportá los dos
```

**Sugerencia.** Si reportás el ARI sin ruido, reportá también el porcentaje de ruido: un método que descarta el 34% de los jugadores puede verse muy bien sobre el 66% restante (en mi barrido, `min_cluster_size=25` en FIFA campo da 15 grupos, 34% de ruido y ARI 0,36 sin ruido contra 0,22 con ruido).

### 8. Críticas teóricas al clustering, para el informe

**Qué dice la fuente.** Laura insiste en que lo difícil del no supervisado es evaluar y que hay que interpretar los grupos con conocimiento del dominio.

**Qué suma el material externo.**
- **Kleinberg, "An Impossibility Theorem for Clustering" (NIPS 2002).** Define tres propiedades razonables de una función de clustering (invariancia de escala, riqueza y consistencia) y demuestra que "there is no clustering function satisfying all three". Cada algoritmo sacrifica alguna, así que no hay un "mejor" en abstracto.
- **Von Luxburg, Williamson y Guyon, "Clustering: Science or Art?" (ICML Workshop on Unsupervised and Transfer Learning, PMLR 27, 2012).** Argumentan que "clustering should not be treated as an application-independent mathematical problem, but should always be studied in the context of its end-use". Es la versión académica de lo que dice Laura.

**Sugerencia.** Citá a los dos en la conclusión del trabajo especial para justificar por qué evaluás con testigos y con interpretación, y no solo con silueta.

### 9. Reglas de asociación con mlxtend: lift, convicción y FP-Growth

**Qué dice la fuente.** Laura explica soporte, confianza, lift y convicción, y la poda de Apriori C4P2 35:58, C4P2 40:22.

**Qué suma el material externo.** La documentación de mlxtend define cada métrica con su fórmula y aclara que la convicción vale "inf" con confianza perfecta y 1 con independencia, igual que el lift. Su función `fpgrowth` usa un FP-tree "without generating the candidate sets explicitly, which makes it particularly attractive for large datasets", y cita a Han, Pei, Yin y Mao.

**Cómo implementarlo.**

```python
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, fpgrowth, association_rules

compras = [["pan", "leche"], ["pan", "pañales", "cerveza", "huevos"],
           ["leche", "pañales", "cerveza", "gaseosa"], ["pan", "leche", "pañales", "cerveza"],
           ["pan", "leche", "pañales", "gaseosa"]]
te = TransactionEncoder()
df = pd.DataFrame(te.fit(compras).transform(compras), columns=te.columns_)

f1 = apriori(df, min_support=0.4, use_colnames=True)
f2 = fpgrowth(df, min_support=0.4, use_colnames=True)
print(len(f1), len(f2))      # mismos conjuntos frecuentes

reglas = association_rules(f2, metric="lift", min_threshold=1.0)
reglas["lift_a_mano"] = reglas["confidence"] / reglas["consequent support"]
print(reglas[["antecedents", "consequents", "support", "confidence",
              "lift", "lift_a_mano", "conviction"]])
```

En el box, las dos funciones dan los mismos conjuntos y `lift_a_mano` coincide con `lift`.

### 10. Grafos: Louvain, Leiden y un detalle de networkx 3.7

**Qué dice la fuente.** Laura menciona detección de comunidades, el algoritmo de Louvain y Gephi para visualizar C4P2 1:09:41.

**Qué suma el material externo.**
- Gephi se presenta como "The Open Graph Viz Platform", libre y de código abierto. [gephi.org](https://gephi.org/)
- Traag, Waltman y van Eck, "From Louvain to Leiden: guaranteeing well-connected communities" (Scientific Reports, 2019): Louvain "may yield arbitrarily badly connected communities"; en sus experimentos, hasta 25% de las comunidades salen mal conectadas y hasta 16% desconectadas. Leiden garantiza comunidades conectadas y además es más rápido.
- networkx 3.7 trae `louvain_communities` y `leiden_communities`. El parámetro `resolution` controla el tamaño: más alto, comunidades más chicas.

**Cómo implementarlo.** Acá hay una trampa que encontré en el box: `leiden_communities` usa por defecto `metric="cpm"` (Constant Potts Model), no modularidad. En el grafo del club de karate, con los valores por defecto, da 17 comunidades (y 34, una por nodo, si ignorás los pesos); con `metric="modularity"` da 4, con la misma modularidad que Louvain (0,444):

```python
import networkx as nx
G = nx.karate_club_graph()
lou = nx.community.louvain_communities(G, seed=0)
lei = nx.community.leiden_communities(G, seed=0, metric="modularity")   # no dejes "cpm"
for nombre, c in [("Louvain", lou), ("Leiden", lei)]:
    print(nombre, len(c), round(nx.community.modularity(G, c), 3))
print(sorted(nx.pagerank(G).items(), key=lambda t: -t[1])[:3])
hubs, autoridades = nx.hits(G)          # HITS de Kleinberg, distinto de PageRank
```

### 11. Recomendación con retroalimentación implícita

**Qué dice la fuente.** Laura cierra con sistemas de recomendación: filtrado colaborativo, el premio Netflix y la cola larga C4P2 1:20:47, y menciona PU learning para clics C4P1 1:44:49.

**Qué suma el material externo.**
- Hu, Koren y Volinsky, "Collaborative Filtering for Implicit Feedback Datasets" (IEEE ICDM 2008): la mayoría de los sistemas reales no tienen puntajes sino historial de compras, reproducciones o navegación, sin "direct input from the users regarding their preferences". Proponen tratar cada interacción como una preferencia con un nivel de confianza. Volinsky es el mismo del equipo ganador del premio Netflix. (La página de IEEE no cargó; leí el PDF del sitio de Yifan Hu.)
- La librería `implicit` (versión 0.7.2) implementa ese ALS, BPR, factorización logística y vecinos ítem a ítem, con soporte de GPU.

**Cómo implementarlo** (no lo corrí: `implicit` no está instalada en el box):

```python
import implicit, scipy.sparse as sp
# filas = usuarios, columnas = ítems, valores = confianza (por ejemplo, cantidad de reproducciones)
usuario_item = sp.csr_matrix(matriz_de_interacciones)
modelo = implicit.als.AlternatingLeastSquares(factors=64)
modelo.fit(usuario_item)
ids, puntajes = modelo.recommend(0, usuario_item[0], N=10)
```

### 12. Texto: BERTopic, pysentimiento y casos argentinos

**Qué dice la fuente.** Para temas, Laura dice que LDA "funciona como piña" y recomienda pysentimiento para sentimiento C4P2 57:18.

**Qué suma el material externo.**
- **BERTopic** (Grootendorst, arXiv 2203.05794, 2022) arma temas en cinco pasos: embeddings de documentos, reducción con UMAP, agrupamiento con HDBSCAN, vectorización y c-TF-IDF para describir cada grupo. La documentación explica por qué no usa centroides: "Models like HDBSCAN assume that clusters can have different shapes and forms", así que el centroide no siempre representa al grupo. Conflicto de interés: documentación del autor.
- **Casos en español rioplatense.** Una tesis de grado de la UADER (Ruhl y Ramos Muzio, 2026) compara LDA, NMF y BERTopic sobre publicaciones de redes sociales argentinas con métricas de coherencia y diversidad, y propone un preprocesamiento para "las particularidades del español argentino en textos cortos e informales". Data Crítica usó BERTopic para agrupar tuits de cuentas de Brasil, Colombia y Ecuador en un análisis de 2023.
- **Mercado Libre** tiene un blog técnico en Medium; la nota que encontré sobre su feature store no cargó con `curl` (devolvió una página corta de Medium), así que no la cito.

**Sugerencia.** El trabajo especial pide que varios LLM interpreten cada grupo con el mismo prompt y que compares sus respuestas C2P2 1:25:13. Pasales las medias de las habilidades por grupo y no los nombres de los jugadores: un LLM sabe de memoria que Messi es delantero, y entonces no está interpretando tus grupos sino recordando el fútbol.

---

## Críticas y límites

1. **Evaluar con testigos es medio circular.** Si tenés las posiciones para medir el ARI, tenés etiquetas, y el problema se parece más a uno supervisado que a uno no supervisado. La materia lo sabe (por eso enseña semisupervisado), pero el trabajo especial evalúa clustering contra una pregunta que ya tiene respuesta. Mi benchmark muestra la consecuencia: 50 etiquetas le ganan al mejor clustering.
2. **Las posiciones no son la estructura de las habilidades.** Ningún método pasa de un ARI de 0,41 en FIFA. Eso no quiere decir que los grupos sean malos: puede haber tipos de jugador (lateral ofensivo, volante de marca) que cruzan las posiciones. Si solo mirás el ARI, castigás justo los hallazgos interesantes.
3. **Las métricas internas premian lo obvio.** La mejor silueta en FIFA es arqueros contra el resto. Kleinberg (2002) demuestra que ninguna función de clustering cumple a la vez tres propiedades razonables, y von Luxburg, Williamson y Guyon (2012) concluyen que la calidad de un agrupamiento depende del uso que le vas a dar. No hay métrica interna que reemplace esa pregunta.
4. **Elegir variables a mano pesa más de lo que parece.** En FIFA hay muchas más columnas de ataque y de técnica que de defensa, y `StandardScaler` les da a todas el mismo peso: el bloque más numeroso domina la distancia. **Sugerencia:** probá agrupar sobre los primeros componentes de PCA, o sobre promedios por bloque de habilidades, y compará.
5. **Las proyecciones distorsionan.** t-SNE iguala tamaños y puede inventar grupos con perplejidad baja; UMAP puede partir grupos reales. Sirven para mirar, no como prueba.
6. **Los datos son de un videojuego.** Los atributos los asignan EA Sports y sus colaboradores, no son mediciones; los jugadores famosos tienen puntajes más cuidados que los de ligas chicas. Para aprender sirve, pero no saques conclusiones sobre fútbol real.
7. **Las herramientas tienen trampas de versión.** Yellowbrick 1.5 falla con scikit-learn 1.9.1 (funciona con 1.6.1, parecida a la de Colab); `leiden_communities` de networkx 3.7 usa CPM por defecto y no modularidad; el `min_samples` de `sklearn.cluster.HDBSCAN` no equivale al de la librería hdbscan; y Ward sobre todos los jugadores necesita mucha memoria.
8. **Las historias contadas de memoria fallan.** Apriori, LDA, HITS, BERT, ladder networks, BloombergGPT, Nvidia, Cloudflare, Andersen y Enron tenían errores de fecha, autor o detalle. No cambian el código, pero si las citás en un informe, citá la fuente primaria.
9. **El acceso a cómputo no está garantizado.** El CCAD evalúa cada pedido y está pensado para investigadores; los 100 dólares de AWS por alumno corresponden a un programa que AWS dejó de ofrecer a instituciones en 2023. Colab sigue siendo la opción sin trámites.
10. **Conflictos de interés.** pysentimiento lo firma la propia docente que lo recomienda. Las documentaciones de UMAP, HDBSCAN y BERTopic las escriben sus autores. Snorkel es el sistema de los autores que lo evalúan. La nota sobre Banco Galicia e IBM tiene tono de comunicado. El post de la caída de Cloudflare es de Cloudflare, el anuncio del cifrado de Messenger es de Meta y todo lo que sé de Claude Fable sale de páginas de Anthropic.
11. **Límites de esta revisión.**
    - **El benchmark** usa FIFA 2019 y no FC 24: el dataset de Kaggle pide cuenta y el archivo de 2025 del GitHub de la diplomatura está en Git LFS y no bajó entero. Usé una muestra de 6.000 jugadores, tres semillas y una sola configuración de UMAP; no ajusté el tipo de covarianza de la mezcla de gaussianas ni barrí `eps` de DBSCAN. Con otros parámetros los números se mueven; el orden general (mezcla de gaussianas arriba en FIFA, UMAP decisivo en los dígitos) fue estable entre semillas.
    - **Leí con `curl`** (el lector web no las trajo o preferí el texto completo): el paper de t-SNE en JMLR, el de Apriori en VLDB, el de Elkan y Noto, el de Hu, Koren y Volinsky, el de Ben-Hur y otros, el de Kleinberg sobre HITS, el de Blum y Mitchell, el de LDA, la página de Wikipedia sobre Arthur Andersen, la nota de CNBC, el blog técnico de Netflix, el README de Kimi K3 y la mayoría de las páginas de documentación (scikit-learn, UMAP, BERTopic, mlxtend, networkx, implicit, Yellowbrick, Gephi, llama.cpp), además de los resúmenes de arXiv y la Ley 25.326 en InfoLEG.
    - **Solo vi en resultados de búsqueda, sin abrir:** el webcast de DSS News donde Blischok repite la historia de los pañales, el material de Mark Madsen (TDWI) sobre esa anécdota, el convenio del CCAD con CONICET de 2023, el tarifario y la wiki del CCAD, la adhesión del Campus Norte de la UNC a AWS Academy, la publicación sobre IBM watsonx y el asistente Gala de 2024, la nota de La Nación de 2025 sobre IA en Galicia y el sitio de optativas de 2020 que lista a Damián Barsotti.
    - **No cargaron:** la nota del New York Times de 2005 sobre Andersen (tiempo agotado), las páginas de Springer de Campello y otros (2013) y de Cybenko (1989) (pidieron verificación), la de ScienceDirect de Hornik (1991) (vacía), las de ACM de Elkan y Noto y de FP-Growth (pidieron verificación), la de IEEE de Hu y otros (vacía), la de PubMed de Ben-Hur (pidió verificación), la de la FERC sobre Enron (error 404), la nota de Mercado Libre en Medium (página corta) y la página de GitHub de Kimi K3 en el lector web (solo metadatos; el README sí bajó con `curl`). Campello, Cybenko y Hornik quedan citados por la referencia de scikit-learn o sin link.

---

## Análisis adversario

> Cómo leer esta sección: pongo el enfoque de la materia contra la alternativa más fuerte que encontré, presentada en su mejor versión. La idea no es decidir quién "gana" en general, sino ver en qué situaciones conviene cada una. Uso mis números del benchmark de la sección 4 como evidencia, junto con papers que abrí.

**La tesis, en dos oraciones.** La materia sostiene que para descubrir estructura en datos sin etiquetas conviene elegir y escalar variables a mano, probar varios algoritmos clásicos (K-means, jerárquicos, mezclas de gaussianas, DBSCAN) y evaluar con métricas internas y con testigos. Detrás está la idea de que los grupos se interpretan con conocimiento del dominio, y de que entender cada algoritmo importa más que la herramienta de moda.

### La alternativa más fuerte: no agrupar, sino etiquetar poco (semisupervisado, supervisión débil o etiquetado con LLM)

**Qué propone.** Si ya sabés qué categorías te importan (y en el trabajo especial las sabés, porque evaluás contra posiciones), no gastes el esfuerzo en buscar el algoritmo de clustering que mejor las recupere. Etiquetá a mano unas decenas o cientos de ejemplos elegidos con criterio, o escribí reglas heurísticas que etiqueten mucho con ruido, o pedile a un LLM que pre-etiquete. Después entrená un clasificador, y si querés aprovechar los no etiquetados, usá autoaprendizaje o propagación de etiquetas.

**Qué dice el curso sobre esta alternativa.** No la ignora: Laura dedica la clase 4 a semisupervisado, con weak supervision y triangulación de etiquetadores C4P1 42:06, autoaprendizaje combinado con aprendizaje activo C4P1 59:07, co-training y PU learning. Y el trabajo especial incluye pedirle a varios LLM que interpreten cada grupo C2P2 1:25:13. Lo que la materia no hace es ponerla como competidora del clustering sobre el mismo problema.

**Por qué elegí esta.** La otra candidata fuerte era el pipeline de embeddings, UMAP y HDBSCAN (el de BERTopic). La medí y en FIFA no gana: UMAP mejora a K-means de 0,36 a 0,39 pero empeora a la mezcla de gaussianas, y HDBSCAN separa arqueros contra el resto o deja mucho ruido. Brilla en los dígitos (de 0,53 a 0,84) y en texto, pero es una versión más moderna del mismo paradigma, con el mismo problema de evaluación. En cambio, etiquetar poco ataca la premisa: en FIFA, 50 etiquetas al azar ya superan al mejor clustering (ARI 0,48 contra 0,41), y 200 llegan a 0,61. Es la crítica que más cambia lo que harías.

### La alternativa en su mejor versión

**Quién la defiende y qué dice.**
- Ratner, Bach, Ehrenberg, Fries, Wu y Ré, "Snorkel: Rapid Training Data Creation with Weak Supervision" (2017): el etiquetado es "increasingly the largest bottleneck"; con funciones de etiquetado heurísticas, expertos del dominio "build models 2.8x faster and increase predictive performance an average 45.5% versus seven hours of hand labeling". Conflicto de interés: es el sistema de los propios autores.
- Gilardi, Alizadeh y Kubli, "ChatGPT Outperforms Crowd-Workers for Text-Annotation Tasks" (2023): sobre 2.382 tuits, la exactitud de ChatGPT sin ejemplos supera a la de trabajadores de MTurk en cuatro de cinco tareas, con un costo por anotación menor a 0,003 dólares, "about twenty times cheaper than MTurk".
- Wang, Liu, Xu, Zhu y Zeng, "Want To Reduce Labeling Cost? GPT-3 Can Help" (2021): para lograr el mismo rendimiento en el modelo final, etiquetar con GPT-3 cuesta "50% to 96% less" que con personas, y combinar etiquetas de GPT-3 con humanas rinde todavía mejor.
- Settles, "Active Learning Literature Survey" (2010): el marco clásico para elegir qué ejemplos etiquetar primero.

**Qué evidencia la respalda.**
- Mi benchmark: con 50 jugadores etiquetados de 6.000, una regresión logística llega a un ARI de 0,48 en las dos versiones de FIFA, contra 0,41 y 0,35 del mejor clustering; con 200, a 0,61 y 0,54.
- La propia documentación de scikit-learn: `SelfTrainingClassifier`, `LabelPropagation` y `LabelSpreading` están listos, y aceptan los no etiquetados con -1.

**Qué evidencia la contradice.**
- Pangakis, Wolken y Fasching, "Automated Annotation with Generative AI Requires Validation" (2023): replicando 27 tareas en 11 datasets con GPT-4, el rendimiento es "highly contingent on both the dataset and the type of annotation task"; sin validar contra etiquetas humanas, no sabés si funcionó.
- Reiss, "Testing the Reliability of ChatGPT for Text Annotation and Classification" (2023): la consistencia "can fall short of scientific thresholds for reliability"; cambios mínimos en el prompt o repetir la misma entrada cambian la respuesta.
- Mi benchmark otra vez: con 20 etiquetas, `LabelSpreading` da 0,25 a 0,27, peor que la mezcla de gaussianas sin ninguna etiqueta. Con muy pocas etiquetas, el clustering sigue siendo competitivo.
- Von Luxburg, Williamson y Guyon (2012): cuando el objetivo es explorar, definir las etiquetas antes es presuponer la respuesta. Ninguna cantidad de etiquetas descubre una categoría que no imaginaste.
- En FIFA hay una trampa extra: un LLM etiquetaría por el nombre del jugador, que conoce de memoria, y no por las habilidades.

### Comparación directa

| Criterio | A: clustering clásico (la materia) | B: pocas etiquetas, semisupervisado o LLM |
|---|---|---|
| Costo | Solo cómputo; minutos en Colab | Horas de etiquetado humano (50 a 200 ejemplos) o costo por consulta a un LLM, más la validación |
| — | Baja en código; alta en interpretación | Baja con scikit-learn; más alta con supervisión débil (reglas, modelo de etiquetas) |
| Tiempo hasta algo útil | Inmediato, pero "útil" depende de interpretar | Después de etiquetar; con LLM, horas |
| Riesgo | Grupos que no responden tu pregunta; métricas internas que premian lo obvio | Etiquetas sesgadas o inconsistentes; categorías definidas de antemano que esconden lo nuevo |
| Madurez | Décadas; todo en scikit-learn | Semisupervisado clásico maduro; etiquetado con LLM desde 2023, en evolución |
| Evidencia | Teoría (Kleinberg) y práctica dicen que depende del uso | Fuerte cuando hay categorías definidas (Snorkel, Gilardi y otros, mi benchmark); mixta para LLM sin validación |
| Equipo o contexto | Analista solo, sin etiquetas, exploración | Alguien que conozca el dominio para etiquetar o validar; categorías claras |
| Qué pregunta responde | "¿Qué grupos hay?" | "¿A qué categoría conocida pertenece cada uno?" |

### Dónde gana la alternativa

1. Cuando las categorías están definidas de antemano y lo que importa es acertarlas: posiciones, fraude, temas de un manual de códigos. Ahí 50 a 200 etiquetas superan a cualquier clustering que medí.
2. Cuando el texto es la materia prima y el etiquetado humano es caro: los LLM bajan el costo por anotación en un orden de magnitud, si validás.
3. Cuando necesitás un modelo que se aplique a datos nuevos con un criterio estable: un clasificador entrenado es más predecible que reagrupar cada vez.

### Dónde pierde

1. Cuando no sabés qué grupos existen: segmentación exploratoria de clientes, tipologías de pacientes, comportamiento de usuarios. Etiquetar supone saber.
2. Cuando no hay quién etiquete con criterio o no hay presupuesto para validar: un LLM sin validación puede ser inconsistente (Reiss) o depender demasiado de la tarea (Pangakis y otros).
3. Con muy pocas etiquetas (20 en mi prueba) o con datos donde el LLM puede "hacer trampa" recordando (nombres de jugadores, empresas famosas).
4. Cuando el objetivo es aprender: la materia enseña a pensar distancias, escalas y densidades, que hacen falta también para elegir qué etiquetar.

### Cómo decidir

**Elegí A (clustering clásico, la materia) si** no sabés de antemano qué grupos hay y querés descubrirlos, no tenés etiquetas ni quién las haga, necesitás explicar cada grupo con las medias de sus variables, o estás haciendo el trabajo especial, que evalúa exactamente eso.

**Elegí B (pocas etiquetas con semisupervisado, supervisión débil o LLM) si** ya sabés qué categorías querés, podés etiquetar entre 50 y 200 ejemplos (o escribir reglas), la medida de éxito es acertar esas categorías y, si usás un LLM, vas a validar sus etiquetas contra una muestra etiquetada por personas.

**Un híbrido posible (sugerencia).**
1. Agrupá primero para explorar: mezcla de gaussianas o K-means sobre datos escalados en tablas; embeddings, UMAP y HDBSCAN si son textos o imágenes.
2. Usá los grupos para decidir qué etiquetar: unos pocos ejemplos de cada grupo, más los puntos de borde (baja probabilidad en la mezcla, o ruido en HDBSCAN).
3. Con esas etiquetas, entrená un clasificador simple o un `SelfTrainingClassifier`, y medí contra una parte etiquetada que no usaste.
4. Si usás un LLM, que nombre los grupos a partir de sus medias, o que pre-etiquete textos, siempre con una muestra validada por personas.
5. Volvé a agrupar lo que el clasificador clasifica con poca confianza: ahí aparecen las categorías que no habías previsto.

**Veredicto.** Para el trabajo especial, el enfoque de la materia es el correcto: es lo que se pide y lo que enseña a pensar. Pero sumá al informe la línea de base de 50 etiquetas: muestra cuánto de las posiciones es recuperable y deja claro que tus grupos responden otra pregunta. En el trabajo real, si las categorías ya están definidas, la alternativa B gana casi siempre; si no lo están, A sigue siendo el punto de partida, y el híbrido es lo que usaría.

---

## Material para seguir

**scikit-learn y librerías**
- [scikit-learn, guía de clustering](https://scikit-learn.org/stable/modules/clustering.html): la tabla de métodos con escalabilidad, geometría y métrica, y las advertencias sobre la inercia; es la referencia de casi todas las correcciones.
- [scikit-learn, comparación de algoritmos en datos de juguete](https://scikit-learn.org/stable/auto_examples/cluster/plot_cluster_comparison.html): la figura que se usa en clase, con la advertencia de que su intuición puede no valer en alta dimensión.
- [scikit-learn, HDBSCAN](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.HDBSCAN.html): parámetros, la diferencia de `min_samples` con la librería hdbscan y las referencias a Campello y otros.
- [scikit-learn, BayesianGaussianMixture](https://scikit-learn.org/stable/modules/generated/sklearn.mixture.BayesianGaussianMixture.html): el proceso de Dirichlet que mencionó Georgina, para no fijar K.
- [scikit-learn, Semi-supervised learning](https://scikit-learn.org/stable/modules/semi_supervised.html): autoaprendizaje y propagación de etiquetas listos para usar.
- [UMAP, Using UMAP for Clustering](https://umap-learn.readthedocs.io/en/latest/clustering.html): la receta y los riesgos de agrupar sobre UMAP, escrita por su autor.
- [BERTopic, The Algorithm](https://maartengr.github.io/BERTopic/algorithm/algorithm.html): el pipeline de embeddings, UMAP, HDBSCAN y c-TF-IDF paso por paso.
- [mlxtend, association_rules](https://rasbt.github.io/mlxtend/user_guide/frequent_patterns/association_rules/) y [fpgrowth](https://rasbt.github.io/mlxtend/user_guide/frequent_patterns/fpgrowth/): todas las métricas de reglas con fórmula y la alternativa rápida a Apriori.
- [networkx, louvain_communities](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.community.louvain.louvain_communities.html) y [leiden_communities](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.community.leiden.leiden_communities.html): para comunidades; ojo con el `metric="cpm"` por defecto de Leiden.
- [implicit](https://benfred.github.io/implicit/): recomendación con clics y compras, con ALS y BPR.
- [Gephi](https://gephi.org/): para visualizar grafos sin programar.

**Lecturas críticas, cortas y muy recomendables**
- [Wattenberg, Viégas y Johnson, "How to Use t-SNE Effectively" (Distill, 2016)](https://distill.pub/2016/misread-tsne/): interactiva; en diez minutos dejás de leer mal un gráfico de t-SNE.
- [Kleinberg, "An Impossibility Theorem for Clustering" (NIPS 2002)](https://papers.nips.cc/paper/2002/hash/43e4e6a6f341e00671e123714de019a8-Abstract.html): por qué no hay un algoritmo de clustering "mejor".
- [Von Luxburg, Williamson y Guyon, "Clustering: Science or Art?" (PMLR 27, 2012)](https://proceedings.mlr.press/v27/luxburg12a.html): el argumento de que el clustering se evalúa según su uso.
- [Von Luxburg, "Clustering Stability: An Overview" (2010)](https://arxiv.org/abs/1007.1075): qué garantiza y qué no elegir K por estabilidad.
- [Ben-Hur, Elisseeff y Guyon, "A stability based method for discovering structure in clustered data" (PSB 2002)](https://psb.stanford.edu/psb-online/proceedings/psb02/benhur.pdf): el método de estabilidad original, con figuras claras.

**Papers fundacionales, para citar bien**
- [Van der Maaten y Hinton, t-SNE (JMLR 2008)](https://www.jmlr.org/papers/volume9/vandermaaten08a/vandermaaten08a.pdf): la fuente de t-SNE, con su sección de debilidades.
- [McInnes, Healy y Melville, UMAP (arXiv 1802.03426)](https://arxiv.org/abs/1802.03426): la fuente de UMAP (2018).
- [Blei, Ng y Jordan, LDA (JMLR 2003)](https://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf): la autoría correcta de LDA.
- [Agrawal y Srikant, Apriori (VLDB 1994)](https://www.vldb.org/conf/1994/P487.PDF): el algoritmo y la fecha correcta.
- [Kleinberg, HITS](https://www.cs.cornell.edu/home/kleinber/auth.pdf) y [Brin y Page, Google](http://infolab.stanford.edu/~backrub/google.html): hubs y authorities por un lado, PageRank por el otro.
- [Traag, Waltman y van Eck, Leiden (Scientific Reports 2019)](https://www.nature.com/articles/s41598-019-41695-z): por qué Louvain puede dar comunidades desconectadas.
- [Hu, Koren y Volinsky, retroalimentación implícita (ICDM 2008)](http://yifanhu.net/PUB/cf.pdf): la base de la recomendación con clics.
- [Elkan y Noto, PU learning (KDD 2008)](https://cseweb.ucsd.edu/~elkan/posonly.pdf), [Blum y Mitchell, co-training (COLT 1998)](https://www.cs.cmu.edu/~avrim/Papers/cotrain.pdf) y [Rasmus y otros, ladder networks (2015)](https://arxiv.org/abs/1507.02672): los tres métodos semisupervisados de la clase 4, en su versión original.

**Sobre la alternativa (etiquetar poco)**
- [Ratner y otros, Snorkel (2017)](https://arxiv.org/abs/1711.10160): supervisión débil con funciones de etiquetado.
- [Gilardi, Alizadeh y Kubli (2023)](https://arxiv.org/abs/2303.15056): el estudio más citado a favor de etiquetar con LLM.
- [Pangakis, Wolken y Fasching (2023)](https://arxiv.org/abs/2306.00176) y [Reiss (2023)](https://arxiv.org/abs/2304.11085): los contrapesos; leelos antes de confiar en etiquetas de un LLM.
- [Settles, Active Learning Literature Survey (2010)](https://burrsettles.com/pub/settles.activelearning.pdf): cómo elegir qué etiquetar.

**Datos y casos**
- [Kaggle, EA Sports FC 24 complete player dataset](https://www.kaggle.com/datasets/stefanoleone992/ea-sports-fc-24-complete-player-dataset): el dataset del trabajo especial (pide cuenta).
- [GitHub DiploDatos/AprendizajeNOSupervisado](https://github.com/DiploDatos/AprendizajeNOSupervisado): FIFA 2018 y 2019 sin cuenta, notebooks y filminas de ediciones anteriores.
- [Enron Email Dataset (CMU)](https://www.cs.cmu.edu/~enron/): el corpus de correos y su historia real.
- [pysentimiento (arXiv 2106.09462)](https://arxiv.org/abs/2106.09462): sentimiento y emociones en español, hecho en Argentina (coautora: Laura).
- [Ruhl y Ramos Muzio, tesis UADER (2026)](https://rd.fcyt.uader.edu.ar/items/865b2f56-9cbe-484d-b770-bcecfbb838a5): LDA, NMF y BERTopic sobre redes sociales argentinas.
- [Data Crítica, análisis con BERTopic (2023)](https://datacritica.github.io/capir-transfronteriza2-2023/): un caso latinoamericano de temas en tuits, con el código.

**Historia, para citar bien**
- [Forbes, "Birth of a legend" (1998)](https://www.forbes.com/forbes/1998/0406/6107128a.html) y [KDnuggets 00:13](https://www.kdnuggets.com/news/2000/n13/23i.html): el origen real de los pañales y la cerveza.
- [Wired, 21/09/2009](https://www.wired.com/2009/09/bellkors-pragmatic-chaos-wins-1-million-netflix-prize/) y [Netflix TechBlog (2012)](https://netflixtechblog.com/netflix-recommendations-beyond-the-5-stars-part-1-55838468f429): cómo terminó el premio Netflix y por qué no se usó la solución ganadora entera.
- [Cloudflare, caída del 18/11/2025](https://blog.cloudflare.com/18-november-2025-outage/): un buen caso de cómo un archivo de features rompe un sistema con ML en producción.
