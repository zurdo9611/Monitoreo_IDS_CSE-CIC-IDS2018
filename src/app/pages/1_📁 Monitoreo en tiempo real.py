# --- Librerías estándar ---
import os
import glob
import time
import pickle

# --- Ciencia de datos ---
import numpy as np
import pandas as pd

# --- Visualización ---
import plotly.express as px

# --- Aplicación ---
import streamlit as st


# --- Constantes y características de CSE-CIC-IDS2018 ---
FEATURES_28 = [
    "dst_port","flow_duration","tot_fwd_pkts","tot_bwd_pkts","fwd_pkt_len_max","bwd_pkt_len_max",
    "flow_byts_s","flow_pkts_s","flow_iat_mean","flow_iat_std","flow_iat_max","fwd_iat_mean",
    "fwd_iat_std","fwd_iat_max","bwd_iat_tot","bwd_iat_mean","bwd_iat_std","bwd_iat_min",
    "fwd_pkts_s","bwd_pkts_s","pkt_len_max","pkt_len_mean","pkt_len_std","pkt_len_var","ece_flag_cnt",
    "init_fwd_win_byts","init_bwd_win_byts","fwd_seg_size_min",
]

ATTACK_TYPES = [
    "Benign",
    "DDOS attack-HOIC",
    "DDoS attacks-LOIC-HTTP",
    "DoS attacks-Hulk",
    "Bot",
    "FTP-BruteForce",
    "SSH-Bruteforce",
    "Infilteration",
    "DoS attacks-SlowHTTPTest",
    "DoS attacks-GoldenEye",
    "DoS attacks-Slowloris",
    "DDOS attack-LOIC-UDP",
    "Brute Force -Web",
    "Brute Force -XSS",
    "SQL Injection"
]

df = pd.DataFrame()

# ── Configuración ─────
st.set_page_config(
    page_title="IDS Monitor — CSE-CIC-IDS2018",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

@st.cache_resource(show_spinner=False)
def cargar_modelo_rf(nombre_modelo: str = "rf_model.pkl"):
    model = pickle.load(open(f"model/{nombre_modelo}", "rb"))
    st.session_state["model"] = model
    st.session_state["modelo_listo"] = True
    return model

@st.cache_data(show_spinner=False)
# Función para cargar y limpiar datos
def cargar_y_limpiar(ruta: str) -> pd.DataFrame:
    """Carga los CSV y aplica todo el pipeline de limpieza del notebook."""
    archivos = glob.glob(os.path.join(ruta, "*.csv"))
    if not archivos:
        st.sidebar.error(f"No se encontraron archivos CSV en: {ruta}")
        st.stop()

    dfs = []
    for a in archivos:
        try:
            dfs.append(pd.read_csv(a, low_memory=False))
        except Exception as e:
            st.sidebar.warning(f"No se pudo leer {os.path.basename(a)}: {e}")

    df = pd.concat(dfs, ignore_index=True)
    del dfs

    # Normalizar
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('/', '_')

    # Eliminar duplicados
    df.drop_duplicates(keep='first', inplace=True)

    # Seleccionar solo las columnas relevantes (del notebook)
    df = df[FEATURES_28]

    # Limpiar inf y NaN
    #df.replace([np.inf, -np.inf], np.nan, inplace=True)
    #df.dropna(inplace=True)

    return df

# ── Sidebar: carga de datos ─────────────────────────────────────────────
st.sidebar.markdown("## 🛡️ Configuración del IDS")
st.sidebar.markdown("**Dataset:** CSE-CIC-IDS2018")
st.sidebar.markdown("---")

st.sidebar.info("Ingresa la ruta de los CSV y pulsa **Cargar datos** para comenzar.")

st.sidebar.markdown("### Ruta de los CSV")
ruta_default = r"data/"
ruta = st.sidebar.text_input("Carpeta con los archivos .csv", value=ruta_default)

cargar = st.sidebar.button("Cargar datos", type="primary", use_container_width=True)

if cargar:
    st.cache_data.clear()
    st.cache_resource.clear()

    with st.sidebar.spinner("Cargando datos…"):
        try:
            df = cargar_y_limpiar(ruta)
            st.session_state["df"] = df
            st.sidebar.success("Archivo cargado correctamente.")
        except Exception as e:
            st.sidebar.error(f"Error al cargar datos: {e}")
            st.stop()

st.sidebar.markdown("---")

st.sidebar.markdown("**Monitoreo en Tiempo Real**")
with st.sidebar:
    col1, col2 = st.columns(2)
    with col1:
        iniciar_monitoreo = st.button("Iniciar")
    with col2:
        detener_monitoreo = st.button("Detener")

# Dashboard central
st.title("Monitoreo de Intrusiones en Red en Tiempo Real")

model_option = st.radio(
    "Seleccione el Modelo de Inferencia:",
    ["Bosque aleatorio", "Bosque aleatorio + PCA"]
)

modelo_actual = st.empty()
ejecucion_actual = st.empty()
col1, col2, col3, col4 = st.columns(4)
metricas_total = col1.empty()
metricas_attaques = col2.empty()
metricas_latencia_rt = col3.empty()
metricas_latencia_avg = col4.empty()
kpi_status = st.empty()

st.subheader("Distribución de Amenazas Detectadas")
chart_container = st.empty()

st.subheader("Historial Reciente de Alertas (Stream)")
table_container = st.empty()

if iniciar_monitoreo:

    if model_option == "Bosque aleatorio":
        model = cargar_modelo_rf("rf_model.pkl")
        modelo_actual.success("Modelo bosque aleatorio cargado.")
    else:
        modelo_actual.warning("Modelo con PCA aún no implementado.")

    if st.session_state["df"].empty:
        st.error("No hay datos cargados.")
    else:
        ejecucion_actual.info("Monitoreo iniciado. Procesando datos en tiempo real...")
        
        conteo_procesos = 0
        conteo_ataques = 0
        historial_latencia = []
        ataques_detectados = {attack: 0 for attack in ATTACK_TYPES if attack != 'Benign'}
        eventos_recientes = []

        for index, row in st.session_state["df"].iterrows():
            if detener_monitoreo:
                ejecucion_actual.warning("Monitoreo detenido.")
                break
            
            vector_actual = row.values.reshape(1, -1)
            start_time = time.perf_counter()
            prediccion = st.session_state["model"].predict(vector_actual)[0]
            end_time = time.perf_counter()
            
            latencia_actual = (end_time - start_time) * 1000
            historial_latencia.append(latencia_actual)
            avg_latencia = np.mean(historial_latencia)
            conteo_procesos += 1
            es_attaque = prediccion != 'Benign'

            if es_attaque:
                conteo_ataques += 1
                ataques_detectados[prediccion] = ataques_detectados.get(prediccion, 0) + 1
                status_color = f"Ataque [{prediccion}] Detectado"
            else:
                status_color = f"Tráfico [{prediccion}] Detectado"

            event_log = {
                "Timestamp": time.strftime("%H:%M:%S"),
                "Dst Port": int(row['dst_port']),
                "Flow Duration": round(row['flow_duration'], 2),
                "Clasificación": prediccion,
                "Latencia (ms)": round(latencia_actual, 3)
            }
            eventos_recientes.insert(0, event_log)
            if len(eventos_recientes) > 8:
                eventos_recientes.pop()

            with kpi_status:
                if es_attaque:
                    kpi_status.error(f"**Estado de la Red:** {status_color}")
                else:
                    kpi_status.success(f"**Estado de la Red:** {status_color}")

            metricas_total.metric(label="Flujos Analizados", value=conteo_procesos)
            metricas_attaques.metric(label="Ataques Detectados", value=conteo_ataques, delta=f"+{conteo_ataques}" if conteo_ataques > 0 else 0, delta_color="inverse")
            metricas_latencia_rt.metric(label="Latencia de Inferencia", value=f"{latencia_actual:.2f} ms")
            metricas_latencia_avg.metric(label="Latencia Promedio Fijo", value=f"{avg_latencia:.2f} ms")

            # --- RENDERIZADO DEL GRÁFICO CON KEY DINÁMICA ÚNICA ---
            df_chart = pd.DataFrame(list(ataques_detectados.items()), columns=['Tipo de Ataque', 'Cantidad'])
            fig = px.bar(df_chart, x='Tipo de Ataque', y='Cantidad', color='Tipo de Ataque', 
                         color_discrete_sequence=px.colors.sequential.OrRd, template="plotly_dark")
            fig.update_layout(showlegend=False, height=320, margin=dict(l=20, r=20, t=20, b=20))
            
            # El uso de key resuelve el error StreamlitDuplicateElementId
            chart_container.plotly_chart(fig, use_container_width=True, key=f"p_chart_{conteo_procesos}")

            table_container.dataframe(pd.DataFrame(eventos_recientes), use_container_width=True)

            time.sleep(0.3)  
    ejecucion_actual.info("Monitoreo en tiempo real finalizado.")