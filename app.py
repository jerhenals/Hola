# app.py
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from io import StringIO


st.set_page_config(page_title="Modelos de Crecimiento", page_icon="📈", layout="wide")


st.title("📈 Modelos de Crecimiento – Explorador de Escenarios")
st.caption("Ajusta parámetros y compara escenarios para crecimiento Exponencial y Logístico.")


# =========================
# Utilidades
# =========================
@st.cache_data
def generar_tiempo(horas, puntos):
return np.linspace(0, horas, puntos)


@st.cache_data
def sim_exponencial(N0, r, t):
return N0 * np.exp(r * t)


@st.cache_data
def sim_logistico(N0, r, K, t):
# Solución analítica del logístico clásico
# N(t) = K / (1 + ((K - N0)/N0)*exp(-r t))
N0 = max(1e-12, N0)
K = max(1e-12, K)
return K / (1 + ((K - N0) / N0) * np.exp(-r * t))


MODEL_OPTIONS = ["Exponencial", "Logístico"]


# =========================
# Sidebar: Configuración base y escenarios
# =========================
st.sidebar.header("⚙️ Configuración")
T = st.sidebar.number_input("Horizonte de tiempo (unidades)", min_value=1.0, value=50.0, step=1.0)
num_puntos = st.sidebar.slider("Resolución (n° de puntos)", 50, 2000, 500)
t = generar_tiempo(T, num_puntos)


st.sidebar.markdown("---")
st.sidebar.subheader("📦 Parámetros por defecto")
def_modelo = st.sidebar.selectbox("Modelo por defecto", MODEL_OPTIONS, index=1)
N0_def = st.sidebar.number_input("N0 (población/valor inicial)", min_value=0.0, value=10.0)
r_def = st.sidebar.number_input("r (tasa de crecimiento)", value=0.1, step=0.01, format="%.3f")
K_def = st.sidebar.number_input("K (capacidad de carga, solo logístico)", min_value=0.0, value=100.0)


# =========================
# Escenarios (tabla editable)
# =========================
if "escenarios" not in st.session_state:
st.session_state.escenarios = pd.DataFrame([
{"Nombre": "Base", "Modelo": def_modelo, "N0": N0_def, "r": r_def, "K": K_def}
])


col_a, col_b, col_c = st.columns([1,1,2], vertical_alignment="center")
with col_a:
if st.button("➕ Añadir escenario"):
st.session_state.escenarios.loc[len(st.session_state.escenarios)] = {
"Nombre": f"Esc {len(st.session_state.escenarios)+1}",
)