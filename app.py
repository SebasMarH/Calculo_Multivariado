import numpy as np
import plotly.graph_objects as go
import streamlit as st

# Configuración de la página web
st.set_page_config(page_title="Tricilindro de Steinmetz", layout="wide")

# Título principal y teoría breve para el profesor
st.title("Intersección de Tres Cilindros (Sólido de Steinmetz)")
st.write(
    "Esta aplicación web interactiva calcula el volumen y renderiza la "
    "geometría de la intersección de tres cilindros mutuamente perpendiculares."
)

# Barra lateral para los controles
st.sidebar.header("Parámetros del Sólido")

# Control deslizante interactivo para el radio
r = st.sidebar.slider(
    "Selecciona el Radio (r):", min_value=0.5, max_value=5.0, value=2.0, step=0.1
)

# Cálculo matemático del volumen exacto (Fórmula de Steinmetz)
volumen_exacto = (16 - 8 * np.sqrt(2)) * (r**3)

# Mostrar los resultados matemáticos en tarjetas llamativas
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Radio Seleccionado (r)", value=f"{r} u")
with col2:
    st.metric(
        label="Volumen del Sólido (V)", value=f"{volumen_exacto:.4f} u³"
    )

# Explicación matemática breve que a los profesores les encanta
st.sidebar.markdown("---")
st.sidebar.markdown("**Fórmula Analítica:**")
st.sidebar.latex(r"V = (16 - 8\sqrt{2})r^3")

# ==========================================================
# GENERACIÓN DE LA GEOMETRÍA 3D
# ==========================================================
# Rejilla de puntos (n=50 para que cargue rápido y fluido en la web)
n = 50
puntos = np.linspace(-r, r, n)
X, Y, Z = np.meshgrid(puntos, puntos, puntos)

# Ecuaciones de los cilindros
cilindro_z = X**2 + Y**2 <= r**2
cilindro_x = Y**2 + Z**2 <= r**2
cilindro_y = X**2 + Z**2 <= r**2
tricilindro = cilindro_z & cilindro_x & cilindro_y
valores = tricilindro.astype(float)

# Crear Isosurface de Plotly
fig = go.Figure(
    data=go.Isosurface(
        x=X.flatten(),
        y=Y.flatten(),
        z=Z.flatten(),
        value=valores.flatten(),
        isomin=0.5,
        isomax=1.0,
        surface_count=1,
        colorscale="Oranges",
        showscale=False,
        caps=dict(x_show=False, y_show=False, z_show=False),
    )
)

fig.update_layout(
    scene=dict(
        xaxis=dict(nticks=6, range=[-r, r]),
        yaxis=dict(nticks=6, range=[-r, r]),
        zaxis=dict(nticks=6, range=[-r, r]),
        aspectmode="cube",
    ),
    margin=dict(r=0, l=0, b=0, t=0),
    height=600,
)

# Renderizar el gráfico de Plotly directamente en la web de Streamlit
st.plotly_chart(fig, use_container_width=True)
