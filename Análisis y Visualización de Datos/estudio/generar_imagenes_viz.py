#!/usr/bin/env python3
"""Genera imágenes de ejemplo para la guía de visualización."""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

sns.set_style('whitegrid')
np.random.seed(42)

IMG_DIR = Path('/home/javier/programacion/Educacion/DiploDatos/Análisis y Visualización de Datos/estudio/img_viz')
IMG_DIR.mkdir(parents=True, exist_ok=True)

def save(fig, name):
    path = IMG_DIR / name
    fig.savefig(path, dpi=100, bbox_inches='tight')
    plt.close(fig)
    print(f'✓ {name}')

# Crear DataFrame sintético reutilizable
n = 300
df = pd.DataFrame({
    'salario': np.concatenate([
        np.random.normal(300000, 50000, n//3),
        np.random.normal(450000, 80000, n//3),
        np.random.normal(600000, 70000, n//3)
    ]),
    'experiencia': np.concatenate([
        np.random.normal(3, 1, n//3),
        np.random.normal(7, 2, n//3),
        np.random.normal(12, 3, n//3)
    ]),
    'horas': np.concatenate([
        np.random.normal(40, 5, n//3),
        np.random.normal(45, 4, n//3),
        np.random.normal(50, 6, n//3)
    ]),
    'lenguaje': np.repeat(['Python', 'JavaScript', 'Java'], n//3),
    'genero': np.random.choice(['F', 'M'], n),
    'dedicacion': np.random.choice(['Full-time', 'Part-time'], n),
    'año': np.random.choice([2021, 2022, 2023, 2024], n)
})
df['salario'] = df['salario'].clip(150000, 900000)
df['experiencia'] = df['experiencia'].clip(0, 25)
df['horas'] = df['horas'].clip(20, 70)

# ── Matplotlib ──

# plt.plot
fig, ax = plt.subplots(figsize=(8, 5))
x = np.linspace(0, 10, 100)
ax.plot(x, np.sin(x), color='steelblue', linewidth=2, linestyle='--')
ax.set_title('plt.plot() — Serie temporal / Función')
ax.set_xlabel('X'); ax.set_ylabel('sin(X)')
save(fig, 'ejemplo_plot.png')

# plt.scatter
fig, ax = plt.subplots(figsize=(8, 5))
x = np.random.randn(200)
y = np.random.randn(200)
ax.scatter(x, y, alpha=0.5, s=50, c='coral')
ax.set_title('plt.scatter() — Relación entre dos variables')
ax.set_xlabel('Variable X'); ax.set_ylabel('Variable Y')
save(fig, 'ejemplo_scatter.png')

# plt.bar
fig, ax = plt.subplots(figsize=(8, 5))
categorias = ['A', 'B', 'C', 'D']
valores = [23, 45, 56, 78]
ax.bar(categorias, valores, color='teal')
ax.set_title('plt.bar() — Barras verticales')
ax.set_ylabel('Valor')
save(fig, 'ejemplo_bar.png')

# plt.barh
fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(categorias, valores, color='teal', edgecolor='black', height=0.6)
ax.set_title('plt.barh() — Barras horizontales')
ax.set_xlabel('Valor')
save(fig, 'ejemplo_barh.png')

# plt.hist
fig, ax = plt.subplots(figsize=(8, 5))
datos = np.random.normal(100, 15, 1000)
ax.hist(datos, bins=30, color='skyblue', edgecolor='white')
ax.set_title('plt.hist() — Histograma')
ax.set_xlabel('Valor'); ax.set_ylabel('Frecuencia')
save(fig, 'ejemplo_hist.png')

# plt.boxplot
fig, ax = plt.subplots(figsize=(8, 5))
datos_box = [np.random.normal(0, 1, 100), np.random.normal(2, 1.5, 100)]
bp = ax.boxplot(datos_box, tick_labels=['Grupo A', 'Grupo B'], patch_artist=True)
for patch in bp['boxes']:
    patch.set_facecolor('lightblue')
ax.set_title('plt.boxplot() — Caja y bigotes')
ax.set_ylabel('Valor')
save(fig, 'ejemplo_boxplot.png')

# plt.pie
fig, ax = plt.subplots(figsize=(8, 5))
tamaños = [30, 20, 50]
etiquetas = ['A', 'B', 'C']
ax.pie(tamaños, labels=etiquetas, autopct='%1.1f%%', startangle=90)
ax.set_title('plt.pie() — Torta (usar con cautela)')
save(fig, 'ejemplo_pie.png')

# plt.imshow
fig, ax = plt.subplots(figsize=(8, 5))
matriz = np.random.rand(10, 10)
im = ax.imshow(matriz, cmap='viridis')
ax.set_title('plt.imshow() — Matriz como imagen')
fig.colorbar(im, ax=ax)
save(fig, 'ejemplo_imshow.png')

# plt.fill_between
fig, ax = plt.subplots(figsize=(8, 5))
x = np.linspace(0, 10, 100)
y = np.sin(x)
ax.fill_between(x, y - 0.3, y + 0.3, alpha=0.2, color='blue')
ax.plot(x, y, color='blue')
ax.set_title('plt.fill_between() — Áreas e intervalos')
ax.set_xlabel('X'); ax.set_ylabel('Y')
save(fig, 'ejemplo_fill_between.png')

# plt.errorbar
fig, ax = plt.subplots(figsize=(8, 5))
x = np.arange(5)
y = [10, 15, 13, 18, 16]
errores = [1, 2, 1.5, 2.5, 1]
ax.errorbar(x, y, yerr=errores, fmt='o', capsize=4, color='darkgreen')
ax.set_title('plt.errorbar() — Barras de error')
ax.set_xticks(x)
ax.set_xticklabels(['A', 'B', 'C', 'D', 'E'])
ax.set_ylabel('Valor')
save(fig, 'ejemplo_errorbar.png')

# Subplots
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
axes[0, 0].plot(x, y, color='steelblue')
axes[0, 0].set_title('plot')
axes[0, 1].scatter(np.random.randn(50), np.random.randn(50), alpha=0.5)
axes[0, 1].set_title('scatter')
axes[1, 0].hist(np.random.normal(0, 1, 1000), bins=20, color='skyblue', edgecolor='white')
axes[1, 0].set_title('hist')
axes[1, 1].boxplot([np.random.normal(0, 1, 100), np.random.normal(2, 1, 100)])
axes[1, 1].set_title('boxplot')
fig.suptitle('Subplots con API de objetos', fontsize=14, fontweight='bold')
plt.tight_layout()
save(fig, 'ejemplo_subplots.png')

# ── Seaborn univariados ──

# histplot
fig, ax = plt.subplots(figsize=(8, 5))
sns.histplot(df['salario'], bins=30, kde=True, color='steelblue', ax=ax)
ax.set_title('sns.histplot() — Histograma con KDE')
save(fig, 'ejemplo_sns_histplot.png')

# kdeplot
fig, ax = plt.subplots(figsize=(8, 5))
sns.kdeplot(df['salario'], fill=True, color='coral', ax=ax)
ax.set_title('sns.kdeplot() — Densidad')
save(fig, 'ejemplo_sns_kdeplot.png')

# displot
fig = sns.displot(df['salario'], kde=True, rug=True, color='darkgreen', height=5, aspect=1.5)
fig.figure.suptitle('sns.displot() — Distribución genérica', y=1.02)
save(fig.figure, 'ejemplo_sns_displot.png')

# ── Seaborn bivariados ──

# scatterplot
fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(data=df, x='experiencia', y='salario', hue='lenguaje', size='horas', alpha=0.7, ax=ax)
ax.set_title('sns.scatterplot() — Scatter con agrupamiento')
save(fig, 'ejemplo_sns_scatterplot.png')

# lineplot
fig, ax = plt.subplots(figsize=(8, 5))
sns.lineplot(data=df, x='año', y='salario', hue='lenguaje', marker='o', errorbar=('ci', 95), ax=ax)
ax.set_title('sns.lineplot() — Tendencia con IC automático')
save(fig, 'ejemplo_sns_lineplot.png')

# barplot
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=df, x='lenguaje', y='salario', hue='genero', dodge=True, ax=ax)
ax.set_title('sns.barplot() — Barras con intervalo de confianza')
save(fig, 'ejemplo_sns_barplot.png')

# countplot
fig, ax = plt.subplots(figsize=(8, 5))
sns.countplot(data=df, x='lenguaje', hue='genero', dodge=True, ax=ax)
ax.set_title('sns.countplot() — Conteo categórico')
save(fig, 'ejemplo_sns_countplot.png')

# boxplot
fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(data=df, x='lenguaje', y='salario', hue='dedicacion', width=0.6, ax=ax)
ax.set_title('sns.boxplot() — Caja y bigotes por grupo')
save(fig, 'ejemplo_sns_boxplot.png')

# violinplot
fig, ax = plt.subplots(figsize=(8, 5))
sns.violinplot(data=df, x='lenguaje', y='salario', inner='quartile', hue='genero', split=True, ax=ax)
ax.set_title('sns.violinplot() — Densidad + boxplot')
save(fig, 'ejemplo_sns_violinplot.png')

# boxenplot
fig, ax = plt.subplots(figsize=(8, 5))
sns.boxenplot(data=df, x='lenguaje', y='salario', ax=ax)
ax.set_title('sns.boxenplot() — Letter-value plot')
save(fig, 'ejemplo_sns_boxenplot.png')

# stripplot
fig, ax = plt.subplots(figsize=(8, 5))
sns.stripplot(data=df, x='lenguaje', y='salario', jitter=True, alpha=0.3, hue='genero', dodge=True, ax=ax)
ax.set_title('sns.stripplot() — Puntos individuales')
save(fig, 'ejemplo_sns_stripplot.png')

# swarmplot (muestreo para no matar el rendimiento)
fig, ax = plt.subplots(figsize=(8, 5))
sns.swarmplot(data=df.sample(150), x='lenguaje', y='salario', size=3, hue='genero', dodge=True, ax=ax)
ax.set_title('sns.swarmplot() — Puntos sin solapar')
save(fig, 'ejemplo_sns_swarmplot.png')

# heatmap
fig, ax = plt.subplots(figsize=(8, 5))
corr = df[['salario', 'experiencia', 'horas']].corr()
sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdBu_r', vmin=-1, vmax=1, linewidths=0.5, ax=ax)
ax.set_title('sns.heatmap() — Mapa de calor de correlaciones')
save(fig, 'ejemplo_sns_heatmap.png')

# jointplot
fig = sns.jointplot(data=df, x='experiencia', y='salario', kind='reg', color='purple', height=6)
fig.figure.suptitle('sns.jointplot() — Scatter + marginales', y=1.02)
save(fig.figure, 'ejemplo_sns_jointplot.png')

# ── Seaborn multivariados ──

# pairplot
fig = sns.pairplot(df[['salario', 'experiencia', 'horas', 'lenguaje']].sample(100), hue='lenguaje', corner=True, diag_kind='kde', height=2)
fig.figure.suptitle('sns.pairplot() — Matriz de scatter', y=1.02)
save(fig.figure, 'ejemplo_sns_pairplot.png')

# lmplot
fig = sns.lmplot(data=df, x='experiencia', y='salario', hue='lenguaje', col='dedicacion',
                 scatter_kws={'alpha': 0.5}, line_kws={'linewidth': 2}, height=4, aspect=1.2)
fig.figure.suptitle('sns.lmplot() — Regresión por panel', y=1.02)
save(fig.figure, 'ejemplo_sns_lmplot.png')

# catplot
fig = sns.catplot(data=df, x='lenguaje', y='salario', kind='violin', col='genero', col_wrap=2,
                  height=4, aspect=1.2)
fig.figure.suptitle('sns.catplot() — Gráfico categórico genérico', y=1.02)
save(fig.figure, 'ejemplo_sns_catplot.png')

# relplot
fig = sns.relplot(data=df, x='experiencia', y='salario', hue='lenguaje', size='horas',
                  col='dedicacion', kind='scatter', height=4, aspect=1.2)
fig.figure.suptitle('sns.relplot() — Relación genérica con facetas', y=1.02)
save(fig.figure, 'ejemplo_sns_relplot.png')

# ── Personalizaciones ──

# Paletas de colores
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
# Secuencial
sns.barplot(data=df, x='lenguaje', y='salario', palette='viridis', ax=axes[0, 0])
axes[0, 0].set_title('Paleta secuencial: viridis')
# Divergente
sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, ax=axes[0, 1])
axes[0, 1].set_title('Paleta divergente: coolwarm')
# Categórica
sns.boxplot(data=df, x='lenguaje', y='salario', palette='Set2', ax=axes[1, 0])
axes[1, 0].set_title('Paleta categórica: Set2')
# Continuo en scatter
sc = axes[1, 1].scatter(df['experiencia'], df['salario'], c=df['horas'], cmap='plasma')
axes[1, 1].set_title('Mapa de color continuo: plasma')
fig.colorbar(sc, ax=axes[1, 1])
fig.suptitle('Paletas de colores en Seaborn', fontsize=14, fontweight='bold')
plt.tight_layout()
save(fig, 'ejemplo_paletas.png')

# Anotaciones
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(df['experiencia'].sort_values().values, np.sort(df['salario'].values), color='steelblue')
ax.set_title('Anotaciones y textos')
ax.set_xlabel('Experiencia (años)')
ax.set_ylabel('Salario')
ax.annotate('Outlier', xy=(20, 850000), xytext=(15, 750000),
            arrowprops=dict(arrowstyle='->', color='red'))
ax.text(2, 750000, 'Zona de entrada', fontsize=10, color='green')
save(fig, 'ejemplo_anotaciones.png')

# Contextos
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
contexts = ['paper', 'notebook', 'talk', 'poster']
for idx, ctx in enumerate(contexts):
    sns.set_context(ctx)
    ax = axes[idx // 2, idx % 2]
    sns.boxplot(data=df, x='lenguaje', y='salario', ax=ax)
    ax.set_title(f"Contexto: '{ctx}'")
fig.suptitle('Comparación de contextos de Seaborn', fontsize=16, fontweight='bold')
plt.tight_layout()
save(fig, 'ejemplo_contextos.png')

# Restaurar contexto default
sns.set_context('notebook')

print('\n✅ Todas las imágenes generadas en:', IMG_DIR)
