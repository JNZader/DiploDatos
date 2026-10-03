# Segunda parte: "Aprendizaje Supervisado", con material externo

**Esta es la continuación de** `aprendizaje-supervisado-apunte-de-estudio.md` y `aprendizaje-supervisado-guia-de-implementacion.md` (las clases de la materia Aprendizaje Supervisado de la diplomatura en ciencia de datos de FAMAF UNC, cohorte 2026, dictadas por Karim Nemer y Diego Gonzalez Dondo en cuatro encuentros: 26 y 27 de junio y 3 y 4 de julio de 2026). Esos archivos resumen lo que dice la materia. Esta segunda parte suma material externo para verificar lo que en el apunte quedó "para verificar" o "dudoso", respaldar con fuentes las correcciones que ya marqué, resolver con el repositorio público del curso lo que en la primera parte no pude ver (notebooks, `mlutils`, datos del práctico), medir con los datos reales del práctico cuánto rinde cada modelo y marcar dónde el enfoque de la materia tiene límites. Revisé todo el 02/10/2026. Solo cito páginas que abrí; cuando una página no cargó en el lector web y la leí con `curl` desde el box, lo digo, y cuando solo vi un resultado de búsqueda, también.

> Cómo leer esto: cuando digo "la materia" o "los docentes" me refiero a lo que dicen Karim y Diego en las clases. Las marcas de tiempo usan la etiqueta de cada grabación del apunte (C1P1 es la clase 1, parte 1, y así hasta C4P2) y llevan al minuto exacto en la grabación; las de C4P2 salen de una transcripción automática hecha con faster-whisper y son menos fieles. Cuando digo "sugerencia" es una idea mía que combina fuentes, no algo que diga una fuente puntual. Todo el código lo corrí en el box el 02/10/2026 con scikit-learn 1.9.1, XGBoost 3.4.1, Keras 3.15.1 (con PyTorch de motor), transformers 5.18 y scikit-surprise 1.1.5, sobre los archivos que la diplomatura publica en su GitHub (DiploDatos/AprendizajeSupervisado, último cambio del 15/07/2026). Ojo: el README de la carpeta de teoría todavía dice "Aprendizaje Supervisado 2025", así que algunas notebooks pueden ser las del año pasado. Marco los conflictos de interés donde importan: varias documentaciones y cursos los escriben los autores o las empresas de la herramienta que recomiendan (XGBoost, Hugging Face, fast.ai, CLIP de OpenAI, el playbook de Google, TabPFN de Prior Labs), y el paper de XGBoost lo firman sus creadores.

---

## Checklist actualizado (curso + mejoras)

1. Bajá los datos del práctico del repo público DiploDatos/AprendizajeSupervisado (carpeta `Práctico`): train con 1.884 filas, test con 524 y `sample_submission.csv`; el link de la competencia de Kaggle está en el aula virtual.
2. Leé el train con `sep=";"` y el test con coma: los dos archivos usan separadores distintos, y las columnas se llaman `id` y `clase` en minúscula aunque el README diga `Id` y `Clase`.
3. Codificá la clase como el baseline oficial, 1 = con barbijo (`ccb`) y 0 = sin barbijo (`csb`), y enviá el CSV con esa misma codificación; mi guía de la primera parte decía lo contrario y estaba mal.
4. Tené en cuenta que el train está desbalanceado (1.436 con barbijo y 448 sin), así que un modelo que siempre dice "con barbijo" tiene 0,76 de accuracy y 0,50 de accuracy balanceada, que es la métrica de la competencia.
5. Escalá con un `Pipeline` que aprenda la escala solo con el train y la aplique al test; no copies el baseline, que ajusta un `StandardScaler` nuevo sobre el test.
6. Empezá por una regresión logística o una SVM lineal con `class_weight="balanced"` y regularización fuerte (C chico): en mi validación cruzada dan 0,986 y 0,987 de accuracy balanceada, contra 0,935 del árbol del baseline.
7. Para los otros dos modelos que pide la consigna, probá una SVM con kernel RBF (0,982), vecinos más cercanos (0,973) o random forest (0,963), y un voto blando si querés combinar.
8. No pierdas tiempo con `bb_width`, `bb_height` y `ch_RGB`: con o sin ellas el resultado es el mismo, la señal está en el vector de la ResNet.
9. Elegí entre modelos con validación cruzada repetida y no con la tabla pública de Kaggle, que usa una parte chica del test; diferencias de menos de un punto entre modelos están dentro del ruido.
10. Confirmá en el aula virtual o en Kaggle, ya logueado, la fecha de cierre, el límite de envíos por día y el reparto entre tabla pública y privada: no están en el repo ni en ninguna página pública.
11. Si necesitás probabilidades de una SVM (por ejemplo, para un voto blando), usá `CalibratedClassifierCV(SVC(), ensemble=False)`; en scikit-learn 1.9 `probability=True` ya avisa que se quita en la 1.11, aunque en el scikit-learn 1.6.1 de Colab todavía anda.
12. Recordá que `class_weight="balanced"` pone pesos inversos a la frecuencia, n_muestras / (n_clases · n_clase): en el práctico, 2,10 para sin barbijo y 0,66 para con barbijo.
13. Recordá que F1 es la media armónica de precisión y recall, y que en la matriz de confusión de scikit-learn las filas son la clase real.
14. Para data augmentation en Keras 3 usá capas `RandomRotation`, `RandomTranslation` y `RandomZoom` dentro del modelo; `ImageDataGenerator` está obsoleto y solo sobrevive en el espacio de compatibilidad `tf.keras` (anda en Colab, pero no lo uses en código nuevo).
15. Guardá los modelos de Keras 3 con extensión `.keras` y usá `model.export()` si necesitás un SavedModel para servir.
16. No esperes que `pip install transformers` te instale PyTorch: usá `pip install "transformers[torch]"` fuera de Colab.
17. En Book-Crossing sacá los ceros antes de usar Surprise (son interacciones implícitas, no notas): con ceros el RMSE de `BaselineOnly` da 3,38 y sin ceros 1,55, y compará siempre contra el desvío de las notas (1,74).
18. Si querés usar los ceros, tratalos como retroalimentación implícita con la librería `implicit` y medí con precisión en los primeros k: en mi prueba, ALS da 0,077 contra 0,030 de recomendar los más populares.
19. Para datos tabulares heterogéneos empezá por boosting (XGBoost, LightGBM, CatBoost o `HistGradientBoostingClassifier`); para vectores densos de una red, empezá por modelos lineales.
20. Si el problema es de imágenes o texto y tenés pocas etiquetas, probá primero un modelo preentrenado más una cabeza lineal: en mi análogo con CIFAR-10, CLIP sin ninguna etiqueta iguala a la ResNet101 con 1.800.
21. Seguí la receta de Karpathy y del playbook de Google: mirá los datos, armá una base tonta, reusá un modelo que ya funciona y cambiá de a una cosa por vez.
22. Cuando cites historia, citá bien: Samuel 1959 y Mitchell 1997 (la definición con E, T y P), Ho 1995 y Breiman 2001 (random forest), Freund y Schapire 1995 y 1997 (AdaBoost), Chen y Guestrin 2016 (XGBoost, famoso desde la competencia Higgs de 2014), AlexNet 2012, ResNet 2015, Transformer 2017 y DeepFace 2014 (97,35% en LFW, sin superar al humano).

---

## Versión completa

### 1. Los datos del curso, verificados

Los docentes avisan varias veces que algunas cosas las cuentan de memoria. Las revisé y las ordené de la corrección que más cambia el práctico a la que menos. "Sí" quiere decir que la fuente lo confirma, "En parte" que es correcto con matices importantes, "No" que la fuente lo contradice, "Desactualizado" que fue cierto pero ya no lo es, y "No verificable" que no encontré una fuente primaria que lo confirme o lo niegue. Dos filas corrigen a mi propia guía de la primera parte, y lo digo en cada una.

| Afirmación | Resultado | Matiz | Fuente |
|---|---|---|---|
| Mi guía: "codificá la clase al revés, el TP quiere detectar a quien no tiene barbijo, así que esa es la clase 1" (por lo que dice Diego en C4P2 1:48:02) | No (corrijo mi guía) | El baseline oficial dice "queremos que sea **1**:**ccb** y **0**:**csb**", o sea 1 = cara **con** barbijo, y el `sample_submission.csv` trae la columna `clase` con 0 y 1. La accuracy balanceada da lo mismo con cualquier codificación mientras entrenes y envíes con la misma; lo que no podés hacer es entrenar con 1 = sin barbijo y subir el CSV como si 1 fuera con barbijo. | [baseline.ipynb del repo](https://github.com/DiploDatos/AprendizajeSupervisado/blob/master/Pr%C3%A1ctico/baseline.ipynb), lo cloné con git |
| "438 imágenes para testeo... 1800 para entrenamiento... para testeo 524" C4P2 1:46:34, y el CSV con exactamente 524 filas C4P2 2:00:13 | En parte | El train tiene **1.884** filas y el test **524**. El 438 es la cantidad de **columnas**: `id`, `clase`, `bb_width`, `bb_height`, `ch_RGB` y 433 características de la ResNet (sus nombres, como "1097" o "595", son índices de las 2.048 salidas originales; el "Drop" del nombre del archivo sugiere que se descartaron las demás). El train trae 1.436 caras con barbijo y 448 sin (24% de la clase minoritaria). | CSV del repo, contado en el box |
| El README: "1 261 caras con protectores buconasal y 993 caras sin ellos" | No coincide con los CSV | Train más test suman 2.408 filas, no 2.254, y solo en el train ya hay 1.436 con barbijo. Puede ser la descripción de otra versión del dataset. Para tu informe usá los números de los CSV. | [README del práctico](https://github.com/DiploDatos/AprendizajeSupervisado/blob/master/Pr%C3%A1ctico/README.md) |
| El baseline sale de "un árbol de clasificación, random forest creo que era" C4P2 1:40:34 y "un árbol sin configurar" C4P2 1:57:05 | Sí, es un árbol | Es un `DecisionTreeClassifier` con una grilla de `GridSearchCV` (criterio, divisor, hojas mínimas, profundidad 5, 10 o 20). En mi validación cruzada da 0,937 de accuracy balanceada; el árbol por defecto, 0,935. | baseline.ipynb del repo; números de la sección 4 |
| La métrica es la accuracy balanceada C4P2 1:41:20 | Sí | El README lo dice ("La métrica a optimizar será el balanced accuracy score") y scikit-learn la define como "the average of recall obtained on each class", pensada para clases desbalanceadas. | README del práctico; [balanced_accuracy_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.balanced_accuracy_score.html) |
| Fechas: "comienza en media hora y termina en 18 días" C4P2 1:54:06; 27 de julio en C1P1 2:12:28 | No verificable | El README no trae fechas ni límite de envíos, y dice que "el link está disponible en la UV de la materia". No encontré la competencia en buscadores (los resultados de "barbijo" en Kaggle son de otras competencias). Confirmá cierre, límite diario y reparto público/privado en el aula virtual o en la página de la competencia, ya logueado. | README del práctico; búsqueda web |
| Límite de envíos por día C4P2 1:58:31 y tabla pública del 26% C4P2 1:57:50 | No verificable | Mismo motivo. | |
| `ImageDataGenerator` para data augmentation C2P2 1:36:05; mi apunte: "En Keras 3.15.1 ya no existe" | En parte (corrijo mi apunte) | Está marcado "DEPRECATED" en la documentación de TensorFlow y Keras 3 lo dejó solo en el espacio de compatibilidad `tf.keras`: en Keras 3.13.2 (la de Colab) y en 3.15.1 (la del box) vive en `keras/src/legacy/preprocessing/image.py` y se exporta solo por `keras._tf_keras.keras.preprocessing.image`. Lo probé en el box y funciona; `keras.preprocessing.image` no lo tiene. La notebook del curso lo importa como `from tensorflow.keras.preprocessing.image import ImageDataGenerator`, que en Colab anda. Para código nuevo usá capas `RandomFlip`, `RandomRotation`, `RandomZoom`. | [Doc de TensorFlow](https://www.tensorflow.org/api_docs/python/tf/keras/preprocessing/image/ImageDataGenerator), [issue #19865 de Keras](https://github.com/keras-team/keras/issues/19865), rueda de Keras 3.13.2 bajada con pip |
| Qué trae Colab hoy | Dato nuevo | El `pip freeze` público de Colab lista TensorFlow 2.21.0, Keras 3.13.2, tf_keras 2.21.0, torch 2.11.0, transformers 5.18.0, XGBoost 3.4.1, LightGBM 4.6.0 y **scikit-learn 1.6.1**. La FAQ de versiones fijables lista como última la 2026.07 (Python 3.12.13, PyTorch 2.11.0, TensorFlow 2.20.0). Ojo con scikit-learn: en Colab tenés una versión tres menores más vieja que la del box, así que avisos como el de `SVC(probability=True)` no te van a aparecer ahí. | [pip-freeze de googlecolab/backend-info](https://github.com/googlecolab/backend-info), [FAQ de versiones de Colab](https://research.google.com/colaboratory/runtime-version-faq.html) |
| "Si instalan transformers también se instala torch por defecto" C3P2 3:16 | No | En PyPI, transformers 5.18.0 depende de huggingface-hub, numpy, packaging, pyyaml, regex, tokenizers, typer, safetensors y tqdm; `torch>=2.5` aparece solo con el extra `torch` (`pip install "transformers[torch]"`). En Colab parece que "viene", pero es porque torch ya está preinstalado. | [transformers en PyPI](https://pypi.org/project/transformers/) (leí su JSON con curl) |
| El summary de la CNN de Fashion MNIST da "total 250.000" C2P2 1:29:29 | En parte | La notebook usa `Conv2D(32, (3,3))`, `MaxPooling2D`, `Conv2D(64, (3,3))`, `MaxPooling2D`, `Flatten`, `Dense(128)` y `Dense(10)`: son 225.034 parámetros (320 + 18.496 + 204.928 + 1.290), lo mismo que calculé en la primera parte. | demo_7.2_CNN.ipynb del repo |
| Ante un R² negativo, "quizás está mal calculado, un menos en mlutils" C1P2 42:08 | No | `mlutils.py` calcula `r2 = r2_score(y, y_pred)`, sin ningún signo cambiado. El R² negativo es real: el modelo predice peor que la media. | mlutils.py del repo |
| El dataset de diabetes "para decir si una persona tiene diabetes o no" C4P1 3:22 | No | La notebook de boosting usa `load_diabetes()`, que es regresión. En la carpeta hay además un `pima-indians-diabetes.csv` (768 filas, 34,9% positivos) que sí es de clasificación, pero la notebook no lo carga. | demo_10_boosting.ipynb y demo_10_dataset del repo |
| XGBoost "ganó varias competencias por el 2009, 2010" C4P1 1:08 | No | Chen cuenta que XGBoost se hizo conocido cuando probó la competencia Higgs Boson de Kaggle y su versión de consola "salta al primer puesto" de la tabla; el trabajo con Tong He sobre Higgs es del taller de NIPS 2014. El paper del sistema es de KDD 2016 (arXiv, 29/01/2016). | [Chen, historia de XGBoost](https://tqchen.com/old_post/2016-03-10-story-and-lessons-behind-the-evolution-of-xgboost), [Chen y He, PMLR 42](https://proceedings.mlr.press/v42/chen14.html), [arXiv 1603.02754](https://arxiv.org/abs/1603.02754) |
| XGBoost hace "procesamiento fuera del núcleo, o sea en la GPU" C3P2 1:28:50 | No | El paper: "To enable out-of-core computation, we divide the data into multiple blocks and store each block on disk", con compresión y reparto en varios discos. Con eso procesa 1.700 millones de ejemplos en una sola máquina. La GPU es otra cosa. | [arXiv 1603.02754](https://arxiv.org/abs/1603.02754), sección 4.3 |
| "La última versión estable va por el 2023" C4P1 15:38 | Desactualizado | Colab trae XGBoost 3.4.1, la misma que el box. | pip-freeze de Colab |
| Random forest "fue publicado en 2008" C3P2 53:17 | No | Breiman, "Random Forests", fechado en enero de 2001 (Machine Learning 45, 2001, según la cita del propio paper de XGBoost). El antecedente es Ho, "Random decision forests", ICDAR 1995, páginas 278 a 282, que arma árboles en subespacios al azar. | [PDF de Breiman en Berkeley](https://www.stat.berkeley.edu/~breiman/randomforest2001.pdf), [ficha de Ho 1995](https://bibtex.github.io/ICDAR-v1-1995-Ho.html) |
| "Para cada árbol elegimos 10, 15 o 20 atributos" C3P2 51:04 | No | Breiman: "Using a random selection of features to split each node". El sorteo es en cada división, no una vez por árbol (eso se parece más al subespacio de Ho). | PDF de Breiman |
| AdaBoost "es menos sensible a valores extremos" C3P2 1:27:06 | No | Breiman compara: los bosques "compare favorably to Adaboost... but are more robust with respect to noise". AdaBoost repondera fuerte los mal clasificados, así que el ruido de etiquetas lo afecta. | PDF de Breiman |
| Boosting "planteado en el 89" C3P2 1:18:42 | En parte | AdaBoost es de Freund y Schapire: "This paper appeared in Journal of Computer and System Sciences, 55(1):119-139, 1997", con un resumen extendido en la Second European Conference on Computational Learning Theory (1995). El 89 corresponde a la pregunta teórica previa sobre aprendizaje débil. | [PDF de Freund y Schapire](http://rob.schapire.net/papers/FreundSc95.pdf) |
| Karim atribuye a Samuel las dos definiciones de aprendizaje automático C1P1 15:05 | En parte | La de experiencia, tarea y medida es de Mitchell: "A computer program is said to learn from experience E with respect to some class of tasks T and performance measure P, if its performance at tasks in T, as measured by P, improves with experience E" (Machine Learning, McGraw Hill, 1997). El paper de Samuel es de 1959 (IBM Journal, vol. 3, n.º 3); la frase "sin ser programada explícitamente" no la encontré en el texto escaneado, así que es una paráfrasis posterior que se le atribuye. | [PDF de Mitchell en CMU](http://www.cs.cmu.edu/~tom/files/MachineLearningTomMitchell.pdf), [página del libro](http://www.cs.cmu.edu/~tom/mlbook.html), [PDF de Samuel en MIT](https://people.csail.mit.edu/brooks/idocs/Samuel.pdf) |
| ResNet "salió hace un par de años" C4P2 1:37:34 | No | arXiv 1512.03385, enviado el 10/12/2015: redes de hasta 152 capas, 3,57% de error en ImageNet, primer puesto en ILSVRC 2015. La ResNet101 del práctico es de ese paper. | [arXiv 1512.03385](https://arxiv.org/abs/1512.03385) |
| "ImageNet tiene 100 mil imágenes y mil categorías" C4P2 1:38:19 | No | La portada de ImageNet: "14,197,122 images, 21841 synsets indexed". La versión de la competencia tiene 1000 clases y unos 1,2 millones de imágenes de entrenamiento (AlexNet: "1.2 million high-resolution images in the LSVRC-2010 ImageNet training set into the 1000 different classes"). | [image-net.org](https://www.image-net.org/), [AlexNet en NeurIPS](https://papers.nips.cc/paper_files/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html) |
| Facebook "99,99 contra 99,98 del ojo humano" en detección de rostros C2P1 1:33:15 | No | DeepFace (Taigman, Yang, Ranzato y Wolf, CVPR 2014): "97.35% on the Labeled Faces in the Wild (LFW) dataset... closely approaching human-level performance". Es verificación de rostros, no detección, y no supera al humano. El 97,53% humano está en el cuerpo del paper; en la página que abrí figura solo el resumen. | [DeepFace en CVF](https://openaccess.thecvf.com/content_cvpr_2014/html/Taigman_DeepFace_Closing_the_2014_CVPR_paper.html) |
| "Estudio de Stanford: 98% en hombres blancos y 3% en mujeres negras" C2P1 1:36:02 | No | Es Gender Shades (Buolamwini y Gebru, FAT* 2018): en tres sistemas comerciales, las mujeres de piel oscura tienen "error rates of up to 34.7%" y los hombres de piel clara un máximo de 0,8%. | [Gender Shades en PMLR](https://proceedings.mlr.press/v81/buolamwini18a.html) |
| "Las convolucionales son bastante modernas, son del 2017" C2P2 49:54 y "de fines de la década del 2000" C1P1 45:50 | No | AlexNet es de NeurIPS 2012 (60 millones de parámetros, cinco capas convolucionales) y LeNet de los noventa. 2017 es el año del Transformer: "Attention Is All You Need", enviado el 12/06/2017, que propone una arquitectura "dispensing with recurrence and convolutions entirely". | AlexNet en NeurIPS; [arXiv 1706.03762](https://arxiv.org/abs/1706.03762) |
| "ChatGPT, Gemini y Claude usan este tipo de redes recurrentes" C2P1 8:05 | No | Ver la fila anterior: el Transformer prescinde de la recurrencia. | arXiv 1706.03762 |
| Dropout "es apagar neuronas que no aportan nada... y consigo modelos más chicos" C2P2 18:30 | No | Srivastava y otros (JMLR 2014): "The key idea is to randomly drop units (along with their connections) from the neural network during training". Al azar, solo durante el entrenamiento; el modelo final tiene el mismo tamaño. | [Dropout en JMLR](https://jmlr.org/papers/v15/srivastava14a.html) |
| `class_weight="balanced"` "multiplica los pesos por la probabilidad de que la clase aparezca" C1P1 1:13:24 | No | scikit-learn: "class weights will be given by n_samples / (n_classes * np.bincount(y))", o sea inversamente proporcional a la frecuencia. En el práctico: 1.884 / (2 × 448) = 2,10 para sin barbijo y 0,66 para con barbijo. | [compute_class_weight](https://scikit-learn.org/stable/modules/generated/sklearn.utils.class_weight.compute_class_weight.html) |
| "F1, la media geométrica" C1P1 1:59:01 | No | scikit-learn: "The F1 score can be interpreted as a harmonic mean of the precision and recall". | [f1_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html) |
| El costo de la SVM es "cero si tiene el mismo signo y está dentro del margen, y si no será uno" C1P1 36:05 | No | La hinge es "max(0, 1 − y f(x))" y scikit-learn la presenta como "equivalent to Support Vector Classification": cero solo fuera del margen y del lado correcto, y crece en forma lineal. | [Guía de SGD de scikit-learn](https://scikit-learn.org/stable/modules/sgd.html) |
| "SVM no da probabilidad o confianza" C1P1 45:50 | En parte | `SVC` da `decision_function` y puede calibrar con Platt ("logistic regression on the SVM's scores, fit by an additional cross-validation"). En scikit-learn 1.9, `probability` figura como "deprecated" y se quita en la 1.11: la doc dice "Use CalibratedClassifierCV(SVC(), ensemble=False)". En la 1.6.1 de Colab todavía anda sin aviso. | [SVC](https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html), [guía de SVM](https://scikit-learn.org/stable/modules/svm.html) |
| Titanic: "en primera clase casi el 50 por ciento sobrevivió" C4P2 1:24:06 | No | En el `train.csv` de la demo (891 pasajeros) sobrevivió el 63,0% de primera, el 47,3% de segunda y el 24,2% de tercera; el 38,4% en total (74,2% de las mujeres y 18,9% de los hombres). Faltan 177 edades. | demo_12_dataset del repo, contado en el box |
| "Tenemos 1.149.000 usuarios" en Book-Crossing C4P1 53:19 | No | GroupLens: "278,858 users... providing 1,149,780 ratings (explicit / implicit) about 271,379 books". En el archivo de puntuaciones del repo aparecen 105.283 usuarios que puntuaron. | [Book-Crossing en GroupLens](https://grouplens.org/datasets/book-crossing/) |
| "El 62% de los libros no tuvo valoración" C4P1 53:51 | En parte | Es el 62,3% de las **puntuaciones** (716.109 de 1.149.780), las que valen 0. | archivo del repo, contado en el box |
| "El cero es un número; es que no le gustó para nada" C4P1 1:16:04 | No | "The ratings are on a 1-10 scale, with 0 indicating an implicit-feedback record". La notebook del curso declara `Reader(rating_scale=(1, 10)) # 0 = N/A`, pero no saca los ceros: en el subconjunto filtrado el 70% de las filas son ceros y el RMSE de 3,38 sale de ahí (sección 6). | [Book Data Tools](https://bookdata.inertial.science/data/bx.html); demo_11 del repo |
| "BaselineOnly es justamente el que calcula los coeficientes de correlación" C4P1 1:01:07 | No | Surprise: "Algorithm predicting the baseline estimate for given user and item", r̂ = μ + b_u + b_i, sin similitudes. Los sesgos se estiman por SGD o por ALS, como hace la notebook. | [Surprise, algoritmos básicos](https://surprise.readthedocs.io/en/stable/basic_algorithms.html), [configuración de baselines](https://surprise.readthedocs.io/en/stable/prediction_algorithms.html) |
| Lógica difusa en el frenado de "trenes rápidos" de Japón C1P1 8:27 | En parte | Es el metro de Sendai: la serie 1000, en servicio desde 1987, "was the world's first train type to use fuzzy logic to control its speed", con un sistema de Hitachi. Es un subte, no un tren rápido. | [Sendai Subway 1000 series en Wikipedia](https://en.wikipedia.org/wiki/Sendai_Subway_1000_series), [artículo de 1988 en J-STAGE](https://www.jstage.jst.go.jp/article/jsmemag/91/836/91_KJ00001465358/_article/-char/en) |

### 2. Nombres y dudas de la transcripción, resueltos

| En la transcripción o el apunte | Qué es | Fuente |
|---|---|---|
| "Karim" y "Diego" | **Karim Alejandra Nemer Pelliza** ("Ing. en Sistemas de Información, Doctora en Ingeniería") y **Diego Gonzalez Dondo** ("Profesor investigador en Universidad Tecnológica Nacional"), en la lista de docentes del sitio de la diplomatura. El README del repo, de 2025, los firma como "Karim Nemer, Diego González Dondo" (con tilde). El sitio presenta la materia como la obligatoria 04: "Redes neuronales, SVMs, métodos de ensamble y arquitecturas profundas aplicadas a lenguaje y visión". | [diplodatos.famaf.unc.edu.ar](https://diplodatos.famaf.unc.edu.ar/), README del repo |
| Carolina, la coordinadora C3P1 0:25 | Carolina Chavero, que figura como coordinadora en el mismo sitio. | sitio de la diplomatura |
| Georgina, la de series temporales C1P1 14:05 | Georgina Flesia, en la lista de docentes del sitio. | sitio de la diplomatura |
| Quiénes dan Ética C3P2 30:51 | El sitio lista a Laura Alonso Alemany entre los docentes, pero no dice qué materia da cada uno. Sigue **para verificar** en el aula virtual. | sitio de la diplomatura |
| "Pancho tamari", el curso de redes de un cuatrimestre en FAMAF C2P2 1:45:24 | Muy probablemente Francisco Antonio Tamarit, "físico argentino con contribuciones en el campo de la física teórica" y rector de la UNC entre 2013 y 2016. Que dé un curso de redes en FAMAF no lo confirmé. | [Wikipedia en español](https://es.wikipedia.org/wiki/Francisco_Tamarit) |
| El paper "muy famoso" de Jorge Sánchez sobre kernels C1P1 1:31:30 | Lo más probable es "Image Classification with the Fisher Vector: Theory and Practice" (J. Sánchez, F. Perronnin, T. Mensink y J. Verbeek, International Journal of Computer Vision, 2013), con unas 1.100 citas indexadas según Rankless. El vector de Fisher sale del "kernel de Fisher", y eso encaja con lo que cuenta Diego. Ninguna de las dos páginas da su afiliación, así que no confirmé que sea el mismo Jorge Sánchez de FAMAF. | [ficha en la UvA](https://ivi.fnwi.uva.nl/isis/publications/bibtexbrowser.php?bib=all.bib&key=SanchezIJCV2013), [Rankless](https://www.rankless.org/hit-papers/10.1007/s11263-013-0636-x) |
| La notebook de recurrentes sale "de un repositorio con libro" C3P1 1:24:00 | La propia notebook lo dice: "Este notebook fue adaptado del capítulo 6 de 'Deep Learning with Python' de François Chollet". Recomienda además los posts de Colah sobre LSTM y de Karpathy sobre RNN. | demo_9_rnn_lstm.ipynb del repo |
| La demo de voting que se pasó por el chat C3P2 1:35:52 | Probablemente ML Playground (ml-playground.com): Karim describe que se ponen puntos naranjas y violetas con los botones del mouse y se elige el clasificador, y el README del proyecto dice que soporta cinco modelos: "KNN, Perceptron, SVMs, neural networks, and Decision Trees". Lo de los clics por color solo lo vi en un resultado de búsqueda; la página es una aplicación JavaScript que el lector no muestra. | [josephch405/ML-Playground](https://github.com/josephch405/ML-Playground) |
| La demo de SVM en el navegador C1P1 28:03, la página de optimizadores C2P1 47:06 y el gráfico de bagging contra boosting C3P2 1:30:00 | No identificados. No aparecen en el repo (busqué todas las URL de las notebooks) y la transcripción no da el nombre. | |
| El dataset de "gato o no gato" | Es el de Andrew Ng: `train_catvnoncat.h5` con 209 imágenes de 64 × 64 × 3, en `demo_6_dataset`. | repo del curso |
| Las herramientas para ver qué palabras pesaron C3P1 1:19:01 | Siguen sin nombre en clase. Sugerencia: para modelos de texto, SHAP o Integrated Gradients; no las probé acá. | |
| "Bustos" C1P1 58:36 y la "materia anterior" de Karim C1P1 1:19:00 | Sin resolver. | |

### 3. El trabajo práctico, desde el repositorio

El repo público resuelve casi todo lo que la primera parte había dejado **para verificar** sobre el práctico. Lo que sigue sale del README y la notebook de `Práctico/`, y de contar los CSV en el box.

- **La tarea.** Clasificar caras con barbijo (`ccb`) o sin barbijo (`csb`) a partir de un vector que sale de una ResNet101 preentrenada, más el ancho y el alto del recorte y el promedio del histograma RGB. Las imágenes vienen de 11 videos de la grabación (industria, vía pública, entrevistas, escuelas).
- **Los archivos.** `mask_prediction_datasetDrop_train-labeled2.csv` (1.884 filas, separado por **punto y coma**), `mask_prediction_datasetDrop_test2.csv` (524 filas, separado por **coma**, con la columna `clase` vacía) y `sample_submission.csv` (524 filas, columnas `id` y `clase` con 0 y 1). El README escribe `Id` y `Clase` con mayúscula, pero en los archivos están en minúscula.
- **Requisitos.** Análisis exploratorio, superar el baseline público, usar al menos tres modelos distintos del árbol de decisión y entregar una notebook con el análisis y los tres mejores modelos que subiste.
- **Pasos.** Cuenta de Kaggle, link de la competencia en el aula virtual, "Join Competition", aceptar reglas, armar el equipo con tu grupo asignado y subir el CSV con "Submit Predictions". Los datos también están en el repo, así que podés trabajar sin entrar a Kaggle hasta el momento de enviar.
- **Tres cosas raras del material oficial que conviene saber.**
  1. El baseline escala el test con un `StandardScaler` **nuevo** ajustado sobre el propio test (`X_test = StandardScaler().fit_transform(X_test)`), en vez de reusar el que ajustó con el train. Funciona porque las distribuciones se parecen, pero es una mala práctica: usá un `Pipeline` que aprenda la escala solo con el train.
  2. El README dice que el baseline guarda `data/submission.csv`, pero la notebook guarda `sample_submission_mask.csv`; y la sección "Subir una predicción" habla de "si fue teletransportado o no a otra dimensión alternativa", un resto de la plantilla de la competencia Spaceship Titanic.
  3. El baseline reporta recall en entrenamiento y prueba con la clase 1 = con barbijo, que es la mayoritaria; el recall que importa para la consigna es el de la clase minoritaria (sin barbijo), y la accuracy balanceada es el promedio de los dos.
### 4. Benchmark: qué modelo conviene sobre vectores de una red preentrenada

La pregunta del práctico es concreta: tenés 433 características que salen de una ResNet101 y tenés que elegir al menos tres modelos además del árbol. La medí de dos maneras: con los **datos reales del práctico** (están en el repo) y con un **análogo público** donde controlo cómo se sacan las características, para comparar la ResNet contra un modelo preentrenado más nuevo.

**4.1. Datos reales del práctico.** Validación cruzada estratificada de 5 particiones repetida 3 veces (15 ajustes por modelo) sobre las 1.884 filas del train, con la accuracy balanceada de la competencia. Los modelos que necesitan escala llevan `StandardScaler` dentro de un `Pipeline`.

| Modelo | Accuracy balanceada | Accuracy simple | Segundos por ajuste |
|---|---|---|---|
| Siempre "con barbijo" (`DummyClassifier`) | 0,500 ± 0,000 | 0,762 | 0,00 |
| Árbol por defecto (el baseline) | 0,935 ± 0,017 | 0,952 | 0,51 |
| Árbol con una grilla como la del baseline | 0,937 ± 0,018 | 0,952 | 10,3 |
| Random forest balanceado (500 árboles) | 0,963 ± 0,011 | 0,978 | 1,8 |
| Vecinos más cercanos (k = 5) | 0,973 ± 0,008 | 0,984 | 0,12 |
| XGBoost (300 árboles, profundidad 3, `scale_pos_weight`) | 0,973 ± 0,011 | 0,983 | 1,3 |
| Red MLP (una capa de 256) con parada temprana | 0,975 ± 0,009 | 0,984 | 3,1 |
| SVM con kernel RBF balanceada (C = 10) | 0,982 ± 0,009 | 0,991 | 0,12 |
| Regresión logística (C = 1, sin balancear) | 0,984 ± 0,008 | 0,989 | 0,16 |
| Regresión logística balanceada (C = 0,01) | 0,986 ± 0,008 | 0,988 | 0,11 |
| SVM lineal balanceada (C = 0,001) | **0,987 ± 0,004** | 0,984 | 0,05 |
| Voto blando (logística + SVM RBF calibrada + XGBoost) | **0,987 ± 0,008** | 0,992 | 3,2 |

Qué se lee:
- **El salto grande es del árbol a un modelo lineal**: de 0,935 a 0,986, o sea que el error balanceado baja de 6,5% a 1,4%, casi cinco veces menos. Entre los mejores modelos las diferencias están dentro del desvío.
- **Sacar `bb_width`, `bb_height` y `ch_RGB` no cambia nada**: la logística balanceada da 0,986 con o sin ellas y la SVM RBF 0,982 en los dos casos. La señal está en el vector de la ResNet.
- **La regularización fuerte ayuda un poco**: en una validación de 5 particiones, la logística balanceada da 0,959 con C = 0,0001, 0,973 con 0,001, 0,984 con 0,01, 0,983 con 0,1 y 0,981 con 1. Con 433 columnas y 1.500 filas por partición, conviene achicar C, pero no demasiado.
- **La accuracy simple engaña**: el modelo que siempre dice "con barbijo" tiene 0,762.
- **Con pocas filas ya alcanza**: una logística balanceada entrenada con 50 filas al azar ya da 0,94 sobre 384 filas de prueba, con 200 da 0,974 y con 1.500 da 0,992 (cinco semillas cada una). El vector de la ResNet separa casi solo las dos clases.
- `HistGradientBoostingClassifier` quedó afuera: en el box tardaba 1,3 segundos por iteración con estos datos (27 segundos por 20 iteraciones), algo anómalo que no investigué.

El código que recomiendo para el práctico, probado en el box de punta a punta (valida y genera el CSV de envío con la codificación del baseline oficial):

```python
# tp_modelos.py
# Práctico: validación cruzada con la métrica de la competencia y archivo de envío con la codificación del baseline
import numpy as np, pandas as pd
from sklearn.model_selection import RepeatedStratifiedKFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC, SVC
from sklearn.tree import DecisionTreeClassifier
P = "/workspace/yt/as_repo/Práctico/"                                   # o la carpeta donde bajaste los datos
train = pd.read_csv(P + "mask_prediction_datasetDrop_train-labeled2.csv", sep=";")   # ojo: punto y coma
test = pd.read_csv(P + "mask_prediction_datasetDrop_test2.csv")                      # ojo: coma
y = (train["clase"] == "ccb").astype(int)          # 1 = con barbijo, 0 = sin barbijo, como el baseline oficial
X = train.drop(columns=["id", "clase"])
X_test = test[X.columns]                            # mismas columnas, mismo orden
cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=3, random_state=0)
modelos = {
    "árbol (baseline)": DecisionTreeClassifier(random_state=0),
    "logística": make_pipeline(StandardScaler(), LogisticRegression(C=0.01, class_weight="balanced", max_iter=5000)),
    "SVM lineal": make_pipeline(StandardScaler(), LinearSVC(C=0.001, class_weight="balanced", max_iter=20000)),
    "SVM RBF": make_pipeline(StandardScaler(), SVC(C=10, class_weight="balanced")),
}
for nombre, m in modelos.items():
    s = cross_val_score(m, X, y, cv=cv, scoring="balanced_accuracy")
    print(f"{nombre}: {s.mean():.3f} ± {s.std():.3f}")
final = modelos["logística"].fit(X, y)              # la escala se aprende solo con el train, dentro del pipeline
envio = pd.DataFrame({"id": test["id"], "clase": final.predict(X_test)})
envio.to_csv("submission.csv", index=False)
print(envio.shape, "| proporción con barbijo predicha:", round(envio["clase"].mean(), 3), "| columnas:", list(envio.columns))
```

Salida en el box:

```
árbol (baseline): 0.935 ± 0.017
logística: 0.986 ± 0.008
SVM lineal: 0.987 ± 0.004
SVM RBF: 0.982 ± 0.009
(524, 2) | proporción con barbijo predicha: 0.693 | columnas: ['id', 'clase']
```

Un detalle de esa salida: el modelo predice 69% de caras con barbijo en el test, contra 76% en el train. O el test tiene otra proporción, o el modelo se equivoca más ahí; no lo vas a saber hasta enviar, y es otra razón para que la competencia use accuracy balanceada.

**4.2. Análogo público: ResNet101 contra CLIP.** Para ver si un modelo preentrenado más nuevo cambia el panorama, armé un problema con la misma forma que el práctico: 3.000 imágenes de CIFAR-10, 2.100 gatos y 900 perros (30% de la clase minoritaria), 1.800 para entrenar y 524 para probar, cinco particiones al azar. Saqué dos representaciones: la ResNet101 de Keras preentrenada en ImageNet, con promedio global (2.048 valores por imagen, como el práctico antes de descartar columnas), y CLIP ViT-B/32 de OpenAI (512 valores). También medí CLIP **sin entrenar nada**, comparando cada imagen con los textos "a photo of a cat" y "a photo of a dog".

| Modelo | ResNet101 (como el TP) | CLIP ViT-B/32 |
|---|---|---|
| Árbol (el baseline) | 0,773 ± 0,025 | 0,812 ± 0,018 |
| Random forest balanceado | 0,867 ± 0,010 | 0,913 ± 0,012 |
| XGBoost (300 árboles, profundidad 3) | 0,891 ± 0,002 (45 s por ajuste) | 0,925 ± 0,010 (2,2 s) |
| SVM RBF balanceada | 0,892 ± 0,011 | 0,932 ± 0,006 |
| Red MLP (256) con parada temprana | 0,898 ± 0,011 | 0,935 ± 0,010 |
| SVM lineal balanceada | 0,907 ± 0,005 | 0,940 ± 0,009 |
| Regresión logística balanceada (C por validación interna) | **0,910 ± 0,006** | **0,944 ± 0,011** |
| CLIP sin entrenar (cero etiquetas) | | 0,913 ± 0,007 |

Y con pocas etiquetas, regresión logística balanceada (C = 0,01) sobre cada representación:

| Etiquetas de entrenamiento | ResNet101 | CLIP |
|---|---|---|
| 20 | 0,682 ± 0,017 | 0,862 ± 0,018 |
| 50 | 0,784 ± 0,030 | 0,908 ± 0,024 |
| 100 | 0,843 ± 0,015 | 0,918 ± 0,017 |
| 200 | 0,869 ± 0,014 | 0,935 ± 0,008 |
| 500 | 0,884 ± 0,012 | 0,936 ± 0,015 |
| 1.800 | 0,896 ± 0,005 | 0,949 ± 0,008 |

Qué se lee:
- **El orden de los modelos se repite** con las dos representaciones y coincide con el práctico: lineal arriba, árbol abajo, boosting y redes en el medio.
- **La representación pesa más que el clasificador.** Pasar de ResNet a CLIP sube unos 3 o 4 puntos a cualquier modelo; cambiar de clasificador dentro de la misma representación mueve menos, salvo el árbol.
- **CLIP sin ninguna etiqueta (0,913) iguala a la mejor ResNet con 1.800 etiquetas (0,910)**, y con 50 etiquetas ya le gana a la ResNet con 500.
- **XGBoost sobre 2.048 columnas densas es caro**: 45 segundos por ajuste contra 3 de la logística, para rendir menos.

Así extraje las características (extracto de `feats.py` y `clip.py`, corridos en el box en CPU: 478 segundos la ResNet y 186 CLIP para las 3.000 imágenes):

```python
base = keras.applications.ResNet101(include_top=False, weights="imagenet", pooling="avg", input_shape=(224, 224, 3))
with torch.no_grad():                                   # sin esto PyTorch guarda el grafo y se queda sin memoria
    b = torch.nn.functional.interpolate(torch.tensor(lote).permute(0, 3, 1, 2).float(), size=224, mode="bilinear").permute(0, 2, 3, 1).numpy()
    vec = keras.ops.convert_to_numpy(base(keras.applications.resnet.preprocess_input(b), training=False))
# CLIP con transformers 5.18 (necesita Pillow para el procesador de imágenes)
m = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").eval(); p = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
emb = m.get_image_features(**p(images=list(lote), return_tensors="pt"))
```

### 5. Keras 3 y Colab: qué cambia para las notebooks de la materia

**Qué dice la fuente.** Las demos de redes usan `tensorflow.keras` y `ImageDataGenerator` C2P2 1:36:05, guardan modelos y cargan datasets de `keras.datasets`. Karim prefiere no subir datos a Colab C4P2 4:31.

**Qué suma el material externo.**
- La guía oficial de migración de Keras 2 a Keras 3 dice que el costo "is minimal": cambiar `from tensorflow import keras` por `import keras` y `tf.keras.*` por `keras.*`. Los cambios que más te pueden morder: `model.save()` ya no guarda en formato SavedModel de TensorFlow (usá extensión `.keras`, o `model.export()` para servir), `jit_compile` viene en `True` por defecto en GPU, y se quitaron cosas de poco uso como `LocallyConnected2D` y los argumentos `constants` y `time_major` de las capas recurrentes.
- `ImageDataGenerator` sigue existiendo solo como legado (sección 1). La documentación de TensorFlow lo marca "DEPRECATED" y en el issue #19865 de Keras el equipo remite a `image_dataset_from_directory` y a las capas de preprocesamiento.
- Colab hoy trae TensorFlow 2.21, Keras 3.13.2 y también `tf_keras` 2.21 (el Keras 2 de compatibilidad), además de torch 2.11 y JAX. O sea que la misma notebook puede correr con Keras 3 sobre TensorFlow, PyTorch o JAX.

**Cómo implementarlo.** Este es el reemplazo directo del `ImageDataGenerator(rotation_range=10, width_shift_range=0.1, height_shift_range=0.1, zoom_range=0.1)` de la demo, con la misma CNN. Lo corrí en el box con Keras 3.15.1 sobre PyTorch.

```python
# k3_aumento.py
import os; os.environ.setdefault("KERAS_BACKEND", "torch")
import keras
from keras import layers
# Reemplazo de ImageDataGenerator(rotation_range=10, width_shift_range=0.1, height_shift_range=0.1, zoom_range=0.1)
aumento = keras.Sequential([
    layers.RandomRotation(10 / 360),          # el factor es fracción de una vuelta: 10 grados
    layers.RandomTranslation(0.1, 0.1),
    layers.RandomZoom(0.1),
], name="aumento")
modelo = keras.Sequential([
    keras.Input((28, 28, 1)),
    aumento,                                   # solo actúa en fit(); en predict() pasa la imagen igual
    layers.Conv2D(32, 3, activation="relu"), layers.MaxPooling2D(),
    layers.Conv2D(64, 3, activation="relu"), layers.MaxPooling2D(),
    layers.Flatten(), layers.Dense(128, activation="relu"), layers.Dense(10, activation="softmax"),
])
modelo.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
print("parámetros:", modelo.count_params())
(xtr, ytr), (xte, yte) = keras.datasets.fashion_mnist.load_data()
xtr, xte = xtr[..., None] / 255.0, xte[..., None] / 255.0
modelo.fit(xtr[:10000], ytr[:10000], epochs=2, batch_size=128, validation_split=0.1, verbose=0)
print("accuracy de prueba (10.000 imágenes, 2 épocas):", round(modelo.evaluate(xte, yte, verbose=0)[1], 3))
modelo.save("cnn_fashion.keras")              # Keras 3: formato .keras; para servir, modelo.export("carpeta")
print("guardado y recargado:", keras.models.load_model("cnn_fashion.keras").count_params())
```

Salida en el box: 225.034 parámetros (igual que la CNN de la notebook: las capas de aumento no tienen pesos), 0,726 de accuracy de prueba entrenando solo 2 épocas con 10.000 imágenes (es una prueba de que corre, no un resultado para comparar) y el modelo se guarda y se recarga en formato `.keras`.

- **Sugerencia:** si una notebook vieja falla en Colab por algo de Keras, antes de tocar código probá con `pip install tf_keras` y `os.environ["TF_USE_LEGACY_KERAS"] = "1"` antes de importar TensorFlow, que es la vía de compatibilidad que deja TensorFlow; pero para el práctico conviene escribir directo en Keras 3. No lo probé en Colab, solo leí que `tf_keras` está instalado.

### 6. Recomendación: los ceros de Book-Crossing y la retroalimentación implícita

**Qué dice la fuente.** La demo filtra libros y usuarios con más de 50 puntuaciones, compara algoritmos de Surprise y se queda con `BaselineOnly` con ALS, con un RMSE de alrededor de 3,3 C4P1 1:01:07. Ante la pregunta de si 0 es "no puntuar", la respuesta es que el cero es una nota C4P1 1:16:04.

**Qué suma el material externo.** La descripción del dataset dice que las notas van de 1 a 10 y que el 0 es una interacción implícita (sección 1). La documentación de Surprise define `BaselineOnly` como μ + b_u + b_i, y la de `implicit` dice que es una librería para "implicit feedback datasets", con ALS según Hu, Koren y Volinsky.

**Cómo implementarlo.** Repetí el filtro de la notebook con y sin ceros y medí el RMSE de `BaselineOnly` con los mismos parámetros (ALS, 5 épocas, `reg_u=12`, `reg_i=5`, validación cruzada de 3 particiones):

| Datos | Filas | Ceros | Media | Desvío | RMSE de BaselineOnly |
|---|---|---|---|---|---|
| Como la notebook (con ceros) | 140.516 | 70,3% | 2,34 | 3,73 | 3,377 |
| El mismo filtro y después sin ceros | 41.703 | 0% | 7,89 | 1,74 | 1,546 |
| Primero sin ceros y después el filtro | 13.716 | 0% | 8,01 | 1,73 | 1,543 |

Dos lecturas. Primero, el 3,3 de la clase no es "error de recomendación", es sobre todo el modelo tratando de adivinar si una fila es un cero implícito o una nota alta. Segundo, sin ceros el RMSE baja a 1,55 con cualquiera de los dos órdenes de filtrado, pero el desvío de las notas es 1,74: el modelo apenas le gana a predecir siempre la media, y por eso conviene compararlo siempre contra esa referencia.

```python
# bench_bx.py
# Book-Crossing: el notebook del curso deja los ceros (interacciones implícitas) como si fueran notas
import pandas as pd, numpy as np
from surprise import Reader, Dataset, BaselineOnly
from surprise.model_selection import cross_validate
P = "/workspace/yt/as_repo/Teórico/demo_11_dataset/"
u = pd.read_csv(P + "BX-Users.csv", sep=";", encoding="latin-1"); u.columns = ["userID", "Location", "Age"]
r = pd.read_csv(P + "BX-Book-Ratings.csv", sep=";", encoding="latin-1"); r.columns = ["userID", "ISBN", "bookRating"]
df = pd.merge(u, r, on="userID")[["userID", "ISBN", "bookRating"]]
print("filas tras unir con usuarios", len(df), "ceros", round((df.bookRating == 0).mean(), 3))
def filtra(d):
    b = d.ISBN.value_counts(); us = d.userID.value_counts()
    return d[d.ISBN.isin(b[b > 50].index) & d.userID.isin(us[us > 50].index)]
opts = {"method": "als", "n_epochs": 5, "reg_u": 12, "reg_i": 5}
variantes = [("como el curso (con ceros, escala 0 a 10)", filtra(df), (0, 10)),
             ("mismo filtro y después sin ceros", filtra(df).query("bookRating > 0"), (1, 10)),
             ("sin ceros y después el filtro", filtra(df[df.bookRating > 0]), (1, 10))]
for nombre, d, escala in variantes:
    data = Dataset.load_from_df(d, Reader(rating_scale=escala))
    res = cross_validate(BaselineOnly(bsl_options=opts, verbose=False), data, measures=["RMSE"], cv=3, verbose=False)
    print(nombre, "| filas", len(d), "| ceros", round((d.bookRating == 0).mean(), 3), "| media", round(d.bookRating.mean(), 2),
          "| desvío", round(d.bookRating.std(), 2), "| RMSE BaselineOnly", round(np.mean(res["test_rmse"]), 3))
```

- **Sugerencia:** usá las notas de 1 a 10 con Surprise (escala `(1, 10)` de verdad) y, si querés aprovechar el 62% de ceros, tratalos como señales de interés con `implicit` y evaluá con métricas de ranking (precisión o recall en los primeros k), no con RMSE. En mi prueba con `implicit` 0.7.3 (usuarios y libros con al menos 10 interacciones: 7.057 usuarios, 14.007 libros y 379.717 interacciones, donde una nota explícita pesa más que un cero), ALS da una precisión en los primeros 10 de 0,077, contra 0,030 de recomendarle a cada usuario los 10 libros más populares que no leyó:

```python
# bx_implicit.py
# Book-Crossing como retroalimentación implícita: toda fila (con nota o con 0) es "interactuó con el libro"
import os; os.environ["OPENBLAS_NUM_THREADS"] = "1"
import numpy as np, pandas as pd, scipy.sparse as sp
from implicit.als import AlternatingLeastSquares
from implicit.evaluation import train_test_split, precision_at_k
r = pd.read_csv("/workspace/yt/as_repo/Teórico/demo_11_dataset/BX-Book-Ratings.csv", sep=";", encoding="latin-1")
r.columns = ["user", "isbn", "nota"]
for _ in range(3):                                   # usuarios y libros con al menos 10 interacciones
    b = r.isbn.value_counts(); u = r.user.value_counts()
    r = r[r.isbn.isin(b[b >= 10].index) & r.user.isin(u[u >= 10].index)]
ui = r.user.astype("category").cat.codes.values; ii = r.isbn.astype("category").cat.codes.values
peso = np.where(r.nota.values > 0, 1.0 + r.nota.values / 2, 1.0)   # una nota explícita pesa más que un 0
M = sp.csr_matrix((peso, (ui, ii)))
print("usuarios", M.shape[0], "libros", M.shape[1], "interacciones", M.nnz)
tr, te = train_test_split(M, train_percentage=0.8, random_state=0)
als = AlternatingLeastSquares(factors=64, regularization=0.05, iterations=15, random_state=0)
als.fit(tr, show_progress=False)
print("ALS implícito, precisión en los primeros 10:", round(precision_at_k(als, tr, te, K=10, show_progress=False), 4))
orden = np.asarray((tr > 0).sum(0)).ravel().argsort()[::-1]          # libros de más a menos populares
def top10(u):                                                        # los 10 más populares que el usuario no leyó
    vistos = set(tr[u].indices); return [i for i in orden[:200] if i not in vistos][:10]
hits = [len(set(top10(u)) & set(te[u].indices)) / min(10, te[u].nnz) for u in range(te.shape[0]) if te[u].nnz]
print("Los 10 más populares para todos, precisión en los primeros 10:", round(float(np.mean(hits)), 4))
```

Salida en el box:

```
usuarios 7057 libros 14007 interacciones 379717
ALS implícito, precisión en los primeros 10: 0.0767
Los 10 más populares para todos, precisión en los primeros 10: 0.0297
```

### 7. SVM, probabilidades y boosting: qué conviene usar hoy

**Qué dice la fuente.** La materia usa `SVC` con kernels y `class_weight` C1P1 1:13:24, dice que la SVM no da probabilidades C1P1 45:50 y presenta AdaBoost, gradient boosting y XGBoost C3P2 1:28:50.

**Qué suma el material externo.**
- **Probabilidades de la SVM.** La guía de scikit-learn explica que las probabilidades de `SVC` salen de una calibración de Platt con validación cruzada interna, que es lenta y puede no coincidir con `predict`. Desde la 1.9 el camino es `CalibratedClassifierCV(SVC(), ensemble=False)`. Para el práctico la métrica es accuracy balanceada, así que no necesitás probabilidades salvo para un voto blando o para mover el umbral.
- **Boosting.** Además de XGBoost, LightGBM se presenta como "a gradient boosting framework that uses tree based learning algorithms" pensado para ser distribuido y eficiente, y CatBoost como "gradient boosting on decision trees" con manejo nativo de variables categóricas. scikit-learn trae `HistGradientBoostingClassifier`, que no necesita instalar nada. Las tres documentaciones las escriben los autores de cada librería.
- **Cuándo no.** En el práctico los datos son 433 salidas de una red, densas y de la misma naturaleza; ahí los modelos lineales tienen ventaja (sección 4). El boosting brilla con tablas heterogéneas: Grinsztajn, Oyallon y Varoquaux muestran que "tree-based models remain state-of-the-art on medium-sized data (~10K samples)".

**Cómo implementarlo.**

```python
from sklearn.calibration import CalibratedClassifierCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
svm_con_proba = make_pipeline(StandardScaler(), CalibratedClassifierCV(SVC(C=10, class_weight="balanced"), ensemble=False))
```

Esta es la SVM que usé dentro del voto blando de la sección 4.

### 8. Una receta de entrenamiento, con fuentes

**Qué dice la fuente.** La clase 4 cierra con buenas prácticas: separar entrenamiento, validación y prueba, registrar experimentos, curvas de aprendizaje y el libro de Andrew Ng C4P2 40:33.

**Qué suma el material externo.**
- Karpathy, "A Recipe for Training Neural Networks": el primer paso es "not touch any neural net code at all" y mirar los datos; después armar una base tonta, verificar que el modelo puede "overfit a single batch", y para la arquitectura, "Don't be a hero": copiá la del paper más parecido a tu problema.
- El Deep Learning Tuning Playbook de Google (que aclara "This is not an officially supported Google product") arranca con "try to reuse a model that already works" y propone ajustar de a un hiperparámetro por vez, con experimentos que respondan una pregunta concreta.
- Las dos fuentes van en la misma dirección que el práctico: el vector de una ResNet ya entrenada es "reusar un modelo que ya funciona".

**Cómo implementarlo en el práctico (sugerencia).**
1. Mirá los datos: proporción de clases, escalas de `bb_width`, `bb_height` y `ch_RGB` contra las de la ResNet, y si hay filas duplicadas.
2. Base tonta: `DummyClassifier` da 0,50 de accuracy balanceada (y 0,76 de accuracy simple, que engaña).
3. Base del curso: el árbol, 0,935.
4. Modelo lineal con escala y `class_weight="balanced"`: ahí ya estás arriba de 0,98 (sección 4).
5. Recién después, SVM con kernel, boosting o una red, y un voto blando si los errores no coinciden.
6. Registrá cada envío a Kaggle con fecha, modelo, hiperparámetros y puntaje de validación cruzada; la tabla pública usa una parte chica del test y te puede engañar.

## Críticas y límites

- **El repo puede ser del año pasado.** El README de teoría dice "Aprendizaje Supervisado 2025" con clases del 28 y 29 de junio y 11 y 12 de julio; el último cambio es del 15/07/2026. Las notebooks pueden no ser exactamente las que se mostraron en 2026, aunque el práctico coincide con lo que describe Diego en C4P2.
- **La competencia de Kaggle no es pública para mí.** No pude ver fechas, límite de envíos, reparto público y privado ni el puntaje del baseline público. Todo eso sigue **para verificar** en el aula virtual.
- **Mi benchmark es una validación cruzada sobre el train**, no el puntaje de Kaggle. Con 448 caras sin barbijo, un punto de accuracy balanceada son unas cuatro o cinco caras mal clasificadas; diferencias de menos de un punto entre modelos están dentro del ruido (miralo en los desvíos).
- **Las características del práctico ya son "preentrenadas".** Eso sesga la comparación a favor de los modelos lineales; con píxeles crudos el ranking sería otro (las CNN de la materia ganarían). Por eso sumé el análogo de CIFAR-10, que tampoco es caras con barbijo.
- **El análogo de CIFAR-10 sube imágenes de 32 × 32 a 224 × 224.** La ResNet y CLIP rinden menos que con fotos de buena resolución, así que las cifras absolutas son pesimistas; lo que importa es la comparación entre modelos con la misma entrada.
- **Hiperparámetros con poca búsqueda.** Elegí valores razonables y una grilla chica de C; un ajuste más fino podría mover cada modelo uno o dos puntos, sobre todo XGBoost y la red.
- **Conflictos de interés.** El paper de XGBoost y la historia de Chen los escriben sus creadores; el curso de Hugging Face, fast.ai, la documentación de LightGBM, CatBoost, Surprise e `implicit` los escriben los autores de cada herramienta; el paper de CLIP es de OpenAI, el de transferencia de Kornblith y el playbook son de Google, y TabPFN lo publican fundadores de Prior Labs, que lo comercializa. Grinsztajn y otros (Inria) no venden ninguna de las herramientas que comparan.
- **Afirmaciones que no pude cerrar:** qué docente da Ética, quién es "Bustos", qué paper exacto de Jorge Sánchez se mencionó, la demo de SVM en el navegador, la página de optimizadores y el gráfico de bagging contra boosting.
- **Leí con curl** (el lector web no las mostraba completas o preferí bajar solo el texto): arXiv de ResNet, CLIP, Kornblith, Grinsztajn y el Transformer; los PDF de Breiman, Freund y Schapire, Samuel y Mitchell (con `pdftotext`); las páginas de DeepFace, AlexNet, Gender Shades, dropout, Chen y He, la historia de XGBoost, ImageNet, GroupLens, Book Data Tools, Surprise, scikit-learn (SVC, guía de SVM, SGD, `compute_class_weight`, `f1_score`, `balanced_accuracy_score`), la FAQ y el `pip freeze` de Colab, el JSON de transformers en PyPI, la doc de TensorFlow sobre `ImageDataGenerator`, el issue #19865 de Keras, la ficha de Ho, las de Sánchez en la UvA y Rankless, Wikipedia (metro de Sendai y Tamarit), J-STAGE, ML-Playground, Karpathy, el playbook, d2l.ai, fast.ai, el curso de Hugging Face, LightGBM, CatBoost, `implicit`, Nature (TabPFN), la documentación de XGBoost, la página de capas de aumento de Keras y la página del libro de Ng. El repo del curso lo cloné con git porque la API de GitHub me devolvió límite de pedidos.
- **Abrí con el lector web:** el sitio de la diplomatura, el paper de XGBoost en arXiv y la guía de migración a Keras 3.
- **Solo vi en resultados de búsqueda:** que ML Playground usa clic izquierdo para naranja y derecho para violeta; el PDF de Ho en Purdue; las notas de Colab sobre la subida a TensorFlow 2.19 y Keras 3.10 (julio de 2025).
- **No cargaron:** la página de Breiman en Springer y la del paper de Sánchez en Springer (devolvieron una página vacía con curl), la de Ho en IEEE Xplore, la de Freund y Schapire en ScienceDirect, las de HAL (piden una prueba anti robots), la API de dblp, la página original de Book-Crossing en Friburgo y la de ml-playground.com (es una aplicación JavaScript).

## Análisis adversario

> Cómo leer esto: acá discuto el enfoque de la materia contra la alternativa más fuerte que encontré, con la mejor versión posible de esa alternativa. No es una crítica a los docentes: una materia de cuatro encuentros tiene que elegir, y esto sirve para que sepas qué elegirías vos en un trabajo real.

**La tesis.** La materia hace un recorrido amplio por familias de modelos (SVM, perceptrón y MLP, CNN, RNN, Transformers, árboles y ensambles, recomendadores), cada una con su demo, y un práctico donde se prueban varios clasificadores sobre vectores ya extraídos. La idea implícita es que conviene conocer muchas familias y elegir entre ellas con validación cruzada.

### La alternativa más fuerte: "primero el modelo preentrenado"

Consideré dos alternativas. Una es la **profundidad en pocas familias**: boosting para datos tabulares y modelos preentrenados para percepción, dejando de lado SVM con kernels, RNN y MLP hechos a mano. La otra es **"primero el modelo preentrenado"**: para imágenes, texto o audio, empezar por representaciones de un modelo grande ya entrenado más una cabeza lineal (o directamente un modelo que clasifica sin entrenar, como CLIP, o un LLM con un buen prompt), y entrenar algo a medida solo si eso no alcanza. Elegí la segunda porque es la que más cambia la práctica, porque mis números del práctico la respaldan y porque la primera es en buena parte un caso particular de ella (lo preentrenado para percepción ya está adentro; el boosting para tablas lo trato en "Dónde pierde").

### La alternativa en su mejor versión

**Quién la defiende.** El playbook de Google ("try to reuse a model that already works"), Karpathy ("Don't be a hero": copiá la arquitectura del paper más parecido), el curso de Hugging Face (construido alrededor de ajustar modelos preentrenados), Kornblith, Shlens y Le en Google, y Radford y otros en OpenAI con CLIP. Conflicto de interés: Google, OpenAI y Hugging Face producen y distribuyen esos modelos.

**Qué evidencia la respalda.**
- Kornblith y otros, sobre 16 redes y 12 datasets: usadas como extractores fijos, la precisión en ImageNet y la de transferencia tienen "a strong correlation" (r = 0,99). O sea, mejor modelo preentrenado, mejor resultado con una cabeza simple.
- El paper de CLIP reporta que su clasificación sin entrenar "match[es] the accuracy of the original ResNet-50 on ImageNet zero-shot" y que es "often competitive with a fully supervised baseline without the need for any dataset specific training".
- Mis números: en el práctico, una regresión logística sobre los vectores de la ResNet llega a 0,986 de accuracy balanceada, contra 0,935 del árbol; en el análogo de CIFAR-10, CLIP sin ninguna etiqueta (0,913) iguala a la mejor ResNet con 1.800 etiquetas (0,910), y con 50 etiquetas CLIP más una logística (0,908) supera a la ResNet con 500 (0,884).
- Para tablas chicas también existe una versión preentrenada: TabPFN (Nature, 2025) "outperforms all previous methods on datasets with up to 10,000 samples by a wide margin". Lo publican sus creadores, que lo venden; no lo probé.

**Qué evidencia la contradice.**
- Kornblith y otros también encuentran que la relación es "very sensitive to the way in which networks are trained on ImageNet": algunas regularizaciones mejoran ImageNet pero empeoran las características para transferir. El modelo más nuevo no siempre es el mejor extractor.
- En datos tabulares, Grinsztajn y otros muestran que "tree-based models remain state-of-the-art on medium-sized data (~10K samples)", y ahí no hay un "ResNet de las tablas" consolidado (TabPFN es reciente y tiene límites de tamaño).
- En mi análogo, el árbol sobre CLIP (0,812) sigue siendo mucho peor que una logística sobre la ResNet vieja (0,910): una buena representación no salva un mal clasificador para datos densos.
- Lo preentrenado trae sesgos de su entrenamiento: Gender Shades midió errores de hasta 34,7% en mujeres de piel oscura contra 0,8% en hombres de piel clara en sistemas comerciales de 2018. Si tu dominio está mal representado (caras con barbijo en videos de baja resolución, por ejemplo), hay que medir por subgrupo.
- Depender de un modelo de terceros tiene costos que no salen en la accuracy: licencias, versiones que cambian, datos que mandás a una API (el punto de Karim sobre no regalar los datos C4P2 4:31).

### Comparación directa

| Criterio | A: recorrido amplio de familias (la materia) | B: primero el modelo preentrenado |
|---|---|---|
| Costo | Bajo en cómputo para modelos clásicos; alto si entrenás CNN o RNN desde cero | Extraer características una vez: 8 minutos la ResNet y 3 CLIP para 3.000 imágenes en CPU; las API de LLM cobran por uso |
| — | Muchas APIs y conceptos; cada familia con sus hiperparámetros | Una librería de modelos (transformers o keras.applications) más una cabeza lineal |
| Tiempo hasta valor | Lento si hay que probar todo; rápido con datos tabulares | Muy rápido en percepción: con 50 etiquetas, 0,908 en mi análogo |
| Riesgo | Sobreajustar la validación de tanto probar modelos; elegir mal la familia | Sesgos y licencias del modelo base; cambio de dominio; dependencia de terceros |
| Madurez | Muy alta: scikit-learn, XGBoost, Keras | Alta en imágenes y texto; reciente en tablas (TabPFN) |
| Evidencia | Grinsztajn (boosting en tablas); mi benchmark (lineal sobre vectores) | Kornblith; CLIP; mi benchmark (CLIP sin etiquetas iguala a ResNet con 1.800) |
| Contexto donde rinde | Formación, tablas heterogéneas, datos privados, necesidad de explicar | Imágenes, texto y audio, pocas etiquetas, prototipos rápidos |

### Dónde gana la alternativa

- **En el propio práctico.** El dataset ya es "preentrenado más cabeza": la ResNet hizo el trabajo pesado y lo que queda es elegir una cabeza. Una logística o una SVM lineal balanceadas son la respuesta de B y están arriba de todo.
- **Con pocas etiquetas.** Con 20 etiquetas, CLIP más logística da 0,862 y la ResNet 0,682.
- **En tiempo de desarrollo.** Probar cuatro familias con sus grillas lleva horas; una cabeza lineal con una grilla chica de C, minutos.

### Dónde pierde

- **En datos tabulares heterogéneos** (el Titanic, la diabetes, la mayoría de los datos de negocio): ahí el boosting de la materia sigue siendo la primera opción según Grinsztajn y otros, y es exactamente lo que se ve en las demos de XGBoost.
- **Cuando hay que entender o explicar** por qué funciona un modelo: la materia enseña el margen de la SVM, el gradiente, la convolución y la atención, y sin eso no sabés diagnosticar cuando lo preentrenado falla.
- **Con datos que no podés mandar afuera** o un dominio muy distinto del de preentrenamiento (imágenes SAR como las que trabaja Karim C2P1 1:37:25), donde quizás tengas que entrenar o ajustar con tus propios datos.
- **En la evaluación de la materia**, que pide al menos tres modelos distintos del árbol: B no te exime de comparar.

### Cómo decidir

**Elegí A (el recorrido amplio de la materia) si…**
- estás aprendiendo y necesitás entender qué hace cada familia y cómo se rompe;
- tus datos son una tabla con columnas de distinto tipo y unos miles de filas (empezá por boosting);
- no podés usar modelos o servicios de terceros por privacidad, licencia o costo;
- tenés que explicar el modelo a alguien que va a decidir con él.

**Elegí B (primero el modelo preentrenado) si…**
- tus datos son imágenes, texto o audio;
- tenés pocas etiquetas (decenas o cientos);
- existe un modelo preentrenado en un dominio parecido al tuyo;
- necesitás una primera versión que funcione en un día.

**Un híbrido posible (sugerencia).** Usá el modelo preentrenado como extractor y la caja de herramientas de la materia como cabeza y como control de calidad: (1) extraé vectores con el mejor modelo disponible; (2) entrená una logística o una SVM lineal con `class_weight="balanced"` y elegí C con validación cruzada; (3) compará contra el árbol, una SVM RBF y XGBoost para ver si queda algo no lineal; (4) si hay columnas tabulares además del vector, probá boosting con esas columnas y voto blando; (5) ajustá el modelo preentrenado completo solo si la cabeza lineal se estanca y tenés suficientes datos; y (6) medí por subgrupo antes de usarlo en serio. Para el práctico, eso se traduce en: logística o SVM lineal balanceadas como modelo principal, SVM RBF y un voto blando como segundo y tercer modelo, y el análisis de por qué el árbol queda tan atrás.

**Veredicto.** Para el práctico y para cualquier problema de percepción, B gana con claridad y la materia ya te la da hecha a medias (el vector de la ResNet); la parte que falta es animarse a que el mejor modelo sea el más simple. Para tablas, A sigue siendo lo que usaría, empezando por boosting. Lo que la materia enseña de cada familia es lo que te permite saber cuándo estás en un caso o en el otro.

## Material para seguir

**Para el práctico, en este orden**
- [Repo del curso, carpeta Práctico](https://github.com/DiploDatos/AprendizajeSupervisado/tree/master/Pr%C3%A1ctico): datos, baseline y consigna, sin necesidad de entrar a Kaggle.
- [Karpathy, A Recipe for Training Neural Networks](https://karpathy.github.io/2019/04/25/recipe/): mirá los datos primero, base tonta, sobreajustá un lote, "don't be a hero".
- [Guía de SVM de scikit-learn](https://scikit-learn.org/stable/modules/svm.html): kernels, `class_weight`, escalado y por qué las probabilidades salen de Platt.
- [SVC en scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html): el aviso de `probability` obsoleto y el reemplazo con `CalibratedClassifierCV`.
- [balanced_accuracy_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.balanced_accuracy_score.html): la métrica de la competencia, en una página.

**Redes y aprendizaje profundo**
- [Dive into Deep Learning (d2l.ai)](https://d2l.ai/): libro gratis con código en PyTorch, JAX, TensorFlow y MXNet; "adopted at 500 universities from 70 countries".
- [fast.ai, Practical Deep Learning for Coders](https://course.fast.ai/): curso gratis, de arriba hacia abajo, con su propia librería (conflicto de interés leve: enseña su herramienta).
- [Deep Learning Tuning Playbook de Google](https://github.com/google-research/tuning_playbook): cómo elegir arquitectura, optimizador y lote, y ajustar con método.
- [Guía de migración a Keras 3](https://keras.io/guides/migrating_to_keras_3/): todo lo que se rompe al pasar de `tf.keras` a Keras 3.
- [Capas de aumento de imágenes de Keras](https://keras.io/api/layers/preprocessing_layers/image_augmentation/): el reemplazo de `ImageDataGenerator`.
- [Curso de LLM de Hugging Face](https://huggingface.co/learn/llm-course/chapter1/1): "completely free and without ads"; Transformers, ajuste fino y `Trainer` (lo escribe la empresa de la librería).

**Árboles y boosting**
- [Documentación de XGBoost](https://xgboost.readthedocs.io/en/stable/): parámetros, `scale_pos_weight`, GPU y datos fuera de memoria.
- [Documentación de LightGBM](https://lightgbm.readthedocs.io/en/latest/): boosting por histogramas, rápido con muchas filas.
- [Documentación de CatBoost](https://catboost.ai/docs/en/): boosting con variables categóricas sin codificar a mano.
- [Chen y Guestrin, XGBoost (arXiv 1603.02754)](https://arxiv.org/abs/1603.02754): el paper del sistema, escrito por sus autores.
- [Breiman, Random Forests (PDF)](https://www.stat.berkeley.edu/~breiman/randomforest2001.pdf): el original de 2001, legible y con la comparación contra AdaBoost.
- [Grinsztajn, Oyallon y Varoquaux, árboles contra redes en tablas (arXiv 2207.08815)](https://arxiv.org/abs/2207.08815): por qué el boosting sigue ganando en datos tabulares medianos.

**Recomendación**
- [Surprise, algoritmos básicos](https://surprise.readthedocs.io/en/stable/basic_algorithms.html): qué hace exactamente `BaselineOnly`.
- [Surprise, configuración de baselines y similitudes](https://surprise.readthedocs.io/en/stable/prediction_algorithms.html): SGD contra ALS y sus parámetros.
- [implicit](https://benfred.github.io/implicit/): ALS y otros métodos para clics, compras y los ceros de Book-Crossing.
- [Book-Crossing en GroupLens](https://grouplens.org/datasets/book-crossing/): la descripción oficial del dataset.

**Modelos preentrenados como punto de partida**
- [Kornblith, Shlens y Le, Do Better ImageNet Models Transfer Better? (arXiv 1805.08974)](https://arxiv.org/abs/1805.08974): características fijas más regresión logística en 12 datasets (Google).
- [Radford y otros, CLIP (arXiv 2103.00020)](https://arxiv.org/abs/2103.00020): clasificación sin entrenar y sondas lineales (OpenAI, autores del modelo).
- [Hollmann y otros, TabPFN (Nature, 2025)](https://www.nature.com/articles/s41586-024-08328-6): un modelo preentrenado para tablas chicas (sus autores lo comercializan).
- [He y otros, ResNet (arXiv 1512.03385)](https://arxiv.org/abs/1512.03385): de dónde salen las características del práctico.

**Ética y contexto**
- [Buolamwini y Gebru, Gender Shades (PMLR 81)](https://proceedings.mlr.press/v81/buolamwini18a.html): el estudio real detrás del ejemplo de reconocimiento facial.
- [Andrew Ng, Machine Learning Yearning](https://info.deeplearning.ai/machine-learning-yearning-book): el libro que cita Karim sobre cómo partir datos y priorizar errores.
