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
# ESTILOA
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
        "Monotonia": "Gorakorra: m>0; Beherakorra: m<0",
        "Kurbatura": "Ahurra eta ganbila batera",
        "Ebaki puntuak": "Abzisa ardatza: x=-b/m; Ordenatu ardatza: y=b",
        "Asintotak": "Ez ditu",
        "Deribatua": "f′(x)=m",
        "Alderantzizkoa": "f-1(x)=(x-b)/m"
    },
    "2. MAILAKO FUNTZIO POLINOMIKOA": {
        "Adierazpen aljebraikoa": "f(x)=ax²+bx+c",
        "Izate eremua": "ℝ",
        "Monotonia": "Mutur erlatibo bakarra (maximoa edo minimoa): f′(x)=0",
        "Kurbatura": "Ez du inflexio-punturik (beti ahurra/beti ganbila)",
        "Ebaki puntuak": "Ordenatu ardatza gehienez 2 puntutan ebakitzen du",
        "Asintotak": "Ez ditu",
        "Deribatua": "f′(x)=2ax+b",
        "Alderantzizkoa": "-"
    },
    "FUNTZIO POLINOMIKOA": {
        "Adierazpen aljebraikoa": "f(x)=axn+⋯+bx+c",
        "Izate eremua": "ℝ",
        "Monotonia": "Gehienez n−1 mutur erlatibo izan ditzake",
        "Kurbatura": "Gehienez n−2 inflexio-puntu izan ditzake",
        "Ebaki puntuak": "≤n",
        "Asintotak": "Ez ditu",
        "Deribatua": "f′(x)=n⋅x^(n-1)",
        "Alderantzizkoa": "-"
    },
    "FUNTZIO ESPONENTZIALA": {
        "Adierazpen aljebraikoa": "f(x)=e^x",
        "Izate eremua": "ℝ",
        "Monotonia": "Gorakorra",
        "Kurbatura": "-",
        "Ebaki puntuak": "-",
        "Asintotak": "Horizontala: y=0",
        "Deribatua": "f′(x)=e^x",
        "Alderantzizkoa": "-"
    },
    "FUNTZIO LOGARITMIKOA": {
        "Adierazpen aljebraikoa": "f(x)=ln(x)",
        "Izate eremua": "Logaritmo barrukoak positiboa izan behar du (adibidez, ln(4−x) kasuan x<4)",
        "Monotonia": "-",
        "Kurbatura": "-",
        "Ebaki puntuak": "Ordenatu ardatza: (1,0) puntuan ebakitzen du",
        "Asintotak": "Asintota bertikala izan ohi du logaritmoaren argumentua 0 denean",
        "Deribatua": "f′(x)=1/x",
        "Alderantzizkoa": "-"
    },
    "FUNTZIO KONSTANTEA": {
        "Adierazpen aljebraikoa": "f(x)=k",
        "Izate eremua": "ℝ",
        "Monotonia/Kurbatura": "Ez da ez gorakorra ez beherakorra (horizontal mantentzen da) eta ez du kurbadurarik",
        "Ebaki puntuak": "Abzisa ardatza: (0,k); Ordenatu ardatza: ez du ebakitzen (k=0 denean izan ezik)",
        "Asintotak": "Ez ditu",
        "Deribatua": "f′(x)=0",
        "Alderantzizkoa": "-"
    },
    "FUNTZIO IRRAZIONALA": {
        "Adierazpen aljebraikoa": "f(x)=√x",
        "Izate eremua": "x≥0",
        "Monotonia": "f′(x)=0 ekuazioaren puntu kritikoak",
        "Kurbatura": "f′’(x)=0 ekuazioaren inflexio-puntuak",
        "Ebaki puntuak": "Abzisa ardatza: x=0; Ordenatu ardatza: y=0",
        "Asintotak": "Bertikala: Izendatzailea duten funtzio irrazionaletan agertzen dira, izendatzailea zero egiten den puntuetan; Horizontala: Limitea infinituan kalkulatuz lortzen dira; adibidez, y=0 asintota horizontala izan daiteke x→+∞ denean",
        "Deribatua": "-",
        "Alderantzizkoa": "-"
    },

     "FUNTZIO ARRAZIONALA": {
        "Adierazpen aljebraikoa": "f(x)=(Q(x))/(P(x))",
        "Izate eremua": "ℝ−{Q(x)=0}",
        "Monotonia/Kurbatura": "Deribatuak anulatzen diren puntuetan eta izate-eremutik kanpoko puntuetan aztertzen da",
        "Ebaki puntuak": "Ordenatu ardatza: P(x)=0",
        "Asintotak": "Bertikala: Q(x)=0; Horizontala: Limitea infinituan balio finitu bat denean; Zeiharra: Zenbakitzailearen maila izendatzailearena baino unitate bat handiagoa denean",
        "Deribatua": "[f/g]′= (f′·g-f·g′)/(g²)",
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
    # Izenburua
    st.markdown("""
    <h3>-FUNTZIOEN PORTFOLIOA-</h3>
    <p style='font-size:13px;'>Saioa Otegi Merino</p>
    """, unsafe_allow_html=True)

    # Pistak botoia
    pistak_clicked = st.button("Pistak...")

    if pistak_clicked:
        st.session_state.pistak = not st.session_state.pistak

    # CSS inline estiloarekin botoia simulatzea (letra zuria, fondo gris)
    st.markdown("""
    <style>
    button[data-baseweb="button"] {
        background-color: #d3d3d3 !important;
        color: #ffffff !important;      /* letra zuria */
        font-weight: bold !important;
        padding: 4px 8px !important;
        border-radius: 4px !important;
        margin-bottom: 6px !important;
    }
    button[data-baseweb="button"]:hover {
        background-color: #c6c6c6 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Pistak zerrenda bistaratzea botoia sakatuta badago
    if st.session_state.pistak:
        for izena, d in funtzioak.items():
            st.markdown(f"<div class='funtzio-tipo'>{izena} → {d['Adierazpen aljebraikoa']}</div>", unsafe_allow_html=True)

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

        # ---------------------------
        # KONSTANTEAK (free_symbols hutsik eta ez dira funtzioak)
        # ---------------------------
        if f.free_symbols == set():
            tipo = "FUNTZIO KONSTANTEA"

        # ---------------------------
        # FUNTZIOAK X-rekin
        # ---------------------------
        elif f.has(x):

            # IRRAZIONALAK: x^(1/2) edo sqrt(x)
            if any(p.is_Pow and p.exp.is_Rational and p.exp.q == 2 for p in f.atoms(sp.Pow)):
                tipo = "FUNTZIO IRRAZIONALA"

            # EXPONENTZIALAK: a^x edo e^x
            elif f.has(sp.exp) or any(
                p.is_Pow and x in p.exp.free_symbols and not p.base.has(x)
                for p in f.atoms(sp.Pow)
            ):
                tipo = "FUNTZIO ESPONENTZIALA"

            # POLINOMIOAK: x^n bakarrik
            elif f.is_polynomial():
                deg = sp.degree(f, x)
                if deg == 1:
                    tipo = "FUNTZIO LINEALA"
                elif deg == 2:
                    tipo = "2. MAILAKO FUNTZIO POLINOMIKOA"
                else:
                    tipo = "FUNTZIO POLINOMIKOA"

            # LOGARITMOAK
            elif f.has(sp.log):
                tipo = "FUNTZIO LOGARITMIKOA"

        # ---------------------------
        # BISTARATZE
        # ---------------------------
        if tipo:
            st.markdown(f"<div class='funtzio-tipo'>{tipo}</div>", unsafe_allow_html=True)
            for k, v in funtzioak[tipo].items():
                st.write(f"**{k}**: {v}")
        else:
            st.write("🚧 Laster erabilgarri")

    except Exception as e:
        st.write("—")

