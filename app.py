import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import re

# =============================
# ORRIALDEAREN KONFIGURAZIOA
# =============================
st.set_page_config(
    page_title="-FUNTZIOEN PORTFOLIOA-",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =============================
# ESTILOA (MINIMALISTA – EZ UKITUA)
# =============================
st.markdown("""
<style>
.stApp {
    background-color: #ffffff;
    color: #333333;
}
h1, h2, h3, h4, h5, h6, p, span, div {
    color: #333333;
}
.funtzio-tipo {
    background-color: #d3d3d3;
    font-weight: bold;
    padding: 4px 8px;
    border-radius: 4px;
    display: inline-block;
    margin-bottom: 6px;
}
</style>
""", unsafe_allow_html=True)

# =============================
# FUNTZIO MOTAK
# =============================
funtzioak = {
    "FUNTZIO LINEALA": {
        "Adierazpen aljebraikoa": "f(x)=mx+b",
        "Izate eremua": "ℝ",
        "Monotonia": "Gorakorra / Beherakorra",
        "Kurbatura": "Ez du",
        "Ebaki puntuak": "2",
        "Asintotak": "Ez ditu",
        "Deribatua": "m",
        "Alderantzizkoa": "Bai"
    },
    "2. MAILAKO FUNTZIO POLINOMIKOA": {
        "Adierazpen aljebraikoa": "f(x)=ax²+bx+c",
        "Izate eremua": "ℝ",
        "Monotonia": "Maximo edo minimo",
        "Kurbatura": "Bai",
        "Ebaki puntuak": "≤2",
        "Asintotak": "Ez ditu",
        "Deribatua": "2ax+b",
        "Alderantzizkoa": "-"
    },
    "FUNTZIO POLINOMIKOA": {
        "Adierazpen aljebraikoa": "f(x)=axⁿ+…",
        "Izate eremua": "ℝ",
        "Monotonia": "Anitza",
        "Kurbatura": "Anitza",
        "Ebaki puntuak": "≤n",
        "Asintotak": "Ez ditu",
        "Deribatua": "Bai",
        "Alderantzizkoa": "-"
    },
    "FUNTZIO ESPONENTZIALA": {
        "Adierazpen aljebraikoa": "f(x)=a^x",
        "Izate eremua": "ℝ",
        "Monotonia": "Gorakorra",
        "Kurbatura": "-",
        "Ebaki puntuak": "-",
        "Asintotak": "y=0",
        "Deribatua": "a^x ln(a)",
        "Alderantzizkoa": "-"
    },
    "FUNTZIO LOGARITMIKOA": {
        "Adierazpen aljebraikoa": "f(x)=ln(x)",
        "Izate eremua": "x>0",
        "Monotonia": "Gorakorra",
        "Kurbatura": "-",
        "Ebaki puntuak": "(1,0)",
        "Asintotak": "x=0",
        "Deribatua": "1/x",
        "Alderantzizkoa": "-"
    },
    "FUNTZIO KONSTANTEA": {
        "Adierazpen aljebraikoa": "f(x)=k",
        "Izate eremua": "ℝ",
        "Monotonia": "Konstantea",
        "Kurbatura": "Ez du",
        "Ebaki puntuak": "-",
        "Asintotak": "-",
        "Deribatua": "0",
        "Alderantzizkoa": "-"
    },
    "FUNTZIO IRRAZIONALA": {
        "Adierazpen aljebraikoa": "f(x)=√x",
        "Izate eremua": "x≥0",
        "Monotonia": "-",
        "Kurbatura": "-",
        "Ebaki puntuak": "(0,0)",
        "Asintotak": "-",
        "Deribatua": "-",
        "Alderantzizkoa": "-"
    }
}

# =============================
# ESTADO
# =============================
if "pistak" not in st.session_state:
    st.session_state.pistak = False

# =============================
# LAYOUT NAGUSIA — 3 ZUTABE
# =============================
col_left, col_center, col_right = st.columns(3)

# -----------------------------
# EZKERRA — IZENBURUA + PISTAK
# -----------------------------
with col_left:
    st.markdown("""
    <h3>-FUNTZIOEN PORTFOLIOA-</h3>
    <p style='font-size:13px;'>Saioa Otegi Merino</p>
    """, unsafe_allow_html=True)

    if st.button("Pistak..."):
        st.session_state.pistak = not st.session_state.pistak

    if st.session_state.pistak:
        for izena, d in funtzioak.items():
            st.write(f"**{izena}** → {d['Adierazpen aljebraikoa']}")

# -----------------------------
# ERDIA — INPUT + GRAFIKOA
# -----------------------------
with col_center:
    x = sp.symbols("x")

    f_input = st.text_input(
        "✎ Idatzi funtzioa (x^2, √x, x^(1/2), e^x, 3^x, pi*x…)",
        "x^2"
    )

    # ---- GARBIKETA ----
    f_clean = f_input.replace("^", "**")
    f_clean = re.sub(r"√\s*([a-zA-Z0-9_()]+)", r"sqrt(\1)", f_clean)

    try:
        f = sp.sympify(
            f_clean,
            locals={"e": sp.E, "pi": sp.pi}
        )

        x_vals = np.linspace(-5, 5, 400)

        if f.free_symbols == set():
            y_vals = np.full_like(x_vals, float(f))
        else:
            f_num = sp.lambdify(
                x,
                f,
                modules=[{"pi": np.pi, "e": np.e}, "numpy"]
            )
            with np.errstate(all="ignore"):
                y_vals = f_num(x_vals)
                y_vals = np.where(np.isfinite(y_vals), y_vals, np.nan)

        fig, ax = plt.subplots(figsize=(4, 2.5))
        ax.plot(x_vals, y_vals, color="#333333", linewidth=2)
        ax.grid(True, linestyle="--", alpha=0.4)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        st.pyplot(fig)

    except:
        st.warning("⚠️ Funtzioa ez da zuzena")

# -----------------------------
# ESKUINA — EZAUGARRIAK
# -----------------------------
with col_right:
    st.subheader("︙EZAUGARRIAK︙")

    try:
        tipo = None

        if f.free_symbols == set():
            tipo = "FUNTZIO KONSTANTEA"

        elif any(
            p.is_Pow and p.exp.is_Rational and p.exp.q == 2
            for p in f.atoms(sp.Pow)
        ):
            tipo = "FUNTZIO IRRAZIONALA"

        elif any(p.is_Pow and p.base.has(x) for p in f.atoms(sp.Pow)):
            tipo = "FUNTZIO ESPONENTZIALA"

        elif f.has(sp.log):
            tipo = "FUNTZIO LOGARITMIKOA"

        elif f.is_polynomial():
            deg = sp.degree(f)
            if deg == 1:
                tipo = "FUNTZIO LINEALA"
            elif deg == 2:
                tipo = "2. MAILAKO FUNTZIO POLINOMIKOA"
            else:
                tipo = "FUNTZIO POLINOMIKOA"

        if tipo in funtzioak:
            st.markdown(
                f"<div class='funtzio-tipo'>{tipo}</div>",
                unsafe_allow_html=True
            )
            for k, v in funtzioak[tipo].items():
                st.write(f"**{k}**: {v}")
        else:
            st.write("🚧 Laster erabilgarri")

    except:
        st.write("—")
