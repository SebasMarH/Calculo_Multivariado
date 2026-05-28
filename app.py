import streamlit as st
import numpy as np
import plotly.graph_objects as go
import scipy.integrate as integrate

# Configuración de la página
st.set_page_config(
    page_title="Visualizador del Tricilindro de Steinmetz",
    page_icon="📐",
    layout="wide"
)

# Estilos CSS personalizados para una interfaz profesional
st.markdown("""
    <style>
    .main-title {
        color: #f97316;
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .description {
        text-align: center;
        color: #475569;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .result-card {
        background-color: #fff7ed;
        border-left: 5px solid #f97316;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
    }
    .result-title {
        color: #9a3412;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Título y descripción
st.markdown('<div class="main-title">Visualizador del Tricilindroz</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="description">'
    ''
    '</div>', 
    unsafe_allow_html=True
)

# Crear columnas para organizar los controles y la visualización
col1, col2 = st.columns([1, 2])

with col1:
    st.header("🎛️ Parámetros")
    
    # Entrada numérica para el radio
    radius = st.number_input(
        "Ingresa el radio de los cilindros (r):",
        min_value=0.0,
        value=2.0,
        step=0.1,
        help="El valor debe ser mayor que cero."
    )
    
    calcular = st.button("🚀 Calcular y visualizar", use_container_width=True)

if calcular or radius > 0:
    if radius <= 0:
        st.error("⚠️ Por favor, ingresa un valor válido mayor a cero para el radio.")
    else:
        # ---- CÁLCULOS MATEMÁTICOS DE CÁLCULO MULTIVARIADO ----
        # 1. Fórmula exacta analítica
        vol_analitico = 8 * (2 - np.sqrt(2)) * (radius**3)
        
        # 2. Cálculo mediante Integración Numérica Real
        # Integramos la porción de 1/16 del volumen en el primer octante:
        # Región dividida por la línea de simetría y = x:
        # Int1: de 0 a r/sqrt(2) de x * sqrt(r^2 - x^2)
        # Int2: de r/sqrt(2) a r de (r^2 - x^2)
        int1, _ = integrate.quad(lambda x: x * np.sqrt(radius**2 - x**2), 0, radius / np.sqrt(2))
        int2, _ = integrate.quad(lambda x: radius**2 - x**2, radius / np.sqrt(2), radius)
        vol_integral = 16 * (int1 + int2)
        
        with col1:
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown('<div class="result-title">📊 Resultados del Volumen</div>', unsafe_allow_html=True)
            st.write(f"**Radio ingresado ($r$):** {radius:.4f}")
            st.write(f"**Fórmula analítica:** $V = 8(2 - \\sqrt{{2}}) \\cdot r^3$")
            st.markdown(f"**Resultado exacto:** <span style='color:#f97316; font-weight:bold; font-size:1.2rem;'>{vol_analitico:.4f} unidades cúbicas</span>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Sección de explicación matemática con ecuaciones en LaTeX
            with st.expander("📚 Ver planteamiento con Integrales Múltiples"):
                st.write("Por la simetría del sólido, podemos calcular **1/16 del volumen total** en el primer octante usando una integral doble sobre la proyección en el plano $xy$, donde la altura está limitada por los cilindros superiores:")
                st.latex(r"V_{\text{total}} = 16 \times \iint_{D} z(x,y) \, dA")
                st.write("Donde la altura z del techo es la intersección de los cilindros superiores: $z = \min(\sqrt{r^2-x^2}, \sqrt{r^2-y^2})$. Al proyectar sobre el plano $xy$ y dividir la región simétrica mediante la recta $y = x$, la integral se simplifica a:")
                st.latex(r"V = 16 \left[ \int_{0}^{\frac{r}{\\sqrt{2}}} \int_{0}^{x} \sqrt{r^2-x^2}\,dy\,dx + \int_{\frac{r}{\\sqrt{2}}}^{r} \int_{0}^{\sqrt{r^2-x^2}} \sqrt{r^2-x^2}\,dy\,dx \right]")
                st.write("Integrando con respecto a $y$ obtenemos las funciones que resuelve Python en tiempo real:")
                st.latex(r"V = 16 \left[ \int_{0}^{\frac{r}{\\sqrt{2}}} x\sqrt{r^2-x^2}\,dx + \int_{\frac{r}{\\sqrt{2}}}^{r} (r^2-x^2)\,dx \right]")
                st.write(f"**Resultado evaluado numéricamente por la librería SciPy:**")
                st.info(f"**$V_{{\\text{{integral}}}}$ = {vol_integral:.4f} unidades cúbicas**")
                st.caption("¡Nota cómo el resultado de las integrales múltiples coincide con total precisión con la fórmula analítica general!")

        with col2:
            st.header("🔮 Visualización Interactiva 3D")
            
            # ---- GENERACIÓN DEL GRÁFICO 3D CON CAMPO ESCALAR IMPLÍCITO (SDF) ----
            grid_res = 50  # Resolución de la cuadrícula tridimensional
            padding = radius * 1.15
            x = np.linspace(-padding, padding, grid_res)
            y = np.linspace(-padding, padding, grid_res)
            z = np.linspace(-padding, padding, grid_res)
            X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
            
            # Evaluar el campo escalar de los 3 cilindros simultáneamente:
            # f(x,y,z) = max(x^2+y^2-r^2, y^2+z^2-r^2, x^2+z^2-r^2)
            # El sólido comprende los puntos donde f(x,y,z) <= 0. La frontera exacta es f = 0.
            f_val = np.maximum(
                np.maximum(X**2 + Y**2 - radius**2, Y**2 + Z**2 - radius**2),
                X**2 + Z**2 - radius**2
            )
            
            # Crear la Isosuperficie tridimensional con Plotly
            fig = go.Figure(data=go.Isosurface(
                x=X.flatten(),
                y=Y.flatten(),
                z=Z.flatten(),
                value=f_val.flatten(),
                isomin=0.5,        # Renderiza todo el volumen sólido interior
                isomax=1.0,           # La superficie corta exactamente en la frontera matemática 0
                surface_count=1,    # Una capa superficial nítida y lisa
                colorscale='Oranges',
                reversescale=False,
                opacity=0.9,
                showscale=False,
                lighting=dict(
                    ambient=0.5,
                    diffuse=0.8,
                    fresnel=0.3,
                    specular=1.2,
                    roughness=0.3
                ),
                lightposition=dict(x=padding*2, y=padding*2, z=padding*3)
            ))
            
            # Configurar el diseño responsivo y encuadre automático de cámara
            fig.update_layout(
                margin=dict(l=0, r=0, b=0, t=0),
                scene=dict(
                    xaxis=dict(title='Eje X (r)', range=[-padding, padding], backgroundcolor="rgb(240, 244, 248)"),
                    yaxis=dict(title='Eje Y (r)', range=[-padding, padding], backgroundcolor="rgb(240, 244, 248)"),
                    zaxis=dict(title='Eje Z (r)', range=[-padding, padding], backgroundcolor="rgb(240, 244, 248)"),
                    aspectmode='manual',
                    aspectratio=dict(x=1, y=1, z=1),
                    camera=dict(
                        eye=dict(x=1.4, y=1.4, z=1.4)  # Encuadre perfecto tridimensional
                    )
                ),
                height=550
            )
            
            # Renderizar gráfico interactivo nativo dentro de Streamlit
            st.plotly_chart(fig, use_container_width=True)
            st.caption("💡 Interacción: Haz clic izquierdo y arrastra para rotar la figura. Usa la rueda del ratón para hacer zoom.")
else:
    with col2:
        st.info("👈 Modifica el radio si lo deseas y presiona 'Calcular y visualizar' para generar el modelo 3D con sus integrales.")
