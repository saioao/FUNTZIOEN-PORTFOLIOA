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
    .stApp { background-color: #ffffff; color: #000000; }
    h1, h2, h3, h4, h5, h6, p, span, div { color: #000000; }
    .funtzio-tipo {
        background-color: #d3d3d3;
        font-weight: bold;
        text-decoration: underline;
        padding: 4px 8px;
        border-radius: 4px;
        display: inline-block;
        margin-bottom: 5px;
    }
    .stButton>button { height: 3em; width: 100%; font-size:16px; }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# FUNTZIO MOTAK
# -----------------------------
funtzioak = {
    "Funtzio lineala": {"adierazpen aljebraikoa": "a·x + b", "izate eremua": "ℝ",
                        "monotonia": "Gorakorra a>0 bada, beherakorra a<0 bada",
                        "kurbatura": "Nulua", "ebaki puntuak": "x = -b/a",
                        "asintotak": "Ez dauka", "alderantzizkoa": "(x - b)/a"},
    "2. mailako funtzio polinomikoa": {"adierazpen aljebraikoa": "a·x² + b·x + c",
                                       "izate eremua": "ℝ", "monotonia": "Erpinaren araberakoa",
                                       "kurbatura": "Ahurra edo ganbila a-ren arabera",
                                       "ebaki puntuak": "Bigarren mailako formula",
                                       "asintotak": "Ez dauka", "alderantzizkoa": "Ez dauka ℝ-n"},
    "Funtzio polinomikoa": {"adierazpen aljebraikoa": "P(x)≥3", "izate eremua": "ℝ",
                            "monotonia": "Polinomioaren arabera", "kurbatura": "Polinomioaren arabera",
                            "ebaki puntuak": "Polinomioaren arabera", "asintotak": "Ez dauka",
                            "alderantzizkoa": "Normalean ez du"},
    "Funtzio arrazionala": {"adierazpen aljebraikoa": "P(x)/Q(x)", "izate eremua": "ℝ, Q(x)=0 denean izan ezik",
                            "monotonia": "Deribatuaren araberakoa", "kurbatura": "Aldakorra",
                            "ebaki puntuak": "P(x)=0", "asintotak": "Bertikalak / horizontalak",
                            "alderantzizkoa": "Funtzioaren araberakoa"},
    "Funtzio esponentziala": {"adierazpen aljebraikoa": "a^x", "izate eremua": "ℝ",
                              "monotonia": "Gorakorra a>1 bada", "kurbatura": "Ganbila",
                              "ebaki puntuak": "Ez du X ardatza mozten", "asintotak": "y = 0",
                              "alderantzizkoa": "logₐ(x)"},
    "Funtzio logaritmikoa": {"adierazpen aljebraikoa": "log(x)", "izate eremua": "x > 0",
                             "monotonia": "Gorakorra", "kurbatura": "Ahurra",
                             "ebaki puntuak": "x = 1", "asintotak": "x = 0",
                             "alderantzizkoa": "a^x"},
    "Funtzio konstantea": {"adierazpen aljebraikoa": "c", "izate eremua": "ℝ",
                           "monotonia": "Konstantea", "kurbatura": "Nulua",
                           "ebaki puntuak": "c-ren araberakoa", "asintotak": "Ez dauka",
                           "alderantzizkoa": "Ez dauka"},
    "Funtzio irrazionala": {"adierazpen aljebraikoa": "√x", "izate eremua": "x ≥ 0",
                            "monotonia": "Gorakorra", "kurbatura": "Ahurra",
                            "ebaki puntuak": "x = 0", "asintotak": "Ez dauka",
                            "alderantzizkoa": "x²"}
}

# -----------------------------
# SESIÓN PARA PESTAÑA ❓
# -----------------------------
if "pistak_ireki" not in st.session_state:
    st.session_state.pistak_ireki = False

# -----------------------------
# LAYOUT PRINCIPAL: ❓ izquierda + contenido
# -----------------------------
if st.session_state.pistak_ireki:
    col_panel, col_main = st.columns([1,5])
else:
    col_panel, col_main = st.columns([0.05,5])

# -----------------------------
# PANEL PISTAS (solo si abierto)
# -----------------------------
with col_panel:
    if st.session_state.pistak_ireki:
        st.info("**Pista: adierazpen algebraikoak**")
        for izena, datuak in funtzioak.items():
            st.write(f"**{izena}** → {datuak['adierazpen aljebraikoa']}")

# -----------------------------
# CONTENIDO PRINCIPAL
# -----------------------------
with col_main:
    x = sp.symbols("x")

    # Gráfico centrado usando columnas internas
    col_l, col_c, col_r = st.columns([1,1,1])
    with col_c:
        try:
            f = sp.sympify(f_input if 'f_input' in locals() else "x")
            f_num = sp.lambdify(x, f, "numpy")
            x_vals = np.linspace(-5,5,250)
            y_vals = f_num(x_vals)

            fig, ax = plt.subplots(figsize=(2.5,2))
            ax.plot(x_vals, y_vals, color="#000000", linewidth=2)
            ax.grid(True, linestyle='--', alpha=0.5)
            ax.set_facecolor("#ffffff")
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color("#000000")
            ax.spines['bottom'].set_color("#000000")
            ax.tick_params(colors="#000000")
            st.pyplot(fig)
        except Exception as e:
            st.error(f"⚠️ Funtzioa ez da zuzena: {e}")

    # Input debajo del gráfico
    f_input = st.text_input("✏️ Idatzi funtzioa", f_input if 'f_input' in locals() else "x")

    # Características a la derecha (usando columnas)
    col_graf, col_ez = st.columns([3,2])
    with col_ez:
        st.subheader("📌 Ezaugarriak")
        try:
            tipo = None
            f = sp.sympify(f_input)
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
                for k,v in funtzioak[tipo].items():
                    st.write(f"**{k.capitalize()}**: {v}")
            else:
                st.warning("🚧 Laster erabilgarri")
                st.write("Funtzio mota hau oraindik ez dago inplementatuta.")
        except Exception as e:
            st.error(f"⚠️ Arazoa ezaugarriak erakusten: {e}")
