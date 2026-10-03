# Guía de implementación: Aprendizaje Supervisado (Diplodatos, FAMAF UNC, Karim Nemer Pelliza y Diego González Dondo)

**Videos:** C1P1, C1P2, C2P1, C2P2, C3P1, C3P2, C4P1, C4P2. Ocho videos, 14:25:19 en total, grabados entre el 26 de junio y el 4 de julio de 2026.
**De qué va:** la parte práctica de la materia, ordenada por tema y no por clase: cómo preparar el entorno y las particiones, y cómo entrenar, evaluar y ajustar SVM, SVR, redes densas, convolucionales y recurrentes, un fine tuning de DistilBERT, ensambles con XGBoost y un recomendador con Surprise. Cierra con las buenas prácticas de la última clase y lo que se sabe del trabajo práctico de Kaggle. El apunte de estudio que acompaña a esta guía (`aprendizaje-supervisado-apunte-de-estudio.md`) tiene la teoría y las correcciones de cada clase.

> Nota: los links llevan al minuto de la clase donde se ve cada cosa ("C3P1 1:02:15" es la clase 3, parte 1, en la hora 1, minuto 2, segundo 15). La transcripción de C4P2 se hizo con faster-whisper porque la grabación no dejó bajar sus subtítulos, así que sus citas son menos fieles. No tuve acceso a las notebooks de la materia ni a la librería `mlutils`: el código de esta guía está escrito de nuevo siguiendo lo que se ve en pantalla y lo que se dice, con los mismos datasets cuando son públicos. Todo lo probé en el box con Python 3.13, scikit-learn 1.9.1, NumPy 2.2.4, Keras 3.15.1 (backend PyTorch, CPU), XGBoost 3.4.1, Surprise 1.1.5 y Transformers 5.18; los números que muestro salen de esas corridas, con pocas épocas para que entren en una CPU. Lo que no pude comprobar está marcado como **para verificar**, lo que no se entiende bien del audio como **dudoso**, y las ideas mías como **Sugerencia**.

## Checklist para arrancar ya
1. Armá un entorno virtual con scikit-learn, Keras con un backend, XGBoost, Surprise y `transformers[torch]`, y guardá `pip freeze` para tu grupo (sección 1).
2. Antes de entrenar nada, mirá los datos: tipos, nulos, desbalance y correlaciones; probá primero lo más simple (estadística, regresión logística) C4P2 6:03.
3. Separá entrenamiento, validación y prueba estratificados; la prueba se mira una sola vez al final C4P2 17:17.
4. Fijá la métrica de optimización y los umbrales de las de satisfacción antes de empezar C4P2 33:52.
5. Calculá las líneas base bobas (clase más frecuente, uniforme, estratificada) con `DummyClassifier` C4P2 35:16.
6. Meté el escalado dentro de un `Pipeline` y escalá siempre para SVM, vecinos y redes (no hace falta para árboles) C1P1 2:09:04.
7. En SVM empezá por el kernel lineal; después RBF con C y gamma barridos en escala logarítmica con `GridSearchCV` C1P1 2:01:47.
8. Con desbalance, usá `class_weight="balanced"` y medí con F1 macro o accuracy balanceada, no con accuracy C1P1 1:13:24.
9. Para redes, sobreajustá a propósito 100 ejemplos como chequeo de sanidad antes de entrenar con todo C2P2 27:18.
10. Entrená en Keras con `EarlyStopping(restore_best_weights=True)` y `ModelCheckpoint`, y pasá los argumentos de `compile` con nombre C2P2 3:05.
11. En imágenes, usá transfer learning con la base congelada y aumento de datos con capas `Random*`, solo si los aumentos son físicamente posibles C2P2 1:38:21, C4P2 1:09:42.
12. Para texto, probá LSTM antes que SimpleRNN, y para algo serio, fine tuning de un Transformer preentrenado C3P1 1:04:14, C3P2 20:51.
13. En datos tabulares, usá random forest como modelo a vencer y mirá el `oob_score_`; después probá XGBoost con poca profundidad y muchos árboles C3P2 1:01:50.
14. Registrá cada experimento (fecha, datos, configuración, métricas) en un CSV o en MLflow C4P2 40:33.
15. Analizá los errores: listá los mal clasificados y buscá qué tienen en común C4P2 1:00:04.
16. Para el TP: armá el equipo en Kaggle, superá el baseline con al menos tres modelos distintos del árbol, subí un CSV con id y clase y la misma cantidad de filas que el test, no ajustes mirando la tabla pública y entregá la notebook con todo el análisis C4P2 1:41:20, C4P2 1:57:50.

## Versión completa

### 1. Preparar el entorno
**En clase:** C1P1 44:40, C2P1 1:02:06, C2P1 1:06:32, C3P1 1:11:32, C3P2 0:29, C3P2 1:34, C3P2 3:16, C4P1 0:34, C4P1 49:49.

Diego corre las notebooks en Jupyter local y pasa a Colab cuando su máquina no da (graficar el árbol de XGBoost o el fine tuning de DistilBERT); Karim prefiere entrenar en sus máquinas para no subir datos propios C4P2 4:31. Cualquiera de las dos sirve; lo que importa es fijar versiones.

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install "scikit-learn>=1.5" numpy pandas matplotlib xgboost scikit-surprise
pip install keras torch            # Keras 3 con backend PyTorch (o tensorflow, que es el default)
pip install "transformers[torch]" datasets accelerate
pip freeze > requirements.txt      # para que tu grupo tenga las mismas versiones
```

Qué tenés que saber:
- `transformers` solo no instala torch; `transformers[torch]` sí C3P2 3:16.
- Keras 3 corre sobre TensorFlow, PyTorch o JAX. Para elegir PyTorch, poné `os.environ["KERAS_BACKEND"] = "torch"` antes del `import keras`. En Colab viene con TensorFlow y no hace falta tocar nada.
- `scikit-surprise` 1.1.5 anda con NumPy 2 (probado en el box con 2.2.4).
- La librería `mlutils` de la materia está en el repositorio del curso: si usás Colab, subila junto con la notebook C1P1 44:40. No la tuve, así que esta guía no la usa.
- **Sugerencia:** si trabajás en Colab, no subas datos sensibles de terceros; para la competencia de Kaggle podés usar también las notebooks de Kaggle, que tienen GPU gratis con cupo semanal (**para verificar** el cupo vigente).

### 2. Particiones, métricas y líneas base
**En clase:** C1P1 17:51, C1P1 24:43, C1P1 1:59:01, C2P2 33:33, C4P2 14:15, C4P2 16:32, C4P2 18:00, C4P2 19:30, C4P2 29:26, C4P2 31:34, C4P2 33:52, C4P2 35:16, C4P2 36:50.

Qué tenés que hacer:
- Separá entrenamiento, validación y prueba con la misma distribución que la población; estratificá si hay clases chicas. En C4P2 el ejemplo es un dataset de 230.000 imágenes satelitales de barcos con una clase de solo 530 C4P2 16:32: con un sorteo simple esa clase puede no aparecer en validación ni en prueba.
- Tamaños típicos: 80/20 o 70/10/20; con muchos datos, la prueba puede ser un porcentaje chico mientras tenga la distribución de la población C4P2 18:00, C4P2 18:46.
- Elegí una **métrica de optimización** (la que vas a mejorar) y fijá umbrales para las **métricas de satisfacción** (tiempo de entrenamiento, de inferencia, un recall mínimo) **antes** de empezar, y acordalos con quien pide el modelo C4P2 31:34, C4P2 33:52.
- Con desbalance, el accuracy engaña: usá F1 macro, accuracy balanceada o las curvas ROC y precisión recall C4P2 29:26, C4P2 30:55.
- Calculá siempre una línea base "boba": la clase más frecuente, al azar uniforme y al azar respetando las proporciones. Tu modelo tiene que superarlas C4P2 35:16, C4P2 36:50.
- La prueba se mira una sola vez, al final. En la competencia de Kaggle, esa parte la tiene la cátedra, como el cliente que se guarda su test C4P2 19:30.

El código de la sección 12 (`g10_practicas.py`) arma un 70/10/20 estratificado con 5 clases desbalanceadas y calcula las tres líneas base. En el box, la más frecuente da accuracy 0,498 pero F1 macro 0,133; la uniforme 0,178 y la estratificada 0,220 de F1 macro. Un random forest con todos los datos llega a 0,632 y un SVC buscado al azar a 0,70 en test.

### 3. SVM para clasificación y kernels
**En clase:** C1P1 28:03, C1P1 36:05, C1P1 50:43, C1P1 1:07:19, C1P1 1:13:24, C1P1 1:23:08, C1P1 1:36:46, C1P1 2:01:47, C1P1 2:09:04.

Qué tenés que hacer:
- Escalá siempre (dentro de un `Pipeline`, así el escalado se ajusta solo con los datos de entrenamiento de cada fold).
- Empezá por `LinearSVC` o `SVC(kernel="linear")`; si no alcanza, probá RBF y polinomial.
- Barré C en escala logarítmica (0,001 a 1000) y gamma igual; mirá la brecha entre entrenamiento y validación.
- Con clases desbalanceadas, probá `class_weight="balanced"` y medí con el reporte por clase, no con el accuracy.
- Si necesitás probabilidades, usá `CalibratedClassifierCV` (en scikit-learn 1.9 `SVC(probability=True)` está obsoleto).

```python
# g01_svm.py
import numpy as np
from sklearn.datasets import make_blobs, make_circles
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC, SVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import classification_report, confusion_matrix, f1_score
from sklearn.utils.class_weight import compute_class_weight

# 1. Hinge loss: max(0, 1 - y f(x)), con y en {-1, 1}
yf = np.array([2, 1, 0.5, 0, -1])
print("hinge:", np.maximum(0, 1 - yf))

# 2. Barrido de C con escalado
X, y = make_blobs(n_samples=500, centers=2, cluster_std=2.0, random_state=0)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=0, stratify=y)
for C in [0.001, 0.1, 10, 1000]:
    m = make_pipeline(StandardScaler(), LinearSVC(C=C, max_iter=20000)).fit(Xtr, ytr)
    print(f"C={C}: train {m.score(Xtr, ytr):.3f} test {m.score(Xte, yte):.3f}")

# 3. Desbalance: pesos inversos a la frecuencia
X, y = make_blobs(n_samples=[400, 100], centers=[[0, 0], [2, 2]], cluster_std=1.2, random_state=1)
print("pesos balanced:", compute_class_weight("balanced", classes=np.array([0, 1]), y=y))
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)
for cw in [None, "balanced"]:
    m = make_pipeline(StandardScaler(), SVC(kernel="linear", class_weight=cw)).fit(Xtr, ytr)
    print("class_weight =", cw)
    print(classification_report(yte, m.predict(Xte), digits=3))

# 4. Kernels en círculos y GridSearchCV con Pipeline
X, y = make_circles(n_samples=500, noise=0.1, factor=0.4, random_state=0)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=0, stratify=y)
for k in ["linear", "sigmoid", "rbf", "poly"]:
    m = make_pipeline(StandardScaler(), SVC(kernel=k, degree=2)).fit(Xtr, ytr)
    print(f"kernel {k}: test {m.score(Xte, yte):.2f}")
pipe = Pipeline([("sc", StandardScaler()), ("svc", SVC())])
grid = [{"svc__kernel": ["rbf"], "svc__C": [0.1, 1, 10, 100], "svc__gamma": [0.01, 0.1, 1, 10]},
        {"svc__kernel": ["poly"], "svc__C": [0.1, 1, 10], "svc__degree": [2, 3]}]
gs = GridSearchCV(pipe, grid, cv=5, scoring="f1").fit(Xtr, ytr)
print("mejor:", gs.best_params_, f"cv {gs.best_score_:.3f} test {gs.score(Xte, yte):.3f}")

# 5. Probabilidades sin SVC(probability=True), que está obsoleto en scikit-learn 1.9
cal = CalibratedClassifierCV(make_pipeline(StandardScaler(), SVC(kernel="rbf")), ensemble=False).fit(Xtr, ytr)
print("proba:", cal.predict_proba(Xte[:3]).round(3))
print("decision_function:", gs.best_estimator_.decision_function(Xte[:3]).round(3))

# 6. Matriz de confusión: filas = clase real, columnas = predicha
yt = np.array([1, 1, 1, 1, 0, 0, 0, 0]); yp = np.array([1, 1, 0, 0, 0, 0, 0, 0])
print(confusion_matrix(yt, yp))
P, R = 1.0, 0.5
print("F1 sklearn", round(f1_score(yt, yp), 3), "armónica", round(2*P*R/(P+R), 3), "geométrica", round(np.sqrt(P*R), 3))
```

Lo que da en el box (scikit-learn 1.9.1):
- La hinge loss para y·f(x) = 2, 1, 0,5, 0 y −1 vale 0, 0, 0,5, 1 y 2: crece linealmente, no es 0 o 1 como se dijo en C1P1 36:05.
- Los pesos "balanced" para 400 y 100 son 0,625 y 2,5. El recall de la clase chica sube de 0,767 a 0,967 y su precisión baja de 0,852 a 0,674: es un intercambio, como en la clase (81% a 94%).
- En círculos: lineal 0,55, sigmoide 0,59, RBF 1,00 y polinomial 0,99. El GridSearch elige RBF con C = 1 y gamma = 1.
- La matriz de confusión de ejemplo `[[4 0] [2 2]]` tiene las clases reales en las filas: el recall de la clase 1 es 2/(2+2) = 0,5, leído por fila. F1 = 0,667, que es la media armónica (la geométrica daría 0,707).

### 4. SVR
**En clase:** C1P2 0:10, C1P2 10:43, C1P2 16:57, C1P2 32:27, C1P2 40:40, C1P2 43:48, C1P2 48:48, C1P2 50:55.

Qué tenés que hacer:
- Elegí ε según el error que te da igual en las unidades del objetivo; C y gamma por búsqueda.
- Recordá los valores por defecto: ε = 0,0 en `LinearSVR` y 0,1 en `SVR`.
- SVR con kernel escala mal con la cantidad de muestras (más o menos cuadrático en memoria y entre cuadrático y cúbico en tiempo): con decenas de miles de filas probá primero con una muestra, o pasá a `LinearSVR` o a árboles.
- Un R² negativo en test no es necesariamente un error de código: significa que el modelo predice peor que la media.

```python
# g02_svr.py
import numpy as np
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR, LinearSVR
from sklearn.metrics import mean_squared_error, r2_score

print("epsilon por defecto: LinearSVR", LinearSVR().epsilon, "SVR", SVR().epsilon)
rng = np.random.RandomState(0)
X = np.sort(5 * rng.rand(200, 1), axis=0); y = np.sin(X).ravel() + 0.1 * rng.randn(200)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0)
for k in ["linear", "poly", "rbf"]:
    m = make_pipeline(StandardScaler(), SVR(kernel=k, C=10, degree=3)).fit(Xtr, ytr)
    print(f"{k}: MSE {mean_squared_error(yte, m.predict(Xte)):.4f}")
for eps in [0.0, 0.1, 0.3, 0.5]:
    m = SVR(kernel="rbf", C=10, epsilon=eps).fit(Xtr, ytr)
    print(f"epsilon {eps}: vectores de soporte {len(m.support_)}")
gs = GridSearchCV(SVR(kernel="rbf"), {"C": [0.1, 1, 10, 100], "epsilon": [0.01, 0.1, 0.2, 0.5],
                  "gamma": ["scale", 0.1, 1, 10]}, cv=5, scoring="neg_mean_squared_error").fit(Xtr, ytr)
print("candidatos", len(gs.cv_results_["params"]), "ajustes", len(gs.cv_results_["params"]) * 5, gs.best_params_)
print("R2 test", round(r2_score(yte, gs.predict(Xte)), 3))
print("un modelo peor que la media da R2 negativo:", r2_score([1, 2, 3], [3, 2, 1]))

# California housing: SVR escala mal con n; probá primero con una muestra
c = fetch_california_housing()
Xtr, Xte, ytr, yte = train_test_split(c.data, c.target, test_size=0.2, random_state=0)
m = make_pipeline(StandardScaler(), SVR(kernel="rbf", C=1, epsilon=0.1)).fit(Xtr[:5000], ytr[:5000])
print("California (5000 de entrenamiento): RMSE test", round(mean_squared_error(yte, m.predict(Xte)) ** 0.5, 3))
```

Lo que da en el box:
- MSE en la senoidal: lineal 0,23, polinomial 0,31, RBF 0,009. RBF gana, como en clase.
- Con ε = 0; 0,1; 0,3 y 0,5 quedan 140, 48, 4 y 2 vectores de soporte: nunca cero.
- El GridSearch de 4 × 4 × 4 son 64 candidatos y 320 ajustes con 5 folds, igual que en C1P2 48:48; elige C = 10 y ε = 0,1, con R² 0,98.
- California con 5000 filas de entrenamiento: RMSE 0,605 en test, en segundos. Con las 16.512 filas tarda varios minutos, que es lo que le pasó a Diego en C1P2 56:57.

### 5. Redes en scikit-learn
**En clase:** C2P1 1:14:54, C2P1 1:16:37, C2P1 1:27:39, C2P1 1:29:12, C2P1 1:31:15, C2P1 1:46:25.

Qué tenés que hacer:
- `hidden_layer_sizes=(5,)` es una capa de 5 neuronas; `(64, 32)` son dos capas.
- Usá `early_stopping=True` con `n_iter_no_change` para cortar cuando la validación deja de mejorar.
- Para algo más que un ejercicio, pasá a Keras o PyTorch: `MLPClassifier` no usa GPU.

```python
# g03_mlp.py
import numpy as np, warnings
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.exceptions import ConvergenceWarning
warnings.filterwarnings("ignore", category=ConvergenceWarning)
X, y = make_classification(n_samples=600, n_features=192, n_informative=20, random_state=0)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0)
m = MLPClassifier(hidden_layer_sizes=(5,), solver="sgd", learning_rate_init=0.001, batch_size=20,
                  max_iter=1000, early_stopping=True, n_iter_no_change=10, random_state=0).fit(Xtr, ytr)
print("capas (entrada + ocultas + salida):", m.n_layers_, "formas de pesos:", [w.shape for w in m.coefs_])
print("neuronas de salida:", m.n_outputs_, "activación de salida:", m.out_activation_)
print("predict_proba:", m.predict_proba(Xte[:2]).round(3), "iteraciones:", m.n_iter_)
print(f"train {m.score(Xtr, ytr):.3f} test {m.score(Xte, yte):.3f}")
print("parámetros de 64x64x3 -> 5 -> 1:", 12288 * 5 + 5 + 5 * 1 + 1)
```

Lo que da en el box: `n_layers_` = 3 (entrada, una oculta, salida), pesos de forma (192, 5) y (5, 1), una sola neurona de salida logística y `predict_proba` con dos columnas. La cuenta de parámetros de la red de gato o no gato da 61.451, igual que el `summary` de la clase.

### 6. Redes en Keras: densas, callbacks y dropout
**En clase:** C2P1 1:48:18, C2P2 0:20, C2P2 3:05, C2P2 6:30, C2P2 15:55, C2P2 21:00, C2P2 23:54, C2P2 27:18, C2P2 28:24, C2P2 42:32.

Qué tenés que hacer:
- Pasá los argumentos de `compile` siempre con nombre (`optimizer=`, `loss=`, `metrics=`). En Keras 3 el tercer argumento posicional es `loss_weights`, no `metrics`, y falla.
- Usá `EarlyStopping(restore_best_weights=True)` y `ModelCheckpoint(save_best_only=True)`: es la respuesta al "se cortó la luz a las 4 horas y media" C2P2 3:05.
- Antes de entrenar con todo, sobreajustá 100 ejemplos: si la pérdida no llega cerca de cero, hay un error C2P2 27:18.
- Para multiclase: `softmax` en la salida y `categorical_crossentropy` con one hot (o `sparse_categorical_crossentropy` con enteros). El índice del argmax es la clase.

```python
# g04_keras_densa.py
import os; os.environ["KERAS_BACKEND"] = "torch"   # en Colab podés dejar TensorFlow
import keras, numpy as np
from keras import layers, regularizers
keras.utils.set_random_seed(0)
print("keras", keras.__version__, keras.backend.backend())

# Red de "gato o no gato": 64x64x3 = 12288 entradas, 5 ocultas, 1 salida sigmoide
gato = keras.Sequential([keras.Input((64 * 64 * 3,)),
                         layers.Dense(5, activation="relu", kernel_regularizer=regularizers.l2(0.01)),
                         layers.Dense(1, activation="sigmoid")])
gato.compile(optimizer=keras.optimizers.SGD(learning_rate=0.005), loss="binary_crossentropy", metrics=["accuracy"])
print("parámetros gato:", gato.count_params())

# MNIST con dropout, checkpoints y parada temprana
(xtr, ytr), (xte, yte) = keras.datasets.mnist.load_data()
xtr = xtr.reshape(-1, 784).astype("float32") / 255; xte = xte.reshape(-1, 784).astype("float32") / 255
ytr_oh = keras.utils.to_categorical(ytr, 10)
print("etiqueta", ytr[0], "one hot", ytr_oh[0])
m = keras.Sequential([keras.Input((784,)),
                      layers.Dense(256, activation="relu", kernel_regularizer=regularizers.l2(1e-4)),
                      layers.Dropout(0.2),
                      layers.Dense(256, activation="relu"),
                      layers.Dropout(0.2),
                      layers.Dense(10, activation="softmax")])
m.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])  # siempre con nombres
print("parámetros MNIST:", m.count_params())
cbs = [keras.callbacks.EarlyStopping(monitor="val_loss", patience=2, restore_best_weights=True),
       keras.callbacks.ModelCheckpoint("/tmp/mnist_mejor.keras", monitor="val_loss", save_best_only=True)]
h = m.fit(xtr, ytr_oh, batch_size=128, epochs=3, validation_split=0.1, callbacks=cbs, verbose=0)
print({k: [round(v, 3) for v in vs] for k, vs in h.history.items()})
p = m.predict(xte[:1], verbose=0)[0]
print("argmax", p.argmax(), "etiqueta real", yte[0], "probabilidad", round(float(p.max()), 3))
mejor = keras.models.load_model("/tmp/mnist_mejor.keras")
print("test del checkpoint:", round(mejor.evaluate(xte, keras.utils.to_categorical(yte, 10), verbose=0)[1], 3))

# Chequeo de sanidad: sobreajustar 100 ejemplos
s = keras.models.clone_model(m); s.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
hs = s.fit(xtr[:100], ytr_oh[:100], epochs=60, verbose=0)
print("sanidad: pérdida final", round(hs.history["loss"][-1], 3), "accuracy", round(hs.history["accuracy"][-1], 3))

# Dropout: en entrenamiento apaga al azar y escala; en inferencia no hace nada
d = layers.Dropout(0.5); x = np.ones((1, 8), dtype="float32")
print("dropout entrenando:", keras.ops.convert_to_numpy(d(x, training=True)))
print("dropout infiriendo:", keras.ops.convert_to_numpy(d(x, training=False)))
```

Lo que da en el box (Keras 3.15.1 con backend PyTorch, CPU):
- Parámetros: gato 61.451 y MNIST 269.322 (los "270.000" de C2P2 23:54).
- MNIST en 3 épocas: entrenamiento 0,901, 0,958 y 0,969; validación 0,969, 0,975 y 0,976. La validación queda arriba porque el dropout solo actúa al entrenar. Test del checkpoint: 0,973.
- La primera imagen de test da argmax 7 y la etiqueta real es 7.
- El chequeo de sanidad con 100 ejemplos llega a pérdida 0,025 y accuracy 1,0.
- `Dropout(0.5)` entrenando devuelve `[2, 0, 2, 2, ...]` (apaga al azar y escala por 1/(1 − p)) y en inferencia devuelve la entrada sin tocar.

### 7. CNN, aumento de datos y transfer learning
**En clase:** C2P2 1:00:00, C2P2 1:26:19, C2P2 1:29:29, C2P2 1:31:04, C2P2 1:31:44, C2P2 1:36:05, C2P2 1:38:21, C2P2 1:41:05.

Qué tenés que hacer:
- Agregá el canal a las imágenes en escala de grises: forma (28, 28, 1).
- Hacé el aumento de datos con capas (`RandomFlip`, `RandomRotation`, `RandomZoom`) dentro del modelo: solo actúan al entrenar. `ImageDataGenerator` ya no existe en Keras 3.15.
- Elegí aumentos que produzcan imágenes posibles; con pocas épocas el aumento hace que la red converja más lento.
- Transfer learning: congelá la base entera (`base.trainable = False`) y entrená una cabeza nueva; recién después, si querés, descongelá las últimas capas con una tasa baja (1e-5).

```python
# g05_cnn.py
import os; os.environ["KERAS_BACKEND"] = "torch"
import keras, numpy as np
from keras import layers
keras.utils.set_random_seed(0)
(xtr, ytr), (xte, yte) = keras.datasets.fashion_mnist.load_data()
xtr = xtr[..., None].astype("float32") / 255; xte = xte[..., None].astype("float32") / 255   # agregar canal
aumento = keras.Sequential([layers.RandomFlip("horizontal"), layers.RandomRotation(0.05),
                            layers.RandomZoom(0.1)], name="aumento")   # reemplaza ImageDataGenerator
cnn = keras.Sequential([keras.Input((28, 28, 1)),
                        aumento,                      # solo actúa al entrenar
                        layers.Conv2D(32, 3, activation="relu"), layers.MaxPooling2D(2),
                        layers.Conv2D(64, 3, activation="relu"), layers.MaxPooling2D(2),
                        layers.Flatten(), layers.Dropout(0.25),
                        layers.Dense(128, activation="relu"), layers.Dense(10, activation="softmax")])
cnn.summary(line_length=80)
cnn.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
es = keras.callbacks.EarlyStopping(monitor="val_loss", patience=2, restore_best_weights=True)
h = cnn.fit(xtr[:20000], ytr[:20000], batch_size=64, epochs=3, validation_split=0.1, callbacks=[es], verbose=0)
print({k: [round(v, 3) for v in vs] for k, vs in h.history.items()})
print("test:", round(cnn.evaluate(xte, yte, verbose=0)[1], 3))
from sklearn.metrics import confusion_matrix
pred = cnn.predict(xte, verbose=0).argmax(1)
cm = confusion_matrix(yte, pred); print("remera (0) predicha como camisa (6):", cm[0, 6], "camisa como remera:", cm[6, 0])

# Transfer learning: base congelada + cabeza nueva
base = keras.applications.MobileNetV2(input_shape=(96, 96, 3), include_top=False, weights="imagenet")
base.trainable = False
tl = keras.Sequential([keras.Input((96, 96, 3)), layers.Rescaling(1 / 127.5, offset=-1), base,
                       layers.GlobalAveragePooling2D(), layers.Dropout(0.2), layers.Dense(10, activation="softmax")])
ent = sum(int(np.prod(w.shape)) for w in tl.trainable_weights)
noent = sum(int(np.prod(w.shape)) for w in tl.non_trainable_weights)
print("MobileNetV2 base:", base.count_params(), "entrenables:", ent, "no entrenables:", noent)
# Fine tuning: descongelar solo las últimas capas de la base y bajar la tasa
base.trainable = True
for capa in base.layers[:-20]: capa.trainable = False
tl.compile(optimizer=keras.optimizers.Adam(1e-5), loss="sparse_categorical_crossentropy", metrics=["accuracy"])
print("entrenables tras descongelar 20 capas:", sum(int(np.prod(w.shape)) for w in tl.trainable_weights))
```

Lo que da en el box:
- El `summary` da 225.034 parámetros: 320, 18.496, 204.928 y 1.290. Si la notebook de clase daba "250.000" C2P2 1:29:29, usa otra cantidad de filtros o de neuronas.
- Con 20.000 imágenes, 3 épocas, aumento y dropout: 0,814 en test. Remera y camisa son la confusión principal (167 y 142 casos), como en C2P2 1:34:29.
- MobileNetV2 sin la cabeza tiene 2.257.984 parámetros (los "2.250.000" de C2P2 1:38:21). Con la base congelada solo se entrenan 12.810 (la capa densa nueva); al descongelar las últimas 20 capas pasan a ser 1.218.890.

### 8. RNN y LSTM
**En clase:** C3P1 44:12, C3P1 46:20, C3P1 47:29, C3P1 48:39, C3P1 52:37, C3P1 1:01:32, C3P1 1:05:27, C3P1 1:11:32.

Qué tenés que hacer:
- Rellená o recortá las secuencias a un largo fijo con `pad_sequences`.
- Para apilar capas recurrentes, todas menos la última llevan `return_sequences=True`.
- Para predecir una crítica nueva con el IMDB de Keras, sumá 3 a los índices de `get_word_index()` (0 es relleno, 1 inicio y 2 palabra desconocida) y marcá con 2 las palabras fuera del vocabulario. Si no, la red ve otras palabras.
- Fijá las versiones (`pip freeze > requirements.txt`) y trabajá en un entorno virtual; el problema de `word_index` de C3P1 1:11:32 es de versiones.

```python
# g06_rnn.py
import os; os.environ["KERAS_BACKEND"] = "torch"
import keras, numpy as np, re, time
from keras import layers
keras.utils.set_random_seed(0)
V, L = 10000, 200
(xtr, ytr), (xte, yte) = keras.datasets.imdb.load_data(num_words=V)   # índices desplazados en 3
xtr = keras.utils.pad_sequences(xtr[:5000], maxlen=L); ytr = ytr[:5000]
xte = keras.utils.pad_sequences(xte[:2000], maxlen=L); yte = yte[:2000]
for celda in (layers.SimpleRNN, layers.LSTM):
    m = keras.Sequential([keras.Input((L,)), layers.Embedding(V, 32), celda(32), layers.Dense(1, activation="sigmoid")])
    print(celda.__name__, [c.count_params() for c in m.layers])
apiladas = keras.Sequential([keras.Input((L,)), layers.Embedding(V, 32),
                             layers.SimpleRNN(32, return_sequences=True),   # devuelve toda la secuencia
                             layers.SimpleRNN(32), layers.Dense(1, activation="sigmoid")])
print("dos SimpleRNN apiladas:", apiladas.count_params())
m = keras.Sequential([keras.Input((L,)), layers.Embedding(V, 32), layers.LSTM(32), layers.Dense(1, activation="sigmoid")])
m.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
t = time.time(); h = m.fit(xtr, ytr, epochs=3, batch_size=128, validation_split=0.2, verbose=0)
print("LSTM val", [round(v, 3) for v in h.history["val_accuracy"]], "test", round(m.evaluate(xte, yte, verbose=0)[1], 3), round(time.time() - t), "s")

# Predecir una crítica nueva: ojo con el desplazamiento de 3 (0 relleno, 1 inicio, 2 desconocida)
wi = keras.datasets.imdb.get_word_index()
def codificar(texto):
    ids = [1] + [wi[w] + 3 if w in wi and wi[w] + 3 < V else 2 for w in re.findall(r"[a-z']+", texto.lower())]
    return keras.utils.pad_sequences([ids], maxlen=L)
inv = {v + 3: k for k, v in wi.items()}
print("decodificada:", " ".join(inv.get(i, "?") for i in xtr[0] if i > 2)[:80])
for t in ["This movie was wonderful, the acting was brilliant and I loved the story.",
          "Terrible film. Boring, too long and the worst acting I have seen."]:
    print(round(float(m.predict(codificar(t), verbose=0)[0, 0]), 3), t[:40])
```

Lo que da en el box:
- Parámetros: Embedding 320.000, SimpleRNN 2.080, LSTM 8.320, Dense 33; la LSTM tiene 4 veces los de la SimpleRNN (no menos, como se dijo en C3P1 1:01:32).
- LSTM con 5000 críticas, largo 200 y 3 épocas: validación 0,621, 0,74 y 0,836; test 0,831, en 33 segundos de CPU. En otra corrida con la SimpleRNN, en las mismas condiciones, el test dio 0,613.
- La crítica positiva de ejemplo da 0,672 y la negativa 0,276.

### 9. Fine tuning de DistilBERT con Hugging Face
**En clase:** C3P2 3:16, C3P2 4:23, C3P2 8:48, C3P2 10:19, C3P2 13:10, C3P2 18:09, C3P2 19:48, C3P2 20:51, C3P2 25:17.

Qué tenés que hacer:
- Instalá torch además de transformers (`pip install "transformers[torch]" datasets accelerate`); en Colab ya viene.
- En Transformers 5 el argumento es `eval_strategy` (el viejo `evaluation_strategy` ya no va), y conviene `report_to=[]` si no usás un servicio de seguimiento.
- En CPU usá un subconjunto chico y `max_length` de 128 o 256 para probar; en Colab con GPU podés hacer las 3000 y 1000 críticas de la clase.

```python
# g09_finetune.py
import numpy as np, time, torch
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
from sklearn.metrics import accuracy_score, f1_score
torch.manual_seed(0)
ds=load_dataset("stanfordnlp/imdb"); print(ds)
tr=ds["train"].shuffle(seed=42).select(range(400)); te=ds["test"].shuffle(seed=42).select(range(200))
tok=AutoTokenizer.from_pretrained("distilbert-base-uncased")
f=lambda b: tok(b["text"],truncation=True,padding="max_length",max_length=128)
tr=tr.map(f,batched=True); te=te.map(f,batched=True)
model=AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased",num_labels=2)
def compute_metrics(p):
    preds=np.argmax(p.predictions,axis=-1); return {"accuracy":accuracy_score(p.label_ids,preds),"f1":f1_score(p.label_ids,preds)}
args=TrainingArguments(output_dir="/tmp/distil_imdb",eval_strategy="epoch",save_strategy="no",learning_rate=2e-5,per_device_train_batch_size=16,per_device_eval_batch_size=32,num_train_epochs=1,logging_steps=10,report_to=[],seed=0)
trainer=Trainer(model=model,args=args,train_dataset=tr,eval_dataset=te,compute_metrics=compute_metrics)
t=time.time(); trainer.train(); print("train s",round(time.time()-t)); print(trainer.evaluate())
enc=tok("This movie was really good, the acting and the story were excellent.",return_tensors="pt")
with torch.no_grad(): print("pred",model(**{k:v.to(model.device) for k,v in enc.items()}).logits.softmax(-1))
```

Lo que da en el box (CPU, 400 críticas de entrenamiento y 200 de prueba, largo 128, una época, 194 segundos de entrenamiento):
- El tokenizador devuelve `input_ids` y `attention_mask`; "Transformers are powerful models" da `[101, 19081, 2024, 3928, 4275, 102]` (101 y 102 son `[CLS]` y `[SEP]`), y "unbelievably" se parte en `un ##bel ##ie ##va ##bly`.
- La configuración de DistilBERT: dimensión 768, 6 capas, 12 cabezas, dropout 0,1 y vocabulario de 30.522; todos los IDs se decodifican a un token.
- Con tan pocos datos y una época el modelo apenas aprende: accuracy 0,605 y F1 0,32 en las 200 de prueba, y la crítica positiva de ejemplo sale 0,48 positiva. El código anda de punta a punta; para llegar al 0,87 de la clase C3P2 25:17 hacen falta las 3000 críticas y 2 épocas, que en CPU tardan horas y en una GPU de Colab unos minutos.
- **Sugerencia:** si no tenés GPU, congelá DistilBERT y entrená solo la cabeza, o sacá los embeddings del `[CLS]` y pasalos a una regresión logística: es lo mismo que hace la cátedra con ResNet en el TP.

### 10. Ensambles: bagging, random forest y boosting
**En clase:** C3P2 36:56, C3P2 38:45, C3P2 51:04, C3P2 55:03, C3P2 1:03:25, C3P2 1:05:46, C3P2 1:13:48, C3P2 1:22:37, C3P2 1:23:45, C3P2 1:32:12, C4P1 7:50, C4P1 12:14, C4P1 13:53.

Qué tenés que hacer:
- Usá random forest como modelo a vencer en datos tabulares: casi no necesita ajuste ni escalado.
- Mirá el `oob_score_`: es una validación gratis con los ejemplos que quedaron fuera de cada bootstrap.
- No saques conclusiones de 10 contra 15 árboles con un test chico: promediá varias semillas o usá validación cruzada.
- En voting blando, todos los modelos tienen que dar `predict_proba`.
- En XGBoost probá menos profundidad y más árboles con una tasa baja; y compará siempre con un modelo simple.

```python
# g07_ensambles.py
import numpy as np, warnings; warnings.filterwarnings("ignore")
from math import comb, log
from sklearn.datasets import load_breast_cancer, make_moons, load_diabetes, load_wine
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (RandomForestClassifier, BaggingClassifier, AdaBoostClassifier,
                              GradientBoostingClassifier, VotingClassifier)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, recall_score
import xgboost as xgb

p = 0.8; print("mayoría de 5 con p=0,8:", round(sum(comb(5, k) * p**k * (1 - p)**(5 - k) for k in (3, 4, 5)), 5))
for e in (0.30, 0.21, 0.137): print(f"AdaBoost eps={e}: alpha={0.5 * log((1 - e) / e):.3f}")
rng = np.random.RandomState(0); n = 10000
print("fracción única en bootstrap:", round(len(np.unique(rng.randint(0, n, n))) / n, 3))

X, y = load_breast_cancer(return_X_y=True)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
t = DecisionTreeClassifier(random_state=0).fit(Xtr, ytr)
print(f"árbol: train {t.score(Xtr, ytr):.3f} test {t.score(Xte, yte):.3f}")
for n_est in (1, 10, 20, 100):
    sc = [RandomForestClassifier(n_estimators=n_est, random_state=s).fit(Xtr, ytr).score(Xte, yte) for s in range(5)]
    print(f"RF {n_est} árboles: media {np.mean(sc):.3f} (min {min(sc):.3f}, max {max(sc):.3f})")
rf = RandomForestClassifier(n_estimators=300, oob_score=True, random_state=0, n_jobs=-1).fit(Xtr, ytr)
print("OOB", round(rf.oob_score_, 3), "test", round(rf.score(Xte, yte), 3), "recall malignos", round(recall_score(yte, rf.predict(Xte), pos_label=0), 3))
nombres = load_breast_cancer().feature_names
print("importancias (suman", round(rf.feature_importances_.sum(), 3), "):", [nombres[i] for i in np.argsort(rf.feature_importances_)[::-1][:4]])
for nombre, m in [("bagging", BaggingClassifier(DecisionTreeClassifier(), n_estimators=100, random_state=0)),
                  ("pasting", BaggingClassifier(DecisionTreeClassifier(), n_estimators=100, bootstrap=False, max_samples=0.8, random_state=0)),
                  ("AdaBoost", AdaBoostClassifier(n_estimators=200, random_state=0)),
                  ("GradientBoosting", GradientBoostingClassifier(random_state=0))]:
    print(f"{nombre}: test {m.fit(Xtr, ytr).score(Xte, yte):.3f}")

# Voting duro y blando (SVC calibrado en vez de probability=True)
X, y = make_moons(n_samples=400, noise=0.3, random_state=0)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0)
est = [("knn", make_pipeline(StandardScaler(), KNeighborsClassifier(5))),
       ("svc", CalibratedClassifierCV(make_pipeline(StandardScaler(), SVC(C=10, kernel="rbf")), ensemble=False)),
       ("mlp", make_pipeline(StandardScaler(), MLPClassifier((10, 10, 10), max_iter=2000, random_state=0))),
       ("arbol", DecisionTreeClassifier(max_depth=5, random_state=0))]
for v in ("hard", "soft"):
    print(f"voting {v}: {VotingClassifier(est, voting=v).fit(Xtr, ytr).score(Xte, yte):.3f}")
vc = VotingClassifier(est, voting="soft").fit(Xtr, ytr)
print("blando = promedio de probabilidades:", np.mean([e.predict_proba(Xte[:1])[0] for e in vc.estimators_], 0).round(3), vc.predict_proba(Xte[:1]).round(3))

# XGBoost: diabetes es regresión; los árboles no necesitan escalar
d = load_diabetes(); print("diabetes objetivo de", d.target.min(), "a", d.target.max())
Xtr, Xte, ytr, yte = train_test_split(d.data, d.target, test_size=0.2, random_state=0)
for nombre, m in [("como en clase (prof. 10, 10 árboles)", xgb.XGBRegressor(max_depth=10, n_estimators=10)),
                  ("más árboles, menos profundos", xgb.XGBRegressor(max_depth=3, n_estimators=300, learning_rate=0.05, subsample=0.8))]:
    print(f"XGB {nombre}: R2 {r2_score(yte, m.fit(Xtr, ytr).predict(Xte)):.3f}")
from sklearn.linear_model import LinearRegression
print(f"regresión lineal de referencia: R2 {r2_score(yte, LinearRegression().fit(Xtr, ytr).predict(Xte)):.3f}")
w = load_wine(); cv = StratifiedKFold(4, shuffle=True, random_state=0)
for nombre, m in [("XGB", xgb.XGBClassifier(n_estimators=10, max_depth=5)), ("RF", RandomForestClassifier(random_state=0))]:
    print(f"vinos {nombre}: {cross_val_score(m, w.data, w.target, cv=cv).mean():.3f}")
print("objetivo multiclase:", xgb.XGBClassifier().fit(w.data, w.target).get_params()["objective"])
```

Lo que da en el box:
- 0,94208 para la mayoría de 5 modelos de 0,8; α de AdaBoost 0,424, 0,662 y 0,920; un bootstrap tiene 63,3% de ejemplos únicos.
- Cáncer de mama: el árbol solo da 1,000 en entrenamiento y 0,918 en test. El bosque promedia 0,923 con 1 árbol, 0,940 con 10, 0,939 con 20 y 0,943 con 100: se estabiliza. OOB 0,972 y test 0,942. Las importancias suman 1 y las primeras son worst perimeter, worst concave points, worst radius y worst area.
- Bagging 0,942, pasting 0,924, AdaBoost 0,959 y gradient boosting 0,942.
- Voting en lunas: duro 0,925, blando 0,917; las probabilidades del blando son exactamente el promedio de las de cada modelo.
- Diabetes (objetivo de 25 a 346, regresión): XGBoost como en clase R² 0,191, con más árboles 0,176, y una regresión lineal 0,332. Con 442 filas y poca señal, el modelo simple gana.
- Vinos con validación cruzada de 4 partes: XGBoost 0,927, random forest 0,978. El objetivo multiclase es `multi:softprob`.

### 11. Sistemas de recomendación
**En clase:** C4P1 32:51, C4P1 34:33, C4P1 36:16, C4P1 37:25, C4P1 46:26, C4P1 49:49, C4P1 57:17, C4P1 59:24, C4P1 1:01:07, C4P1 1:04:33, C4P1 1:16:04.

Qué tenés que hacer:
- Para entender la cuenta, hacé el filtro colaborativo a mano en una matriz chica.
- En Book Crossing separá los ceros (interacciones implícitas) de las notas de 1 a 10 antes de entrenar; si no, el RMSE mide otra cosa.
- Filtrá usuarios y libros con pocas puntuaciones, como en la notebook (al menos 50).
- Compará BaselineOnly, SVD y KNNWithMeans con validación cruzada.
- SVD en Surprise no es la descomposición de álgebra lineal: es una factorización r̂ = μ + b_u + b_i + p_u·q_i ajustada por descenso de gradiente sobre las notas observadas (el algoritmo de Simon Funk, popularizado en el premio Netflix). El código de abajo la implementa en diez líneas.

```python
# g08_recsys.py
import numpy as np, pandas as pd
# 1. Filtro colaborativo por usuarios "a mano" (ejemplo clásico de Alice; en clase, Claudia)
R = np.array([[5, 3, 4, 4, np.nan], [3, 1, 2, 3, 3], [4, 3, 4, 3, 5], [3, 3, 1, 5, 4], [1, 5, 5, 2, 1]])
def pearson(a, b):
    m = ~np.isnan(R[a]) & ~np.isnan(R[b]); ra, rb = R[a, m], R[b, m]
    da, db = ra - ra.mean(), rb - rb.mean()
    return da @ db / np.sqrt((da @ da) * (db @ db))
sims = {u: pearson(0, u) for u in range(1, 5)}
print("Pearson:", {f"U{u}": round(s, 2) for u, s in sims.items()})
vecinos = sorted([u for u in sims if sims[u] > 0], key=lambda u: -sims[u])[:2]   # k=2, similitud positiva
pred = np.nanmean(R[0]) + sum(sims[u] * (R[u, 4] - np.nanmean(R[u])) for u in vecinos) / sum(sims[u] for u in vecinos)
print("predicción para Claudia, ítem 5:", round(pred, 2))
# coseno ajustado entre ítems (resta la media de cada usuario)
def coseno_ajustado(i, j):
    us = [u for u in range(5) if not np.isnan(R[u, i]) and not np.isnan(R[u, j])]
    d = np.array([(R[u, i] - np.nanmean(R[u]), R[u, j] - np.nanmean(R[u])) for u in us])
    return d[:, 0] @ d[:, 1] / np.sqrt((d[:, 0] @ d[:, 0]) * (d[:, 1] @ d[:, 1]))
print("coseno ajustado ítem 5 contra 1..4:", [round(coseno_ajustado(4, j), 2) for j in range(4)])

# 2. Qué hace SVD (factorización): r_ui ~ mu + b_u + b_i + p_u . q_i, ajustado por descenso de gradiente
rng = np.random.RandomState(0)
obs = [(u, i, R[u, i]) for u in range(5) for i in range(5) if not np.isnan(R[u, i])]
mu = np.mean([r for _, _, r in obs]); k = 2
bu, bi = np.zeros(5), np.zeros(5); P, Q = rng.normal(0, .1, (5, k)), rng.normal(0, .1, (5, k))
for _ in range(500):
    for u, i, r in obs:
        e = r - (mu + bu[u] + bi[i] + P[u] @ Q[i])
        bu[u] += 0.01 * (e - 0.02 * bu[u]); bi[i] += 0.01 * (e - 0.02 * bi[i])
        P[u], Q[i] = P[u] + 0.01 * (e * Q[i] - 0.02 * P[u]), Q[i] + 0.01 * (e * P[u] - 0.02 * Q[i])
print("SVD casero, Claudia ítem 5 (recortado a 1..5):", round(float(np.clip(mu + bu[0] + bi[4] + P[0] @ Q[4], 1, 5)), 2))

# 3. Surprise: los ceros implícitos hay que sacarlos antes
from surprise import Dataset, Reader, SVD, KNNWithMeans, BaselineOnly
from surprise.model_selection import cross_validate
nu, ni = 300, 200; b_u = rng.normal(0, 1, nu); b_i = rng.normal(0, 1, ni)
Pu, Qi = rng.normal(0, .7, (nu, 3)), rng.normal(0, .7, (ni, 3)); filas = []
for u in range(nu):
    for i in rng.choice(ni, 40, replace=False):
        r = np.clip(np.round(6 + b_u[u] + b_i[i] + Pu[u] @ Qi[i] + rng.normal(0, .8)), 1, 10)
        filas.append((f"u{u}", f"b{i}", r if rng.rand() > 0.6 else 0))   # 60% de ceros, como en Book Crossing
df = pd.DataFrame(filas, columns=["user", "isbn", "rating"])
print("proporción de ceros:", round((df.rating == 0).mean(), 2))
for nombre, d in [("con ceros", df), ("sin ceros", df[df.rating > 0])]:
    data = Dataset.load_from_df(d, Reader(rating_scale=(0 if nombre == "con ceros" else 1, 10)))
    for algo in [BaselineOnly(verbose=False), SVD(random_state=0), KNNWithMeans(verbose=False)]:
        r = cross_validate(algo, data, measures=["RMSE"], cv=3, verbose=False)
        print(f"{nombre} {type(algo).__name__}: RMSE {r['test_rmse'].mean():.3f}")
```

Lo que da en el box (Surprise 1.1.5):
- Pearson de Claudia con U1 a U4: 0,85, 0,71, 0,00 y −0,79; predicción para el ítem 5 con los 2 vecinos positivos: 4,87.
- El SVD casero predice 5 para el mismo ítem (recortado a la escala).
- Con 60% de ceros tratados como notas, el RMSE queda alrededor de 3,1 y gana BaselineOnly, como el 3,3 de la clase. Sin los ceros baja a 1,3 o 1,4 y gana SVD.

### 12. Buenas prácticas: líneas base, búsqueda y registro de experimentos
**En clase:** C4P2 6:03, C4P2 17:17, C4P2 35:16, C4P2 38:16, C4P2 40:33, C4P2 42:03, C4P2 42:50, C4P2 45:00, C4P2 49:34, C4P2 50:15, C4P2 51:46, C4P2 54:53, C4P2 1:00:04, C4P2 1:08:23, C4P2 1:14:17, C4P2 1:15:46, C4P2 1:26:21, C4P2 1:29:17, C4P2 1:31:33.

Qué tenés que hacer (resumen de la clase de Karim y de la notebook de Titanic de Diego):
- Empezá con un modelo rápido, con parámetros por defecto y una fracción de los datos, para ver la tendencia; agrandá después C4P2 39:01, C4P2 50:15.
- Compará varios modelos en una tabla y, si las métricas son parecidas, quedate con el más simple C4P2 1:29:17, C4P2 1:31:33.
- Usá búsqueda aleatoria cuando haya muchos hiperparámetros; guardá las tres o cuatro mejores configuraciones, no solo la mejor C4P2 49:34, C4P2 51:46.
- Registrá cada experimento. MLflow lo hace con interfaz web; un CSV con fecha, modelo, parámetros, tamaño de entrenamiento y métricas ya alcanza para un TP.
- Diagnosticá: si el error de entrenamiento es alto, el problema es sesgo (modelo más grande, menos regularización); si es bajo y el de validación alto, varianza (más datos, regularización, ensambles) C4P2 54:53.
- Hacé tests baratos antes de entrenar: formas de los arreglos, rangos de las salidas, que las probabilidades sumen 1, que no haya fuga de datos (por ejemplo, escalar antes de dividir) C4P2 1:14:17.
- Imputá y codificá dentro del `Pipeline` (con `SimpleImputer`, `OneHotEncoder` y `ColumnTransformer`), así las mismas transformaciones se aplican a validación y a test sin fuga C4P2 1:26:21, C4P2 1:52:32.

```python
# g10_practicas.py
import numpy as np, pandas as pd, json, time, os
from datetime import datetime
from scipy.stats import loguniform
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, RandomizedSearchCV, StratifiedKFold
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import f1_score, balanced_accuracy_score, accuracy_score

# Datos desbalanceados: 5 clases, una muy chica (como los barcos de C4P2)
X, y = make_classification(n_samples=6000, n_features=20, n_informative=8, n_classes=5,
                           weights=[0.5, 0.25, 0.15, 0.08, 0.02], random_state=0)
# 70/10/20 estratificado: la clase chica aparece en las tres particiones
Xtmp, Xte, ytmp, yte = train_test_split(X, y, test_size=0.2, stratify=y, random_state=0)
Xtr, Xva, ytr, yva = train_test_split(Xtmp, ytmp, test_size=0.125, stratify=ytmp, random_state=0)
for nombre, yy in [("población", y), ("train", ytr), ("val", yva), ("test", yte)]:
    print(nombre, len(yy), np.bincount(yy) / len(yy))

# Líneas base "bobas": cualquier modelo tiene que superarlas
for s in ["most_frequent", "uniform", "stratified"]:
    d = DummyClassifier(strategy=s, random_state=0).fit(Xtr, ytr); p = d.predict(Xva)
    print(f"dummy {s}: accuracy {accuracy_score(yva, p):.3f} balanced {balanced_accuracy_score(yva, p):.3f} f1 macro {f1_score(yva, p, average='macro'):.3f}")

# Registro de experimentos en un CSV (MLflow hace esto mismo con interfaz web)
LOG = "/tmp/experimentos.csv"
if os.path.exists(LOG): os.remove(LOG)
def registrar(modelo, params, n_train, metricas):
    fila = {"fecha": datetime.now().isoformat(timespec="seconds"), "modelo": modelo,
            "params": json.dumps(params), "n_train": n_train, **metricas}
    pd.DataFrame([fila]).to_csv(LOG, mode="a", header=not os.path.exists(LOG), index=False)

# Empezar simple y con una parte de los datos; crecer después
for frac in [0.1, 0.3, 1.0]:
    n = int(len(ytr) * frac)
    for nombre, m in [("logistica", make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000))),
                      ("random_forest", RandomForestClassifier(n_estimators=200, random_state=0, n_jobs=-1))]:
        t = time.time(); m.fit(Xtr[:n], ytr[:n]); p = m.predict(Xva)
        registrar(nombre, m.get_params(deep=False) if nombre == "random_forest" else {}, n,
                  {"f1_macro": round(f1_score(yva, p, average="macro"), 3), "segundos": round(time.time() - t, 2)})
print(pd.read_csv(LOG)[["modelo", "n_train", "f1_macro", "segundos"]])

# Búsqueda aleatoria: más barata que la grilla cuando hay muchos hiperparámetros
rs = RandomizedSearchCV(make_pipeline(StandardScaler(), SVC()),
                        {"svc__C": loguniform(1e-2, 1e3), "svc__gamma": loguniform(1e-4, 1e0)},
                        n_iter=15, scoring="f1_macro", cv=StratifiedKFold(5, shuffle=True, random_state=0),
                        random_state=0, n_jobs=-1).fit(Xtr, ytr)
print("mejores:", {k: round(v, 4) for k, v in rs.best_params_.items()}, "cv", round(rs.best_score_, 3))
top = pd.DataFrame(rs.cv_results_).sort_values("rank_test_score").head(3)[["params", "mean_test_score"]]
print(top.to_string(index=False))   # guardá varias configuraciones buenas, no solo la mejor
print("test final (una sola vez):", round(f1_score(yte, rs.predict(Xte), average="macro"), 3))
```

Lo que da en el box:
- El 70/10/20 estratificado deja la clase chica (2,1%) con la misma proporción en las tres particiones.
- Líneas base en validación: la más frecuente tiene accuracy 0,498 pero accuracy balanceada 0,200 y F1 macro 0,133; la uniforme 0,178 de F1 macro y la estratificada 0,220. Si mirás solo accuracy, la más frecuente parece aceptable.
- El registro muestra que con el 10% de los datos la regresión logística gana (0,516 contra 0,452) y con el 100% gana el random forest (0,632): el orden de los modelos puede cambiar con el tamaño de los datos, por eso conviene crecer de a poco.
- La búsqueda aleatoria de 15 combinaciones de C y gamma llega a 0,68 en validación cruzada y 0,702 en test, mirado una sola vez.

### 13. El trabajo práctico: la competencia de Kaggle
**En clase:** C1P1 2:12:28, C4P2 1:36:02, C4P2 1:37:34, C4P2 1:39:50, C4P2 1:40:34, C4P2 1:41:20, C4P2 1:43:32, C4P2 1:48:02, C4P2 1:50:16, C4P2 1:52:32, C4P2 1:54:51, C4P2 1:57:50, C4P2 1:58:31, C4P2 2:00:13.

Lo que se sabe de la competencia (detalles en el módulo 14 del apunte):
- Clasificar caras con o sin barbijo a partir del vector de características de una ResNet 101, más ancho, alto y promedio RGB del recorte. `train` con etiqueta y `test` sin ella; el envío es un CSV con id y clase, con tantas filas como el test (Diego dice 524).
- Métrica: accuracy balanceada. Baseline: un árbol sin configurar. Hay que probar al menos tres modelos distintos del árbol, participar y entregar la notebook.
- La tabla pública usa el 26% del test; la final, el 74% restante. Hay un límite de envíos por día.

El código de abajo reproduce el flujo con datos **simulados** con la misma forma (1800 filas de entrenamiento con 256 características y 30% de la clase positiva, 524 de test), porque no tuve acceso al dataset real. Los nombres de las columnas (`image_id`, `clase`) y los textos de las clases son **para verificar** contra el archivo `sample_submission` de la competencia.

```python
# g11_kaggle.py
import numpy as np, pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_val_score, GridSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

# Datos simulados con la forma del TP (en el TP: pd.read_csv("train.csv") y pd.read_csv("test.csv"))
rng = np.random.RandomState(0); d = 256
def simular(n, con_etiqueta=True):
    y = (rng.rand(n) < 0.3).astype(int)                       # 30% sin barbijo: desbalance
    X = rng.normal(0, 1, (n, d)) + y[:, None] * rng.normal(0, 0.35, d)
    df = pd.DataFrame(X, columns=[f"f{i}" for i in range(d)])
    df.insert(0, "rgb_mean", rng.uniform(80, 160, n)); df.insert(0, "alto", rng.randint(60, 200, n))
    df.insert(0, "ancho", rng.randint(60, 200, n)); df.insert(0, "image_id", np.arange(n))
    df.insert(1, "clase", np.where(y == 1, "cara sin barbijo", "cara con barbijo") if con_etiqueta else None)
    return df
train, test = simular(1800), simular(524, con_etiqueta=False)

y = (train["clase"] == "cara sin barbijo").astype(int)       # 1 = lo que queremos detectar
X = train.drop(columns=["image_id", "clase"]); X_test = test.drop(columns=["image_id", "clase"])
print("proporción sin barbijo:", round(y.mean(), 3), "| columnas:", X.shape[1])

cv = StratifiedKFold(5, shuffle=True, random_state=0)
modelos = {"arbol (baseline)": DecisionTreeClassifier(random_state=0),
           "logistica": make_pipeline(StandardScaler(), LogisticRegression(max_iter=3000, class_weight="balanced")),
           "svc_rbf": make_pipeline(StandardScaler(), SVC(class_weight="balanced")),
           "random_forest": RandomForestClassifier(n_estimators=300, class_weight="balanced", n_jobs=-1, random_state=0),
           "xgboost": XGBClassifier(n_estimators=300, max_depth=3, learning_rate=0.1, scale_pos_weight=(1 - y.mean()) / y.mean())}
res = {n: cross_val_score(m, X, y, cv=cv, scoring="balanced_accuracy", n_jobs=-1).mean() for n, m in modelos.items()}
print(pd.Series(res).sort_values(ascending=False).round(3).to_string())

gs = GridSearchCV(make_pipeline(StandardScaler(), LogisticRegression(max_iter=3000, class_weight="balanced")),
                  {"logisticregression__C": [0.001, 0.01, 0.1, 1]}, cv=cv, scoring="balanced_accuracy").fit(X, y)
print("mejor C:", gs.best_params_, "cv", round(gs.best_score_, 3))

# El pipeline aplica al test exactamente las mismas transformaciones que al train
pred = gs.best_estimator_.predict(X_test)
sub = pd.DataFrame({"image_id": test["image_id"], "clase": pred.astype(int)})
sub.to_csv("/tmp/submission.csv", index=False)
print(sub.shape, sub.columns.tolist(), "filas OK" if len(sub) == len(test) else "FALTAN FILAS")
```

Lo que da en el box (con los datos simulados, así que los números solo muestran el flujo):
- Accuracy balanceada en validación cruzada estratificada: regresión logística 0,995, SVC 0,994, XGBoost 0,955, random forest 0,948 y el árbol 0,757. Sobre vectores de una red preentrenada, los modelos lineales suelen andar muy bien; probalos primero.
- El CSV sale con 524 filas y dos columnas.

Errores típicos que conviene evitar:
- Codificar la clase al revés: el TP quiere detectar a quien no tiene barbijo, así que esa es la clase 1 C4P2 1:48:02.
- Ajustar el escalado o la imputación con train y test juntos: es fuga de datos. Con el `Pipeline` no pasa.
- Elegir el modelo por la tabla pública. Usá tu validación cruzada; la tabla privada decide C4P2 2:03:01.
- Gastar los envíos del día en variaciones mínimas: probá en local y subí solo lo que mejora en validación cruzada.
- **para verificar:** la fecha de cierre (27 de julio según C1P1, "18 días" según el Overview que muestra Diego) y el límite de envíos diarios.

## Glosario
- **Accuracy balanceada:** promedio del recall de cada clase; un clasificador que responde siempre la clase mayoritaria da 1/(cantidad de clases).
- **Backpropagation:** cálculo del gradiente de la pérdida respecto de cada peso con la regla de la cadena, de la salida hacia la entrada.
- **Bagging:** ensamble del mismo modelo entrenado sobre muestras bootstrap (con reemplazo) y combinado por voto o promedio. Sin reemplazo se llama pasting.
- **Boosting:** ensamble secuencial en el que cada modelo corrige los errores del anterior (AdaBoost repondera ejemplos; gradient boosting ajusta el gradiente de la pérdida).
- **C (en SVM):** inversa de la fuerza de regularización; C alto castiga más los errores y deja un margen más angosto.
- **Callback:** función que Keras llama durante el entrenamiento (`EarlyStopping`, `ModelCheckpoint`).
- **Coseno ajustado:** similitud entre ítems que resta a cada nota la media del usuario.
- **Dropout:** apagar al azar una fracción de neuronas en cada paso de entrenamiento; en inferencia se usan todas.
- **Embedding:** capa que convierte IDs de tokens en vectores densos aprendidos.
- **Épsilon (en SVR):** ancho del tubo dentro del cual los errores no cuestan.
- **Fine tuning:** seguir entrenando un modelo preentrenado (o parte de él) con tus datos y una tasa baja.
- **Gamma (en RBF):** cuánto alcanza la influencia de cada punto; grande sobreajusta.
- **Hinge loss:** max(0, 1 − y·f(x)), la pérdida de la SVM.
- **Kernel:** función que calcula un producto interno en un espacio de mayor dimensión sin construirlo.
- **Línea base boba:** clasificador sin información (`DummyClassifier`) que marca el piso de las métricas.
- **LSTM:** red recurrente con compuertas que conserva mejor la información a largo plazo; tiene 4 veces los parámetros de una SimpleRNN.
- **OOB (out of bag):** ejemplos que quedaron fuera de un bootstrap; sirven como validación gratis.
- **Pearson (en recomendación):** correlación entre las notas de dos usuarios restando la media de cada uno.
- **Pooling:** reducción de resolución tomando el máximo o el promedio de una ventana.
- **Self attention:** mecanismo por el que cada token pondera a todos los demás con softmax(Q·Kᵀ/√d_k)·V.
- **SVD (en Surprise):** factorización r̂ = μ + b_u + b_i + p_u·q_i ajustada por descenso de gradiente.
- **Tabla pública y privada (Kaggle):** puntajes calculados con una parte del test durante la competencia y con el resto al cierre.
- **Transfer learning:** reutilizar una red entrenada en otro problema, con la base congelada y una cabeza nueva.
- **Vectores de soporte:** los puntos que definen la frontera (en SVR, los que están sobre el borde del tubo o fuera de él).

### Nombres que la transcripción deforma
| Se oye o se lee | Es |
|---|---|
| super vector machine | support vector machine (SVM) |
| King Los | hinge loss |
| ML utils | `mlutils` |
| softgar | softmax |
| squishy | `np.squeeze` |
| la vela en color | `LabelEncoder` |
| simple imputación | `SimpleImputer` |
| el balance aquí uve si | balanced accuracy |
| cagle, kail | Kaggle |
| Machine Learning Jaring | *Machine Learning Yearning* |
| Con Iset | Conicet |
| uve, el ové | aula virtual |
