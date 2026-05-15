#!/usr/bin/env python3
"""Inserta referencias a imágenes en el markdown de visualización."""
import re
from pathlib import Path

MD_PATH = Path('/home/javier/programacion/Educacion/DiploDatos/Análisis y Visualización de Datos/estudio/13-guia-de-visualizacion.md')

# Mapeo de títulos de sección a imagen
# Busca headers ### que contengan estos textos
IMAGE_MAP = [
    # Sección 1
    ('### Matplotlib: `plt.plot()`', 'ejemplo_plot.png'),
    ('### Matplotlib: `plt.scatter()` — puntos', 'ejemplo_scatter.png'),
    ('### Matplotlib: `plt.bar()` / `plt.barh()`', 'ejemplo_bar.png'),
    ('### Matplotlib: `plt.hist()`', 'ejemplo_hist.png'),
    ('### Matplotlib: `plt.boxplot()`', 'ejemplo_boxplot.png'),
    ('### Matplotlib: `plt.pie()`', 'ejemplo_pie.png'),
    ('### Matplotlib: `plt.imshow()`', 'ejemplo_imshow.png'),
    ('### Matplotlib: `plt.fill_between()`', 'ejemplo_fill_between.png'),
    ('### Matplotlib: `plt.errorbar()`', 'ejemplo_errorbar.png'),
    ('### Matplotlib: Subplots', 'ejemplo_subplots.png'),
    ('### Seaborn: `sns.histplot()`', 'ejemplo_sns_histplot.png'),
    ('### Seaborn: `sns.kdeplot()`', 'ejemplo_sns_kdeplot.png'),
    ('### Seaborn: `sns.displot()`', 'ejemplo_sns_displot.png'),
    # Sección 2
    ('### Matplotlib: `plt.scatter()` (revisitado', 'ejemplo_scatter.png'),
    ('### Seaborn: `sns.scatterplot()`', 'ejemplo_sns_scatterplot.png'),
    ('### Seaborn: `sns.lineplot()`', 'ejemplo_sns_lineplot.png'),
    ('### Seaborn: `sns.barplot()`', 'ejemplo_sns_barplot.png'),
    ('### Seaborn: `sns.countplot()`', 'ejemplo_sns_countplot.png'),
    ('### Seaborn: `sns.boxplot()` — caja', 'ejemplo_sns_boxplot.png'),
    ('### Seaborn: `sns.violinplot()`', 'ejemplo_sns_violinplot.png'),
    ('### Seaborn: `sns.boxenplot()`', 'ejemplo_sns_boxenplot.png'),
    ('### Seaborn: `sns.stripplot()`', 'ejemplo_sns_stripplot.png'),
    ('### Seaborn: `sns.swarmplot()`', 'ejemplo_sns_swarmplot.png'),
    ('### Seaborn: `sns.heatmap()`', 'ejemplo_sns_heatmap.png'),
    ('### Seaborn: `sns.jointplot()`', 'ejemplo_sns_jointplot.png'),
    # Sección 3
    ('### Seaborn: `sns.pairplot()`', 'ejemplo_sns_pairplot.png'),
    ('### Seaborn: `sns.lmplot()`', 'ejemplo_sns_lmplot.png'),
    ('### Seaborn: `sns.catplot()`', 'ejemplo_sns_catplot.png'),
    ('### Seaborn: `sns.relplot()`', 'ejemplo_sns_relplot.png'),
    # Sección 4
    ('### Colores y paletas', 'ejemplo_paletas.png'),
    ('### Textos: títulos, labels, anotaciones', 'ejemplo_anotaciones.png'),
    ('### Estilos y contextos', 'ejemplo_contextos.png'),
]

# Caso especial para barh: queremos una imagen adicional después del bloque de barh
BARH_MARKER = '```python\nplt.barh('

text = MD_PATH.read_text(encoding='utf-8')

inserted = 0
for marker, img_name in IMAGE_MAP:
    # Buscar la posición del header
    idx = text.find(marker)
    if idx == -1:
        print(f'⚠ No encontrado: {marker}')
        continue
    
    # Buscar el siguiente bloque de código después del header
    # Un bloque de código es ```python ... ```
    code_start = text.find('```python', idx)
    if code_start == -1:
        print(f'⚠ No encontrado bloque de código para: {marker}')
        continue
    
    # Buscar el cierre del bloque de código
    code_end = text.find('```', code_start + 3)
    if code_end == -1:
        print(f'⚠ No encontrado cierre de código para: {marker}')
        continue
    
    # La posición justo después del cierre del bloque de código
    insert_pos = code_end + 3
    
    # Verificar si ya hay una imagen insertada
    rest = text[insert_pos:insert_pos+200].strip()
    if rest.startswith('!'):
        print(f'⏭ Ya tiene imagen: {marker}')
        continue
    
    image_line = f"\n\n![Ejemplo de {img_name.replace('ejemplo_', '').replace('.png', '')}](img_viz/{img_name})"
    
    text = text[:insert_pos] + image_line + text[insert_pos:]
    inserted += 1
    print(f'✓ Insertado {img_name} en {marker[:40]}...')

# Caso especial: barh tiene un bloque de código separado
barh_idx = text.find(BARH_MARKER)
if barh_idx != -1:
    code_end = text.find('```', barh_idx + 3)
    if code_end != -1:
        insert_pos = code_end + 3
        rest = text[insert_pos:insert_pos+200].strip()
        if not rest.startswith('!'):
            image_line = "\n\n![Ejemplo de barh](img_viz/ejemplo_barh.png)"
            text = text[:insert_pos] + image_line + text[insert_pos:]
            inserted += 1
            print('✓ Insertado ejemplo_barh.png después de plt.barh()')

MD_PATH.write_text(text, encoding='utf-8')
print(f'\n✅ Total imágenes insertadas: {inserted}')
