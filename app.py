import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# ORRIALDEAREN KONFIGURAZIOA MINIMALISTA
# -----------------------------
st.set_page_config(
    page_title="Funtzioen simulazioa",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #ffffff;
        color: #000000;
    }
    h1, h2, h3, h4, h5, h6, p, span, div {
        color: #000000;
    }
    .funtzio-tipo {
        color: gray;
        font-weight: bold;
        text-decoration: underline;
    }
    .stButton>button {
        height: 3em;
        width: 100%;
        font-size:16px;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# FUNTZIO MOTAK (Ez aldatu)
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
        "kurbatura": "Ahurra edo ganbila a-ren arabera",
        "ebaki puntuak": "Bigarren mailako formula",
        "asintotak": "Ez dauka",
        "alderantzizkoa": "Ez dauka ℝ-n"
    },
    "Funtzio polinomikoa": {
        "adierazpen aljebraikoa": "P(x)≥3",
        "izate eremua": "ℝ",
        "monotonia": "Polinomioaren arabera",
        "kurbatura": "Polinomioaren arabera",
        "ebaki puntuak": "Polinomioaren arabera",
        "asintotak": "Ez dauka",
        "alderantzizkoa": "Normalean ez du"
    },
    "Funtzio arrazionala": {
        "adierazpen aljebraikoa": "P(x)/Q(x)",
        "izate eremua": "ℝ, Q(x)=0 denean izan ezik",
        "monotonia": "Deribatuaren araberakoa",
        "kurbatura": "Aldakorra",
        "ebaki puntuak": "P(x)=0",
        "asintotak": "Bertikalak / horizontalak",
        "alderantzizkoa": "Funtzioaren araberakoa"
    },
    "Funtzio esponentziala": {
        "adierazpen aljebraikoa": "a^x",
        "izate eremua": "ℝ",
        "monotonia": "Gorakorra a>1 bada",
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
# BOTÓN PISTAK
# -----------------------------
if "pistak_ireki" not in st.session_state:
    st.session_state.pistak_ireki = False

# -----------------------------
# GOIKO LERROA: Botón ❓ eta inputa
# -----------------------------
col_botoia, col_input = st.columns([1,3])
with col_botoia:
    if st.button("❓"):
        st.session_state.pistak_ireki = not st.session_state.pistak_ireki

with col_input:
    f_input = st.text_input("✏️ Idatzi funtzioa", "x")

if st.session_state.pistak_ireki:
    st.info("**Pista: adierazpen algebraikoak**")
    for izena, datuak in funtzioak.items():
        st.write(f"**{izena}** → {datuak['adierazpen aljebraikoa']}")

# -----------------------------
# ERDIKO LERROA: Grafikoa eta Ezaugarriak
# -----------------------------
col_grafikoa, col_ezaugarriak = st.columns([2,1])
x = sp.symbols("x")

# Grafikoa txikia eta zentratua
with col_grafikoa:
    st.subheader("📊 Grafikoa")
    try:
        f = sp.sympify(f_input)
        f_num = sp.lambdify(x, f, "numpy")
        x_balioak = np.linspace(-5,5,250)
        y_balioak = f_num(x_balioak)

        fig, ax = plt.subplots(figsize=(4,3))
        ax.plot(x_balioak, y_balioak, color="#000000", linewidth=2)
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.set_facecolor("#ffffff")
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color("#000000")
        ax.spines['bottom'].set_color("#000000")
        ax.tick_params(colors="#000000")
        st.pyplot(fig, use_container_width=True)
    except Exception as e:
        st.error(f"⚠️ Funtzioa ez da zuzena: {e}")

# Ezaugarriak
with col_ezaugarriak:
    st.subheader("📌 Ezaugarriak")
    try:
        tipo = None
        f = sp.sympify(f_input)
        # Detekzio automatikoa
        if f.is_number:
            tipo = "Funtzio konstantea"
        elif f.is_polynomial():
            g = sp.degree(f)
            if g == 1:
                tipo = "Funtzio lineala"
            elif g == 2:
                tipo = "2. mailako funtzio polinomikoa"
            else:
                tipo = "Funtzio polinomikoa"
        elif f.is_rational_function(x):
            tipo = "Funtzio arrazionala"
        elif f.has(sp.exp):
            tipo = "Funtzio esponentziala"
        elif f.has(sp.log):
            tipo = "Funtzio logaritmikoa"
        elif any(isinstance(term, sp.Pow) and term.exp.is_Rational and term.exp != 1 for term in f.args):
            tipo = "Funtzio irrazionala"

        if tipo in funtzioak:
            st.markdown(f"<span class='funtzio-tipo'>{tipo}</span>", unsafe_allow_html=True)
            for k, v in funtzioak[tipo].items():
                st.write(f"**{k.capitalize()}**: {v}")
        else:
            st.warning("🚧 Laster erabilgarri")
            st.write("Funtzio mota hau oraindik ez dago inplementatuta.")
    except Exception as e:
        st.error(f"⚠️ Arazoa ezaugarriak erakusten: {e}")
