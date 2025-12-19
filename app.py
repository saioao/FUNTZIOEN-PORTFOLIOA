import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# CONFIGURACIÓN DE LA PÁGINA
# -----------------------------
st.set_page_config(
    page_title="Funtzioen simulazioa",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
.stApp { background-color: #ffffff; color: #333333; }
h1, h2, h3, h4, h5, h6, p, span, div { color: #333333; }
.funtzio-tipo {
    background-color: #d3d3d3;
    font-weight: bold;
    padding: 4px 8px;
    border-radius: 4px;
    display: inline-block;
    margin-bottom: 6px;
}
.stButton>button { width: 100%; height: 3em; }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# FUNTZIO MOTAK
# -----------------------------
funtzioak = {
    "Funtzio lineala": {
        "adierazpen aljebraikoa": "a·x + b",
        "izate eremua": "ℝ",
        "monotonia": "Gorakorra a>0 bada, beherakorra a<0 bada",
        "kurbatura": "Nulua",
        "ebaki puntuak": "x = -b/a",
        "asintotak": "Ez dauka",
        "alderantzizkoa": "(x - b)/a"
    },
    "2. mailako funtzio polinomikoa": {
        "adierazpen aljebraikoa": "a·x² + b·x + c",
        "izate eremua": "ℝ",
        "monotonia": "Erpinaren araberakoa",
        "kurbatura": "Ahurra edo ganbila",
        "ebaki puntuak": "Bigarren mailako formula",
        "asintotak": "Ez dauka",
        "alderantzizkoa": "Ez dauka ℝ-n"
    },
    "Funtzio polinomikoa": {
        "adierazpen aljebraikoa": "P(x) ≥ 3",
        "izate eremua": "ℝ",
        "monotonia": "Polinomioaren araberakoa",
        "kurbatura": "Polinomioaren araberakoa",
        "ebaki puntuak": "Polinomioaren araberakoa",
        "asintotak": "Ez dauka",
        "alderantzizkoa": "Normalean ez du"
    },
    "Funtzio arrazionala": {
        "adierazpen aljebraikoa": "P(x)/Q(x)",
        "izate eremua": "Q(x)=0 izan ezik",
        "monotonia": "Deribatuaren araberakoa",
        "kurbatura": "Aldakorra",
        "ebaki puntuak": "P(x)=0",
        "asintotak": "Bertikalak / horizontalak",
        "alderantzizkoa": "Funtzioaren araberakoa"
    },
    "Funtzio esponentziala": {
        "adierazpen aljebraikoa": "a^x",
        "izate eremua": "ℝ",
        "monotonia": "Gorakorra",
        "kurbatura": "Ganbila",
        "ebaki puntuak": "Ez du X ardatza mozten",
        "asintotak": "y = 0",
        "alderantzizkoa": "logₐ(x)"
    },
    "Funtzio logaritmikoa": {
        "adierazpen aljebraikoa": "log(x)",
        "izate eremua": "x > 0",
        "monotonia": "Gorakorra",
        "kurbatura": "Ahurra",
        "ebaki puntuak": "x = 1",
        "asintotak": "x = 0",
        "alderantzizkoa": "a^x"
    },
    "Funtzio konstantea": {
        "adierazpen aljebraikoa": "c",
        "izate eremua": "ℝ",
        "monotonia": "Konstantea",
        "kurbatura": "Nulua",
        "ebaki puntuak": "c-ren araberakoa",
        "asintotak": "Ez dauka",
        "alderantzizkoa": "Ez dauka"
    },
    "Funtzio irrazionala": {
        "adierazpen aljebraikoa": "√x",
        "izate eremua": "x ≥ 0",
        "monotonia": "Gorakorra",
        "kurbatura": "Ahurra",
        "ebaki puntuak": "x = 0",
        "asintotak": "Ez dauka",
        "alderantzizkoa": "x²"
    }
}

# -----------------------------
# ESTADO
# -----------------------------
if "pistak" not in st.session_state:
    st.session_state.pistak = False

# -----------------------------
# LAYOUT: 3 COLUMNAS IGUALES
# -----------------------------
col_left, col_center, col_right = st.columns(3)

# -----------------------------
# COLUMNA IZQUIERDA (❓)
# -----------------------------
with col_left:
    if st.button("❓"):
        st.session_state.pistak = not st.session_state.pistak
    if st.session_state.pistak:
        for izena, d in funtzioak.items():
            st.write(f"**{izena}** → {d['adierazpen aljebraikoa']}")

# -----------------------------
# COLUMNA CENTRAL (GRAFICO + INPUT)
# -----------------------------
with col_center:
    x = sp.symbols("x")

    f_input = st.text_input("✏️ Idatzi funtzioa", "x^2")

    f_clean = (
        f_input
        .replace("^", "**")
        .replace("√", "sqrt")
    )

    try:
        f = sp.sympify(f_clean)
        f_num = sp.lambdify(x, f, "numpy")

        x_vals = np.linspace(-5, 5, 250)
        y_vals = f_num(x_vals)

        fig, ax = plt.subplots(figsize=(4, 2.5))
        ax.plot(x_vals, y_vals, color="#333333", linewidth=2)
        ax.grid(True, linestyle="--", alpha=0.4)
        ax.set_facecolor("white")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.tick_params(colors="#333333")

        st.pyplot(fig)
    except:
        st.warning("⚠️ Funtzioa ez da zuzena")

# -----------------------------
# COLUMNA DERECHA (EZAUGARRIAK)
# -----------------------------
with col_right:
    st.subheader("Ezaugarriak")

    try:
        tipo = None

        if f.is_number:
            tipo = "Funtzio konstantea"
        elif f.is_polynomial():
            deg = sp.degree(f)
            if deg == 1:
                tipo = "Funtzio lineala"
            elif deg == 2:
                tipo = "2. mailako funtzio polinomikoa"
            else:
                tipo = "Funtzio polinomikoa"
        elif f.is_rational_function(x):
            tipo = "Funtzio arrazionala"
        elif f.has(sp.exp):
            tipo = "Funtzio esponentziala"
        elif f.has(sp.log):
            tipo = "Funtzio logaritmikoa"
        elif f.has(sp.sqrt):
            tipo = "Funtzio irrazionala"

        if tipo in funtzioak:
            st.markdown(f"<div class='funtzio-tipo'>{tipo}</div>", unsafe_allow_html=True)
            for k, v in funtzioak[tipo].items():
                st.write(f"**{k.capitalize()}**: {v}")
        else:
            st.write("🚧 Laster erabilgarri")

    except:
        st.write("—")
