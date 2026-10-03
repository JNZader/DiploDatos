# Segunda parte: "Introducción al Aprendizaje Automático", con material externo

**Esta es la continuación de** `introduccion-aprendizaje-automatico-apunte-de-estudio.md` y `introduccion-aprendizaje-automatico-guia-de-implementacion.md` (las clases de la materia Introducción al Aprendizaje Automático de la diplomatura en ciencia de datos de FAMAF UNC, edición 2026, dictadas por Vanesa Meinardi y Edgardo en cuatro encuentros entre el 22 de mayo y el 6 de junio). Esos archivos resumen lo que dice la materia. Esta segunda parte suma material externo para verificar lo que en el apunte quedó "para verificar", respaldar con fuentes las correcciones que ya marqué, resolver los nombres que la transcripción automática deformó, proponer mejoras concretas para el práctico 2 y para el trabajo real, y marcar dónde el enfoque tiene límites. Revisé todo el 02/10/2026. Solo cito páginas que abrí; cuando una página no cargó en el lector web y la leí por otra vía (con `curl` desde el box, o por la API de Europe PMC), lo digo, y cuando solo tengo un resultado de búsqueda, también.

> Cómo leer esto: cuando digo "la materia" o "las docentes" me refiero a lo que dicen Vanesa y Edgardo en las clases. Las marcas de tiempo usan la etiqueta de cada grabación del apunte (C1P1 es la clase 1, parte 1, y así hasta C4P3) y llevan al minuto exacto en la grabación. Cuando digo "sugerencia" es una idea mía que combina fuentes, no algo que diga una fuente puntual. Todo el código de este archivo lo corrí en el box el 02/10/2026 sobre el dataset real del práctico 2, con scikit-learn 1.9.1 y también en un entorno armado con las versiones que hoy lista Colab (scikit-learn 1.6.1); cuando los números cambian entre versiones, lo aclaro. Marco los conflictos de interés donde importan: varios benchmarks de modelos tabulares los firman autores de las herramientas que salen ganando (scikit-learn, AutoGluon, TabPFN), y los informes de OpenAI hablan de sus propios modelos.

---

## Checklist actualizado (curso + mejoras)

1. Antes de modelar, leé las líneas con `#` de `loan_data.csv`: la etiqueta `TARGET` vale 1 si el cliente **incumplió** el préstamo y 0 si lo pagó; todos los clientes recibieron el préstamo, así que no es "si se le dio o no".
2. No copies las cifras del encabezado del archivo: describen el HMEQ original (5.960 préstamos, 20% de incumplimiento), pero el archivo del práctico tiene 1.854 filas, 10 variables numéricas, ningún faltante y 309 positivos (16,7%).
3. Separá el conjunto de test una sola vez, al principio y estratificado (`stratify=y`), y no lo mires hasta el final, como pide la materia.
4. Meté todo el preprocesamiento (escalado, imputación, remuestreo) dentro de un `Pipeline`, para que la validación cruzada no filtre información de los folds de validación.
5. Si usás `GridSearchCV` y además querés una estimación honesta del rendimiento, hacé validación cruzada anidada: la búsqueda de hiperparámetros va adentro de cada fold externo.
6. Antes de tocar los datos por el desbalance, ajustá el umbral de decisión con `TunedThresholdClassifierCV` (desde scikit-learn 1.5, así que está en Colab): en el práctico mejora F1 y exactitud balanceada sin romper las probabilidades.
7. Si usás `class_weight="balanced"`, sabé que el peso es **inverso** a la frecuencia, n_muestras / (n_clases × n_clase): en el práctico da 0,60 a los que pagaron y 3,00 a los que incumplieron.
8. Si usás SMOTE, recordá que no duplica ejemplos sino que crea ejemplos sintéticos interpolando entre vecinos de la clase minoritaria, y aplicalo con el `Pipeline` de imbalanced-learn para que solo toque los folds de entrenamiento.
9. Tené en cuenta que pesos y remuestreo inflan las probabilidades de la clase minoritaria: en el práctico, la probabilidad media de incumplimiento pasa de 0,16 a 0,40 con `class_weight="balanced"`, cuando la tasa real es 0,167.
10. Reportá varias métricas a la vez: área bajo la curva PR (`average_precision`), exactitud balanceada, F1 de la clase positiva, F1 macro, MCC y Brier, y no solo la exactitud.
11. Leé bien la curva PR: con un umbral alto el modelo predice pocos positivos, la precisión sube y el recall baja; al bajar el umbral pasa lo contrario.
12. Si las probabilidades importan (por ejemplo, para fijar una tasa o un límite de crédito), mirá la curva de calibración y el Brier, y calibrá con `CalibratedClassifierCV` si hace falta.
13. Sumá siempre un ensamble de árboles (`RandomForestClassifier` o `HistGradientBoostingClassifier`) como "techo" de rendimiento, aunque después elijas un modelo más simple: en el práctico la regresión logística llega a un AUC de 0,79 y el bosque aleatorio a 0,93.
14. Recordá que el encabezado del dataset pide un modelo "suficientemente interpretable" para justificar los rechazos: si el ensamble gana por poco, quedate con el modelo que puedas explicar.
15. Comprobá qué versión de scikit-learn tenés (`sklearn.__version__`): Colab lista hoy la 1.6.1, donde `penalty` de `LogisticRegression` todavía no está deprecado; en 1.8 y posteriores sí lo está, así que no lo pases y controlá la regularización con `C`.
16. Para la impureza de un árbol, recordá que Gini va de 0 a 1 - 1/k (0,5 con dos clases) y la entropía de 0 a log2(k) (1 con dos clases).
17. Para KNN con dos clases, elegí un K impar, que evita empates en la votación.
18. Cuando cites historia, citá bien: "regresión" viene de Galton (1886) y su "regresión a la mediocridad", el libro que frenó al perceptrón es "Perceptrons" de Minsky y Papert (1969) y la retropropagación que lo reactivó es de Rumelhart, Hinton y Williams (Nature, 1986).
19. No des cifras de parámetros de ChatGPT: OpenAI no publica el tamaño de GPT-4 ni de sus sucesores, y GPT-3, de 2020, ya tenía 175.000 millones, no 5.000 millones.
20. Si te preguntan por lotes en potencias de dos, la respuesta honesta es que no hay evidencia de que la potencia de dos en sí importe; lo que NVIDIA documenta es que las dimensiones múltiplos de 8 aprovechan mejor los Tensor Cores.
21. Para estudiar, usá las figuras originales: las del sobreajuste polinómico salen del capítulo 1 de Bishop (gratis en PDF) y el ejemplo China/Japón, del capítulo 13 del libro de Manning, Raghavan y Schütze (gratis en línea).
22. Confirmá en el aula virtual las fechas de entrega: el calendario público confirma las clases (22 y 23 de mayo, 5 y 6 de junio), pero no publica el 8 de junio ni el 22 de junio de los prácticos, y las dos fechas ya pasaron.

---

## Versión completa

### 1. Los datos del curso, verificados

Las docentes avisan varias veces que algunas cosas las cuentan de memoria. Las revisé y las ordené de la corrección más importante a la menos importante. "Sí" quiere decir que la fuente lo confirma, "En parte" que es correcto con matices importantes, "No" que la fuente lo contradice, "Desactualizado" que fue cierto pero ya no lo es, y "No verificable" que no encontré una fuente primaria que lo confirme o lo niegue.

| Afirmación | Resultado | Matiz | Fuente |
|---|---|---|---|
| La etiqueta del práctico 2 dice "si se le dio un préstamo o no" C4P3 1:05:11 | No | El encabezado del archivo dice: "TARGET Label: 1 = client defaulted on loan - 0 = loan repaid". Todos los clientes recibieron el préstamo; la etiqueta dice si después lo incumplieron (o tuvieron mora grave). El encabezado cita como origen el HMEQ de Kaggle (no abrí la página de Kaggle). Cambia la lectura de todo el práctico: el "positivo" es el cliente riesgoso. | [loan_data.csv en el GitHub de DiploDatos](https://raw.githubusercontent.com/DiploDatos/IntroduccionAprendizajeAutomatico/master/data/loan_data.csv) (descargado con `curl`) |
| El dataset del práctico 2 es de clientes de un banco, con los metadatos en los comentarios del archivo y en el GitHub de la diplomatura C4P3 1:00:27, C4P3 1:13:28 | Sí, con un matiz importante | Es una versión del HMEQ (Home Equity). Pero el encabezado describe el dataset original (5.960 préstamos, 1.189 incumplimientos, 20%, 12 variables), y el archivo tiene otra cosa: 1.854 filas, 10 variables numéricas (faltan `REASON` y `JOB`), ningún valor faltante y 309 positivos (16,7%). Parece el subconjunto de casos completos, pero el archivo no lo dice. Calculá vos la prevalencia. El repositorio no se actualizó para 2026 (último commit del 14/06/2025). | [loan_data.csv](https://raw.githubusercontent.com/DiploDatos/IntroduccionAprendizajeAutomatico/master/data/loan_data.csv); [historial de commits](https://github.com/DiploDatos/IntroduccionAprendizajeAutomatico/commits/master) |
| Con `class_weight` el peso de cada clase "es la proporción de datos" (con 60/40, la parte positiva se multiplica por 0,60) C2P1 52:35, C4P3 11:41 | No | Es al revés: el modo "balanced" usa pesos **inversamente** proporcionales a la frecuencia, `n_samples / (n_classes * np.bincount(y))`. En el práctico 2 da 0,60 a la clase 0 y 3,00 a la clase 1 (lo calculé con `compute_class_weight`). Con el peso igual a la proporción, la clase mayoritaria pesaría más y empeorarías el problema. | [scikit-learn, LogisticRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html) |
| SMOTE "duplica ejemplos existentes" C4P3 9:43 | No | Duplicar es el sobremuestreo aleatorio (`RandomOverSampler`). SMOTE crea ejemplos sintéticos de la clase minoritaria interpolando entre un ejemplo y sus vecinos de la misma clase. El paper original dice "our method of over-sampling the minority class involves creating synthetic minority class examples" y lo combina con submuestreo de la mayoritaria. | [Chawla, Bowyer, Hall y Kegelmeyer, JAIR 16, 321 a 357, 2002 (arXiv 1106.1813)](https://arxiv.org/abs/1106.1813); [imbalanced-learn, sobremuestreo](https://imbalanced-learn.org/stable/over_sampling.html) |
| En la curva PR, con "umbral muy alto, el modelo predice todos positivos pero casi todos correctos" C4P2 44:02 | No (está al revés en la primera parte) | Con umbral alto el modelo predice **pocos** positivos: la precisión suele ser alta y el recall bajo. Bajar el umbral sube el recall y, en general, baja la precisión (aunque no siempre en forma monótona). En el práctico, con un umbral de 0,8 salen 29 positivos con precisión 1,00 y recall 0,47 (sección 5). | [scikit-learn, ejemplo Precision-Recall](https://scikit-learn.org/stable/auto_examples/model_selection/plot_precision_recall.html) |
| El F1 refleja qué tan bien se clasifican "ambas clases" C4P2 48:21 | No | En un problema binario, `f1_score` con `average="binary"` (el valor por defecto) devuelve el F1 de `pos_label`, es decir, de la clase positiva; los verdaderos negativos no entran. Para mirar las dos clases usá `average="macro"` o la exactitud balanceada. | [scikit-learn, f1_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html); [scikit-learn, evaluación de modelos](https://scikit-learn.org/stable/modules/model_evaluation.html) |
| Error de clasificación, entropía y Gini "varían entre 0 y 1" C3P1 1:08:51 | En parte | La documentación define Gini como la suma de p(1 - p) sobre las clases; su máximo, con k clases equiprobables, es 1 - 1/k: 0,5 con dos clases. El error de clasificación tiene el mismo máximo y la entropía en bits llega a log2(k), que vale 1 con dos clases. Solo la entropía binaria va de 0 a 1. El máximo lo deduje yo de la fórmula. | [scikit-learn, árboles de decisión](https://scikit-learn.org/stable/modules/tree.html) |
| El FWHM "suele ser como un 38% más grande que sigma" C1P2 33:27 | No | Para una gaussiana, FWHM = 2√(2 ln 2) σ ≈ 2,355 σ, o sea, un 135% más grande. El ancho entre los dos puntos de inflexión, que es lo que Edgardo describe como σ, es 2σ. | [Wikipedia, Full width at half maximum](https://en.wikipedia.org/wiki/Full_width_at_half_maximum) (leída con `curl`); [MathWorld, Gaussian Function](https://mathworld.wolfram.com/GaussianFunction.html) (leída con `curl`; la fórmula está en una imagen) |
| "ChatGPT anda por los 5000 millones de parámetros" C1P2 21:34 | No (y la cifra actual no es pública) | GPT-3, de 2020, ya tenía 175.000 millones de parámetros, 35 veces más. El informe técnico de GPT-4 dice que no da detalles sobre la arquitectura, "including model size". Cualquier cifra para los modelos actuales de ChatGPT es una estimación de terceros. Los dos documentos son de OpenAI. | [arXiv 2005.14165 (GPT-3)](https://arxiv.org/abs/2005.14165); [arXiv 2303.08774 (GPT-4)](https://arxiv.org/abs/2303.08774) |
| "Regresión" viene de que el modelo "regresa datos" C1P2 9:54 | No | El término viene de Francis Galton, "Regression towards Mediocrity in Hereditary Stature" (Journal of the Anthropological Institute 15, 246 a 263, 1886): la altura de los hijos se desvía de la media, en promedio, dos tercios de lo que se desvían sus padres; "regresan" hacia la media. Antes lo había visto con semillas, en una conferencia de 1877. | [Galton, 1886 (PDF en la Universidad de York)](https://www.york.ac.uk/depts/maths/histstat/galton_reg.pdf) (leído con `curl` y `pdftotext`) |
| "Alguien escribió un libro" mostrando que el perceptrón solo separa linealmente, y después se juntaron varios perceptrones C1P2 1:58:10 | Sí, con nombres | El libro es "Perceptrons", de Marvin Minsky y Seymour Papert (MIT Press, 1969). La retropropagación que permitió entrenar redes multicapa es "Learning representations by back-propagating errors", de Rumelhart, Hinton y Williams (Nature 323, 533 a 536, publicado el 09/10/1986); su resumen la contrasta con el "perceptron-convergence procedure" y su lista de referencias cita el libro de 1969 y un trabajo previo de Le Cun (1985). La página de MIT Press del libro me devolvió "Access Denied"; lo confirmo por la referencia de Nature. | [Nature, 323533a0](https://www.nature.com/articles/323533a0) |
| Las figuras del seno con M = 0, 1, 3 y 9 y la regularización con ln λ = -18 C1P1 1:09:56, C1P1 1:26:21 | Sí | Son del capítulo 1 de "Pattern Recognition and Machine Learning" de Christopher Bishop (Springer, 2006): datos generados con sin(2πx) y N = 10, figura 1.4 (página 7) con M = 0, 1, 3 y 9, figura 1.7 (página 10) con ln λ = -18 y ln λ = 0, y tabla 1.1 con los coeficientes. Microsoft Research ofrece el libro completo en PDF. | [Microsoft Research, PRML](https://www.microsoft.com/en-us/research/publication/pattern-recognition-machine-learning/) (el PDF lo bajé con `curl`) |
| Con grado alto los coeficientes se disparan por el "costo computacional" C1P1 1:22:20 | No | Bishop lo explica en la misma sección: con M = 9 "the coefficients have become finely tuned to the data by developing large positive and negative values", es decir, el polinomio se acomoda a cada punto y al ruido. Es varianza del modelo (y, en la práctica, mal condicionamiento numérico), no costo de cómputo. | [Bishop, PRML, sección 1.1 y tabla 1.1](https://www.microsoft.com/en-us/research/publication/pattern-recognition-machine-learning/) |
| Con ln λ = 0 (λ = 1) se está "penalizando lo máximo posible" C1P1 1:26:21 | No | λ puede ser cualquier número no negativo; en Bishop, ln λ = 0 es solo el segundo ejemplo de la figura 1.7, elegido para mostrar un modelo demasiado regularizado. En scikit-learn el equivalente (`alpha` en `Ridge`, o `1/C` en `LogisticRegression`) tampoco tiene techo. | [Bishop, PRML, figura 1.7](https://www.microsoft.com/en-us/research/publication/pattern-recognition-machine-learning/) |
| El ejemplo China/Japón de Naive Bayes C2P2 39:53 | Sí | Es la tabla 13.1 de "Introduction to Information Retrieval" (Manning, Raghavan y Schütze): los documentos "Chinese Beijing Chinese", "Chinese Chinese Shanghai", "Chinese Macao" y "Tokyo Japan Chinese", y el de test "Chinese Chinese Chinese Tokyo Japan", con el mismo resultado (0,0003 contra 0,0001). Esos números redondeados dan 75/25; sin redondear, la cuenta da 69/31, que es lo que devuelve `predict_proba` (lo verifiqué en el box) C2P2 1:02:25. | [IIR, sección 13.2](https://nlp.stanford.edu/IR-book/html/htmledition/naive-bayes-text-classification-1.html) |
| Los tamaños de lote son potencias de dos por una optimización de hardware C3P2 1:30:17 | En parte | NVIDIA documenta que los Tensor Cores son más eficientes cuando las dimensiones de las matrices son múltiplos de 8 en FP16 (de 64 en A100), no potencias de dos. En el experimento de Sebastian Raschka (MobileNetV3 en CIFAR-10, una V100), entrenar con lotes de 127, 128 y 129 tardó 9,80, 9,78 y 9,92 minutos: sin diferencia práctica. Él mismo aclara que corrió cada configuración una sola vez. Es un blog, no un paper. | [NVIDIA, Matrix Multiplication Background](https://docs.nvidia.com/deeplearning/performance/dl-performance-matrix-multiplication/index.html) (leída con `curl`); [Raschka, 05/07/2022](https://sebastianraschka.com/blog/2022/batch-size-2.html) (leído con `curl`) |
| Shannon trabajaba en Bell Labs y murió en 2001 C3P2 55:42 | Sí | Claude Shannon (30/04/1916 a 24/02/2001) estuvo en Bell Labs de 1941 a 1972, donde publicó "A Mathematical Theory of Communication" (1948), y murió en Medford, Massachusetts, a los 84 años. | [MIT News, 2001](https://news.mit.edu/2001/shannon) (leído con `curl`); [Britannica](https://www.britannica.com/biography/Claude-Shannon) (leída con `curl`) |
| En California Housing, un target de 4,526 son "52.000 aproximadamente" C2P3 40:34 | No | El target es el valor mediano de la vivienda por distrito "in units of 100,000", del censo de 1990: 4,526 equivale a unos USD 452.600 de 1990. | [scikit-learn, fetch_california_housing](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.fetch_california_housing.html); [scikit-learn, datasets reales](https://scikit-learn.org/stable/datasets/real_world.html) |
| Los umbrales de los árboles se evalúan donde cambia la clase entre observaciones ordenadas C3P1 1:20:46 | En parte | scikit-learn, con `splitter="best"`, prueba todos los puntos medios entre valores distintos y ordenados de cada variable, no solo donde cambia la clase (aunque el óptimo cae en uno de esos cambios). Por eso entre 8 y 12 el umbral sale 10, como verifiqué en el apunte. | [scikit-learn, árboles de decisión](https://scikit-learn.org/stable/modules/tree.html) |
| El "pulgar arriba o abajo" del chat es el aprendizaje por refuerzo de los modelos de lenguaje C1P1 49:30 | En parte | El RLHF es una etapa de entrenamiento aparte: en InstructGPT, OpenAI juntó demostraciones de etiquetadores, después rankings de respuestas, y con eso ajustó el modelo por refuerzo. El informe de GPT-4 dice que el modelo se ajustó con RLHF. Si el pulgar del usuario alimenta entrenamientos futuros depende de cada proveedor y no lo verifiqué. Son documentos de OpenAI. | [arXiv 2203.02155 (InstructGPT)](https://arxiv.org/abs/2203.02155); [arXiv 2303.08774](https://arxiv.org/abs/2303.08774) |
| No hay autosupervisión con imágenes, "lo que conozco es que le pasás etiqueta" C1P1 44:37 | No (sí existe) | Los masked autoencoders (He y otros, 2021) son "scalable self-supervised learners for computer vision": tapan el 75% de los parches de la imagen y entrenan a reconstruirlos, sin etiquetas. Es el análogo visual del enmascaramiento de BERT que se explica en esa misma clase. | [arXiv 2111.06377](https://arxiv.org/abs/2111.06377) |
| El coeficiente de correlación de Matthews (MCC), que propone un alumno y las docentes no conocen C4P3 17:41 | Sí, existe en scikit-learn | Está como `matthews_corrcoef` en `sklearn.metrics`. Usa las cuatro celdas de la matriz de confusión, así que no se infla con la clase mayoritaria. | [scikit-learn, evaluación de modelos](https://scikit-learn.org/stable/modules/model_evaluation.html) |
| Valores por defecto de `LogisticRegression`: `penalty` deprecado, `l1_ratio = 0.0`, `tol = 1e-4` (lo que anoté en el apunte con scikit-learn 1.9.1) | En parte (depende de la versión) | La documentación estable lo confirma: `penalty` está deprecado desde la versión 1.8 y se quita en la 1.10. Pero Colab lista hoy scikit-learn 1.6.1, donde `penalty` vale `"l2"` sin aviso y `l1_ratio` vale `None`; `tol = 1e-4` es igual en las dos (lo comprobé en un entorno con 1.6.1). El listado de Colab avisa que puede no reflejar exactamente el contenedor en producción. | [scikit-learn, LogisticRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html); [googlecolab/backend-info, pip-freeze.txt](https://raw.githubusercontent.com/googlecolab/backend-info/main/pip-freeze.txt) (leído con `curl`; último commit del 02/10/2026) |
| Con dos clases "conviene elegir un K par" en KNN C2P3 6:29 | No | Es al revés: con dos clases, un K impar evita los empates en la votación. Es aritmética; no hace falta fuente. | Aritmética |
| x, x² y x³ "son ortogonales entre sí, independientes" C1P2 1:03:34 | No | Con x uniforme en [0, 1], la correlación entre x y x² es (1/12) / √((1/12)(4/45)) ≈ 0,97. La regresión polinomial es lineal porque el modelo es lineal en los coeficientes w, no porque las potencias sean independientes. | Cálculo propio |
| Clases los días 22 y 23 de mayo y 5 y 6 de junio; "nos vemos de nuevo el cinco" C2P3 55:04 | Sí | El calendario público de la cohorte 2026 da esas cuatro fechas para Introducción al Aprendizaje Automático. | [Diplodatos, calendario](https://diplodatos.famaf.unc.edu.ar/metodologia-y-modalidad-de-cursado/calendario/) |
| El práctico 1 vence el 8 de junio y el práctico 2 el 22 de junio ("ya confirmo") C2P3 37:09, C4P3 59:37 | No verificable | El calendario público no da fechas de entrega, la página de la materia tampoco, y el repositorio de GitHub sigue con el README de 2025. Confirmalas en el aula virtual; si eran esas, ya pasaron. | [Diplodatos, calendario](https://diplodatos.famaf.unc.edu.ar/metodologia-y-modalidad-de-cursado/calendario/); [página de la materia](https://diplodatos.famaf.unc.edu.ar/metodologia-y-modalidad-de-cursado/materias-obligatorias/materia-introduccion-al-aprendizaje-automatico/) |

**Lo más importante para corregir en el apunte.** Las correcciones que cambian lo que harías en el práctico 2 son cuatro: la etiqueta mide el incumplimiento (no si se dio el préstamo), la prevalencia real del archivo es 16,7% y no el 20% del encabezado, `class_weight="balanced"` pondera al revés de lo que se dijo (más peso a la clase minoritaria), y SMOTE no duplica. Para el examen conviene corregir además la lectura de la curva PR, el alcance del F1, el máximo del Gini, el FWHM, los 5.000 millones de parámetros y el origen de "regresión". Lo histórico y bibliográfico salió bien parado: Minsky y Papert, Rumelhart, Hinton y Williams, Bishop, Manning y Shannon son exactamente lo que la clase recordaba.

### 2. Nombres y dudas de la transcripción, resueltos

| En la transcripción | Resultado | Cómo lo resolví |
|---|---|---|
| Vanessa Mainardi (así la escribí en el apunte), "CONISET", "Villamaría" C1P1 0:04 | **Vanesa Beatriz Meinardi**, confirmado | Su ficha de CONICET la presenta como investigadora asistente (especialidad Estadística) en el Centro de Investigaciones y Transferencia de Villa María (CONICET y UNVM), con el tema "Machine Learning y Teoría de la Información aplicado a la búsqueda de alteraciones en ECG", licenciatura (2001 a 2007) y doctorado en Matemática (2007 a 2011) en la UNC, y se describe como "Doctora en Matemáticas (teoría de Lie), Magíster en Estadística Aplicada y especialista en Ciencia de Datos" ([CONICET](https://bicyt.conicet.gov.ar/fichas/p/vanesa-beatriz-meinardi)). La página del equipo docente de la diplomatura la lista como "Vanesa Meinardi, Dra. en Matemática" ([equipo docente](https://diplodatos.famaf.unc.edu.ar/equipo-docente/)), y el README de 2025 del repositorio la escribe "Vanesa Meinard" ([GitHub](https://github.com/DiploDatos/IntroduccionAprendizajeAutomatico)). Lo de "CONICET hace más de 12 años" coincide con un perfil de LinkedIn que dice "desde mayo de 2013", pero eso lo vi solo en resultados de búsqueda. Su tema en CONICET es ECG; un preprint de 2026 sobre EEG y epilepsia lo vi solo en resultados de búsqueda |
| Edgardo, "Edo", doctor en física, ex profesor titular de FAMAF, redes neuronales para espectros C1P1 0:58, C4P3 1:16:04 | **Edgardo Bonzi**, muy probable (no confirmado) | FAMAF lista al "Dr. Edgardo Bonzi" como integrante y subresponsable del Grupo de Espectroscopía Atómica y Nuclear, cuyas líneas incluyen "redes neuronales en el análisis y optimización de espectrometría" ([FAMAF, grupo](https://www.famaf.unc.edu.ar/investigaci%C3%B3n/%C3%A1reas-de-investigaci%C3%B3n/f%C3%ADsica-ofi/espectroscop%C3%ADa-at%C3%B3mica-y-nuclear/)), y anuncia un seminario suyo de 2021 sobre espectros de aceleradores lineales reconstruidos con redes neuronales ([FAMAF, seminario](https://www.famaf.unc.edu.ar/investigaci%C3%B3n/%C3%A1reas-de-investigaci%C3%B3n/computaci%C3%B3n-ofi/an%C3%A1lisis-y-procesamiento-de-grandes-redes-sociales-y-sem%C3%A1nticas/el-grupo-apgsys-comprometido-con-la-transferencia-tecnol%C3%B3gica/medici%C3%B3n-de-espectros-de-aceleradores-lineales-reconstruidos-a-partir-de-curvas-de-dosis-de-profundidad-porcentuales-mediante-redes-neuronales/)). Todo coincide con lo que cuenta en clase, pero ninguna página que abrí lo vincula con esta materia: no aparece en el equipo docente de la diplomatura ni en el README. Un repositorio "EdgardoBonzi/Curso-de-Redes-Neuronales-con-Python" lo vi solo en resultados de búsqueda |
| Caro, la coordinadora | **Carolina Chavero**, confirmado | "Dra. en Astronomía, Coordinadora de la Diplomatura" ([equipo docente](https://diplodatos.famaf.unc.edu.ar/equipo-docente/)) |
| Luis "Vietma", coordinador de mentorías C4P2 0:07 | **Luis Biedma**, confirmado | "Dr. en Matemática FAMAF-UNC", coordinador de mentorías ([mentorías](https://diplodatos.famaf.unc.edu.ar/metodologia-y-modalidad-de-cursado/mentorias/)) |
| Yanina "Iberra" C4P2 0:07 | **Yanina Iberra**, confirmado (la transcripción acertó) | "Data Scientist. Analista en Sistemas", coordinadora de mentorías ([mentorías](https://diplodatos.famaf.unc.edu.ar/metodologia-y-modalidad-de-cursado/mentorias/)) |
| "Jamie Kight", junto a ChatGPT y Copilot C1P2 46:45 | Probablemente **Gemini**; dudoso | Por el contexto (una lista de asistentes de IA) y por cómo suena; no hay forma de confirmarlo con una fuente |
| "el libro de Bishop", "Manning" (sin título en clase) | **Pattern Recognition and Machine Learning** e **Introduction to Information Retrieval**, confirmado | Ver la sección 1 |
| "Claus Shanon" | **Claude Shannon**, confirmado | [MIT News](https://news.mit.edu/2001/shannon) |
| Docentes en la página pública de la materia | Desactualizado | La página de la materia lista a Jorge Sánchez y Diego González Dondo ([página de la materia](https://diplodatos.famaf.unc.edu.ar/metodologia-y-modalidad-de-cursado/materias-obligatorias/materia-introduccion-al-aprendizaje-automatico/)), y el README de 2025, a Vanesa Meinardi y Diego González Dondo. Ninguno de los dos refleja la edición 2026 |
| Dataset del práctico 2, "de un banco" C4P3 1:00:27 | **HMEQ** (Home Equity), versión reducida, confirmado | Ver la sección 1 y la sección 3 |

### 3. El dataset del práctico 2: leelo antes de modelar

**Qué dice la fuente.** El práctico 2 es "armado de un esquema de aprendizaje automático": elegir un modelo, ajustar hiperparámetros y evaluar, con un dataset de clientes de un banco que tiene líneas de comentario con `#` C4P3 1:00:27. Cuando una alumna pregunta qué es la etiqueta, la respuesta es "si se le dio un préstamo o no" C4P3 1:05:11, y los metadatos están "en el archivo" y en el GitHub C4P3 1:13:28.

**Qué suma el material externo.**
- El archivo público dice que la etiqueta es el incumplimiento: "1 = client defaulted on loan - 0 = loan repaid" ([loan_data.csv](https://raw.githubusercontent.com/DiploDatos/IntroduccionAprendizajeAutomatico/master/data/loan_data.csv)).
- El encabezado también explica el contexto: el banco quiere automatizar la aprobación de líneas de crédito siguiendo la Equal Credit Opportunity Act, y "the created model must be sufficiently interpretable to provide a reason for any adverse actions (rejections)". Es un requisito de negocio que el práctico casi no explota.
- Las cifras del encabezado (5.960 filas, 20% de incumplimiento) son del HMEQ original; el archivo tiene 1.854 filas y 16,7%.

**Cómo implementarlo.** Este script lee la definición de la etiqueta, carga el archivo y separa test. Lo corrí con scikit-learn 1.9.1 y con 1.6.1:

```python
import urllib.request
import pandas as pd
from sklearn.model_selection import train_test_split

URL = "https://raw.githubusercontent.com/DiploDatos/IntroduccionAprendizajeAutomatico/master/data/loan_data.csv"

# 1. Leé los comentarios: ahí está la definición de la etiqueta
with urllib.request.urlopen(URL) as f:
    for linea in f.read().decode().splitlines():
        if linea.startswith("# TARGET"):
            print(linea)

# 2. Cargá los datos salteando las líneas con "#"
df = pd.read_csv(URL, comment="#")
print(df.shape)                               # filas y columnas
print(df.TARGET.value_counts().to_dict())     # cuántos 0 y cuántos 1
print("faltantes:", int(df.isna().sum().sum()))

# 3. Separá test una sola vez, estratificado
X, y = df.drop(columns="TARGET"), df.TARGET
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=0)
print(round(y_train.mean(), 3), round(y_test.mean(), 3))
```

Salida:

```
# TARGET  Label: 1 = client defaulted on loan - 0 = loan repaid
(1854, 11)
{0: 1545, 1: 309}
faltantes: 0
0.167 0.167
```

**Sugerencia.** Escribí en la primera celda del práctico, con tus palabras, qué es un positivo ("cliente que incumplió"), qué cuesta un falso negativo (prestarle a alguien que no va a pagar) y qué cuesta un falso positivo (rechazar a un buen cliente). Esa frase decide la métrica de la sección 5 y el umbral de la sección 4.

### 4. Desbalance: primero el umbral, después los pesos, y el remuestreo al final

**Qué dice la fuente.** La clase 4 da tres caminos para el desbalance: submuestrear la clase mayoritaria, sobremuestrear la minoritaria (SMOTE, ADASYN, aumentación de imágenes) o ponderar la función de costo C4P3 9:43, C4P3 11:41, y en la clase 2 ya se había mencionado `class_weight` C2P1 52:35. Vanesa prefiere ponderar porque no toca los datos.

**Qué suma el material externo.**
- **Los pesos son inversos a la frecuencia.** `class_weight="balanced"` usa `n_samples / (n_classes * np.bincount(y))` ([scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html)).
- **Corregir el desbalance puede empeorar las probabilidades.** Van den Goorbergh, van Smeden, Timmerman y Van Calster simularon submuestreo, sobremuestreo y SMOTE con regresión logística: ninguno mejoró el AUC, todos llevaron a "strong overestimation of the probability to belong to the minority class", y la mejora en sensibilidad y especificidad se conseguía igual moviendo el umbral. Concluyen que "outcome imbalance is not a problem in itself" ([arXiv 2202.09101](https://arxiv.org/abs/2202.09101); se publicó en JAMIA en 2022, dato que vi en resultados de búsqueda y no en la página de la revista).
- **Con clasificadores fuertes, balancear suele no ayudar.** Elor y Averbuch-Elor encontraron que balancear sirve para clasificadores débiles, pero "does not improve prediction performance for the strong ones" ([arXiv 2201.08528](https://arxiv.org/abs/2201.08528)).
- **scikit-learn ya trae el ajuste de umbral.** `TunedThresholdClassifierCV` elige el umbral con validación cruzada interna optimizando una métrica; está desde la versión 1.5 ([guía de usuario](https://scikit-learn.org/stable/modules/classification_threshold.html); [API](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TunedThresholdClassifierCV.html)).

**Cómo implementarlo.** El script compara tres versiones de la misma regresión logística sobre el test del práctico: umbral 0,5, `class_weight="balanced"` y umbral ajustado para la exactitud balanceada:

```python
import pandas as pd
from sklearn.model_selection import train_test_split, TunedThresholdClassifierCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, balanced_accuracy_score, brier_score_loss

URL = "https://raw.githubusercontent.com/DiploDatos/IntroduccionAprendizajeAutomatico/master/data/loan_data.csv"
df = pd.read_csv(URL, comment="#")
X, y = df.drop(columns="TARGET"), df.TARGET
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=0)

modelos = {
    "umbral 0,5": make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
    "class_weight balanced": make_pipeline(
        StandardScaler(), LogisticRegression(max_iter=1000, class_weight="balanced")),
    "umbral ajustado": TunedThresholdClassifierCV(
        make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
        scoring="balanced_accuracy", cv=5),
}
for nombre, m in modelos.items():
    m.fit(X_train, y_train)
    pred = m.predict(X_test)
    proba = m.predict_proba(X_test)[:, 1]
    print(f"{nombre:22s} F1={f1_score(y_test, pred):.3f} "
          f"bacc={balanced_accuracy_score(y_test, pred):.3f} "
          f"Brier={brier_score_loss(y_test, proba):.3f} "
          f"prob. media={proba.mean():.3f} (real {y_test.mean():.3f})")
print("umbral elegido:", round(modelos["umbral ajustado"].best_threshold_, 3))
```

Salida (igual en 1.9.1 y en 1.6.1):

```
umbral 0,5             F1=0.506 bacc=0.673 Brier=0.094 prob. media=0.160 (real 0.167)
class_weight balanced  F1=0.500 bacc=0.726 Brier=0.159 prob. media=0.399 (real 0.167)
umbral ajustado        F1=0.602 bacc=0.747 Brier=0.094 prob. media=0.160 (real 0.167)
umbral elegido: 0.253
```

El umbral ajustado mejora F1 y exactitud balanceada más que los pesos, y deja intactas las probabilidades. Con `class_weight="balanced"`, el modelo dice en promedio que el 40% de los clientes va a incumplir, cuando la tasa real es 16,7%: es justo la sobreestimación que describen van den Goorbergh y otros. Con validación cruzada repetida (5 × 5) sobre todo el dataset vi lo mismo: con pesos, el AUC de la regresión logística no cambia (0,790 contra 0,793), la exactitud balanceada sube de 0,648 a 0,717 y el Brier empeora de 0,101 a 0,170. En los ensambles de árboles los pesos casi no movieron el Brier (0,069 contra 0,066 en LightGBM).

Si igual querés probar SMOTE, hacelo con el `Pipeline` de imbalanced-learn, que aplica el remuestreo solo al ajustar y nunca a los datos de validación. Este lo corrí con imbalanced-learn 0.14.2, la versión que lista Colab:

```python
import pandas as pd
from imblearn.pipeline import make_pipeline          # el Pipeline de imblearn, no el de sklearn
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_validate

URL = "https://raw.githubusercontent.com/DiploDatos/IntroduccionAprendizajeAutomatico/master/data/loan_data.csv"
df = pd.read_csv(URL, comment="#")
X, y = df.drop(columns="TARGET"), df.TARGET

cv = StratifiedKFold(5, shuffle=True, random_state=0)
metricas = ["roc_auc", "average_precision", "balanced_accuracy", "neg_brier_score"]
for nombre, pasos in [("sin SMOTE", []), ("con SMOTE", [SMOTE(random_state=0)])]:
    modelo = make_pipeline(StandardScaler(), *pasos, LogisticRegression(max_iter=1000))
    r = cross_validate(modelo, X, y, cv=cv, scoring=metricas)   # SMOTE solo toca los folds de entrenamiento
    print(nombre, {m: round(float(abs(r["test_" + m].mean())), 3) for m in metricas})
```

Salida:

```
sin SMOTE {'roc_auc': 0.781, 'average_precision': 0.584, 'balanced_accuracy': 0.645, 'neg_brier_score': 0.101}
con SMOTE {'roc_auc': 0.786, 'average_precision': 0.579, 'balanced_accuracy': 0.707, 'neg_brier_score': 0.172}
```

Mismo patrón: SMOTE no cambia la capacidad de ordenar (AUC y AP casi iguales), sube la exactitud balanceada porque corre el umbral efectivo y empeora el Brier. **Sugerencia:** en el informe del práctico, mostrá las tres opciones lado a lado y justificá la elegida con la métrica que definiste en la sección 3.

### 5. Métricas: la curva PR bien leída y más de un número

**Qué dice la fuente.** La clase 4 recorre la matriz de confusión, exactitud, precisión, recall, F1, ROC y PR, y advierte que con desbalance la exactitud engaña C4P2 48:21, C4P2 44:02. Un alumno propone el MCC y queda pendiente C4P3 17:41.

**Qué suma el material externo.**
- La documentación de scikit-learn explica que un sistema con "high precision but low recall" devuelve "very few of the relevant items, but most of its predicted labels are correct", y que bajar el umbral puede subir el recall ([ejemplo Precision-Recall](https://scikit-learn.org/stable/auto_examples/model_selection/plot_precision_recall.html)).
- `average_precision_score` resume la curva PR, y con predicciones al azar vale la proporción de positivos (0,167 en el práctico), que es la línea de base contra la que tenés que comparar. La misma página advierte que interpolar linealmente la curva PR da una medida demasiado optimista ([evaluación de modelos](https://scikit-learn.org/stable/modules/model_evaluation.html)).
- `f1_score` mira solo `pos_label` en el caso binario, y `average="macro"` promedia las dos clases ([f1_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html)).

**Cómo implementarlo.** El script entrena un `HistGradientBoostingClassifier` y muestra cómo cambian precisión y recall con el umbral:

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import precision_score, recall_score, average_precision_score, matthews_corrcoef, f1_score

URL = "https://raw.githubusercontent.com/DiploDatos/IntroduccionAprendizajeAutomatico/master/data/loan_data.csv"
df = pd.read_csv(URL, comment="#")
X, y = df.drop(columns="TARGET"), df.TARGET
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=0)

m = HistGradientBoostingClassifier(random_state=0).fit(X_train, y_train)
proba = m.predict_proba(X_test)[:, 1]
print("AP (área bajo la curva PR):", round(average_precision_score(y_test, proba), 3))
for umbral in [0.2, 0.5, 0.8]:
    pred = (proba >= umbral).astype(int)
    print(f"umbral {umbral}: positivos={pred.sum():3d} "
          f"precision={precision_score(y_test, pred):.2f} recall={recall_score(y_test, pred):.2f} "
          f"F1={f1_score(y_test, pred):.2f} F1 macro={f1_score(y_test, pred, average='macro'):.2f} "
          f"MCC={matthews_corrcoef(y_test, pred):.2f}")
```

Salida con scikit-learn 1.9.1:

```
AP (área bajo la curva PR): 0.88
umbral 0.2: positivos= 52 precision=0.83 recall=0.69 F1=0.75 F1 macro=0.85 MCC=0.71
umbral 0.5: positivos= 39 precision=1.00 recall=0.63 F1=0.77 F1 macro=0.87 MCC=0.77
umbral 0.8: positivos= 29 precision=1.00 recall=0.47 F1=0.64 F1 macro=0.79 MCC=0.65
```

Con umbral alto hay menos positivos, la precisión se mantiene arriba y el recall cae: lo contrario de lo que se dijo en clase. Con scikit-learn 1.6.1 los números del boosting cambian un poco (por ejemplo, con umbral 0,5 salen 38 positivos con precisión 0,95 y recall 0,58), porque la implementación cambió entre versiones. Ojo también con el tamaño: el test tiene 371 filas y solo 62 positivos, así que un cliente más o menos mueve la precisión varios puntos; por eso conviene reportar la validación cruzada (sección 8) además del test.

### 6. Probabilidades calibradas, si las vas a usar

**Qué dice la fuente.** La materia presenta la regresión logística como un modelo que devuelve probabilidades y usa `predict_proba` en Naive Bayes C2P2 1:02:25, pero no discute si esas probabilidades son confiables.

**Qué suma el material externo.**
- Niculescu-Mizil y Caruana mostraron que los árboles con boosting empujan las probabilidades lejos de 0 y 1, que Naive Bayes las empuja hacia 0 y 1, y que después de calibrar con Platt o con regresión isotónica los árboles con boosting, los bosques aleatorios y las SVM dan las mejores probabilidades ([ICML 2005, PDF](https://www.cs.cornell.edu/~alexn/papers/calibration.icml05.crc.rev3.pdf), leído con `curl`).
- La guía de scikit-learn explica las curvas de calibración (diagramas de confiabilidad), que el Brier y la log loss miden a la vez calibración y discriminación, y cómo usar `CalibratedClassifierCV` ([calibración](https://scikit-learn.org/stable/modules/calibration.html)).

**Cómo implementarlo.**

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.metrics import brier_score_loss

URL = "https://raw.githubusercontent.com/DiploDatos/IntroduccionAprendizajeAutomatico/master/data/loan_data.csv"
df = pd.read_csv(URL, comment="#")
X, y = df.drop(columns="TARGET"), df.TARGET
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=0)

base = HistGradientBoostingClassifier(random_state=0)
calibrado = CalibratedClassifierCV(HistGradientBoostingClassifier(random_state=0),
                                   method="isotonic", cv=5)
for nombre, m in [("sin calibrar", base), ("isotónica", calibrado)]:
    proba = m.fit(X_train, y_train).predict_proba(X_test)[:, 1]
    frac_pos, prob_media = calibration_curve(y_test, proba, n_bins=5, strategy="quantile")
    print(f"{nombre:13s} Brier={brier_score_loss(y_test, proba):.3f}")
    for p, f in zip(prob_media, frac_pos):
        print(f"   predicho {p:.2f} -> observado {f:.2f}")
```

En el box (1.9.1) el Brier pasó de 0,055 a 0,052 con calibración isotónica, y en 1.6.1 de 0,057 a 0,051. Es una mejora chica y sobre un solo test de 371 filas, así que no la vendas como un resultado general. **Sugerencia:** en un problema de crédito, si vas a convertir la probabilidad en una tasa o en un límite, mirá la curva de calibración antes de usarla; si solo necesitás aprobar o rechazar, alcanza con elegir bien el umbral.

### 7. Sin fugas: Pipeline y validación cruzada anidada

**Qué dice la fuente.** La materia insiste en separar train y test antes de cualquier ajuste y en no mirar el test C1P1 50:37, explica la validación cruzada y `GridSearchCV`, y Edgardo cuenta que a veces divide en hasta cuatro conjuntos.

**Qué suma el material externo.**
- La guía de "Common pitfalls" de scikit-learn define la fuga de datos como usar información que no estaría disponible al predecir, y recomienda los pipelines para que el preprocesamiento se ajuste solo con los datos de entrenamiento de cada fold ([common pitfalls](https://scikit-learn.org/stable/common_pitfalls.html)).

**Cómo implementarlo.** El escalado va adentro del pipeline, y la búsqueda de `C` va adentro de una validación cruzada externa:

```python
import pandas as pd
from sklearn.model_selection import GridSearchCV, StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

URL = "https://raw.githubusercontent.com/DiploDatos/IntroduccionAprendizajeAutomatico/master/data/loan_data.csv"
df = pd.read_csv(URL, comment="#")
X, y = df.drop(columns="TARGET"), df.TARGET

pipe = Pipeline([("escala", StandardScaler()),
                 ("modelo", LogisticRegression(max_iter=1000))])
grilla = {"modelo__C": [0.01, 0.1, 1, 10]}
interna = StratifiedKFold(5, shuffle=True, random_state=0)
externa = StratifiedKFold(5, shuffle=True, random_state=1)

busqueda = GridSearchCV(pipe, grilla, cv=interna, scoring="average_precision")
# Validación cruzada anidada: la búsqueda se repite adentro de cada fold externo
scores = cross_val_score(busqueda, X, y, cv=externa, scoring="average_precision")
print(f"AP anidada: {scores.mean():.3f} ± {scores.std():.3f}")
busqueda.fit(X, y)
print("mejor C con todos los datos:", busqueda.best_params_)
```

Salida (igual en 1.9.1 y 1.6.1): `AP anidada: 0.592 ± 0.020` y `mejor C con todos los datos: {'modelo__C': 10}`. El 0,592 es la estimación honesta; el mejor puntaje interno de `GridSearchCV` sería optimista porque se usó para elegir `C`. **Sugerencia:** si el práctico pide reportar en test, usá la anidada para elegir entre familias de modelos y el test solo una vez, al final.

### 8. Un techo de rendimiento: ensambles de árboles junto a los clásicos

**Qué dice la fuente.** La materia ve en detalle regresión lineal y polinomial, perceptrón, regresión logística, SVM, Naive Bayes, KNN y árboles, y menciona los ensambles: bosques aleatorios y "boosted trees en secuencia sobre los errores del anterior" C3P1 1:18:29. Edgardo muestra un bosque aleatorio en el práctico sobre `make_moons` C4P1 34:24. El boosting queda para la materia siguiente, Aprendizaje Supervisado, cuyo repositorio lista XGBoost entre sus requisitos ([DiploDatos/AprendizajeSupervisado](https://github.com/DiploDatos/AprendizajeSupervisado)).

**Qué suma el material externo.** En datos tabulares, los ensambles de árboles son la referencia: Grinsztajn, Oyallon y Varoquaux muestran que "tree-based models remain state-of-the-art on medium-sized data (~10K samples)" en 45 datasets ([arXiv 2207.08815](https://arxiv.org/abs/2207.08815)), y la guía de scikit-learn dice que `HistGradientBoostingClassifier` maneja faltantes y categóricas de forma nativa y puede ser órdenes de magnitud más rápido que `GradientBoostingClassifier` con decenas de miles de filas ([ensambles](https://scikit-learn.org/stable/modules/ensemble.html)). Conflicto de interés: Varoquaux es uno de los creadores de scikit-learn.

**Cómo implementarlo: lo que medí en el box.** Corrí validación cruzada de 5 folds (semilla 0) con valores por defecto, en scikit-learn 1.9.1 y LightGBM 4.7.0, sobre 8 núcleos:

*California Housing (regresión, 20.640 filas):*

| Modelo | RMSE | R² | Tiempo |
|---|---|---|---|
| Regresión lineal (escalada) | 0,726 ± 0,012 | 0,604 ± 0,008 | menos de 0,1 s |
| Bosque aleatorio (500 árboles) | 0,501 ± 0,009 | 0,811 ± 0,007 | 30 s |
| HistGradientBoosting | 0,467 ± 0,008 | 0,836 ± 0,004 | 1,4 s |
| LightGBM | 0,465 ± 0,009 | 0,837 ± 0,005 | 0,6 s |

*Práctico 2 (clasificación, 1.854 filas, validación cruzada estratificada 5 × 5):*

| Modelo | AUC | AP | F1 | Exactitud balanceada | Brier |
|---|---|---|---|---|---|
| Regresión logística (escalada) | 0,790 ± 0,037 | 0,591 ± 0,050 | 0,444 | 0,648 | 0,101 |
| Bosque aleatorio (500 árboles) | 0,927 ± 0,019 | 0,824 ± 0,046 | 0,663 | 0,756 | 0,066 |
| HistGradientBoosting | 0,901 ± 0,023 | 0,798 ± 0,041 | 0,668 | 0,761 | 0,070 |
| LightGBM | 0,903 ± 0,022 | 0,804 ± 0,039 | 0,680 | 0,769 | 0,069 |
| LightGBM más lento (tasa 0,03, 600 árboles, submuestreo 0,8) | 0,913 ± 0,021 | 0,822 ± 0,036 | 0,691 | 0,773 | 0,070 |

En California, el boosting gana a todo y en un segundo. En el práctico, el bosque aleatorio con valores por defecto le gana al boosting con valores por defecto (0,927 contra 0,903 de AUC, una diferencia de alrededor de un desvío), y el boosting se acerca solo cuando lo hacés más lento. Lo robusto no es "boosting siempre", sino "un ensamble de árboles le saca mucha ventaja al modelo lineal en estos datos". Los tiempos son de un solo intento y dependen de la máquina. El script completo es corto: `cross_validate` con los cuatro modelos y `scoring` con varias métricas.

### 9. Versiones: lo que corre en Colab hoy

**Qué dice la fuente.** Las notebooks corren en Colab y montan Google Drive C1P1 2:18. Edgardo muestra valores por defecto de `LogisticRegression` en clase C2P1 1:07:30, y en el apunte los chequeé con scikit-learn 1.9.1.

**Qué suma el material externo.** El repositorio público googlecolab/backend-info, con un commit del 02/10/2026, lista Python 3.13.15, scikit-learn 1.6.1, pandas 2.2.3, NumPy 2.1.3, SciPy 1.16.3, LightGBM 4.6.0, XGBoost 3.4.1 e imbalanced-learn 0.14.2 ([pip-freeze.txt](https://raw.githubusercontent.com/googlecolab/backend-info/main/pip-freeze.txt), leído con `curl`). El propio archivo advierte que puede no reflejar exactamente el contenedor en producción. La documentación estable de scikit-learn (1.9.1) marca `penalty` como deprecado desde 1.8 ([LogisticRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html)).

**Cómo implementarlo.** Poné esto en la primera celda y escribí código que sirva en las dos versiones: no pases `penalty`, usá `C` para regularizar (L2 es el valor por defecto en ambas), y si necesitás L1, consultá la documentación de tu versión.

```python
import sys, sklearn, pandas, numpy
print(sys.version.split()[0], sklearn.__version__, pandas.__version__, numpy.__version__)
```

Todos los scripts de este archivo corrieron sin cambios en las dos versiones. En el entorno con 1.6.1 apareció un aviso `OptimizeWarning` de SciPy, porque ahí instalé SciPy 1.18.1 en lugar de la 1.16.3 de Colab; no afecta los resultados.

---

## Críticas y límites

1. **Muchos algoritmos, poco tiempo para el práctico real.** En cuatro encuentros la materia recorre regresión, perceptrón, logística, SVM, Naive Bayes, KNN, árboles, métricas y validación. Es una base sólida, pero el práctico 2 pide un esquema completo (selección, ajuste, evaluación) sobre un dataset desbalanceado, y los temas que más pesan ahí (umbral, calibración, fugas, validación anidada) aparecen al final y rápido. Las secciones 4 a 7 cubren ese hueco.
2. **El desbalance se enseña con herramientas que la evidencia cuestiona.** La clase presenta el remuestreo y los pesos como las soluciones, con dos descripciones equivocadas (SMOTE y `class_weight`), y no menciona que mover el umbral consigue lo mismo sin deformar las probabilidades. Van den Goorbergh y otros, y Elor y Averbuch-Elor, sugieren empezar por el umbral.
3. **Errores de detalle que se repiten en temas de evaluación.** La curva PR descrita al revés, el F1 como métrica "de las dos clases", el Gini "de 0 a 1" y el KNN con K par son errores chicos uno por uno, pero caen justo en lo que el práctico evalúa. Conviene que las diapositivas lleven la definición escrita de cada métrica.
4. **La etiqueta del práctico, mal explicada.** Decir que `TARGET` es "si se le dio un préstamo" cambia la interpretación de todo el trabajo, y el encabezado del archivo, que lo aclara, describe cifras de otro dataset (5.960 filas y 20%). Es un problema del material, no solo de la clase.
5. **Sin ensambles fuertes en la práctica de la materia.** Se mencionan los bosques aleatorios y el boosting, pero el práctico no exige un modelo de referencia fuerte. Sin ese techo, un estudiante puede quedarse con una logística de AUC 0,79 sin saber que un bosque llega a 0,93 en los mismos datos.
6. **Versiones y reproducibilidad.** Lo que se dice en clase sobre valores por defecto depende de la versión de scikit-learn, y Colab (1.6.1) no coincide con la documentación estable (1.9.1). La materia no pide fijar ni reportar versiones.
7. **Conflictos de interés que conviene tener presentes.** Del lado de las fuentes externas: los informes de GPT-3, GPT-4 e InstructGPT son de OpenAI; Varoquaux, coautor del estudio que favorece a los árboles, es uno de los creadores de scikit-learn; AutoGluon y TabArena los firman autores de AutoGluon (Amazon), TabArena también lleva la firma de Frank Hutter, y el paper de TabPFN declara que dos autores están afiliados a Prior Labs, la empresa que comercializa el modelo. El blog de Raschka es la opinión y el experimento de una persona.
8. **Límites de esta revisión.**
    - La página de MIT Press de "Perceptrons" devolvió "Access Denied"; confirmé el libro por la lista de referencias de Nature.
    - La página de TabPFN en Nature devolvió error (por límite de pedidos); leí el artículo completo por la API de Europe PMC (PMC11711098).
    - Leí con `curl` el PDF de Galton, el de Bishop, el de Niculescu-Mizil y Caruana, la guía de NVIDIA, el blog de Raschka, MIT News, Britannica, Wikipedia, MathWorld, el archivo del práctico y el listado de Colab.
    - Vi solo en resultados de búsqueda: la publicación de van den Goorbergh y otros en JAMIA, el perfil de LinkedIn de Vanesa Meinardi, su preprint de 2026 sobre EEG y el repositorio de cursos de Edgardo Bonzi.
    - De los papers (SMOTE, van den Goorbergh, Elor, Grinsztajn, Shwartz-Ziv, McElfresh, TabArena, AutoGluon, FLAML, MAE, InstructGPT) leí el resumen, no el texto completo; de TabPFN leí además la declaración de intereses y los métodos.
    - No abrí la página de Kaggle del HMEQ; lo que digo del HMEQ original sale del encabezado del archivo.
    - El apellido de Edgardo sigue sin confirmar: ninguna página que abrí lo vincula con la materia.
    - No corrí TabPFN ni AutoGluon (ver el análisis adversario).

---

## Análisis adversario

> Cómo leer esta sección: pongo el enfoque de la materia contra la alternativa más fuerte que encontré, presentada en su mejor versión. La idea no es desarmar la materia, sino ver en qué contextos conviene y en cuáles no. Solo cito fuentes que abrí el 02/10/2026, y los números del box los medí ese día.

**La tesis, en dos oraciones.** La materia sostiene que para hacer aprendizaje supervisado bien hay que entender desde los principios una serie de algoritmos clásicos (regresión, perceptrón, logística, SVM, Naive Bayes, KNN, árboles) junto con las ideas que los atraviesan (función de costo, sobreajuste, regularización, validación, métricas), y practicarlos en notebooks con scikit-learn. Con esa base, el estudiante arma en el práctico 2 su propio esquema de selección, ajuste y evaluación de modelos C4P3 1:00:27.

### La alternativa más fuerte: ensambles de árboles con boosting como modelo por defecto

**Qué propone.** Para datos tabulares, empezar por un ensamble de árboles con gradient boosting (XGBoost, LightGBM, CatBoost o `HistGradientBoostingClassifier`) como modelo por defecto, y dedicar el tiempo a lo que más rinde: definir bien la etiqueta, validar sin fugas, ajustar unos pocos hiperparámetros, elegir el umbral y calibrar. Los modelos clásicos se aprenden después y en la medida en que hagan falta (como línea de base, por interpretabilidad o para entender una idea). La versión seria no dice "la teoría no importa"; dice "en tabular, el modelo que casi siempre vas a usar es un ensamble de árboles, así que aprendé a usarlo bien primero".

**Qué dice el curso sobre esta alternativa.** No la descarta: menciona los bosques aleatorios y el boosting C3P1 1:18:29, muestra un bosque en el práctico C4P1 34:24 y deja el boosting para la materia siguiente, cuyo repositorio pide XGBoost ([DiploDatos/AprendizajeSupervisado](https://github.com/DiploDatos/AprendizajeSupervisado)). Es decir, el orden de la diplomatura es "clásicos primero, ensambles después", que es justamente lo que la alternativa invierte.

**Por qué elegí esta.** Es la que tiene más evidencia independiente y más años de uso, corre en cualquier notebook de Colab sin GPU ni cuentas, y discute la premisa de la materia (que conviene recorrer muchos algoritmos antes de usar el que vas a terminar usando). Otras alternativas que consideré:
- **AutoML (AutoGluon, FLAML).** AutoGluon-Tabular apila y ensambla muchos modelos con una línea de Python, y en su evaluación fue "faster, more robust, and much more accurate" que otros AutoML, y le ganó al 99% de los participantes en dos competencias de Kaggle tras 4 horas de entrenamiento ([arXiv 2003.06505](https://arxiv.org/abs/2003.06505)). FLAML busca modelos con poco cómputo y dice superar a los AutoML más conocidos con presupuestos iguales o menores ([arXiv 1911.04706](https://arxiv.org/abs/1911.04706); [documentación](https://microsoft.github.io/FLAML/)). No la elegí porque esconde exactamente lo que el práctico quiere enseñar (selección y ajuste), y su evidencia la firman sus propios autores.
- **Modelos fundacionales tabulares (TabPFN).** Es la candidata más interesante para un dataset como el del práctico (1.854 filas y 10 variables). El paper en Nature dice que TabPFN supera a todos los métodos previos en datasets de hasta 10.000 muestras y que "in 2.8 s, TabPFN outperforms an ensemble of the strongest baselines tuned for 4 h" en clasificación ([Hollmann y otros, Nature 637, 319 a 326, 2025](https://www.nature.com/articles/s41586-024-08328-6), leído por Europe PMC), y el benchmark más grande de McElfresh y otros la señala como "a remarkable exception" que gana en promedio aunque esté limitada a 3.000 filas de entrenamiento ([arXiv 2305.02997](https://arxiv.org/abs/2305.02997)). No la elegí como alternativa principal por tres razones: dos autores del paper de Nature están afiliados a Prior Labs, que comercializa el modelo; el README actual dice que los pesos por defecto (TabPFN-3.5) tienen licencia no comercial y piden crear una cuenta y aceptar la licencia, y que en CPU solo admite datasets moderados ([README de TabPFN](https://raw.githubusercontent.com/PriorLabs/TabPFN/main/README.md), leído con `curl`); y es la opción menos madura. Por eso no la corrí en el box.

### La alternativa en su mejor versión

**Quién la defiende y qué dice.**
- **Shwartz-Ziv y Armon** compararon modelos profundos para tabular contra XGBoost, incluso en los datasets de los papers que proponían esos modelos, y concluyeron que "XGBoost outperforms these deep models" y "requires much less tuning" ([arXiv 2106.03253](https://arxiv.org/abs/2106.03253)).
- **Grinsztajn, Oyallon y Varoquaux**, con 45 datasets y una búsqueda de hiperparámetros de 20.000 horas de cómputo por modelo, encontraron que los modelos basados en árboles siguen siendo el estado del arte en datos medianos, "even without accounting for their superior speed" ([arXiv 2207.08815](https://arxiv.org/abs/2207.08815)).
- **McElfresh y otros**, con 19 algoritmos y 176 datasets, dicen que el debate redes contra árboles está sobredimensionado y que muchas veces "light hyperparameter tuning on a GBDT is more important than choosing between NNs and GBDTs" ([arXiv 2305.02997](https://arxiv.org/abs/2305.02997)).
- **TabArena** (2025), un benchmark que se mantiene actualizado, concluye que "gradient-boosted trees are still strong contenders on practical tabular datasets" ([arXiv 2506.16791](https://arxiv.org/abs/2506.16791)).

**Qué evidencia la respalda.**
- **En el box, en regresión.** En California Housing, LightGBM con valores por defecto llega a un R² de 0,837 en 0,6 segundos, contra 0,604 de la regresión lineal y 0,811 de un bosque de 500 árboles que tarda 30 segundos (sección 8).
- **Menos decisiones.** `HistGradientBoostingClassifier` acepta faltantes y categóricas sin preprocesamiento ([scikit-learn, ensambles](https://scikit-learn.org/stable/modules/ensemble.html)), lo que elimina pasos donde suelen aparecer las fugas.
- **Más tiempo para lo importante.** Si el modelo por defecto ya es bueno, las horas del práctico van a la etiqueta, al umbral y a la calibración, que en la sección 4 movieron la exactitud balanceada de 0,673 a 0,747 sin cambiar de modelo.

**Qué evidencia la contradice.**
- **En el práctico, con valores por defecto, ganó el bosque aleatorio.** AUC 0,927 contra 0,903 de LightGBM y 0,901 de `HistGradientBoosting`; el boosting solo se acercó (0,913) cuando lo hice más lento a mano. "Boosting primero" no es automático: en datos chicos hay que ajustarlo.
- **Los propios benchmarks matizan.** TabArena dice que el aprendizaje profundo "caught up under larger time budgets with ensembling" y que "foundation models excel on smaller datasets", y McElfresh y otros encuentran que TabPFN gana en promedio en datasets chicos.
- **Probabilidades.** Niculescu-Mizil y Caruana muestran que el boosting distorsiona las probabilidades y necesita calibración ([ICML 2005](https://www.cs.cornell.edu/~alexn/papers/calibration.icml05.crc.rev3.pdf)).
- **Interpretabilidad.** El propio encabezado del dataset pide un modelo que justifique cada rechazo. Un ensamble de cientos de árboles necesita herramientas de explicación aparte; una logística o un árbol chico se explican solos.

### Comparación directa

| Criterio | A: muchos clásicos desde los principios (la materia) | B: boosting como modelo por defecto |
|---|---|---|
| Costo | Bajo: scikit-learn y Colab, sin GPU. | Bajo: LightGBM, XGBoost y `HistGradientBoosting` son gratuitos y vienen en Colab. |
| — | Media: muchos modelos, cada uno con sus supuestos e hiperparámetros, pero cada uno es simple. | Baja para empezar (un solo modelo) y media para ajustarlo bien (tasa de aprendizaje, número de árboles, hojas, submuestreo). |
| Tiempo hasta obtener valor | Semanas: el práctico llega después de cuatro encuentros; el primer modelo útil depende de elegir bien entre muchos. | Horas: un modelo fuerte con valores por defecto en minutos (0,6 s en California). |
| Riesgo | Quedarse con un modelo flojo sin saberlo (logística con AUC 0,79 en el práctico); errores de concepto en métricas. | Usarlo como caja negra; probabilidades mal calibradas; sobreajuste si se ajustan muchos hiperparámetros con pocos datos; menos interpretable para justificar rechazos. |
| Madurez | Métodos de décadas, en todos los libros de texto. | Herramientas maduras (XGBoost, LightGBM, `HistGradientBoosting`), estándar en la industria y en competencias. |
| Evidencia disponible | Pedagógica y de libro de texto (Bishop, ISLP); no encontré estudios que comparen órdenes de enseñanza. | Varios benchmarks grandes e independientes entre sí a favor en tabular (Shwartz-Ziv y Armon, Grinsztajn y otros, McElfresh y otros, TabArena), con matices para datasets chicos; mis números del box la apoyan en regresión y la matizan en el práctico. |
| Tipo de equipo/contexto | Estudiantes que necesitan entender por qué un modelo sobreajusta, cursos introductorios, problemas donde la interpretabilidad manda (crédito regulado, salud). | Equipos que entregan modelos tabulares con plazos, datasets medianos a grandes, competencias, problemas donde manda el rendimiento. |

### Dónde gana la alternativa

- **Rendimiento por unidad de esfuerzo.** En tabular mediano o grande, un boosting con valores por defecto deja muy atrás a los modelos lineales, y lo hace en segundos.
- **Menos preprocesamiento.** Faltantes y categóricas nativas significan menos código y menos lugares para filtrar información.
- **Lo que vas a usar en el trabajo.** Si tu primer trabajo es con datos tabulares, el modelo que más vas a ver es un ensamble de árboles.

### Dónde pierde

- **Para aprender.** Las ideas de la materia (función de costo, regularización, sobreajuste, geometría de un clasificador lineal) son las que te permiten entender por qué el boosting funciona y cuándo falla. Empezar por la caja negra las saltea.
- **En datos chicos.** En el práctico 2, el bosque aleatorio le ganó al boosting con valores por defecto, y la literatura reciente dice que ahí los modelos fundacionales pueden ser mejores.
- **Cuando hay que justificar cada decisión.** El encabezado del dataset pide explicar los rechazos; una logística con AUC 0,79 explicable puede ser preferible a un ensamble con 0,93 si el regulador lo exige, o al menos obliga a sumar herramientas de explicación.
- **Probabilidades.** Si vas a usar la probabilidad (tasa, límite de crédito), el boosting necesita calibración, cosa que la logística sin pesos ya da razonablemente bien (Brier 0,094 en el test de la sección 4).

### Cómo decidir

**Elegí A (muchos clásicos desde los principios, la materia) si** estás aprendiendo o cursando el práctico, necesitás entender por qué un modelo sobreajusta o qué hace la regularización, el problema exige explicar cada decisión (crédito regulado, salud, sector público), o el dataset es chico y querés comparar con criterio en vez de confiar en un valor por defecto.

**Elegí B (boosting como modelo por defecto) si** tenés que entregar un modelo tabular con buen rendimiento en poco tiempo, el dataset es mediano o grande (miles a millones de filas) y tiene faltantes o categóricas, ya tenés una línea de base simple contra la que comparar, y podés dedicar tiempo a calibrar y a explicar el modelo con herramientas aparte.

**Un híbrido posible (sugerencia).**
1. Empezá como la materia: definí la etiqueta y el costo de cada error (sección 3), separá test estratificado y armá un `Pipeline`.
2. Entrená tres modelos con la misma validación cruzada: una línea de base trivial (`DummyClassifier`), una regresión logística y un ensamble de árboles (bosque aleatorio y `HistGradientBoosting`). El ensamble es tu techo.
3. Si la logística queda cerca del techo, quedate con ella: es explicable y está mejor calibrada. Si queda lejos (como en el práctico, 0,79 contra 0,93 de AUC), usá el ensamble y sumá calibración (sección 6) y una explicación de variables, como la importancia por permutación.
4. Ajustá el umbral con `TunedThresholdClassifierCV` en vez de remuestrear (sección 4), y reportá AP, exactitud balanceada, F1 macro, MCC y Brier (sección 5).
5. Usá validación cruzada anidada para elegir la familia de modelo y el test una sola vez (sección 7).
6. Si tenés tiempo, GPU y una licencia que te sirva, probá TabPFN o AutoGluon solo como control del techo, no como punto de partida, y tené presente quién publica cada benchmark.

**Veredicto.** Para el práctico 2 y para quien está aprendiendo, el enfoque de la materia es el punto de partida correcto: las ideas que enseña son las que permiten usar bien cualquier modelo, y el dataset mismo pide interpretabilidad. Pero la evidencia (cuatro benchmarks grandes y mis números del box) dice que en tabular un ensamble de árboles es el techo que no podés dejar de medir, y que el remuestreo rinde menos que elegir bien el umbral. Lo más sensato es el híbrido: clásicos para entender y como línea de base explicable, un ensamble de árboles siempre como referencia, y el esfuerzo puesto en la etiqueta, el umbral, la calibración y la validación sin fugas.

---

## Material para seguir

**Libros gratuitos**
- [An Introduction to Statistical Learning (ISLR e ISLP)](https://www.statlearning.com/): el mejor compañero de la materia, con laboratorios en R o en Python al final de cada capítulo (la edición en Python es de 2023).
- [The Elements of Statistical Learning (Hastie, Tibshirani y Friedman)](https://hastie.su.domains/ElemStatLearn/): la versión avanzada de ISLR, con el PDF completo de la duodécima reimpresión corregida (enero de 2017) en la página.
- [Pattern Recognition and Machine Learning (Bishop)](https://www.microsoft.com/en-us/research/publication/pattern-recognition-machine-learning/): de acá salen las figuras del sobreajuste polinómico de la clase 1; Microsoft Research ofrece el PDF completo.
- [Probabilistic Machine Learning: An Introduction (Murphy)](https://probml.github.io/pml-book/book1.html): la visión probabilística moderna, con borrador en PDF (licencia CC BY-NC-ND, versión del 18/04/2025) y código para las figuras.
- [Introduction to Information Retrieval, capítulo 13](https://nlp.stanford.edu/IR-book/html/htmledition/naive-bayes-text-classification-1.html): Naive Bayes para texto con el ejemplo China/Japón de la clase 2, gratis en línea.

**Cursos**
- [Machine Learning Specialization, de Andrew Ng (Coursera)](https://www.coursera.org/specializations/machine-learning-introduction): tres cursos introductorios que repasan regresión, logística, árboles y buenas prácticas; se puede cursar gratis (Coursera y DeepLearning.AI venden la certificación).
- [Machine Learning Crash Course, de Google](https://developers.google.com/machine-learning/crash-course): videos, visualizaciones interactivas y ejercicios cortos; ideal para repasar métricas y umbrales.
- [Kaggle Learn](https://www.kaggle.com/learn): cursos sin costo y muy prácticos; "Intro to Machine Learning" e "Intermediate Machine Learning" cubren pipelines, fugas y validación con notebooks listas para correr (lo leí con `curl`; la página necesita JavaScript).

**scikit-learn e imbalanced-learn**
- [Guía de evaluación de modelos](https://scikit-learn.org/stable/modules/model_evaluation.html): todas las métricas del práctico, con sus definiciones exactas y los nombres para `scoring`.
- [Common pitfalls and recommended practices](https://scikit-learn.org/stable/common_pitfalls.html): fugas de datos, preprocesamiento inconsistente y aleatoriedad; leelo antes de entregar.
- [Ajuste del umbral de decisión](https://scikit-learn.org/stable/modules/classification_threshold.html): cómo usar `TunedThresholdClassifierCV`, la alternativa al remuestreo.
- [Calibración de probabilidades](https://scikit-learn.org/stable/modules/calibration.html): curvas de calibración, Brier y `CalibratedClassifierCV`.
- [Choosing the right estimator](https://scikit-learn.org/stable/machine_learning_map.html): el mapa clásico de qué estimador probar según el problema y la cantidad de datos.
- [imbalanced-learn, sobremuestreo](https://imbalanced-learn.org/stable/over_sampling.html): cómo funcionan SMOTE y ADASYN, y cómo meterlos en un pipeline sin fugas.

**Papers sobre desbalance y calibración**
- [Van den Goorbergh y otros (2022), "The harm of class imbalance corrections for risk prediction models"](https://arxiv.org/abs/2202.09101): por qué remuestrear empeora la calibración sin mejorar el AUC.
- [Elor y Averbuch-Elor (2022), "To SMOTE, or not to SMOTE?"](https://arxiv.org/abs/2201.08528): balancear ayuda a clasificadores débiles, no a los fuertes.
- [Chawla y otros (2002), SMOTE](https://arxiv.org/abs/1106.1813): el paper original, para saber qué hace de verdad.
- [Niculescu-Mizil y Caruana (2005), "Predicting Good Probabilities With Supervised Learning"](https://www.cs.cornell.edu/~alexn/papers/calibration.icml05.crc.rev3.pdf): qué modelos dan probabilidades confiables y cómo calibrar los que no.

**Papers sobre modelos para datos tabulares**
- [Grinsztajn, Oyallon y Varoquaux (2022)](https://arxiv.org/abs/2207.08815): por qué los árboles siguen ganando en tabular (coautor de scikit-learn).
- [Shwartz-Ziv y Armon (2021)](https://arxiv.org/abs/2106.03253): XGBoost contra modelos profundos, con menos ajuste.
- [McElfresh y otros (2023)](https://arxiv.org/abs/2305.02997): el benchmark más amplio, que relativiza el debate y destaca a TabPFN en datos chicos.
- [TabArena (2025)](https://arxiv.org/abs/2506.16791): un benchmark vivo, para ver el estado actual (firmado en parte por autores de AutoGluon y de TabPFN).
- [Hollmann y otros (2025), TabPFN, en Nature](https://www.nature.com/articles/s41586-024-08328-6): el modelo fundacional tabular, con conflicto de interés declarado (Prior Labs).

**Historia, para citar bien**
- [Galton (1886)](https://www.york.ac.uk/depts/maths/histstat/galton_reg.pdf): el origen de la palabra "regresión".
- [Rumelhart, Hinton y Williams (1986)](https://www.nature.com/articles/323533a0): la retropropagación que reactivó las redes después de "Perceptrons".
