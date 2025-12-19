import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

# --------------------
# ORRIAREN KONFIGURAZIOA
# --------------------
st.set_page_config(
    page_title="Funtzioen simulazioa",
    layout="wide"
)

# --------------------
# FUNTZIO EZAGUNEN DIBUZIONARIOA
# --------------------
funciones_reconocidas = {
    "FUNTZIO LINEALA": {
        "Adierazpen algebraikoa": "f(x)=m·x + b",
        "Izate eremua": "ℝ",
        "Monotonia": "Handitzen: m>0 denean, Txikitzen: m<0 denean",
        "Kurbatura": "Ahurra eta ganbila",
        "Ebaki puntuak": "Abzisa ardatza: -b/a, Ordenatu ardatza: y=b",
        "Asintotak": "Ez ditu",
        "Deribatua": "f′(x)=m",
        "Alderantzizkoa": "f⁻¹(x)=(x-b)/m"
    },
    "2. MAILAKO FUNTZIO POLINOMIKOA": {
        "Adierazpen algebraikoa": "f(x)=a·x² + b·x + c",
        "Izate eremua": "ℝ",
        "Monotonia": "Mutur erlatibo bakarra (maximoa edo minimoa) du f′(x)=0 den puntuan",
        "Kurbatura": "Ez dute inflexio-punturik (n−2=0). Hau da, funtzioa oso-osorik ahurra (∪) edo ganbila (∩) da bere izate eremu osoan, ez du kurbadura aldatzen",
        "Ebaki puntuak": "(-b ± √(b²-4ac))/(2a). Ordenatu ardatza gehienez 2 puntutan ebaki dezakete",
        "Asintotak": "Ez ditu",
        "Deribatua": "f′(x)=2ax+b",
        "Alderantzizkoa": "Ez du ℝ-n!!!!!!!!!!!!"
    },
    "FUNTZIO POLINOMIKOA": {
        "Adierazpen algebraikoa": "f(x)=a_n·xⁿ + ... + a1·x + a0 (n≥3)",
        "Izate eremua": "ℝ",
        "Monotonia": "Gehienez n−1 izan ditzakete. Adibidez, 3. mailako funtzio batek bi mutur (maximo bat eta minimo bat) izan ditzake",
        "Kurbatura": "n−2 inflexio-puntu izan ditzakete gehienez. 3. mailako funtzio baten kasuan, beti dago inflexio-puntu bat, non kurbadura aldatu egiten den (ahur izatetik ganbil izatera edo alderantziz)",
        "Ebaki puntuak": "Ordenatu ardatza gehienez n puntutan ebaki dezakete (adibidez, 3. mailako batek gehienez 3 puntu)",
        "Asintotak": "Ez ditu",
        "Deribatua": "f′(x)=n⋅x^(n−1)",
        "Alderantzizkoa": "Normalean ez du!!!!!!!!!!!!!"
    },
    "FUNTZIO ESPONENTZIALA": {
        "Adierazpen algebraikoa": "f(x)=eˣ",
        "Izate eremua": "orokorrean: ℝ",
        "Monotonia": "Beti gorakorra da bere deribatua (e^x) beti positiboa delako",
        "Kurbatura": "Konbexa",
        "Ebaki puntuak": "Ez du",
        "Asintotak": "Horizontala izan ohi du: y = 0",
        "Deribatua": "f′(x)=e^x",
        "Alderantzizkoa": "logₐ(x)"
    },
    "FUNTZIO LOGARITMIKOA": {
        "Adierazpen algebraikoa": "f(x)=lnx",
        "Izate eremua": "Logaritmo barrukoak positiboa izan behar du (adibidez, ln(4−x) kasuan x<4)",
        "Monotonia": "Handitzen da a>1 denean",
        "Kurbatura": "Konkaboa",
        "Ebaki puntuak": "x = 1",
        "Asintotak": "Asintota bertikala izan ohi du logaritmoaren argumentua 0 denean",
        "Deribatua": "f′(x)=1/x",
        "Alderantzizkoa": "aˣ"
    },
    "FUNTZIO KONSTANTEA": {
        "Adierazpen algebraikoa": "f(x)=k",
        "Izate eremua": "ℝ",
        "Monotonia": "0",
        "Kurbatura": "0",
        "Ebaki puntuak": "Abzisa ardatza: (0,k); Ordenatu ardatza: ez du ebakitzen (k=0 denean izan ezik).",
        "Asintotak": "Ez ditu",
        "Deribatua": "f′(x)=0",
        "Alderantzizkoa": "Ez du k≠0 denean"
    },
    "FUNTZIO IRRAZIONALA": {
        "Adierazpen algebraikoa": "√x, x^(1/n), ...",
        "Izate eremua": "Erroaren indizea bikoitia denean, errokizunak ≥0 izan behar du. Adibidez, f(x)= (x+1)^(1/2) funtzioan, izate-eremua x≥−1 da, hau da, [−1,+∞)",
        "Monotonia": "f′(x)=0",
        "Kurbatura": "f′′(x)=0",
        "Ebaki puntuak": "Ordenatu ardatza: y=0; Abzisa ardatza: x=0 (lortutako puntua funtzioaren izate-eremuaren barruan badago)",
        "Asintotak": "Bertikalak: Izendatzailea duten funtzio irrazionaletan (izendatzailea zero egiten den puntuetan); Horizontalak: Limitea infinituan kalkulatuz lortzen dira; adibidez, y=0 asintota horizontala izan daiteke x→+∞ denean", 
        "Alderantzizkoa": "Ez du normalean"
 },
    "FUNTZIO ARRAZIONALA": {
        "Adierazpen algebraikoa": "f(x)=(Q(x))/(P(x))",
        "Izate eremua": "R−{Q(x)=0}",
        "Monotonia/Kurbadura": "Deribatuak anulatzen diren puntuetan eta izate-eremutik kanpoko puntuetan aztertzen da",
        "Ebaki puntuak": " Ordenatu ardatza: P(x)=0",
        "Asintotak": "Bertikalak: Q(x)=0 denean; Horizontalak: Limitea infinituan balio finitu bat denean; Zeiharrak: Zenbakitzailearen maila izendatzailearena baino unitate bat handiagoa denean"
    }
}

# --------------------
# BOTON ?-AREN ESTADOA
# --------------------
if "mostrar_pista" not in st.session_state:
    st.session_state.mostrar_pista = False

# --------------------
# GOIBURUA
# --------------------
col_q, col_title = st.columns([1, 12])

with col_q:
    if st.button("❓"):
        st.session_state.mostrar_pista = not st.session_state.mostrar_pista

with col_title:
    st.title("Funtzioen simulazio interaktiboa")

# --------------------
# PISTA PANELA (BARENAK IREKITZEN DENEAN)
# --------------------
if st.session_state.mostrar_pista:
    st.info("**Pista: adierazpen algebraikoak:**")
    for nombre, datos in funciones_reconocidas.items():
        st.write(f"**{nombre}** → {datos['adierazpen algebraikoa']}")

# --------------------
# INPUT ETA GRÁFICOA
# --------------------
col_left, col_right = st.columns([1, 2])
x = sp.symbols("x")

with col_right:
    st.subheader("Gráfica")
    funcion_texto = st.text_input("Sartu f(x):", value="x**2")

    try:
        f = sp.sympify(funcion_texto)
        f_num = sp.lambdify(x, f, "numpy")
        x_vals = np.linspace(-10, 10, 400)
        y_vals = f_num(x_vals)

        fig, ax = plt.subplots()
        ax.plot(x_vals, y_vals)
        ax.grid(True)
        st.pyplot(fig)

    except:
        st.error("Funtzioa ez da zuzena")

# --------------------
# FUNTZIO MOTAREN DETEKZIOA
# --------------------
def detectar_tipo(f_expr):
    try:
        if f_expr.is_number:
            return "Konstantea"
        elif f_expr.is_polynomial():
            grado = sp.degree(f_expr)
            if grado == 1:
                return "Lineala"
            elif grado == 2:
                return "2. mailako funtzio polinomikoa"
            else:
                return "Funtzio polinomikoa"
        elif f_expr.has(sp.exp):
            return "Exponentziala"
        elif f_expr.has(sp.log):
            return "Logaritmikoa"
        elif any(isinstance(term, sp.Pow) and term.exp.is_Rational and term.exp != 1 for term in f_expr.args):
            return "Funtzio irrazionala"
        else:
            return None
    except:
        return None

with col_left:
    st.subheader("Ezaugarriak")
    tipo = detectar_tipo(f)
    if tipo in funciones_reconocidas:
        datos = funciones_reconocidas[tipo]
        for clave, valor in datos.items():
            st.write(f"**{clave}:** {valor}")
    else:
        st.warning("Coming soon…")
