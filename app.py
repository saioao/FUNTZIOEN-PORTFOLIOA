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
    "FUNTZIO LINEALA": {"Adierazpen aljebraikoa": "f(x)=mx+b", "Izate eremua": "ℝ", "Irudi multzoa": "ℝ", "Monotonia": "Gorakorra: m>0; Beherakorra: m<0", "Kurbatura": "Ahurra eta ganbila batera", "Ebaki puntuak": "Abzisa ardatza: x=-b/m (m≠0); Ordenatu ardatza: y=f(0)=b", "Asintotak": "Ez ditu", "Deribatua": "f′(x)=m", "Alderantzizkoa": "f⁻¹(x)=(x-b)/m"},
    "2. MAILAKO FUNTZIO POLINOMIKOA": {"Adierazpen aljebraikoa": "f(x)=ax²+bx+c", "Izate eremua": "ℝ", "Irudi multzoa": "(−∞,f(xv)] edo [f(xv),+∞)", "Monotonia": "Mutur erlatibo bakarra (maximoa edo minimoa): f′(x)=0", "Kurbatura": "Ez du inflexio-punturik (beti ahurra/beti ganbila)", "Ebaki puntuak": "Abzisa ardatza: ax2+bx+c=0; Ordenatu ardatza: x=0-->f(0)=c", "Asintotak": "Ez ditu", "Deribatua": "f′(x)=2ax+b", "Alderantzizkoa": "Ez du"},
    "FUNTZIO POLINOMIKOA": {"Adierazpen aljebraikoa": "f(x)=ax^n+ … +bx+c", "Izate eremua": "ℝ", "Irudi multzoa": "Mailaren eta koefiziente nagusiaren arabera", "Monotonia": "Gehienez n−1 mutur erlatibo izan ditzake", "Kurbatura": "Gehienez n−2 inflexio-puntu izan ditzake", "Ebaki puntuak": "Abzisa ardatza: f(x)=0; Ordenatu ardatza: x=0-->f(0)=c", "Asintotak": "Ez ditu", "Deribatua": "f′(x)=n⋅x^(n-1)", "Alderantzizkoa": "Ez du"},
    "FUNTZIO ESPONENTZIALA": {"Adierazpen aljebraikoa": "f(x)=a·b^x", "Izate eremua": "ℝ", "Irudi multzoa": "(0, +∞)", "Monotonia": "Gorakorra/Beherakorra beti", "Kurbatura": "Ahurra edo ganbila beti", "Ebaki puntuak": "Abzisa ardatza: ez du ebakitzen; Ordenatu ardatza: x=0-->f(0)=a⋅b^0=a", "Asintotak": "Bertikala: ez du ;Horizontala: y=0", "Deribatua": "f'(x) = a·ln(b)·b^x", "Alderantzizkoa": "f⁻¹(x)=log_b(x)"},
    "FUNTZIO LOGARITMIKOA": {"Adierazpen aljebraikoa": "f(x)=log_a(x)", "Izate eremua": "(0,+∞)", "Irudi multzoa": "ℝ", "Monotonia": "Gorakorra: a>1 ; Beherakorra: 0<a<1 ", "Kurbatura": "Ahurra/ganbila beti", "Ebaki puntuak": "Abzisa ardatza: x=1; Ordenatu ardatza: ez du ebakitzen", "Asintotak": "Bertikala: x=0; Horizontala: ez du", "Deribatua": "f′(x)=1/(x ln(a))", "Alderantzizkoa": "f⁻¹(x)=a^x"},
    "FUNTZIO KONSTANTEA": {"Adierazpen aljebraikoa": "f(x)=k", "Izate eremua": "ℝ", "Irudi multzoa": "{k}", "Monotonia/Kurbatura": "Horizontala eta ez du kurbadurarik", "Ebaki puntuak": "Abzisa ardatza: ez du ebakitzen (k=0 denean izan ezik); Ordenatu ardatza: (0, k)", "Asintotak": "Bertikala: Ez du; Horizontala: y=k", "Deribatua": "f′(x)=0", "Alderantzizkoa": "Ez du"},
    "FUNTZIO IRRAZIONALA": {"Adierazpen aljebraikoa": "f(x)=√(ax+b)", "Izate eremua": "Errokizunak >= 0 izan behar du", "Irudi multzoa": "[0, +∞)", "Monotonia": "Gorakorra (a>0) edo beherakorra (a<0)", "Kurbatura": "Ahurra edo ganbila", "Ebaki puntuak": "Abzisa ardatza: erroaren barrukoa = 0; Ordenatu ardatza: x=0 izate-eremuan badago", "Asintotak": "Ez ditu", "Alderantzizkoa": "f⁻¹(x)=x²"},
    "FUNTZIO ARRAZIONALA": {"Adierazpen aljebraikoa": "f(x)=P(x)/Q(x)", "Izate eremua": "ℝ−{Q(x)=0}", "Irudi multzoa": "Asintoten eta funtzioaren forma osoaren araberakoa", "Monotonia/Kurbatura": "Deribatuak zero diren puntutan eta izate-eremutik kanpoko puntuetan aztertzen da", "Ebaki puntuak": "Ordenatu ardatza: Q(x)=0", "Asintotak": "Bertikala: Q(x) = 0; Horizontala: Limitea infinituan balio finitu bat denean; Zeiharra: Zenbakitzailearen maila izendatzailearena baino unitate bat handiagoa denean", "Deribatua": "[f/g]′= (f′·g-f·g′)/(g²)", "Alderantzizkoa": "Ez du"}
}

# =============================
# ESTADO
# =============================
if "pistak" not in st.session_state:
    st.session_state.pistak = False

# =============================
# LAYOUT NAGUSIA
# =============================
col_left, col_center, col_right = st.columns(3)

# -----------------------------
# EZKERRA
# -----------------------------
with col_left:
    st.markdown("<h3>-FUNTZIOEN PORTFOLIOA-</h3><p style='font-size:13px;'>Saioa Otegi Merino</p>", unsafe_allow_html=True)
    if st.button("❔"):
        st.session_state.pistak = not st.session_state.pistak
    if st.session_state.pistak:
        for izena, d in funtzioak.items():
            st.markdown(f"<div class='funtzio-tipo'>{izena} → {d['Adierazpen aljebraikoa']}</div>", unsafe_allow_html=True)

# -----------------------------
# ERDIA
# -----------------------------
with col_center:
    x = sp.symbols("x")
    f_input = st.text_input("✎ f(x)= (4*x², √(x), e^x, pi+2, log_2(3x), 1/x...)", "x")

    sup_map = {"⁰":"0","¹":"1","²":"2","³":"3","⁴":"4","⁵":"5","⁶":"6","⁷":"7","⁸":"8","⁹":"9"}
    def replace_superscripts(expr):
        return re.sub(
            r"[⁰¹²³⁴⁵⁶⁷⁸⁹]+",
            lambda m: "**" + "".join(sup_map[c] for c in m.group()),
            expr
        )

    f_clean = f_input.replace("^", "**").replace("√", "sqrt")
    f_clean = replace_superscripts(f_clean)
    f_clean = re.sub(r"log_([0-9a-zA-Z]+)\(([^)]+)\)", r"log(\2,\1)", f_clean)
    f_clean = re.sub(r"(\d)(x)", r"\1*\2", f_clean)

    try:
        f = sp.sympify(f_clean, locals={"e": sp.E, "pi": sp.pi})
        x_vals = np.linspace(-5, 5, 2000)

        if f.free_symbols == set():
            y_vals = np.full_like(x_vals, float(f))
        else:
            f_num = sp.lambdify(x, f, modules=["numpy"])
            y_vals = f_num(x_vals)

        # ==============================
        # JAUZI INFINITUAK EZ MARRAZTU
        # ==============================
        fig, ax = plt.subplots(figsize=(4, 2.5))

        ax.grid(True, linestyle="--", alpha=0.4, zorder=0)
        ax.axhline(0, color="#949494", linewidth=0.5, zorder=0)
        ax.axvline(0, color="#949494", linewidth=0.5, zorder=0)

        # segmentu bakoitza banan-banan margotu, Inf edo NaN dutenak mozteko
        finite_mask = np.isfinite(y_vals)
        start = None
        for i in range(len(x_vals)):
            if finite_mask[i]:
                if start is None:
                    start = i
            else:
                if start is not None:
                    ax.plot(x_vals[start:i], y_vals[start:i], color="#333333", linewidth=1.5, zorder=1)
                    start = None
        # azken segmentua
        if start is not None:
            ax.plot(x_vals[start:], y_vals[start:], color="#333333", linewidth=1.5, zorder=1)

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        st.pyplot(fig)

    except (sp.SympifyError, SyntaxError, TypeError):
        st.error("👀 Adierazpena ez da zuzena. Kontuan izan adibideak.")
    except Exception:
        st.error("❌ Ezin da funtzioa interpretatu.")


# -----------------------------
# ESKUINA
# -----------------------------
with col_right:
    st.subheader("︙EZAUGARRIAK︙")
    try:
        tipo = None

        if f.free_symbols == set():
            tipo = "FUNTZIO KONSTANTEA"

        elif f.is_polynomial():
            gradua = sp.degree(f)
            if gradua == 1:
                tipo = "FUNTZIO LINEALA"
            elif gradua == 2:
                tipo = "2. MAILAKO FUNTZIO POLINOMIKOA"
            else:
                tipo = "FUNTZIO POLINOMIKOA"

        elif f.has(sp.exp):
            tipo = "FUNTZIO ESPONENTZIALA"

        elif f.has(sp.log):
            tipo = "FUNTZIO LOGARITMIKOA"

        elif f.has(sp.sqrt):
            tipo = "FUNTZIO IRRAZIONALA"

        elif f.is_rational_function(x):
            tipo = "FUNTZIO ARRAZIONALA"

        if tipo:
            st.markdown(f"<div class='funtzio-tipo'>{tipo}</div>", unsafe_allow_html=True)
            for k, v in funtzioak[tipo].items():
                st.write(f"**{k}**: {v}")
    except:
        pass
