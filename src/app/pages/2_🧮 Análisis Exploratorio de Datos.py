import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import os

st.set_page_config( page_title="Inicio", page_icon="⭐️", layout="wide" )
st.title("Análisis Exploratorio de Datos (EDA)")
st.markdown("---")

st.subheader("Vista previa usando df.head()")
st.dataframe(st.session_state["df"].head())

print("Filas y columnas:", st.session_state["df"].shape)
st.write(f"Filas: {st.session_state['df'].shape[0]}")
st.write(f"Columnas: {st.session_state['df'].shape[1]}")

st.subheader("Tipos de datos")
st.write(st.session_state["df"].dtypes)

st.subheader("Estadísticas descriptivas")
st.dataframe(st.session_state["df"].describe())
