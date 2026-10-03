# Guía de implementación: Aprendizaje No Supervisado (Diplodatos, FAMAF UNC, Laura Alonso Alemany y Georgina Flesia)

**Videos:** 8 partes grabadas de las cuatro clases de julio y agosto de 2026 en el canal de FAMAF UNC, C1P1 · C1P2 · C2P1 · C2P2 · C3P1 · C3P2 · C4P1 · C4P2 · Duración total: 13:45:04 (unas 13 horas y 45 minutos).
**De qué va:** Laura Alonso Alemany y Georgina Flesia enseñan a explorar datos sin etiquetas: preparar y escalar las variables, elegir una distancia, correr y comparar algoritmos de clustering, elegir el número de grupos, evaluar contra "testigos" que conocés, mirar los datos con PCA, t-SNE y UMAP, aprovechar unos pocos datos etiquetados (semisupervisado) y, para otros tipos de datos, reglas de asociación, grafos y recomendación. Esta guía junta lo que se puede aplicar, sobre todo para el trabajo especial con FIFA 24; el detalle por tema, con las correcciones a lo dicho en clase, está en el apunte de estudio (`aprendizaje-no-supervisado-apunte-de-estudio.md`).

> Nota: esta guía sale de los subtítulos automáticos en español de 7 videos y de una transcripción hecha con faster-whisper para C3P2, que no tenía subtítulos descargables. Muchos nombres vienen deformados (ver el glosario al final). Lo que las docentes afirmaron y no chequeé va marcado como **para verificar**; lo poco claro, como **dudoso**. Algunas cosas sí las chequeé corriendo scikit-learn 1.9.1 en el box (y 1.6.1, parecida a Colab, cuando cambia algo), mlxtend 0.25, networkx 3.7, umap-learn 0.5 y Yellowbrick 1.5, y lo digo en cada caso. Las ideas mías van marcadas como **Sugerencia**, y los fragmentos de código son todos sugerencias mías: los probé en el box con un dataset sintético que imita los skills de FIFA (cuatro grupos de posiciones), porque no tengo las notebooks de la materia ni el CSV del trabajo. Los fragmentos se encadenan como en una notebook: cada uno usa las variables de los anteriores. Los links dicen video y minuto: "C2P1 1:23:45" es la clase 2, parte 1, en 1:23:45.

---

## Checklist para arrancar ya

1. Escribí la pregunta antes de tocar los datos: en el trabajo, si los skills permiten separar las posiciones de juego.
2. Bajá FIFA 24 de Kaggle, guardá una copia propia del CSV y revisá los nombres de las columnas, que pueden venir con mayúsculas o con el prefijo del factor.
3. Hacé el análisis exploratorio: tamaño, tipos, faltantes, histogramas de los skills y conteo de jugadores por posición.
4. Convertí las columnas tipo "85+3" a números y decidí qué hacés con los NaN de los arqueros en los puntajes por posición.
5. Separá las columnas que vas a usar para agrupar (los skills) de las que solo vas a usar para evaluar (posición, nombre, club).
6. Mirá pares de variables de factores distintos, por ejemplo finishing contra sliding tackle, para tener una intuición visual de los grupos.
7. Escalá los skills con StandardScaler antes de cualquier método basado en distancias.
8. Corré K-means para K entre 2 y 8 con varias inicializaciones y anotá la inercia y la silueta de cada K.
9. Probá al menos un jerárquico con varios linkages (ward, complete, average, single) y mirá el dendrograma truncado.
10. Si probás GMM, compará número de componentes y tipo de covarianza con BIC; si probás DBSCAN, elegí eps con el gráfico de k-distancias.
11. Armá un conjunto de testigos, unos 10 jugadores conocidos por posición, y medí homogeneidad, completitud, V-measure y ARI contra ellos.
12. Juntá todo en una tabla con una fila por agrupamiento y una columna por métrica, y explicá cómo elegiste cada hiperparámetro.
13. Proyectá con PCA, t-SNE y UMAP para mirar los grupos, y probá también agrupar sobre unas pocas componentes principales.
14. Interpretá cada grupo con sus testigos y con la tabla cruzada grupo por posición; nombrá lo que mezcla (el medio campo, por ejemplo).
15. Hacé tu interpretación primero y recién después pasale el mismo prompt a dos o más LLM para comparar coincidencias, diferencias y alucinaciones.
16. Dejá escrito qué probaste y descartaste, para responder "¿y no hiciste otra cosa?".

---

## Versión completa

### 1. Plantear la pregunta y conocer el dato
En no supervisado lo caro no es etiquetar sino analizar lo que sale, y para eso hace falta saber qué estás buscando y qué significan las variables C1P1 22:54, C1P1 15:10. Georgina insiste en pedir contexto: qué se midió, cómo y cuándo C1P2 37:05. En el trabajo la pregunta es si los skills separan las posiciones; las posiciones nunca entran al algoritmo, solo sirven para evaluar C1P2 55:25, C1P2 1:17:34.

**Qué hacer.** Escribí la pregunta en la primera celda. Separá desde el principio las columnas de agrupar y las de evaluar. Si una variable categórica parte los datos de entrada (como un GROUP BY), sacala del agrupamiento y usala para interpretar C1P2 17:23; pero mirá el agrupamiento dentro de cada categoría, porque a veces la categórica es la causa latente C4P1 1:28:02.

### 2. Exploración y columnas difíciles
Las columnas de FIFA traen trampas: valores y salarios con símbolos, puntajes por posición como texto "85+3", NaN de los arqueros en esas columnas y nombres de columnas que cambian entre versiones C1P2 58:20, C1P2 1:07:14, C1P2 1:10:05. Con overall mayor a 70 quedan unos 5.000 jugadores, pero se puede trabajar con todos C2P1 49:36. El FIFA 18 ya no está en Kaggle: guardá tu copia C2P2 37:09.

```python
# Sugerencia: datos sintéticos que imitan los skills de FIFA (reemplazalos por tu df real)
import numpy as np, pandas as pd
rng = np.random.default_rng(0)
skills = ["finishing","dribbling","ball_control","long_passing","short_passing",
          "interceptions","sliding_tackle","standing_tackle","gk_diving","gk_handling"]
perfil = {"ataque":[80,80,78,60,70,30,25,28,10,10],"medio":[60,72,76,75,78,60,55,58,10,10],
          "defensa":[35,50,58,60,65,78,80,80,10,10],"arquero":[12,15,20,30,30,15,12,12,80,78]}
filas = []
for pos, mu in perfil.items():
    n = 120 if pos == "arquero" else 400
    d = pd.DataFrame(rng.normal(mu, 8, size=(n, len(skills))).clip(1, 99).round(), columns=skills)
    d["pos_grupo"] = pos; filas.append(d)
df = pd.concat(filas, ignore_index=True)
df["name"] = [f"jugador_{i}" for i in range(len(df))]
df["ls"] = df["finishing"].astype(int).astype(str) + "+2"

# Sugerencia: convertir "85+3" en 88 (y "85-1" en 84)
def sumar_mas(s):
    return s.astype(str).str.extract(r"(\d+)\s*([+-])?\s*(\d+)?").apply(
        lambda r: np.nan if pd.isna(r[0]) else int(r[0]) + (int(r[2]) if r[1] == "+" else -int(r[2]) if r[1] == "-" else 0),
        axis=1)
df["ls_num"] = sumar_mas(df["ls"])
X = df[skills].copy()
print(X.describe().T[["mean", "std", "min", "max"]])
```

**Para la visualización por pares**, Georgina recomienda no poner dos variables del mismo factor, porque están muy correlacionadas, y usar Plotly con el nombre del jugador en el hover para reconocer testigos C1P2 1:23:15, C1P2 1:24:26. Finishing contra sliding tackle separa bien; interceptions contra sliding tackle pega arqueros con delanteros C1P2 1:20:21.

### 3. Escalar siempre
Los skills van de 0 a 100, pero si sumás edad, valor o salario las escalas no tienen nada que ver; y aun con los skills solos, escalar ayudó en clase C1P2 48:28, C1P2 1:34:07. Sin escalar, la PC1 se comía el 94% de la varianza y K-means cortaba vertical C2P2 35:57, C2P2 53:49. "No escalar son dos puntos menos en cualquier examen de ciencia de datos" C2P2 1:11:15.

```python
from sklearn.preprocessing import StandardScaler
Xs = StandardScaler().fit_transform(X)   # cada columna con media 0 y desvío 1
```

**Ojo con Normalizer.** No escala columnas: lleva cada fila a norma 1 (chequeado: [1, 2] pasa a [0,447; 0,894]). Sirve si querés trabajar con similitud coseno usando K-means, que en scikit-learn solo acepta euclídea.

### 4. K-means como primera exploración
Laura recomienda empezar siempre por K-means, barato y rápido, y después ir a "los cañones grandes" C2P1 42:53. Converge a un óptimo local que depende del inicio, así que usá varias inicializaciones C1P2 1:59:16. La inercia siempre baja al subir K: buscá el codo, no el mínimo C2P1 52:25, C2P1 1:02:16. La silueta compara la distancia a tu grupo con la distancia al grupo vecino C2P1 58:05.

```python
# Sugerencia: inercia y silueta para un rango de K
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
filas = []
for k in range(2, 9):
    km = KMeans(n_clusters=k, n_init=10, random_state=0).fit(Xs)
    filas.append({"K": k, "inercia": km.inertia_, "silueta": silhouette_score(Xs, km.labels_)})
tabla_k = pd.DataFrame(filas)
print(tabla_k)
```

En el dataset sintético la silueta más alta sale con K = 2 (0,64: arqueros contra el resto) aunque hay cuatro grupos, y el codo de la inercia está en 4. Es lo mismo que pasó en clase con FIFA C2P2 42:40: una métrica interna no conoce tu pregunta, por eso necesitás testigos (sección 8). **Para verificar**: el umbral de 0,4 que da Georgina para la silueta C2P1 1:01:42 no es universal.

**Yellowbrick.** KElbowVisualizer dibuja el codo y marca un K. La segunda curva es el tiempo de ajuste, no una medida de calidad (en Yellowbrick 1.5, timings=True por defecto) C2P2 41:01. Dos problemas de versiones que chequeé: en Python 3.12 o más nuevo, Yellowbrick 1.5 falla al importar porque busca distutils (se arregla instalando setuptools); y con scikit-learn 1.9.1 falla al crear el visualizador con "The supplied model is not a clustering estimator", porque Yellowbrick pregunta por el atributo `_estimator_type`, que scikit-learn ya no define. Con scikit-learn 1.6.1 anda bien. Si te falla, dibujá el codo y la silueta a mano desde la tabla anterior:

```python
# Sugerencia: codo y silueta a mano (no depende de Yellowbrick)
import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 2, figsize=(9, 3))
ax[0].plot(tabla_k["K"], tabla_k["inercia"], "o-"); ax[0].set_title("Inercia (buscá el codo)")
ax[1].plot(tabla_k["K"], tabla_k["silueta"], "o-"); ax[1].set_title("Silueta media")
plt.show()
# Con scikit-learn 1.6 también podés: from yellowbrick.cluster import KElbowVisualizer
# KElbowVisualizer(KMeans(n_init=10, random_state=0), k=(2, 9), timings=False).fit(Xs).show()
```

### 5. Mezcla de gaussianas (GMM) y BIC
GMM te da una probabilidad de pertenencia y una forma por grupo, pero tiene muchos parámetros: una covarianza completa por grupo cuesta n(n+1)/2 números, así que con muchas variables hace falta mucho dato C2P2 2:22. Por eso se elige a la vez el número de componentes y el tipo de covarianza (full, tied, diag, spherical) con BIC o AIC: más bajo es mejor C2P2 11:26, C2P2 12:00. Un modelo más simple bien estimado le gana a uno completo mal estimado C2P2 3:28. GMM se puede inicializar con la partición de K-means, que en scikit-learn es lo que hace por defecto (chequeado: init_params="kmeans") C2P2 4:03.

```python
# Sugerencia: BIC por número de componentes y tipo de covarianza
from sklearn.mixture import GaussianMixture
res = []
for cov in ["full", "tied", "diag", "spherical"]:
    for k in range(2, 7):
        gm = GaussianMixture(n_components=k, covariance_type=cov, random_state=0).fit(Xs)
        res.append({"cov": cov, "K": k, "BIC": gm.bic(Xs)})
bic = pd.DataFrame(res).sort_values("BIC")
print(bic.head(3))   # en el sintético gana diag con K = 4
```

**Ojo.** Dos clases no implican dos gaussianas: un grupo puede ser una mezcla de varias, y en clustering es difícil decidir cuáles van juntas C2P2 13:39, C4P1 1:23:33. Si querés que el modelo elija el número de componentes, scikit-learn tiene BayesianGaussianMixture, con un prior de proceso de Dirichlet por defecto (chequeado); es lo que Georgina describe en C3P1 como "una distribución sobre los enteros infinita" C3P1 39:00, aunque ella lo atribuye a K-means.

### 6. Jerárquicos y dendrograma
El aglomerativo une primero puntos y después grupos; un punto nunca sale del grupo donde entró C2P1 30:01. El hiperparámetro es el linkage, la forma de medir distancia entre grupos C2P2 17:03, C2P2 21:02:

| Linkage | Distancia entre dos grupos | Qué esperar |
|---|---|---|
| single | la mínima entre puntos de uno y otro | encadena: sirve para lunas y círculos, pero arma un grupo gigante |
| complete | la máxima | grupos compactos; en clase dio "el mejor de todos" sobre dos variables C2P2 1:01:46 |
| average | el promedio de todas las distancias entre pares | intermedio (en clase se definió mal, ver apunte) C2P2 23:17 |
| ward | la que menos aumenta la varianza dentro de los grupos | lo más parecido a K-means |

Con miles de puntos el dendrograma es ilegible: mostrá solo la parte de arriba C2P2 18:46. Un truco de Georgina: cortá el jerárquico en 7 grupos para ver qué se une con qué, y después pedile 7 a K-means o GMM y compará C2P2 19:52.

```python
# Sugerencia: cuatro linkages y un dendrograma truncado
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt
etiquetas = {}
for link in ["ward", "complete", "average", "single"]:
    etiquetas[link] = AgglomerativeClustering(n_clusters=4, linkage=link).fit_predict(Xs)
    print(link, np.bincount(etiquetas[link]))   # single: [1199 119 1 1], encadena
Z = linkage(Xs, method="ward")
plt.figure(figsize=(8, 3)); dendrogram(Z, truncate_mode="lastp", p=20); plt.show()
```

### 7. DBSCAN y mean shift
Los dos se basan en densidad y no reciben K. DBSCAN tiene dos parámetros, el radio eps y min_samples, y marca como ruido (etiqueta -1) lo que queda suelto C2P1 14:20. Si los grupos se tocan, encadena todo en uno C2P1 38:57. Mean shift busca las modas con una ventana (bandwidth) C1P2 2:05:30. En FIFA ninguno de los dos anduvo: mean shift con bandwidth 1 dio 4.747 grupos, y DBSCAN con eps 0,1 marcó todo como ruido C2P1 1:28:51, C2P1 1:33:28. Diagnóstico de Georgina: los datos son "flat" y hay demasiadas variables; con menos variables tienen más chance C2P1 1:35:11, C2P2 0:40.

**Cómo elegir los parámetros sin adivinar.** Para eps, el gráfico de k-distancias: ordená la distancia de cada punto a su vecino número min_samples y buscá el codo C2P1 1:33:28. Para el bandwidth, `estimate_bandwidth`; un valor fijo como "0,5 o 0,7" no tiene sentido porque depende de la escala (chequeado: en los dígitos de scikit-learn sale cerca de 42,8).

```python
# Sugerencia: eps desde las k-distancias y bandwidth estimado
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import DBSCAN, MeanShift, estimate_bandwidth
min_samples = 2 * Xs.shape[1]          # regla práctica: el doble de las dimensiones
dist, _ = NearestNeighbors(n_neighbors=min_samples).fit(Xs).kneighbors(Xs)
kdist = np.sort(dist[:, -1])
plt.plot(kdist); plt.ylabel("distancia al vecino min_samples"); plt.show()   # buscá el codo
db = DBSCAN(eps=float(np.percentile(kdist, 90)), min_samples=min_samples).fit(Xs)
print("DBSCAN grupos:", len(set(db.labels_)) - (1 if -1 in db.labels_ else 0), "ruido:", int((db.labels_ == -1).sum()))
bw = estimate_bandwidth(Xs, quantile=0.2, random_state=0)
ms = MeanShift(bandwidth=bw, bin_seeding=True).fit(Xs)
print("bandwidth:", round(bw, 2), "grupos mean shift:", len(np.unique(ms.labels_)))
```

En el sintético los dos encuentran 2 grupos (arqueros y el resto): es el mismo comportamiento de clase, y es información. Cuando un método de densidad dice "todo ruido" o "un solo grupo", los datos son una mezcla; probá GMM o K-means C2P1 41:48.

### 8. Testigos y métricas externas
Sin etiquetas no hay error, así que la evaluación se apoya en testigos: casos que conocés, unos 10 por grupo, idealmente elegidos por el experto C2P1 1:05:03, C2P2 1:04:02. Los testigos son filas, no columnas C2P1 1:21:27. Con ellos calculás métricas externas C2P2 47:10, C2P2 48:49:

- **Homogeneidad:** cada grupo tiene una sola clase.
- **Completitud:** cada clase cae en un solo grupo.
- **V-measure:** combina las dos.
- **ARI:** Rand ajustado por azar; puede ser negativo (chequeado: da -0,5 en un caso adverso), así que no es cierto que todas vayan de 0 a 1 C2P2 52:11.
- **AMI:** información mutua ajustada.

La consigna pide elegir dos métricas de este estilo C2P2 49:58. Recordá que el número de cada grupo es arbitrario: para comparar hay que emparejar C2P1 24:59; estas métricas ya no dependen de la numeración.

```python
# Sugerencia: 10 testigos por grupo y métricas externas
from sklearn.metrics import (homogeneity_score, completeness_score, v_measure_score,
                             adjusted_rand_score, adjusted_mutual_info_score)
km4 = KMeans(n_clusters=4, n_init=10, random_state=0).fit(Xs)
testigos = df.groupby("pos_grupo").sample(10, random_state=0).index   # en el TP: elegilos vos
y_t, c_t = df.loc[testigos, "pos_grupo"], km4.labels_[testigos]
def metricas(y, c):
    return {"homog": homogeneity_score(y, c), "complet": completeness_score(y, c),
            "V": v_measure_score(y, c), "ARI": adjusted_rand_score(y, c),
            "AMI": adjusted_mutual_info_score(y, c)}
print({k: round(v, 3) for k, v in metricas(y_t, c_t).items()})
print(pd.crosstab(df["pos_grupo"], km4.labels_))   # tabla cruzada grupo por posición
```

**Sugerencia.** En el TP elegí los testigos a mano (jugadores que conocés de cada posición) y no al azar como en el sintético, y la tabla cruzada con todas las posiciones usala para interpretar, no como nota: en clase el medio campo se repartía entre defensa y ataque C2P1 1:04:30, C2P1 1:10:37.

### 9. Tabla comparativa y entregable
Georgina guarda una tabla con una fila por agrupamiento (método, variables, escalado, K) y una columna por métrica, para poder responder "¿y no hiciste otra cosa?" C2P2 52:11, C2P2 1:14:05. La consigna del trabajo especial es la secuencia de las notebooks de clase C2P2 1:17:23:

1. Exploratorio (bastante de la notebook de exploración).
2. Evaluación visual intuitiva con dos variables (scatter de todos contra todos).
3. Normalización o escalado.
4. Clustering: se espera K-means y el jerárquico que mejor ande, con un mapa de métricas y la explicación de cómo estimaste los hiperparámetros (K, linkage).
5. Análisis cuantitativo e interpretación.

A eso se suman el clustering en el espacio proyectado C3P1 1:28:18 y la comparación con LLM C2P2 1:25:13. **Para verificar**: la numeración exacta de los puntos (el de LLM se nombró como 5, 6 o 7). Aprueba con 70% o más según la rúbrica C2P2 1:41:16.

```python
# Sugerencia: una fila por agrupamiento
candidatos = {"kmeans_4": km4.labels_, **{f"agg_{l}": e for l, e in etiquetas.items()},
              "gmm_4": GaussianMixture(4, random_state=0).fit_predict(Xs)}
tabla = pd.DataFrame({n: {**metricas(y_t, c[testigos]), "silueta": silhouette_score(Xs, c)}
                      for n, c in candidatos.items()}).T.round(3)
print(tabla.sort_values("ARI", ascending=False))
```

**Sugerencia.** Agregá columnas para las variables usadas y si escalaste. En clase las métricas cambiaron más por escalar y por elegir variables que por cambiar de algoritmo C2P2 1:01:46, C3P1 4:39.

### 10. PCA, t-SNE y UMAP
PCA es una rotación lineal ordenada por varianza: con todas las componentes no cambia las distancias (chequeado), y con pocas comprime C3P1 1:20:29, C2P2 31:55. t-SNE y UMAP son no lineales y sirven para mirar: t-SNE conserva vecindarios, no distancias, y cada corrida puede dar otra figura si no fijás la semilla C3P1 1:08:56, C3P1 1:22:42. Escalá antes de PCA: sin escalar, la PC1 se llevó el 94% en clase C2P2 35:57, C2P2 53:49.

**Lo que dijeron al revés.** PCA es mucho más rápido que t-SNE y UMAP, no al revés (chequeado en los dígitos de scikit-learn: PCA 0,003 s, t-SNE 2,3 s, UMAP unos 13 s) C3P1 1:12:11. Y t-SNE (2008) es anterior a UMAP (2018) C3P1 1:11:07.

**Para qué usar cada cosa.** Georgina usa las proyecciones para mirar, no para armar los grupos C2P2 39:21, C3P1 1:35:07; Laura recuerda que en lenguaje se agrupa sobre embeddings C3P1 1:36:12. La consigna pide las dos cosas: proyectar para visualizar y probar clustering en el espacio proyectado C3P1 1:28:18. Georgina pidió una sola función que haga los tres gráficos C4P2 1:30:56.

```python
# Sugerencia: varianza acumulada, tres proyecciones con los mismos colores y clustering en 5 PCs
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import umap                                   # pip install umap-learn
pca = PCA().fit(Xs)
acum = np.cumsum(pca.explained_variance_ratio_)
print("componentes para 90%:", int(np.searchsorted(acum, 0.90) + 1))

def tres_proyecciones(Xs, colores, titulo=""):
    P2 = PCA(n_components=2).fit_transform(Xs)
    T2 = TSNE(n_components=2, perplexity=30, random_state=0).fit_transform(Xs)
    U2 = umap.UMAP(n_components=2, random_state=0).fit_transform(Xs)
    fig, ax = plt.subplots(1, 3, figsize=(12, 4))
    for a, (nombre, E) in zip(ax, [("PCA", P2), ("t-SNE", T2), ("UMAP", U2)]):
        a.scatter(E[:, 0], E[:, 1], c=colores, s=5, cmap="tab10"); a.set_title(f"{nombre} {titulo}")
    plt.show()

tres_proyecciones(Xs, km4.labels_, "K-means 4")
km_pca = KMeans(4, n_init=10, random_state=0).fit(PCA(n_components=5).fit_transform(Xs))
print("ARI testigos K-means en 5 PCs:", round(adjusted_rand_score(y_t, km_pca.labels_[testigos]), 3))
```

**Lo que mostró Georgina en la notebook de embeddings (C3P2).** Con PCA no se reduce "de 40 a 2" para trabajar: mirá la varianza de cada componente y decidí; en su ejemplo las tres primeras explicaban el 67% y ella tomaría 4 C3P2 25:35, C3P2 32:19. El biplot muestra qué variables pesan en cada componente y cuáles van juntas C3P2 30:17. En t-SNE el parámetro clave es la perplexity: baja mira lo local y puede partir un grupo en subgrupos, alta mira lo global y los une; ella usó 30, el valor por defecto C3P2 11:01, C3P2 12:57. Corrió t-SNE con solo 1.000 jugadores porque es pesado C3P2 17:10. Y para comparar sin etiquetas, propuso pedirle el mismo número de grupos a varios métodos y ver cuánto coinciden entre sí antes de nombrarlos con testigos C3P2 39:49.

```python
# Sugerencia: biplot de las dos primeras componentes
pca2 = PCA(n_components=2).fit(Xs); P = pca2.transform(Xs)
plt.figure(figsize=(6, 6)); plt.scatter(P[:, 0], P[:, 1], s=3, alpha=0.3)
for i, v in enumerate(skills):
    x, y = pca2.components_[0, i] * 4, pca2.components_[1, i] * 4
    plt.arrow(0, 0, x, y, color="r", head_width=0.05); plt.text(x * 1.1, y * 1.1, v, fontsize=7)
plt.title("Biplot: flechas juntas = variables que aportan lo mismo"); plt.show()

# Sugerencia: t-SNE con tres perplexities (en datos grandes, probá primero con una muestra)
fig, ax = plt.subplots(1, 3, figsize=(12, 4))
for a, perp in zip(ax, [5, 30, 100]):
    E = TSNE(n_components=2, perplexity=perp, random_state=0).fit_transform(Xs)
    a.scatter(E[:, 0], E[:, 1], c=km4.labels_, s=5, cmap="tab10"); a.set_title(f"perplexity {perp}")
plt.show()

# Sugerencia: cuánto coinciden los métodos entre sí, sin usar etiquetas (ARI entre particiones)
km_umap = KMeans(4, n_init=10, random_state=0).fit(umap.UMAP(n_components=5, random_state=0).fit_transform(Xs))
particiones = {"kmeans": km4.labels_, "ward": etiquetas["ward"], "single": etiquetas["single"],
               "kmeans_pca5": km_pca.labels_, "kmeans_umap5": km_umap.labels_}
nombres = list(particiones)
coinc = pd.DataFrame([[adjusted_rand_score(particiones[a], particiones[b]) for b in nombres] for a in nombres],
                     index=nombres, columns=nombres).round(2)
print(coinc)   # filas con valores altos = grupos estables entre métodos
```

En TSNE usá `max_iter`, no `n_iter`: `n_iter` ya no existe en scikit-learn 1.9.1 (chequeado). **Sugerencia**: pasá a `tres_proyecciones` tanto los grupos de cada método como la posición real, y marcá los testigos con su nombre en un Plotly, como hizo Georgina C1P2 1:24:26.

### 11. Embeddings neuronales
Un embedding neuronal representa cada objeto con los valores de una capa de una red entrenada con una tarea de pretexto que se genera sola a partir de los datos (autosupervisión); la representación depende de la tarea C1P1 59:16, C1P1 1:02:01. Para el TP no hace falta entrenar redes: lo que se pide es al menos PCA C2P2 1:23:34. Laura lo explicó en C3P2:

1. Entrenás una red, le sacás la capa de predicción y te quedás con la anterior: cada neurona es una dimensión nueva C3P2 47:31.
2. La red se entrena con una tarea de pretexto que fabrica etiquetas sola: borrar una palabra y adivinarla, colorear una imagen en blanco y negro, ordenar una imagen desordenada C3P2 55:08, C3P2 1:01:40, C3P2 1:03:13.
3. Un clasificador que trabaja sobre ese espacio acierta mucho más que sobre los píxeles o las palabras crudas C3P2 51:21, C3P2 52:36.
4. La tarea de pretexto define para qué sirve el embedding; PCA, en cambio, es "neutro" C3P2 1:06:31.

Para FIFA podrías entrenar una red que prediga la posición y usar la capa anterior como embedding, pero Laura aclaró que "nadie espera que lo hagan" C3P2 1:07:40, C3P2 1:09:00. Si querés probarlo igual, esta es la idea mínima con scikit-learn, sin bajar a nivel de redes:

```python
# Sugerencia: "embedding" de la capa oculta de un MLP entrenado con los testigos (solo para explorar)
from sklearn.neural_network import MLPClassifier
mlp = MLPClassifier(hidden_layer_sizes=(8,), max_iter=2000, random_state=0)
mlp.fit(Xs[testigos], df.loc[testigos, "pos_grupo"])
H = np.maximum(0, Xs @ mlp.coefs_[0] + mlp.intercepts_[0])   # activaciones ReLU de la capa oculta
km_h = KMeans(4, n_init=10, random_state=0).fit(H)
print("ARI global K-means sobre la capa oculta:", round(adjusted_rand_score(df["pos_grupo"], km_h.labels_), 3))
```

**Ojo.** Esto usa las etiquetas de los testigos para construir el espacio, así que ya no es clustering puro: si lo incluís en el TP, decilo y comparalo con el resto en la tabla. Los LLM tienen en su núcleo justamente este tipo de representación, entrenada con tareas de pretexto, y por eso pueden alucinar C3P2 1:19:08, C3P2 1:21:47.

### 12. Ayudar al clustering con lo que ya sabés (semisupervisado)
Cuando tenés pocos ejemplos etiquetados y muchos sin etiquetar, podés usar los dos C4P1 37:40, C4P1 45:25. Para el TP, lo más directo es lo que propuso Georgina: inicializar K-means o GMM con los testigos en lugar de al azar, porque evita mínimos locales absurdos y ahorra tiempo C4P1 1:16:23, C4P1 1:18:34. Contra lo que se dijo en clase C4P1 1:20:14, scikit-learn sí trae piezas para esto (chequeado): `KMeans(init=array)`, `GaussianMixture(means_init=...)` y el módulo `sklearn.semi_supervised` con SelfTrainingClassifier, LabelPropagation y LabelSpreading. Lo que no trae es EM semisupervisado con restricciones ni clustering con restricciones del tipo "Messi no puede estar con el Dibu" C4P1 1:51:32, C2P1 1:21:27.

**Autoaprendizaje (self-training).** Entrenás con los pocos etiquetados, etiquetás los no etiquetados de mayor confianza (por ejemplo 95%) y repetís C4P1 55:44. Es un envoltorio sobre cualquier clasificador, pero amplifica los errores iniciales y la clase mayoritaria actúa como atractor C4P1 1:07:30, C4P1 1:08:37. Mitigalo revisando a mano los casos dudosos (aprendizaje activo) C4P1 59:07.

```python
# Sugerencia: K-means y GMM inicializados con los centroides de los testigos
grupos = ["ataque", "medio", "defensa", "arquero"]
centros = np.vstack([Xs[testigos[y_t.values == g]].mean(0) for g in grupos])
km_semi = KMeans(n_clusters=4, init=centros, n_init=1).fit(Xs)
print("ARI global con init de testigos:", round(adjusted_rand_score(df["pos_grupo"], km_semi.labels_), 3))
gm_semi = GaussianMixture(4, means_init=centros, random_state=0).fit(Xs)

# Sugerencia: self-training y label spreading con solo los 40 testigos etiquetados (-1 = sin etiqueta)
from sklearn.semi_supervised import SelfTrainingClassifier, LabelSpreading
from sklearn.linear_model import LogisticRegression
codigo = {g: i for i, g in enumerate(grupos)}
y_semi = np.full(len(df), -1); y_semi[testigos] = df.loc[testigos, "pos_grupo"].map(codigo)
st = SelfTrainingClassifier(estimator=LogisticRegression(max_iter=1000), threshold=0.95).fit(Xs, y_semi)
y_real = df["pos_grupo"].map(codigo).values   # en datos reales no la tenés: solo para el ejemplo
print("self-training acierto:", round((st.predict(Xs) == y_real).mean(), 3))
ls = LabelSpreading(kernel="knn", n_neighbors=10).fit(Xs, y_semi)
print("label spreading acierto:", round((ls.transduction_ == y_real).mean(), 3))
```

En SelfTrainingClassifier el parámetro es `estimator`; `base_estimator` existía en 1.6 y ya no está en 1.9.1 (chequeado). **Ojo**: si usás las posiciones como etiquetas, esto deja de ser clustering y pasa a ser clasificación; para el TP, usalo como comparación, no como el resultado principal.

### 13. Reglas de asociación
Convierten probabilidades condicionales en reglas "si X entonces Y", fáciles de discutir con gente de negocio C4P2 0:02, C4P2 1:13. Los datos tienen que ser transacciones: conjuntos de ítems sin orden C4P2 6:29, C4P2 7:03. Casi cualquier cosa se puede modelar así: tickets, documentos como bolsas de palabras, historias clínicas, eventos en ventanas de tiempo C4P2 10:55, C4P2 16:20, C4P2 21:19.

- **Soporte:** proporción de transacciones con X e Y juntos (en mlxtend es proporción) C4P2 25:18.
- **Confianza:** P(Y dado X); no es simétrica: fernet → coca no es lo mismo que coca → fernet C4P2 27:02.
- **Lift:** confianza dividida por el soporte de Y; mayor que 1 indica asociación por encima de la independencia. No es una probabilidad, como se dijo en clase C4P2 35:58.
- **Convicción:** (1 menos soporte de Y) dividido (1 menos confianza); es infinita cuando la confianza es 1 (chequeado en mlxtend).

Lo crítico es ordenar y filtrar: el algoritmo te da miles de reglas, y conviene un soporte bajo seguido de filtros por ítem y orden por la métrica que le importe al negocio C4P2 4:07, C4P2 43:46. Apriori es de 1994, no de 1993 C4P2 5:54, y hay alternativas más rápidas como FP-Growth, que en mlxtend da los mismos itemsets (chequeado) C4P2 40:22. En la clase no hubo notebook de reglas ("pídanla a Claude o a nosotros") C4P2 2:53.

```python
# Sugerencia: apriori y reglas con mlxtend (pip install mlxtend)
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, fpgrowth, association_rules
tickets = [["fernet", "coca", "hielo"], ["fernet", "coca"], ["coca", "pan"],
           ["fernet", "coca", "pan"], ["pan", "leche"], ["leche", "cereal", "pan"]]
te = TransactionEncoder()
B = pd.DataFrame(te.fit(tickets).transform(tickets), columns=te.columns_)
frec = apriori(B, min_support=0.3, use_colnames=True)     # o fpgrowth(B, ...), mismo resultado
reglas = association_rules(frec, metric="confidence", min_threshold=0.5)
print(reglas.sort_values("lift", ascending=False)[["antecedents", "consequents", "support", "confidence", "lift"]].head(3))
```

**Sugerencia.** Antes de correr, reducí la dimensión con abstracciones de dominio (pan embolsado y no embolsado en lugar de 20 tipos de pan) C4P2 8:11, C4P2 14:45.

### 14. Grafos y redes sociales
Fue un tema "para vocabulario" C4P2 48:18. Lo que conviene saber hacer C4P2 1:05:07, C4P2 1:06:47, C4P2 1:08:29, C4P2 1:09:41:

- **Centralidad de grado y de cercanía:** cuántas conexiones tiene un nodo y qué tan cerca está de todos.
- **Intermediación (betweenness):** nodos que conectan grupos, como el estrecho de Gibraltar o, en Enron, los jefes.
- **Prestigio en grafos dirigidos:** hubs (apuntan a muchos) y authorities (muchos los apuntan). Eso es HITS, de Kleinberg; PageRank da un solo puntaje.
- **Comunidades:** algoritmo de Louvain.

Gephi es un programa de escritorio para visualizar; en Python lo habitual es NetworkX.

```python
# Sugerencia: centralidades, comunidades y HITS contra PageRank con NetworkX
import networkx as nx
G = nx.karate_club_graph()
bet = nx.betweenness_centrality(G); clo = nx.closeness_centrality(G)
print("top betweenness:", sorted(bet, key=bet.get, reverse=True)[:3])
comunidades = nx.community.louvain_communities(G, seed=0); print("comunidades:", len(comunidades))
D = nx.DiGraph([(1, 2), (1, 3), (2, 3), (4, 3), (3, 1)])
hubs, autoridades = nx.hits(D); pr = nx.pagerank(D)
print("authority top:", max(autoridades, key=autoridades.get), "pagerank top:", max(pr, key=pr.get))
```

El grafo de semisupervisado es otro uso: nodos que comparten palabras o píxeles se conectan con pesos y las etiquetas se propagan "a los amigos de mis amigos" C4P1 1:31:25, C4P1 1:34:12. LabelSpreading con kernel knn de la sección 12 hace eso.

### 15. Sistemas de recomendación
Son no supervisados porque nadie etiqueta: se infiere de comportamiento (terminar la serie, verla de corrido) C4P2 1:12:28, C4P2 1:19:43. Partís la matriz usuarios por ítems: lo que sabés de Alice son características, y lo que otros dijeron del ítem 5 es lo que predecís C4P2 1:14:08. El método histórico es KNN con usuarios parecidos y voto pesado C4P2 1:16:23. Los problemas clásicos son la cola larga y el arranque en frío; se atacan con características del producto y con factorización de matrices C4P2 1:22:28.

```python
# Sugerencia: filtrado colaborativo por usuarios (Pearson) para el ítem 5 de Alice
R = pd.DataFrame([[5, 3, 4, 4, np.nan], [3, 1, 2, 3, 3], [4, 3, 4, 3, 5], [3, 3, 1, 5, 4], [1, 5, 5, 2, 1]],
                 index=["Alice", "u1", "u2", "u3", "u4"], columns=[f"item{i}" for i in range(1, 6)])
comunes = R.drop(columns="item5")
def sim(a, b):
    a, b = a - a.mean(), b - b.mean()
    return float((a * b).sum() / np.sqrt((a * a).sum() * (b * b).sum()))
sims = {u: sim(comunes.loc["Alice"], comunes.loc[u]) for u in R.index if u != "Alice"}
vecinos = sorted(sims, key=sims.get, reverse=True)[:2]
pred = R.loc["Alice"].drop("item5").mean() + sum(
    sims[u] * (R.loc[u, "item5"] - R.loc[u].drop("item5").mean()) for u in vecinos) / sum(abs(sims[u]) for u in vecinos)
pred = float(np.clip(pred, 1, 5))   # sin recortar da 5,09, fuera de la escala
print("vecinos:", vecinos, "predicción item5 para Alice:", round(pred, 2))
```

**Ojo.** La factorización de matrices está emparentada con la SVD ("es PCA básicamente", se dijo), pero en recomendación se ajusta solo con las celdas observadas; rellenar los NaN con promedios y aplicar TruncatedSVD es una aproximación de juguete.

### 16. Texto: LSA y LDA
LSA es SVD sobre la matriz documentos por términos: los conteos reproyectados se suavizan y los ceros pasan a ser "poco probable" en lugar de imposible C3P1 1:38:50, C3P1 1:42:13. LDA modela cada documento como mezcla de temas y cada tema como distribución de palabras; el número de temas es un parámetro C3P1 1:50:00. LDA es de Blei, Ng y Jordan (2003), no "la tesis de Andrew Ng" C3P1 37:50.

```python
# Sugerencia: LSA (TF-IDF + TruncatedSVD) y LDA sobre un corpus mínimo
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import TruncatedSVD, LatentDirichletAllocation
docs = ["datos recuperación de información datos", "datos información sistemas", "cerebro pulmón paciente",
        "pulmón paciente tratamiento", "datos paciente historia clínica", "fichajes fútbol millones club",
        "club fútbol goles partido", "millones bolsa acciones finanzas"]
tf = TfidfVectorizer().fit(docs)
lsa = TruncatedSVD(n_components=2, random_state=0).fit_transform(tf.transform(docs))
cv = CountVectorizer().fit(docs); C = cv.transform(docs)
lda = LatentDirichletAllocation(n_components=3, random_state=0).fit(C)
vocab = cv.get_feature_names_out()
for t, comp in enumerate(lda.components_):
    print("tema", t, [vocab[i] for i in comp.argsort()[-3:][::-1]])
print("mezcla del doc 0:", lda.transform(C[0]).round(2))
```

Con ocho documentos los temas salen mezclados (en mi corrida, "paciente" cae junto a "millones"); LDA necesita corpus grandes. Laura dijo que para temas en redes sociales "funciona como piña" C4P2 57:18.

### 17. Interpretar, comparar con LLM y cerrar el TP
El punto agregado "a pedido de Carolina": pasarle el mismo prompt a varios LLM (Claude, ChatGPT, Gemini, Grok) para que interpreten cada grupo, y comparar coincidencias, diferencias y alucinaciones con tu propia interpretación C2P2 1:25:13. Georgina pidió hacerlo en ese orden: primero ustedes, después el LLM ("no le den de entrada a Claude") C4P2 1:30:56. Laura advierte que si usás LLM para el análisis, dependés del servicio C2P2 1:34:40, y Georgina, que dos llamadas dan dos respuestas distintas C2P2 1:31:24.

**Sugerencia de prompt** (mío, para adaptar): "Te paso, para cada uno de K grupos de jugadores de FIFA 24, la media estandarizada de cada skill y diez jugadores de ejemplo. Describí qué tipo de jugador representa cada grupo y qué posición crees que juega. No inventes jugadores que no estén en la lista." Corrélo dos veces en cada servicio y anotá si cambia.

**Para defender decisiones.** Tené a mano por qué escalaste (en clase: "son dos puntos menos" no hacerlo C2P2 1:11:15), qué variables elegiste y por qué C2P1 1:23:41, cómo elegiste K y el linkage, y qué hiciste con el medio campo. **Dudoso**: si esta materia pide una charla de defensa; Georgina lo mencionó al pasar C4P2 1:30:56.

### 18. Cómputo, nube y datos personales
Si el clustering tarda 15 minutos en tu computadora, usá Colab o servidores C3P1 5:13. El CCAD de la UNC da acceso a investigadores (**para verificar** condiciones) y hay una optativa de cálculo distribuido C3P1 6:52, C3P1 11:16. Con datos personales, la Ley 25.326 restringe transferirlos a países sin protección adecuada, con excepciones; no es una prohibición absoluta C3P1 12:25.

**Sugerencia para el TP.** Con FIFA no hay datos personales sensibles, pero dejá fijo `random_state` en K-means, GMM, t-SNE y UMAP para que tus números se reproduzcan y coincidan con la tabla.

---

## Glosario

| Término | Qué es |
|---|---|
| Testigo | Caso conocido (una fila) que usás para evaluar o interpretar un agrupamiento. |
| Inercia | Suma de distancias al cuadrado de cada punto a su centroide; siempre baja al subir K. |
| Silueta | Por punto, compara la distancia media a su grupo con la del grupo vecino; va de -1 a 1. |
| BIC y AIC | Criterios basados en verosimilitud que penalizan parámetros; más bajo es mejor. |
| Linkage | Forma de medir la distancia entre dos grupos en un jerárquico. |
| eps y min_samples | Radio y mínimo de vecinos de DBSCAN. |
| Bandwidth | Ancho de la ventana de mean shift; depende de la escala. |
| Homogeneidad y completitud | Cada grupo con una sola clase; cada clase en un solo grupo. |
| V-measure | Combinación de homogeneidad y completitud. |
| ARI | Rand ajustado por azar; 1 es coincidencia perfecta y puede ser negativo. |
| Embedding | Representación de los datos en otro espacio, por proyección o por una capa de red. |
| Tarea de pretexto | Tarea que se fabrica sola desde los datos para entrenar una red sin etiquetas. |
| Self-training | Autoaprendizaje: etiquetar con el propio modelo los casos de mayor confianza y reentrenar. |
| Soporte, confianza, lift | Métricas de reglas de asociación (sección 13). |
| — | Intermediación: cuánto pasa por un nodo el camino más corto entre otros. |
| Cold start | Arranque en frío: no saber qué recomendar a un usuario o ítem nuevo. |

### Nombres que la transcripción deforma

| Lo que dice la transcripción | Qué es |
|---|---|
| clot, cloud, Cloud | Claude, el asistente de Anthropic |
| camas, camedias | K-means, K medias |
| minift | mean shift |
| Word | Ward (linkage) |
| tight | tied (covarianza en GaussianMixture) |
| bas and information, akik | BIC y AIC |
| Kle | Kaggle |
| TCN, Disney, Tesne | t-SNE |
| un map, lumap | UMAP |
| Coolback Libler | divergencia de Kullback-Leibler |
| tendricticlet, late and let allocation | LDA, latent Dirichlet allocation |
| SECAT, Secat | CCAD de la UNC |
| Vietma | Luis Biedma (mentorías) |
| Jorina, Yorgina | Georgina (Flesia) |
| Jarovski | David Yarowsky |
| Exchi Boost | XGBoost |
| Ferné | fernet |
| Lobaina | algoritmo de Louvain |
| Geppi | Gephi |
| pisentimiento | pysentimiento |
| — | divergencia de Kullback-Leibler (en C3P2, transcripción de faster-whisper) |
| Bplot | biplot |
| J.Alamar | Jay Alammar |
| cámedias | K-means |

La tabla completa está en el apunte de estudio.
