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

    # ARRAZIONALAK: polinomio baten zatidura
    elif f.is_rational_function(x):
        tipo = "FUNTZIO ARRAZIONALA"

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
