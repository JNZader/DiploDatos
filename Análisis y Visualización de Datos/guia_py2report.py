# =============================================================================
# GUIA: Como usar py2report.py
# =============================================================================
# py2report convierte cualquier archivo .py comentado en un reporte HTML.
# Los comentarios se vuelven texto, el codigo se muestra con syntax highlighting,
# y los graficos (plt.savefig) se embeben automaticamente.

# =============================================================================
# PASO 1: Instalacion
# =============================================================================
# No hay nada que instalar. py2report.py es un script standalone de Python.
# Solo necesitas Python 3.10+ (usa type hints modernas).
#
# Copialo a cualquier proyecto y listo.

# =============================================================================
# PASO 2: Uso basico
# =============================================================================
# Desde la terminal:
#
#   python py2report.py mi_archivo.py
#
# Esto genera mi_archivo_reporte.html en la misma carpeta.
#
# Con opciones:
#
#   python py2report.py mi_archivo.py -o reporte.html -t "Mi Titulo"
#
#   -o / --output: nombre del archivo HTML de salida
#   -t / --title: titulo que aparece en el reporte

# =============================================================================
# PASO 3: Las convenciones de formato
# =============================================================================
# py2report lee tu .py linea por linea y clasifica cada linea
# en uno de estos tipos:

# --- 3a: Headers (titulos de seccion) ---
# Se generan con bloques de separadores y texto en mayusculas:
#
#   # =============================================================
#   # TITULO DE MI SECCION
#   # =============================================================
#
# El separador (===) se ignora, el texto se convierte en un <h2>
# con fondo azul oscuro. Tambien se detectan lineas que empiezan
# con PASO, OPCION, EJERCICIO, SECCION seguido de un numero.

# --- 3b: Subheaders (subtitulos) ---
# Se generan con guiones triples:
#
#   # --- Mi subtitulo ---
#
# Se convierte en un <h3> con borde lateral violeta.

# --- 3c: Texto explicativo (comentarios normales) ---
# Cualquier linea que empiece con # se convierte en texto:
#
#   # Este es un parrafo de explicacion.
#   # Puede ocupar varias lineas seguidas.
#   #
#   # Una linea vacia entre comentarios genera un parrafo nuevo.
#
# Se muestra en una caja blanca con sombra suave.
# Tambien detecta listas:
#
#   # - Primer item
#   # - Segundo item
#   # 1. Item numerado

# --- 3d: Conceptos destacados ---
# CONCEPTO: Cuando un comentario empieza con "CONCEPTO:" se convierte
# en una caja amarilla con borde naranja. Ideal para definiciones
# y teoria importante que queres que resalte.
#
# Todo lo que siga en lineas de comentario consecutivas se agrupa
# dentro de la misma caja amarilla. Util para explicaciones largas.

# --- 3e: Bloques de codigo ---
# Todo lo que NO es comentario se muestra como codigo Python
# con syntax highlighting (colores) usando Prism.js.
#
# Por ejemplo, este bloque se mostraria como codigo:

x = 42
nombre = "py2report"
print(f"{nombre} convierte {x} tipos de bloques")

# --- 3f: Imagenes embebidas ---
# Si tu codigo tiene plt.savefig("algo.png"), py2report
# busca ese archivo PNG y lo embebe en el HTML como base64.
# Esto significa que el HTML es UN SOLO ARCHIVO — no necesita
# los PNGs por separado.
#
# IMPORTANTE: el .py tiene que haberse ejecutado ANTES para que
# los PNGs existan. py2report NO ejecuta tu codigo, solo lo lee.

# =============================================================================
# PASO 4: Flujo de trabajo recomendado
# =============================================================================
# 1. Escribi tu analisis en un archivo .py
#    - Usa los comentarios con las convenciones de arriba
#    - Pone plt.savefig("img/grafico.png") para cada grafico
#
# 2. Ejecuta tu .py para generar los graficos:
#    python mi_analisis.py
#
# 3. Genera el reporte:
#    python py2report.py mi_analisis.py
#
# 4. Abri el HTML en el browser:
#    xdg-open mi_analisis_reporte.html
#
# 5. Para exportar a PDF: Ctrl+P en el browser → "Guardar como PDF"

# =============================================================================
# PASO 5: Ejemplo completo minimo
# =============================================================================
# Imaginate que tenes este archivo "demo.py":

# --- Ejemplo: demo.py ---
# # ============================================
# # MI ANALISIS DE DATOS
# # ============================================
# # Este es un analisis de ejemplo.
# #
# # CONCEPTO: La media es el promedio de los datos.
# # Se calcula sumando todos los valores y dividiendo
# # por la cantidad.
#
# import numpy as np
# datos = [1, 2, 3, 4, 5]
# print(f"Media: {np.mean(datos)}")
#
# # --- Visualizacion ---
# import matplotlib.pyplot as plt
# plt.plot(datos)
# plt.savefig("img/demo.png")
# plt.close()
# --- Fin del ejemplo ---
#
# Al correr: python py2report.py demo.py
# Genera un HTML con:
#   - Titulo "MI ANALISIS DE DATOS" (h2 azul)
#   - Parrafo "Este es un analisis de ejemplo." (caja blanca)
#   - Concepto sobre la media (caja amarilla)
#   - Bloque de codigo con los imports y el print (syntax highlight)
#   - Subtitulo "Visualizacion" (h3 violeta)
#   - Bloque de codigo del plot
#   - La imagen demo.png embebida

# =============================================================================
# PASO 6: Tips
# =============================================================================
# - Separa secciones con bloques de ====. Hace el .py mas legible
#   Y el reporte queda con secciones claras.
#
# - Usa CONCEPTO: para todo lo que quieras estudiar despues.
#   En el HTML resalta en amarillo, facil de encontrar.
#
# - Los comentarios inline (al final de una linea de codigo)
#   NO se separan. Se muestran como parte del bloque de codigo.
#   Ejemplo: x = 42  # esto se ve como codigo, no como texto
#
# - Lineas en blanco entre comentarios generan parrafos nuevos.
#   Usalo para separar ideas.
#
# - El HTML tiene estilos para imprimir (Ctrl+P).
#   Los bloques de codigo y graficos no se cortan entre paginas.
#
# - Prism.js se carga desde CDN. Necesitas internet la primera vez
#   que abras el HTML (despues queda en cache del browser).

# =============================================================================
# PASO 7: Arquitectura interna (para curiosos)
# =============================================================================
# CONCEPTO: py2report funciona en 3 fases, como un compilador simple:
#
# FASE 1 — CLASIFICACION (classify_line):
#   Lee cada linea y le asigna un tipo: HEADER, SUBHEADER, COMMENT,
#   CONCEPT, CODE, IMAGE o BLANK.
#   Usa regex para detectar patrones (separadores, listas, savefig).
#
# FASE 2 — AGRUPACION (parse_blocks):
#   Junta lineas consecutivas del mismo tipo en "bloques".
#   Por ejemplo, 5 lineas de comentario seguidas = 1 bloque COMMENT.
#   Los headers y las imagenes siempre son bloques de 1 linea.
#
# FASE 3 — RENDERIZADO (block_to_html):
#   Convierte cada bloque en HTML:
#   - HEADER → <h2>
#   - SUBHEADER → <h3>
#   - COMMENT → <div class="explanation"><p>...</p></div>
#   - CONCEPT → <div class="concept"><p>...</p></div>
#   - CODE → <pre><code class="language-python">...</code></pre>
#   - IMAGE → <img src="data:image/png;base64,...">
#
# Finalmente, envuelve todo en un HTML con CSS y Prism.js.
# El CSS tiene media queries para responsive y para impresion.
