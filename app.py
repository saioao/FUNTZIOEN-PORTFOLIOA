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
# ESTILOA (EZ UKITUA)
# =============================
st.markdown("""
<style>
.stApp { background-color: #ffffff; color: #333333; }
h1,h2,h3,h4,h5,h6,p,span,div { color: #333333; }
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
# FUNTZIO MOTAK (BERDIN)
# =============================
# ⚠️ hemen zure funtzioak DIKZIONARIOA doa, aldatu gabe
# (ez dut hemen berriro itsatsi luzeegia delako)
# =============================

# =============================
# ESTADO
# =============================
if "pistak" not in st.session_state:
    st.session_state.pistak = False

# =============================
# INPUT NAGUSIA (BEHIN BAKARRIK)
# =============================
x = sp.symbols("x")

f_input = st.text_input(
    "✎ Idatzi funtzioa (Adib. x^3+x^2+x+5)", "x^2"
)

# =============================
# GARBIKETA ZUZENA
# =============================
f_clean = f_input

# berreketak
f_clean = f_clean.replace("^", "**")

# √x → sqrt(x)
f_clean = re.sub(r"√\s*([a-zA-Z0-9_()]+)", r"sqrt(\1)", f_clean)

# =============================
# SYMPY PARSEA (e eta pi barne)
# =============================
f = None
try:
    f = sp.sympify(
        f_clean,
        locals={"e": sp.E, "pi": sp.pi}
    )
except:
    pass

# =============================
# LAYOUT
# =============================
col_left, col_center, col_right = st.columns(3)

# -----------------------------
# EZKERRA — PISTAK
# -----------------------------
with col_left:
    st.markdown("""
    <h3 style='margin-bottom:4px;'>-FUNTZIOEN PORTFOLIOA-</h3>
    <p style='color:#666666; font-size:13px; margin-top:0;'>
        Saioa Otegi Merino
    </p>
    """, unsafe_allow_html=True)

    if st.button("Pistak..."):
        st.session_state.pistak = not st.session_state.pistak

    if st.session_state.pistak:
        for izena, d in funtzioak.items():
            st.write(f"**{izena}** → {d['Adierazpen aljebraikoa']}")

# -----------------------------
# ERDIA — GRAFIKOA
# -----------------------------
with col_center:
    if f is not None:
        try:
            f_num = sp.lambdify(x, f, "numpy")
            x_vals = np.linspace(-5, 5, 400)

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
            st.warning("⚠️ Funtzioa ez da marraztu ahal")
    else:
        st.warning("⚠️ Funtzioa ez da zuzena")

# -----------------------------
# ESKUINA — EZAUGARRIAK
# -----------------------------
with col_right:
    st.subheader("︙EZAUGARRIAK︙")

    if f is not None:
        tipo = None

        # KONSTANTEA (pi, e, pi^2, e+2…)
        if f.is_number:
            tipo = "FUNTZIO KONSTANTEA"

        # POLINOMIOAK
        elif f.is_polynomial():
            deg = sp.degree(f)
            if deg == 1:
                tipo = "FUNTZIO LINEALA"
            elif deg == 2:
                tipo = "2. MAILAKO FUNTZIO POLINOMIKOA"
            else:
                tipo = "FUNTZIO POLINOMIKOA"

        # ESPONENTZIALAK (e^x, 3^x)
        elif any(p.is_Pow and p.exp.has(x) for p in f.atoms(sp.Pow)):
            tipo = "FUNTZIO ESPONENTZIALA"

        # LOGARITMIKOA
        elif f.has(sp.log):
            tipo = "FUNTZIO LOGARITMIKOA"

        # IRRAZIONALA (√x, x^(1/2))
        elif any(
            p.is_Pow and p.exp.is_Rational and p.exp.q == 2
            for p in f.atoms(sp.Pow)
        ):
            tipo = "FUNTZIO IRRAZIONALA"

        if tipo in funtzioak:
            st.markdown(
                f"<div class='funtzio-tipo'>{tipo}</div>",
                unsafe_allow_html=True
            )
            for k, v in funtzioak[tipo].items():
                st.write(f"**{k.capitalize()}**: {v}")
        else:
            st.write("🚧 Laster erabilgarri")
