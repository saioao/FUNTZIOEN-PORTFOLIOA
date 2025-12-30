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
.stApp { background-color: #ffffff; color: #333333; }
h1, h2, h3, h4, h5, h6, p, span, div { color: #333333; }
.funtzio-tipo {
    background-color: #d3d3d3; font-weight: bold; padding: 4px 8px; border-radius: 4px;
    display: inline-block; margin-bottom: 6px;
}
button[data-baseweb="button"] {
    background-color: #d3d3d3 !important; color: #ffffff !important; font-weight: bold !important;
    padding: 4px 8px !important; border-radius: 4px !important; margin-bottom: 6px !important;
}
button[data-baseweb="button"]:hover { background-color: #c6c6c6 !important; }
</style>
""", unsafe_allow_html=True)

# =============================
# FUNTZIO MOTAK
# =============================
funtzioak = {
    "FUNTZIO LINEALA": {"Adierazpen aljebraikoa": "f(x)=mx+b", "Izate eremua": "ℝ", "Irudi multzoa": "ℝ", "Monotonia": "Gorakorra: m>0; Beherakorra: m<0", "Kurbatura": "Ahurra eta ganbila batera", "Ebaki puntuak": "Abzisa ardatza: x=-b/m; Ordenatu ardatza: y=b", "Asintotak": "Ez ditu", "Deribatua": "f′(x)=m", "Alderantzizkoa": "f⁻¹(x)=(x-b)/m"},
    "2. MAILAKO FUNTZIO POLINOMIKOA": {"Adierazpen aljebraikoa": "f(x)=ax²+bx+c", "Izate eremua": "ℝ", "Irudi multzoa": "(−∞,f(xv)] edo [f(xv),+∞)", "Monotonia": "Mutur erlatibo bakarra (maximoa edo minimoa): f′(x)=0", "Kurbatura": "Ez du inflexio-punturik (beti ahurra/beti ganbila)", "Ebaki puntuak": "Abzisa ardatza: ax2+bx+c=0; Ordenatu ardatza: x=0-->f(0)=c", "Asintotak": "Ez ditu", "Deribatua": "f′(x)=2ax+b", "Alderantzizkoa": "-"},
    "FUNTZIO POLINOMIKOA": {"Adierazpen aljebraikoa": "f(x)=ax^n+⋯+bx+c", "Izate eremua": "ℝ", "Irudi multzoa": "Mailaren eta koefiziente nagusiaren arabera", "Monotonia": "Gehienez n−1 mutur erlatibo izan ditzake", "Kurbatura": "Gehienez n−2 inflexio-puntu izan ditzake", "Ebaki puntuak": "Abzisa ardatza: f(x)=0; Ordenatu ardatza: x=0-->f(0)=a0", "Asintotak": "Ez ditu", "Deribatua": "f′(x)=n⋅x^(n-1)", "Alderantzizkoa": "Ez du"},
    "FUNTZIO ESPONENTZIALA": {"Adierazpen aljebraikoa": "f(x)=a·b^x", "Izate eremua": "ℝ", "Irudi multzoa": "(0, +∞)", "Monotonia": "Gorakorra/Beherakorra beti", "Kurbatura": "Ahurra edo ganbila beti", "Ebaki puntuak": "Abzisa ardatza: ez du ebakitzen; Ordenatu ardatza: x=0-->f(0)=a⋅b^0=a", "Asintotak": "Bertikala: ez du ;Horizontala: y=0", "Deribatua": "f′(x)=e^x", "Alderantzizkoa": "f⁻¹(x)=logb(x)"},
    "FUNTZIO LOGARITMIKOA": {"Adierazpen aljebraikoa": "f(x)=ln(x)", "Izate eremua": "(0,+∞)", "Irudi multzoa": "ℝ", "Monotonia": "Gorakorra edo beherakorra", "Kurbatura": "Ahurra beti", "Ebaki puntuak": "Abzisa ardatza: logb(x)=0-->x=1; Ordenatu ardatza: ez du ebakitzen", "Asintotak": "Bertikala: x=0; Horizontala: ez du", "Deribatua": "f′(x)=1/x", "Alderantzizkoa": "f⁻¹(x)=bx"},
    "FUNTZIO KONSTANTEA": {"Adierazpen aljebraikoa": "f(x)=k", "Izate eremua": "ℝ", "Irudi multzoa": "{k}", "Monotonia/Kurbatura": "Horizontala eta ez du kurbadurarik", "Ebaki puntuak": "Abzisa ardatza: (0,k); Ordenatu ardatza: x=0-->f(0)=k", "Asintotak": "Bertikala: Ez du; Horizontala: y=k", "Deribatua": "f′(x)=0", "Alderantzizkoa": "Ez du"},
    "FUNTZIO IRRAZIONALA": {"Adierazpen aljebraikoa": "f(x)=√ax+b", "Izate eremua": "x≥0", "Irudi multzoa": "[0, +∞)", "Monotonia": "Gorakorra edo beherakorra", "Kurbatura": "Ahurra edo ganbila", "Ebaki puntuak": "Abzisa ardatza: f(x)=0-->erroaren barrukoa=0; Ordenatu ardatza: y=0", "Asintotak": "Ez ditu", "Alderantzizkoa": "f⁻¹(x)=x2"},
    "FUNTZIO ARRAZIONALA": {"Adierazpen aljebraikoa": "f(x)=(P(x))/(Q(x))", "Izate eremua": "ℝ−{Q(x)=0}", "Irudi multzoa": "Asintoten eta funtzioaren formaren araberakoa", "Monotonia": "Ez du", "Kurbatura": "Ahurra edo ganbila", "Ebaki puntuak": "Ordenatu ardatza: Q(x)=0", "Asintotak": "Bertikala/Horizontala/Zeiharra", "Deribatua": "[f/g]′= (f′·g-f·g′)/(g²)", "Alderantzizkoa": "Ez du"}
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
    st.markdown("<h3>-FUNTZIOEN PORTFOLIOA-</h3><p style='font-size:13px;'>Saioa Otegi Merino</p>", unsafe_allow_html=True)
    pistak_clicked = st.button("❔")
    if pistak_clicked:
        st.session_state.pistak = not st.session_state.pistak
    if st.session_state.pistak:
        for izena, d in funtzioak.items():
            st.markdown(f"<div class='funtzio-tipo'>{izena} → {d['Adierazpen aljebraikoa']}</div>", unsafe_allow_html=True)

import re
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# ERDIA — INPUT + GRAFIKOA
# -----------------------------
with col_center:
    x = sp.symbols("x")
    f_input = st.text_input("✎ f(x)= (x², x³, x⁴⁵, √(x), e^x, pi+2...)", "x")

    # -----------------------------
    # Superíndizeak ordezkatzeko funtzio segurua
    sup_map = {"⁰":"0","¹":"1","²":"2","³":"3","⁴":"4","⁵":"5",
               "⁶":"6","⁷":"7","⁸":"8","⁹":"9"}
    def replace_superscripts(expr):
        # Regex: superíndize bat edo gehiago segidan
        pattern = re.compile(r"[⁰¹²³⁴⁵⁶⁷⁸⁹]+")
        def repl(match):
            return "**" + "".join(sup_map[c] for c in match.group())
        return pattern.sub(repl, expr)

    # -----------------------------
    # Sarrera garbitzea
    f_clean = f_input.replace("^", "**")    # x^2 -> x**2
    f_clean = f_clean.replace("√", "sqrt")  # √x -> sqrt(x)
    f_clean = replace_superscripts(f_clean) # x³, x⁴⁵ -> x**3, x**45

    # -----------------------------
    # Funtzioa interpretatzen saiatu
    try:
        f = sp.sympify(f_clean, locals={"e": sp.E, "pi": sp.pi})
        x_vals = np.linspace(-5, 5, 400)

        if f.free_symbols == set():
            y_vals = np.full_like(x_vals, float(f))
        else:
            f_num = sp.lambdify(x, f, modules=[{"pi": np.pi,"e": np.e},"numpy"])
            with np.errstate(all="ignore"):
                y_vals = f_num(x_vals)
            # Balio ez finituak edo jauzi handiak ezabatu
            y_vals = np.where(np.isfinite(y_vals), y_vals, np.nan)
            jauziak = np.abs(np.diff(y_vals))
            y_vals[1:][jauziak=∞] = np.nan
            y_vals = np.where(np.abs(y_vals)>1e3, np.nan, y_vals)

        # -----------------------------
        # Grafikoa erakutsi
        fig, ax = plt.subplots(figsize=(4,2.5))
        ax.plot(x_vals, y_vals, color="#333333", linewidth=2)
        ax.grid(True, linestyle="--", alpha=0.4)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        st.pyplot(fig)

    except Exception as e:
        st.warning(f"Funtzioa interpretatzen errorea: {e}")
        fig, ax = plt.subplots(figsize=(4,2.5))
        ax.grid(True, linestyle="--", alpha=0.4)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        st.pyplot(fig)



# -----------------------------
# ESKUINA — EZAUGARRIAK
# -----------------------------
with col_right:
    st.subheader("︙EZAUGARRIAK︙")
    try:
        tipo = None
        if f.free_symbols == set():
            tipo = "FUNTZIO KONSTANTEA"
        elif f.has(x):
            if any(p.is_Pow and p.exp.is_Rational and p.exp.q == 2 for p in f.atoms(sp.Pow)):
                tipo = "FUNTZIO IRRAZIONALA"
            elif f.has(sp.exp) or any(p.is_Pow and x in p.exp.free_symbols and not p.base.has(x) for p in f.atoms(sp.Pow)):
                tipo = "FUNTZIO ESPONENTZIALA"
            elif f.is_polynomial():
                deg = sp.degree(f, x)
                if deg == 1:
                    tipo = "FUNTZIO LINEALA"
                elif deg == 2:
                    tipo = "2. MAILAKO FUNTZIO POLINOMIKOA"
                else:
                    tipo = "FUNTZIO POLINOMIKOA"
            elif f.has(sp.log):
                tipo = "FUNTZIO LOGARITMIKOA"
            elif f.is_rational_function(x):
                tipo = "FUNTZIO ARRAZIONALA"

        # 🔑 Mezua 8 funtzio motetatik kanpo dagoenean
        if tipo:
            st.markdown(f"<div class='funtzio-tipo'>{tipo}</div>", unsafe_allow_html=True)
            for k,v in funtzioak[tipo].items():
                st.write(f"**{k}**: {v}")
        else:
            st.write("👀 Errepasatu, (kontuan eduki adibideak)")

    except:
        st.write("—")
