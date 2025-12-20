import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

# =============================
# ORRIALDEAREN KONFIGURAZIOA
# =============================
st.set_page_config(
    page_title="-FUNTZIOEN PORTFOLIOA-",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =============================
# ESTILOA (MINIMALISTA)
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
        "Kurbatura": "Ahurra eta ganbila",
        "Ebaki puntuak": "Abzisa ardatza: x=-b/m; Ordenatu ardatza: y=b",
        "Asintotak": "Ez ditu",
        "Deribatua": "f'(x)=m",
        "Alderantzizkoa": "f^-1(x)=(x-b)/m"
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
        "Adierazpen aljebraikoa": " f(x)=ax^n+⋯+bx+c",
        "Izate eremua": "ℝ",
        "Monotonia": "Gehienez n−1 mutur erlatibo izan ditzake",
        "Kurbatura": "Gehienez n−2 inflexio-puntu izan ditzake",
        "Ebaki puntuak": "Ordenatu ardatza gehienez n puntutan ebakitzen du",
        "Asintotak": "Ez ditu",
        "Deribatua": "f′(x)=n⋅x^(n-1)",
        "Alderantzizkoa": "-"
    },
    "FUNTZIO ARRAZIONALA": {
        "Adierazpen aljebraikoa": "f(x)=(Q(x))/(P(x))",
        "Izate eremua": "ℝ−{Q(x)=0}",
        "Monotonia/Kurbadura": "Deribatuak anulatzen diren puntuetan eta izate-eremutik kanpoko puntuetan aztertzen da",
        "Ebaki puntuak": "Ordenatu ardatza: P(x)=0",
        "Asintotak": "Bertikala: Q(x)=0; Horizontala: Limitea infinituan balio finitu bat denean; Zeiharra: Zenbakitzailearen maila izendatzailearena baino unitate bat handiagoa denean",
        "Deribatua": "[f/g]′= (f′·g-f·g′)/(g²)",
        "Alderantzizkoa": "-"
    },
    "FUNTZIO ESPONENTZIALA": {
        "Adierazpen aljebraikoa": "f(x)=e^x",
        "Izate eremua": "ℝ",
        "Monotonia": "Gorakorra beti",
        "Kurbatura": "-",
        "Ebaki puntuak": "-",
        "Asintotak": "Horizontala: y = 0",
        "Deribatua": "f′(x)=e^x",
        "Alderantzizkoa": "-"
    },
    "FUNTZIO LOGARITMIKOA": {
        "Adierazpen aljebraikoa": "f(x)=lnx",
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
        "Monotonia/Kurbadura": "Ez da ez gorakorra ez beherakorra (horizontal mantentzen da) eta ez du kurbadurarik",
        "Ebaki puntuak": "Abzisa ardatza: (0, k); Ordenatu ardatza: ez du ebakitzen (k=0 denean izan ezik)",
        "Asintotak": "Ez ditu",
        "Deribatua": "f′(x)=0",
        "Alderantzizkoa": "-"
    },
    "FUNTZIO IRRAZIONALA": {
        "Adierazpen aljebraikoa": "f(x)=√x",
        "Izate eremua": "Erroaren indizea bikoitia denean, errokizunak positiboa edo zero (≥0) izan behar du. Adibidez, f(x)=√x+1 funtzioan, izate-eremua x≥−1 da, hau da, [−1,+∞)",
        "Monotonia": "f′(x)=0 ekuazioaren puntu kritikoak",
        "Kurbatura": "f′’(x)=0 ekuazioaren inflexio-puntuak",
        "Ebaki puntuak": "Ordenatu ardatza: y=0; Abzisa ardatza: x=0",
        "Asintotak": "Bertikala: Izendatzailea duten funtzio irrazionaletan, izendatzailea zero egiten den puntuetan; Horizontalak: Limitea infinituan kalkulatuz lortzen dira; adibidez, y=0 asintota horizontala izan daiteke x→+∞ denean",
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
# LAYOUT NAGUSIA (3 ZUTABE)
# =============================
col_left, col_center, col_right = st.columns(3)

# -----------------------------
# Pistak... PISTAK (EZKERRA)
# -----------------------------
with col_left:
    st.markdown(
        """
        <h3 style='margin-bottom:4px;'>
            -FUNTZIOEN PORTFOLIOA-
        </h3>
        <p style='color:#666666; font-size:13px; margin-top:0;'>
            Saioa Otegi Merino
        </p>
        """,
        unsafe_allow_html=True
    )

with col_left:
    if st.button("Pistak..."):
        st.session_state.pistak = not st.session_state.pistak
    if st.session_state.pistak:
        for izena, d in funtzioak.items():
            st.write(f"**{izena}** → {d['Adierazpen aljebraikoa']}")

# -----------------------------
# GRAFIKOA + INPUT (ERDIA)
# -----------------------------
with col_center:
    x = sp.symbols("x")

    f_input = st.text_input("✎ Idatzi funtzioa (Adib. x^3+x^2+x+5)", "x^2")

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
# EZAUGARRIAK (ESKUMA)
# -----------------------------
with col_right:
    st.subheader("︙EZAUGARRIAK︙")

    try:
        tipo = None

        if f.is_number:
            tipo = "FUNTZIO KONSTANTEA"
        elif f.is_polynomial():
            deg = sp.degree(f)
            if deg == 1:
                tipo = "FUNTZIO LINEALA"
            elif deg == 2:
                tipo = "2. MAILAKO FUNTZIO POLINOMIKOA"
            else:
                tipo = "FUNTZIO POLINOMIKOA"
        elif f.is_rational_function(x):
            tipo = "FUNTZIO ARRAZIONALA"
        elif f.has(sp.exp):
            tipo = "FUNTZIO ESPONENTZIALA"
        elif f.has(sp.log):
            tipo = "FUNTZIO LOGARITMIKOA"
        elif f.has(sp.sqrt):
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

    except:
        st.write("—")
