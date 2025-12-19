import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# ORRIALDEAREN KONFIGURAZIOA
# -----------------------------
st.set_page_config(
    page_title="Funtzioen simulazioa",
    layout="wide"
)

st.title("FUNTZIOEN PORTFOLIOA")
st.write("Idatzi funtzio bat eta ikusi bere grafikoa eta ezaugarriak.")

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
# BOTON PISTAK
# -----------------------------
if "pistak_ireki" not in st.session_state:
    st.session_state.pistak_ireki = False

# -----------------------------
# GOIKO LERROA: Input + Pistak
# -----------------------------
col_input, col_pistak = st.columns([3,1])

with col_input:
    f_input = st.text_input("✏️ Idatzi funtzioa", "x")

with col_pistak:
    if st.button("❓ Pistak ireki/itxi"):
        st.session_state.pistak_ireki = not st.session_state.pistak_ireki

    if st.session_state.pistak_ireki:
        st.info("**Pista: adierazpen aljebraikoak**")
        for izena, datuak in funtzioak.items():
            st.write(f"**{izena}** → {datuak['adierazpen aljebraikoa']}")

# -----------------------------
# BEHEKO LERROA: Grafikoa + Ezaugarriak
# -----------------------------
col_grafikoa, col_ezaugarriak = st.columns([2,1])
x = sp.symbols("x")

# -----------------------------
# GRAFIKOA
# -----------------------------
with col_grafikoa:
    st.subheader("📊 Grafikoa")
    try:
        f = sp.sympify(f_input)
        f_num = sp.lambdify(x, f, "numpy")
        x_balioak = np.linspace(-5,5,300)
        y_balioak = f_num(x_balioak)

        fig, ax = plt.subplots()
        ax.plot(x_balioak, y_balioak)
        ax.grid(True)
        st.pyplot(fig)
    except Exception as e:
        st.error(f"⚠️ Funtzioa ez da zuzena: {e}")

# -----------------------------
# FUNTZIO MOTAREN DETEKZIOA
# -----------------------------
def detektatu_mota(f_expr):
    try:
        if f_expr.is_number:
            return "Funtzio konstantea"
        elif f_expr.is_polynomial():
            g = sp.degree(f_expr)
            if g == 1:
                return "Funtzio lineala"
            elif g == 2:
                return "2. mailako funtzio polinomikoa"
            else:
                return "Funtzio polinomikoa"
        elif f_expr.is_rational_function(x):
            return "Funtzio arrazionala"
        elif f_expr.has(sp.exp):
            return "Funtzio esponentziala"
        elif f_expr.has(sp.log):
            return "Funtzio logaritmikoa"
        elif any(isinstance(term, sp.Pow) and term.exp.is_Rational and term.exp != 1 for term in f_expr.args):
            return "Funtzio irrazionala"
        else:
            return None
    except:
        return None

# -----------------------------
# EZAUGARRIAK
# -----------------------------
with col_ezaugarriak:
    st.subheader("📌 Ezaugarriak")
    try:
        f = sp.sympify(f_input)
        tipo = detektatu_mota(f)
        if tipo in funtzioak:
            st.success(tipo)
            for k, v in funtzioak[tipo].items():
                st.write(f"**{k.capitalize()}**: {v}")
        else:
            st.warning("🚧 Laster erabilgarri")
            st.write("Funtzio mota hau oraindik ez dago inplementatuta.")
    except Exception as e:
        st.error(f"⚠️ Arazoa ezaugarriak erakusten: {e}")
