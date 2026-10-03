# Guía de implementación: Introducción al Aprendizaje Automático (Diplodatos, FAMAF UNC, Vanessa Mainardi y Edgardo)

**Videos:** 10 partes grabadas de las cuatro clases de mayo y junio de 2026 en el canal de FAMAF UNC, C1P1 · C1P2 · C2P1 · C2P2 · C2P3 · C3P1 · C3P2 · C4P1 · C4P2 · C4P3 · Duración total: 14:22:21 (unas 14 horas y 20 minutos).
**De qué va:** Vanessa Mainardi y Edgardo enseñan a armar un esquema de aprendizaje supervisado de punta a punta: plantear el problema, separar los datos sin contaminar el test, arrancar con un modelo simple, elegir la complejidad con curvas de validación, regularizar, ajustar hiperparámetros con validación cruzada, elegir la métrica según el costo de cada error, elegir el umbral después de entrenar y lidiar con clases desbalanceadas. Esta guía junta lo que se puede aplicar; el detalle por tema, con las correcciones a lo dicho en clase, está en el apunte de estudio (`introduccion-aprendizaje-automatico-apunte-de-estudio.md`).

> Nota: esta guía sale de los subtítulos automáticos en español de los 10 videos, todos con transcripción completa. Muchos nombres vienen deformados (ver el glosario al final). Lo que los docentes afirmaron y no chequeé va marcado como **para verificar**; lo poco claro, como **dudoso**. Algunas cosas sí las chequeé corriendo scikit-learn 1.9.1 en el box, y lo digo en cada caso. Las ideas mías van marcadas como **Sugerencia**, y los fragmentos de código son todos sugerencias mías: los probé en el box con datos sintéticos, pero las notebooks de la materia no están transcriptas. Los fragmentos se encadenan como en una notebook: cada uno usa las variables de los anteriores. Los links dicen video y minuto: "C2P1 1:23:45" es la clase 2, parte 1, en 1:23:45.

---

## Checklist para arrancar ya

1. Antes de abrir un modelo, escribí qué querés predecir, si es regresión o clasificación y qué significa cada clase del target.
2. Hacé un análisis exploratorio mínimo: tamaño, tipos de variables, faltantes, distribuciones, target y balance de clases.
3. Escribí qué error es más grave en tu problema (falso positivo o falso negativo) y para quién, antes de elegir la métrica.
4. Separá el test al principio, estratificado si es clasificación, y no lo mires hasta el modelo final.
5. Fijá `random_state` en la partición y en los modelos para que tus resultados sean reproducibles.
6. Entrená primero un modelo simple con los valores por defecto como baseline y anotá sus métricas en train y en test.
7. Para cada hiperparámetro de complejidad (grado, K, profundidad), graficá el error de train y de validación y elegí donde la validación deja de mejorar.
8. Probá la regularización con valores en escala logarítmica y elegí el que mejor valida, no el más fuerte.
9. Escalá las variables antes de KNN, de los modelos lineales entrenados con gradiente y de cualquier modelo sensible a distancias.
10. Ajustá hiperparámetros con `GridSearchCV` o `RandomizedSearchCV` usando validación cruzada estratificada sobre el entrenamiento.
11. Pasale a la búsqueda una métrica alineada con tu objetivo (`f1`, `recall`, `average_precision`) en lugar de dejar la exactitud por defecto.
12. Mirá la media y el desvío de la métrica entre folds para juzgar la estabilidad del modelo.
13. Reentrená el modelo elegido con todo el entrenamiento y evaluá una sola vez en el test.
14. Reportá exactitud, precisión, recall, F1 y la matriz de confusión, e interpretá qué tipo de error comete el modelo.
15. En multiclase, reportá el macro y el micro average y explicá cuál usás para decidir.
16. Si el modelo devuelve probabilidades, elegí el umbral con las curvas PR o ROC sobre validación, no sobre el test.
17. Con clases desbalanceadas, empezá por pesos de clase inversos a la frecuencia (`class_weight="balanced"`) antes de remuestrear.
18. Si remuestreás (SMOTE, submuestreo), hacelo solo dentro del entrenamiento de cada fold.
19. En regresión, reportá RMSE o MAE en las unidades del target y R², y graficá los residuos.
20. Compará los modelos en una tabla y justificá la recomendación con evidencia, no copiando números.
21. Si usaste IA para programar o redactar, revisá lo que te dio y dejá escrito qué corregiste: el responsable sos vos.

---

## Versión completa

### 1. Plantear el problema antes que el modelo
**Dónde:** C1P1 13:04, C1P1 37:33, C1P1 57:43, C4P3 1:01:21, C4P3 1:03:13, C4P3 1:04:05, C4P3 1:06:39, C4P2 30:57

**Contexto.** Qué modelo usar depende del tipo de problema y del análisis exploratorio; "si uno va ciego..." Lo que define si es regresión o clasificación es la variable respuesta: con las mismas casas, el precio es regresión y el tipo de propiedad es clasificación. El práctico 2 pide arrancar por comprender el problema y el dataset, el target, el balance de clases y el costo de cada error, con preguntas como qué significan las clases 0 y 1 o qué información adicional le pedirías al banco.

**Por qué importa.** Si no definiste qué error es más caro, la métrica la elige el default, y la exactitud puede verse excelente mientras el modelo no detecta lo que importa.

**Cómo implementarlo.**
1. Escribí en una frase qué se predice, para quién y con qué decisión se va a usar.
2. Identificá el target y anotá qué significa cada valor.
3. Hacé el análisis exploratorio mínimo: tamaño, tipos, faltantes, distribuciones, target y desbalance (`y.value_counts(normalize=True)`).
4. Escribí cuál es el falso positivo y cuál el falso negativo en tu caso, y cuál es más costoso para cada parte (por ejemplo, el banco y el cliente).
5. Validá tus intuiciones sobre relaciones (lineal, inversa, ninguna) con gráficos de pares y estadística descriptiva antes de modelar.

### 2. Separar los datos sin contaminar el test
**Dónde:** C1P1 50:37, C4P1 0:07, C4P1 1:46, C4P1 3:27, C1P2 44:10, C1P2 49:22, C1P2 53:14, C4P1 13:47, C2P1 3:26

**Contexto.** El test se separa antes de cualquier ajuste, queda "bajo llave" y se usa una sola vez con el modelo definitivo; si lo usás más de una vez queda contaminado. Las decisiones intermedias se toman con validación, dentro del entrenamiento. Con clases desbalanceadas, "sí o sí muestreo estratificado". Edgardo guarda incluso un cuarto conjunto de datos medidos por otros para el contraste final.

**Por qué importa.** Cada decisión que tomás mirando el test convierte al test en otro conjunto de validación, y tu estimación final deja de ser honesta.

**Cómo implementarlo.**
1. Separá el test al principio con `stratify=y` si es clasificación.
2. Fijá `random_state` para poder repetir la partición.
3. Pasá `test_size` o `train_size`, no los dos.
4. Hacé todo el resto (escalado, selección de variables, remuestreo, búsqueda) solo con el entrenamiento.

```python
# Sugerencia: partición estratificada y reproducible
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42)
```

### 3. Arrancar con un baseline simple
**Dónde:** C1P1 1:03:52, C2P2 8:00, C2P2 21:38, C4P3 1:08:45, C4P3 1:10:55

**Contexto.** "Siempre hay que empezar con el más simple" y complejizar después. Naive Bayes sirve como baseline porque entrenar es contar, aunque Vanessa advierte que un baseline demasiado pobre "te estás mintiendo vos mismo". El práctico 2 pide entrenar primero `SGDClassifier` y `DecisionTreeClassifier` con los valores por defecto, fijando solo la semilla, y recién después ajustar.

**Por qué importa.** Sin un punto de comparación no sabés si el modelo complejo aporta algo; si rinde parecido al simple, no tiene sentido.

**Cómo implementarlo.**
1. Entrená un modelo simple con los defaults y anotá sus métricas en train y en test.
2. Elegí un baseline razonable para el dominio (por ejemplo, para texto algo mejor que una bolsa de palabras trivial).
3. Cada modelo nuevo se compara contra ese baseline en la misma partición.

### 4. Elegir la complejidad con curvas de train y validación
**Dónde:** C1P1 1:16:07, C1P1 1:18:56, C1P2 1:16:39, C1P2 1:20:01, C1P2 1:21:08, C1P2 1:22:08, C2P3 17:17, C2P3 19:45, C3P1 1:15:43, C4P1 28:15, C4P1 37:03

**Contexto.** El error de entrenamiento baja siempre al aumentar la complejidad; el de validación baja y después sube. Lo vieron con el grado del polinomio (el 3 gana con el seno), con K en KNN (K = 21 suaviza la frontera), con la profundidad del árbol (después de 7 u 8 memoriza). "El juez es la validación" y, entre dos modelos parecidos, gana el más simple.

**Por qué importa.** Un ajuste perfecto en entrenamiento es una ilusión: con tantos parámetros como datos, la curva pasa por todos los puntos y copia el ruido.

**Cómo implementarlo.**
1. Elegí el hiperparámetro de complejidad y una grilla de valores.
2. Para cada valor, calculá el score en train y el score de validación cruzada.
3. Graficá las dos curvas y elegí donde la validación deja de mejorar.
4. Si la escala te aplasta una curva, graficalas por separado o en escala logarítmica.

```python
# Sugerencia: curva de complejidad para un árbol
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
for d in [1, 2, 4, 8, None]:
    m = DecisionTreeClassifier(max_depth=d, random_state=42).fit(X_train, y_train)
    tr = m.score(X_train, y_train)
    va = cross_val_score(m, X_train, y_train, cv=cv, scoring="f1").mean()
    print(d, round(tr, 3), round(va, 3))
```

### 5. Regularizar y elegir lambda
**Dónde:** C1P1 1:23:28, C1P1 1:26:21, C1P1 1:28:01, C1P1 1:29:08, C1P2 5:37, C1P2 7:07, C2P1 46:47, C2P3 52:14

**Contexto.** La regularización suma al costo un término que penaliza los pesos grandes. Lambda se prueba en escala logarítmica; la penalización más fuerte da coeficientes estables pero no el mejor modelo. L2 (Ridge) achica los pesos; L1 (Lasso) lleva algunos a cero y sirve si sospechás que sobran variables. En scikit-learn, `alpha` de Ridge es lambda y `C` de `LogisticRegression` es su inversa.

**Por qué importa.** Con un modelo flexible y pocos datos, regularizar es lo que separa memorizar de generalizar.

**Cómo implementarlo.**
1. Escalá las variables antes de regularizar, para que la penalización sea pareja.
2. Probá valores en escala logarítmica (por ejemplo `np.logspace(-6, 2, 9)`).
3. Elegí el valor con mejor error de validación.
4. Cambiá una cosa por vez (grado o regularización) para saber qué funcionó, como recomienda Vanessa.

```python
# Sugerencia: polinomio de grado alto con Ridge y alpha en escala logarítmica
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV
pipe = make_pipeline(PolynomialFeatures(degree=9), StandardScaler(), Ridge())
search = GridSearchCV(pipe, {"ridge__alpha": np.logspace(-6, 2, 9)},
                      cv=5, scoring="neg_mean_squared_error")
search.fit(X_train, y_train)
print(search.best_params_)
```

### 6. Escalar cuando el modelo depende de distancias o de gradientes
**Dónde:** C2P3 22:04, C2P1 1:13:45, C4P3 1:08:45

**Contexto.** KNN depende de la métrica de distancia, así que hay que escalar o normalizar. Los algoritmos de gradiente "no trabajan bien con números grandes". Ojo: `load_digits` viene de 0 a 16 y no está normalizado, aunque en clase se dijo que sí (lo chequeé en el box).

**Por qué importa.** Sin escalar, la variable de mayor rango domina la distancia o el gradiente.

**Cómo implementarlo.**
1. Meté el escalador dentro de un `Pipeline`, así se ajusta solo con el entrenamiento de cada fold.
2. Usá `StandardScaler` por defecto; para píxeles alcanza con dividir por el máximo.
3. Los árboles no necesitan escalado.

### 7. Clasificadores lineales y regresión logística en la práctica
**Dónde:** C1P2 1:28:22, C1P2 1:50:16, C2P1 32:20, C2P1 38:32, C2P1 50:10, C2P1 1:07:30, C2P1 1:11:29, C2P1 1:23:51, C2P1 1:25:55, C2P1 1:29:00

**Contexto.** El perceptrón solo converge con datos linealmente separables y "generalmente no se usa, pero es la base de todo". La logística da el mismo hiperplano más una probabilidad, entrena con log loss (convexa) y es más robusta a outliers que usar una regresión lineal para clasificar. En la práctica con dígitos, `coef_` tiene una fila por clase y la matriz de confusión muestra qué dígitos se confunden.

**Por qué importa.** Las probabilidades te dejan elegir el umbral después; los coeficientes te dejan interpretar qué variables pesan.

**Cómo implementarlo.**
1. Usá `LogisticRegression` con un escalador; si avisa que no convergió, subí `max_iter` (100 por defecto, chequeado en scikit-learn 1.9.1).
2. Ajustá `C` (inversa de la regularización) con validación cruzada.
3. Mirá `predict_proba`, no solo `predict`.
4. Graficá la matriz de confusión con `normalize="true"` para ver tasas por clase (**Sugerencia**: con conteos, una clase chica bien clasificada se ve más clara que una grande).
5. **Para verificar:** en scikit-learn 1.9.1 el parámetro `penalty` figura como deprecado y la mezcla L1/L2 se controla con `l1_ratio`; revisá qué versión corre en tu Colab antes de copiar código de la clase.

### 8. Árboles y bosques sin sobreajuste
**Dónde:** C3P1 36:25, C3P1 1:08:51, C3P1 1:12:03, C3P1 1:16:19, C3P1 1:18:29, C3P2 16:51, C3P2 21:52, C3P2 39:34, C4P1 26:20, C4P1 30:01, C4P1 34:24, C4P1 35:25

**Contexto.** "Los árboles de decisión, por definición, tienen sobreajuste": sin restricciones, la exactitud de entrenamiento es 1.0. Se controlan con `max_depth` (complejidad global) y `min_samples_leaf` (suavizado), más `min_samples_split` y poda. El criterio (gini, entropy, log_loss) casi no cambia el árbol; "no inviertas tiempo" ahí. Un random forest promedia árboles diversos y reduce la varianza.

**Por qué importa.** Un árbol solo es interpretable pero inestable; el bosque es más estable pero menos legible.

**Cómo implementarlo.**
1. Entrená un árbol por defecto y mirá la profundidad que alcanza y la brecha entre train y test.
2. Ajustá `max_depth` y `min_samples_leaf` con validación cruzada.
3. Visualizá el árbol con `plot_tree(..., filled=True)` para explicar las reglas.
4. Compará contra un `RandomForestClassifier` variando `n_estimators`.
5. Mirá `feature_importances_` con cuidado: es una pista, no una prueba causal.

### 9. Optimización: tasa de aprendizaje, parada y semillas
**Dónde:** C3P2 1:25:51, C3P2 1:32:32, C3P2 1:35:18, C3P2 1:38:35, C3P2 1:42:05, C3P2 1:43:53, C1P2 1:51:22

**Contexto.** Casi todos los modelos, salvo la regresión lineal, se entrenan iterando. La tasa de aprendizaje muy chica es lenta; grande, rebota; muy grande, diverge. El rango común va de 10⁻⁴ a 10⁻¹, empezando grande y achicando. Se para por convergencia, por un máximo de iteraciones o por early stopping sobre validación. Con funciones no convexas el resultado depende del punto de inicio.

**Por qué importa.** Una curva de pérdida con picos o que no baja te avisa de un problema de optimización antes de que lo confundas con un problema de datos.

**Cómo implementarlo.**
1. Graficá la pérdida de train y de validación por iteración.
2. Si oscila o diverge, bajá la tasa de aprendizaje; si baja muy lento, subila.
3. Activá early stopping cuando el modelo lo permita (`early_stopping=True` en `SGDClassifier`).
4. Repetí con varias semillas; si con una converge y con otra no, sospechá de la superficie de costo.

### 10. Validación cruzada y búsqueda de hiperparámetros
**Dónde:** C4P1 5:08, C4P1 7:51, C4P1 9:27, C4P1 9:59, C4P1 11:50, C4P1 17:45, C4P1 20:40, C4P1 44:38, C4P1 49:18, C4P1 51:11, C4P1 1:03:27, C4P1 1:05:56, C4P1 1:12:15, C3P2 2:01:40, C4P2 29:10, C4P3 1:08:45

**Contexto.** La validación cruzada rota el conjunto de validación entre K partes y promedia, así que cada observación pasa una vez por validación. `StratifiedKFold` conserva las proporciones y la cantidad de folds no puede superar los casos de la clase minoritaria. En grid search cada combinación se evalúa en todos los folds; `cv_results_` trae media, desvío y ranking (el 1 es el mejor). El modelo final no es un promedio: es el elegido, reentrenado con todo el entrenamiento.

**Por qué importa.** Una sola partición puede ser poco afortunada; la media y el desvío entre folds te dicen cuánto confiar en el número.

**Cómo implementarlo.**
1. Definí un `StratifiedKFold` con `shuffle=True` y semilla.
2. Armá un `Pipeline` con el preprocesamiento y el modelo.
3. Pasá una grilla (o distribuciones con `RandomizedSearchCV`) y un `scoring` alineado con tu objetivo.
4. Mirá `mean_test_score` y `std_test_score`, no solo `best_score_`.
5. Usá `best_estimator_` (ya reentrenado con todo el entrenamiento por `refit=True`) para evaluar una vez en el test.

```python
# Sugerencia: búsqueda con validación cruzada estratificada y F1
import numpy as np
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import GridSearchCV, StratifiedKFold
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
pipe = make_pipeline(StandardScaler(), SGDClassifier(random_state=42))
grid = {"sgdclassifier__alpha": np.logspace(-5, 1, 7),
        "sgdclassifier__loss": ["hinge", "log_loss"],
        "sgdclassifier__class_weight": [None, "balanced"]}
search = GridSearchCV(pipe, grid, cv=cv, scoring="f1")
search.fit(X_train, y_train)
res = pd.DataFrame(search.cv_results_)
print(res[["params", "mean_test_score", "std_test_score", "rank_test_score"]]
      .sort_values("rank_test_score").head())
```

### 11. Elegir y leer las métricas de clasificación
**Dónde:** C4P2 7:54, C4P2 27:30, C4P2 30:57, C4P2 38:38, C4P2 42:27, C4P2 44:40, C4P2 48:21, C4P2 28:04, C4P3 3:53, C4P3 6:07, C4P3 7:50, C4P3 36:26, C4P3 39:09, C4P3 51:30, C4P3 52:01, C4P3 17:41

**Contexto.** La exactitud es engañosa con desbalance. La precisión importa cuando el falso positivo es caro (spam, alertas); el recall, cuando el falso negativo es caro (diagnóstico, fraude); F1 equilibra las dos para la clase positiva. "La métrica no se elige por comodidad técnica, se elige en función del problema real." En multiclase, el macro pesa igual a cada clase y el micro favorece a las grandes.

**Por qué importa.** Dos modelos con la misma exactitud pueden cometer errores muy distintos; la matriz de confusión te dice cuáles.

**Cómo implementarlo.**
1. Calculá exactitud, precisión, recall, F1 y la matriz de confusión con `classification_report` y `confusion_matrix`.
2. Recordá que en scikit-learn las filas son la clase real y las columnas la predicha.
3. Si necesitás el valor predictivo negativo, calculalo a mano: TN/(TN + FN).
4. Con dos clases que te importan por igual, mirá F1 macro o balanced accuracy, porque F1 solo mira la positiva.
5. **Para verificar:** con desbalance fuerte, el coeficiente de Matthews (`matthews_corrcoef`) resume la matriz entera en un número; lo propuso un alumno y los docentes no lo conocían.
6. Si una clase nunca se predice vas a ver `UndefinedMetricWarning`; revisá el modelo en lugar de silenciar la advertencia.

```python
# Sugerencia: reporte completo y NPV
from sklearn.metrics import classification_report, confusion_matrix
y_pred = search.best_estimator_.predict(X_test)
print(classification_report(y_test, y_pred, digits=3))
tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
print("NPV:", tn / (tn + fn))
```

### 12. Elegir el umbral después de entrenar
**Dónde:** C4P2 12:13, C4P2 22:56, C4P2 31:57, C4P2 32:59, C4P2 37:45, C4P2 41:46, C4P2 42:56, C4P2 45:42, C4P2 48:31, C4P3 27:07, C4P3 54:53

**Contexto.** En los modelos basados en score, el umbral se elige con el modelo ya entrenado. La curva ROC (TPR contra FPR) sirve para comparar modelos y para elegir umbral, con 0.5 de AUC como azar. Con desbalance, la ROC engaña y conviene la curva PR, cuyo baseline es la proporción de positivos. Mover el umbral no requiere reentrenar.

**Por qué importa.** El 0.5 por defecto rara vez es el umbral que minimiza el costo de tu problema.

**Cómo implementarlo.**
1. Obtené probabilidades de validación fuera de muestra con `cross_val_predict(..., method="predict_proba")`.
2. Calculá la curva PR (o ROC) y elegí el umbral según tu criterio (máximo F1, recall mínimo, costo).
3. Aplicá ese umbral fijo al test, sin volver a elegirlo ahí.
4. Reportá AUC y AUPRC junto con el umbral elegido.

```python
# Sugerencia: umbral que maximiza F1 sobre validación cruzada
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import precision_recall_curve, roc_auc_score, average_precision_score
lr = make_pipeline(StandardScaler(), LogisticRegression(class_weight="balanced", max_iter=1000))
scores = cross_val_predict(lr, X_train, y_train, cv=cv, method="predict_proba")[:, 1]
prec, rec, thr = precision_recall_curve(y_train, scores)
f1 = 2 * prec[:-1] * rec[:-1] / (prec[:-1] + rec[:-1] + 1e-12)
umbral = thr[f1.argmax()]
print(umbral, roc_auc_score(y_train, scores), average_precision_score(y_train, scores))
lr.fit(X_train, y_train)
y_pred_test = (lr.predict_proba(X_test)[:, 1] >= umbral).astype(int)
```

### 13. Clases desbalanceadas
**Dónde:** C4P3 8:36, C4P3 9:05, C4P3 9:43, C4P3 11:41, C4P3 13:13, C4P3 19:22, C4P3 26:35, C4P3 27:07, C4P1 13:47, C2P1 52:35

**Contexto.** El modelo se sesga hacia la clase mayoritaria. Las estrategias son submuestrear, sobremuestrear (SMOTE, ADASYN, aumentación de imágenes) o ponderar el costo sin tocar los datos, que es lo primero que prueba Vanessa porque conserva la distribución original. Duplicar ejemplos no siempre ayuda: depende del problema, y no se pueden inventar enfermedades ni electrocardiogramas.

**Por qué importa.** Con un 1% de positivos, un modelo que dice siempre "negativo" tiene 99% de exactitud y no sirve.

**Cómo implementarlo.**
1. Estratificá la partición y los folds.
2. Empezá con `class_weight="balanced"`, que da a cada clase un peso inverso a su frecuencia (n / (k · n_clase)). **Ojo:** en clase se dijo que el peso es la proporción de cada clase; eso favorece todavía más a la mayoritaria (ver el apunte, módulo 14).
3. Si remuestreás, hacelo solo dentro del entrenamiento de cada fold (por ejemplo con un pipeline de imbalanced-learn; **Sugerencia**, no se vio en clase).
4. Evaluá con precisión, recall, F1, AUPRC y la matriz de confusión, y ajustá el umbral.

```python
# Sugerencia: ver los pesos que usa class_weight="balanced"
import numpy as np
from sklearn.utils.class_weight import compute_class_weight
print(compute_class_weight("balanced", classes=np.unique(y_train), y=y_train))
# con 80/20 da algo como [0.63, 2.45]: más peso a la minoritaria
```

### 14. Métricas de regresión
**Dónde:** C4P3 31:12, C4P3 40:18, C4P3 41:24, C4P3 42:50, C4P3 44:09, C1P2 31:14, C1P2 57:16, C2P3 47:48

**Contexto.** El MSE penaliza los errores grandes y queda en unidades al cuadrado; el RMSE vuelve a las unidades del target; el MAE es más robusto a los extremos; R² compara contra predecir la media (negativo es peor que la media, y "si da 1 hay que sospechar"). Edgardo sugiere mirar si los residuos tienen forma gaussiana.

**Por qué importa.** Un error "de 0.5" no dice nada si no sabés en qué unidades está; en California Housing el target está en cientos de miles de dólares.

**Cómo implementarlo.**
1. Reportá RMSE o MAE en las unidades del target, más R².
2. Compará train y test para ver el sobreajuste.
3. Graficá el histograma de residuos y los residuos contra la predicción.

```python
# Sugerencia: métricas de regresión (con errores 2, 2 y 3 da MSE 5.67, RMSE 2.38)
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
mse = mean_squared_error(y_true, y_pred)
print(mse, np.sqrt(mse), mean_absolute_error(y_true, y_pred), r2_score(y_true, y_pred))
```

### 15. Documentar, justificar y usar IA con responsabilidad
**Dónde:** C2P3 38:36, C2P3 52:53, C1P2 46:45, C4P3 1:12:02, C2P1 53:11

**Contexto.** El objetivo de los prácticos no es correr modelos sino justificar elecciones e interpretar errores: qué modelo elegirías y por qué, con qué evidencia, qué advertencias harías. Sobre la IA: "los responsables de los resultados son ustedes", como el médico que firma el informe aunque lo haya ayudado una herramienta. Y sobre los outliers: "no es limpiar por limpiar".

**Por qué importa.** Un número sin interpretación no ayuda a decidir; una decisión sin evidencia no se puede defender.

**Cómo implementarlo.**
1. Armá una tabla comparativa con modelo, hiperparámetros, métrica media, desvío entre folds y resultado en test.
2. Escribí por qué esa métrica es la adecuada para el problema.
3. Indicá si el modelo es estable, si hay señales de sobreajuste y qué error te preocupa más.
4. Antes de borrar un outlier, explicá si es un error de carga o un caso real.
5. Si usaste IA, anotá para qué, qué verificaste y qué corregiste.

---

## Glosario

| Término | Qué significa en esta guía |
|---|---|
| Baseline | Modelo simple que sirve de punto de comparación |
| Hiperparámetro | Valor que elegís antes de entrenar (grado, K, profundidad, alpha, C, tasa de aprendizaje) |
| Validación cruzada | Rotar la validación entre K partes del entrenamiento y promediar |
| Estratificar | Mantener la proporción de clases en cada partición |
| `random_state` | Semilla que fija la serie pseudoaleatoria para poder repetir resultados |
| Regularización | Penalización de los pesos grandes en el costo (L2 Ridge, L1 Lasso) |
| `C` | Inversa de la regularización en `LogisticRegression` |
| Log loss | Entropía cruzada, el costo de la regresión logística |
| Early stopping | Cortar el entrenamiento cuando la validación deja de mejorar |
| Umbral | Valor de probabilidad a partir del cual se predice la clase positiva |
| Precisión | TP/(TP + FP): de lo que dijiste positivo, cuánto lo era |
| Recall | TP/(TP + FN): de los positivos reales, cuántos encontraste |
| F1 | Media armónica de precisión y recall |
| NPV | TN/(TN + FN): de lo que dijiste negativo, cuánto lo era |
| Macro y micro average | Promedio por clase con igual peso, o métrica sobre los conteos sumados |
| AUC | Área bajo la curva ROC; 0.5 es azar |
| AUPRC | Área bajo la curva PR; se compara con la proporción de positivos |
| SMOTE | Sobremuestreo que interpola entre vecinos de la clase minoritaria |
| `class_weight="balanced"` | Pesos de clase inversos a la frecuencia |

### Nombres que la transcripción deforma
| Como aparece | Qué es probablemente |
|---|---|
| cycle learn, cycit learn, sakarn | scikit-learn |
| M classification | `make_classification` |
| comorized | `CountVectorizer` |
| cross bar score | `cross_val_score` |
| Cafold, CFOL, Stratifier | `KFold`, `StratifiedKFold` |
| parámeter grid | `ParameterGrid` |
| max dep | `max_depth` |
| lif | leaf (`min_samples_leaf`) |
| trillol, trillón, trisol | threshold, umbral |
| acuracy, acurais, cura así | accuracy |
| récord, recol, rico | recall |
| curva rock, R cube | curva ROC, `roc_curve` |
| SMOE, adasín | SMOTE, ADASYN |
| Matthw | coeficiente de correlación de Matthews |
| NPB | NPV |
| resapha | `reshape` |
| softmap | softmax |
| vallas | bias |
