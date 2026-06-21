import streamlit as st

st.set_page_config( page_title="Inicio", page_icon="⭐️", layout="wide" )

st.subheader("🌐 Aplicación Streamlit: Bienvenido a la plataforma de simulación de monitoreo de intrusiones en red en tiempo real")
st.markdown("---")
st.markdown("""
📌 Esta aplicación está diseñada para comprender cómo se comporta el tráfico de red y cómo se pueden identificar actividades sospechosas utilizando modelos de machine learning. Desde esta interfaz podrás acceder al análisis exploratorio de datos, visualizar patrones relevantes y observar cómo evoluciona el tráfico en tiempo real. Es una herramienta ideal para estudiantes, analistas y entusiastas de la ciberseguridad." \n
""")

st.markdown("---")
st.write("""
📦 Conjunto de datos original.
""")
st.markdown(
    '<a href="https://www.unb.ca/cic/datasets/ids-2018.html" target="_blank">Dataset original CSE-CIC-IDS2018</a>',
    unsafe_allow_html=True
)

st.markdown("---")
st.write("""
📦 Conjunto de datos utilizado en el entrenamiento del modelo de Bosque aleatorio.
""")
st.markdown(
    '<a href="https://data.mendeley.com/datasets/29hdbdzx2r/1" target="_blank">Dataset original CSE-CIC-IDS2018 en Mendeley</a>',
    unsafe_allow_html=True
)

st.markdown("---")
st.markdown("🎀 Puedes descargar un subconjunto del dataset para pruebas y experimentación.")

with open("data/sample_traffic.csv", "rb") as file:
    st.download_button(
        label="📥 Descargar dataset original",
        data=file,
        file_name="dataset_original.csv",
        mime="text/csv"
    )


st.markdown("---")
