import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import os

np.random.seed(42)
n = 100
edad = np.random.randint(22, 65, n)
salario = edad * 800 + np.random.normal(0, 5000, n) + 25000
genero = np.random.choice(["F", "M"], n)

df = pd.DataFrame({"edad": edad, "salario": salario, "genero": genero})

os.makedirs("img_viz", exist_ok=True)

# --- 1. Matplotlib + Seaborn style ---
plt.figure(figsize=(8, 5))
colors = {"F": "#e74c3c", "M": "#3498db"}
for g in ["F", "M"]:
    subset = df[df["genero"] == g]
    plt.scatter(subset["edad"], subset["salario"], c=colors[g], label=g, alpha=0.7, edgecolors="white", s=80)
plt.title("Salario vs Edad (Matplotlib + Seaborn)", fontsize=14, fontweight="bold")
plt.xlabel("Edad (años)", fontsize=11)
plt.ylabel("Salario ($)", fontsize=11)
plt.legend(title="Género")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("img_viz/comparativa_seaborn.png", dpi=150)
plt.close()

# --- 2. Plotly style (clean, white bg, subtle grid) ---
plt.figure(figsize=(8, 5))
colors = {"F": "#FF6B6B", "M": "#4ECDC4"}
for g in ["F", "M"]:
    subset = df[df["genero"] == g]
    plt.scatter(subset["edad"], subset["salario"], c=colors[g], label=g, alpha=0.75, edgecolors="white", s=90, linewidth=0.8)
plt.title("Salario vs Edad (Plotly Express)", fontsize=15, fontweight="bold", color="#2c3e50")
plt.xlabel("Edad (años)", fontsize=12, color="#555")
plt.ylabel("Salario ($)", fontsize=12, color="#555")
plt.legend(title="Género", frameon=True, fancybox=True, shadow=True)
plt.grid(True, alpha=0.15, linestyle="--")
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.set_facecolor("#fafafa")
plt.tight_layout()
plt.savefig("img_viz/comparativa_plotly.png", dpi=150, facecolor="white")
plt.close()

# --- 3. Bokeh style (darker, glyph-like, custom grid) ---
plt.figure(figsize=(8, 5))
colors = {"F": "#f1c40f", "M": "#9b59b6"}
for g in ["F", "M"]:
    subset = df[df["genero"] == g]
    plt.scatter(subset["edad"], subset["salario"], c=colors[g], label=g, alpha=0.85, s=70, marker="o")
plt.title("Salario vs Edad (Bokeh)", fontsize=14, fontweight="bold", color="#1a1a2e")
plt.xlabel("Edad (años)", fontsize=11, color="#1a1a2e")
plt.ylabel("Salario ($)", fontsize=11, color="#1a1a2e")
plt.legend(title="Género", loc="upper left")
ax = plt.gca()
ax.set_facecolor("#f5f5f0")
ax.grid(True, color="#ccccbb", linestyle="-", alpha=0.6)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#888")
ax.spines["bottom"].set_color("#888")
plt.tight_layout()
plt.savefig("img_viz/comparativa_bokeh.png", dpi=150, facecolor="#f5f5f0")
plt.close()

# --- 4. Streamlit style (app simulation) ---
fig, ax = plt.subplots(figsize=(9, 6))
# Simulate a streamlit app container
fig.patch.set_facecolor("#ffffff")
ax.set_facecolor("#ffffff")

# Title bar simulation
ax.text(0.5, 1.08, "Mi primera app con Streamlit", transform=ax.transAxes,
        fontsize=16, fontweight="bold", ha="center", color="#1f1f1f")
ax.text(0.5, 1.02, "Scatterplot interactivo de salario vs edad", transform=ax.transAxes,
        fontsize=11, ha="center", color="#555")

colors = {"F": "#ff4b4b", "M": "#0068c9"}
for g in ["F", "M"]:
    subset = df[df["genero"] == g]
    ax.scatter(subset["edad"], subset["salario"], c=colors[g], label=g, alpha=0.7, s=80, edgecolors="white")

ax.set_title("Salario vs Edad", fontsize=13, fontweight="bold", pad=20, color="#1f1f1f")
ax.set_xlabel("Edad (años)", fontsize=11, color="#333")
ax.set_ylabel("Salario ($)", fontsize=11, color="#333")
ax.legend(title="Género")
ax.grid(True, alpha=0.2)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Add a "sidebar" hint on the left
fig.text(0.02, 0.5, "Sidebar\n• Filtro género\n• Rango edad\n• Descargar CSV",
         fontsize=9, color="#555", va="center", ha="left",
         bbox=dict(boxstyle="round,pad=0.4", facecolor="#f0f2f6", edgecolor="#d1d5db"))

plt.tight_layout(rect=[0.12, 0, 1, 1])
plt.savefig("img_viz/comparativa_streamlit.png", dpi=150, facecolor="white")
plt.close()

print("4 imágenes generadas en img_viz/")
