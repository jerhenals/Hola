import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

# --- Definición de los Modelos ---

def exponential_growth(P0, r, t_values):
    """Calcula el crecimiento exponencial."""
    # P(t) = P0 * e^(r*t)
    return P0 * np.exp(r * t_values)

def logistic_growth(P0, r, K, t_values):
    """Calcula el crecimiento logístico."""
    # P(t) = K / (1 + ((K - P0) / P0) * e^(-r*t))
    return K / (1 + ((K - P0) / P0) * np.exp(-r * t_values))

# --- Configuración de la Página de Streamlit ---
st.set_page_config(page_title="Simulador de Crecimiento", layout="wide")
st.title("📈 Simulador de Modelos de Crecimiento")
st.write("Usa los controles en la barra lateral para ajustar los parámetros de diferentes modelos de crecimiento y ver cómo evolucionan.")

# --- Barra Lateral de Controles ---
st.sidebar.header("Parámetros de Simulación")

# Parámetros comunes
P0 = st.sidebar.slider("Población Inicial (P0)", 1, 1000, 50)
t_max = st.sidebar.slider("Número de Períodos (t)", 10, 200, 50)
r = st.sidebar.slider("Tasa de Crecimiento (r)", 0.01, 1.0, 0.1, step=0.01)

# Parámetro específico para el modelo logístico
st.sidebar.markdown("---")
st.sidebar.subheader("Parámetros Logísticos")
K = st.sidebar.slider("Capacidad de Carga (K)", 500, 50000, 10000)
st.sidebar.info("La Capacidad de Carga (K) solo se aplica al modelo logístico.")


# --- Generación de Datos ---
t_values = np.arange(0, t_max + 1)

# Crear un DataFrame para almacenar los resultados
df_growth = pd.DataFrame({'Período': t_values})

# Calcular los dos escenarios
df_growth['Crecimiento Exponencial'] = exponential_growth(P0, r, t_values)
df_growth['Crecimiento Logístico'] = logistic_growth(P0, r, K, t_values)

# --- Visualización ---
st.subheader("Visualización de Escenarios de Crecimiento")

# Re-formatear el DataFrame para que sea compatible con Plotly (formato "largo")
df_melted = df_growth.melt(
    id_vars='Período', 
    value_vars=['Crecimiento Exponencial', 'Crecimiento Logístico'],
    var_name='Tipo de Modelo', 
    value_name='Población'
)

# Crear el gráfico interactivo con Plotly
fig = px.line(
    df_melted,
    x='Período',
    y='Población',
    color='Tipo de Modelo',
    title=f"Simulación de Crecimiento (P0={P0}, r={r}, K={K})",
    labels={'Población': 'Población Total', 'Período': 'Tiempo / Períodos'}
)

# Añadir una línea horizontal para la Capacidad de Carga (K)
fig.add_hline(y=K, line_dash="dot",
              annotation_text="Capacidad de Carga (K)",
              annotation_position="bottom right",
              line_color="red")

st.plotly_chart(fig, use_container_width=True)


# --- Mostrar Datos (Opcional) ---
st.subheader("Datos Generados")
st.dataframe(df_melted.tail(10)) # Mostrar los últimos 10 registros
