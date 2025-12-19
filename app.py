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

st.title("📈 Funtzioen simulazio interaktiboa")
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
# DISEINUA
# -----------------------------
col_ezaugarriak, col_grafikoa = st.columns([1, 2])

# -----------------------------
# FUNTZIOAREN SARRERA
# -----------------------------
st.markdown("---")
f_input = st.text_input("✏️ Idatzi funtzioa (adib.: x**2 + 3*x + 1)", "x")

x = sp.symbols("x")

# -----------------------------
# GRAFIKOA
# -----------------------------
with col_grafikoa:
    st.subheader("📊 Grafikoa")

    try:
        f = sp.sympify(f_input)
        f_num = sp.lambdify(x, f, "numpy")

        x_balioak = np.linspace(-10, 10, 400)
        y_balioak = f_num(x_balioak)

        fig, ax = plt.subplots()
        ax.plot(x_balioak, y_balioak)
        ax.grid(True)
        st.pyplot(fig)

    except:
        st.error("⚠️ Funtzioa ez da zuzena")

# -----------------------------
# EZAUGARRIAK
# -----------------------------
with col_ezaugarriak:
    st.subheader("📌 Ezaugarriak")

    aurkitua = False
    for izena, datuak in funtzioak.items():
        if datuak["adierazpen aljebraikoa"].replace("·", "") in f_input:
            aurkitua = True
            st.success(izena)
            for k, v in datuak.items():
                st.write(f"**{k.capitalize()}**: {v}")
            break

    if not aurkitua:
        st.warning("🚧 Laster erabilgarri")
        st.write("Funtzio mota hau oraindik ez dago inplementatuta.")

# -----------------------------
# LAGUNTZA
# -----------------------------
with st.sidebar:
    st.markdown("## ❓ Pistak")
    for izena, datuak in funtzioak.items():
        st.write(f"**{izena}** → {datuak['adierazpen aljebraikoa']}")
