with col_center:
    x = sp.symbols("x")
    col_l, col_c, col_r = st.columns([1,6,1])
    with col_c:
        # Preparar el input del usuario
        f_raw = st.session_state["f_input"]

        # Reemplazos para SymPy
        f_clean = f_raw.replace("^", "**").replace("√", "sqrt")

        # Input debajo, mismo ancho que el gráfico
        st.session_state["f_input"] = st.text_input("✏️ Idatzi funtzioa", f_raw)

        # Gráfico
        try:
            f = sp.sympify(f_clean)
            f_num = sp.lambdify(x, f, "numpy")
            x_vals = np.linspace(-5,5,250)
            y_vals = f_num(x_vals)

            fig, ax = plt.subplots(figsize=(4,2.5))  # tamaño intermedio
            ax.plot(x_vals, y_vals, color="#333333", linewidth=2)
            ax.grid(True, linestyle='--', alpha=0.5)
            ax.set_facecolor("#ffffff")
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color("#333333")
            ax.spines['bottom'].set_color("#333333")
            ax.tick_params(colors="#333333")
            st.pyplot(fig)
        except Exception as e:
            st.error(f"⚠️ Funtzioa ez da zuzena: {e}")
