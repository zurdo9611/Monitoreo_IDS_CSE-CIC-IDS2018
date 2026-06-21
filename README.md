# 🛡️ Monitoreo IDS: Monitoreo de Intrusiones en Red en Tiempo Real

Aplicación desarrollada con **Streamlit** para simular y visualizar el monitoreo de intrusiones en red en tiempo real utilizando modelos de *Machine Learning*.  
Incluye análisis exploratorio de datos (EDA), visualización de patrones, carga de modelos y procesamiento de flujos simulados.

El sistema utiliza un modelo de **Bosque Aleatorio** entrenado con un subconjunto del dataset **CSE‑CIC‑IDS2018**, ampliamente utilizado en investigación de ciberseguridad.

---

## 🚀 Características principales

- **Monitoreo en tiempo real** de flujos de red simulados  
- **Detección de ataques** con Random Forest y Random Forest + PCA  
- **Análisis Exploratorio de Datos (EDA)**  
- **Visualización interactiva** con Plotly  
- **Descarga del dataset** desde la interfaz  
- **Interfaz multipágina** con navegación lateral  
- **Simulación de métricas en tiempo real** (latencia, amenazas detectadas, estado de la red)

---

## 📄 Paginas disponibles

- **Inicio**: Breve introducción a la aplicación, su propósito y el dataset utilizado.  
- **📁 Monitoreo en tiempo real**: Simulación del tráfico de red con detección automática de intrusiones y métricas en vivo.  
- **🧮 Análisis Exploratorio de Datos**:  Vista previa del dataset, estadísticas básicas y exploración de las características del conjunto de datos cargados por el usuario.

---

## 🏗️ Estructura del proyecto

Streamlimit/
│── src/
│   ├── app/
│   │   ├── Inicio.py              # Página de inicio
│   │   ├── pages
│   │   │   ├── 2_Monitoreo.py     # Monitoreo en tiempo real
│   │   │   ├── 3_EDA.py           # Análisis Exploratorio
│── data/
│   ├──generate_sample.ipynb       # Código para generar el subconjunto con el dataset original
│   ├── dataset.csv                # Subconjunto del dataset
│── model/
│   ├── rf_model.pkl               # Modelo Random Forest
│   ├── rf_pca_model.pkl           # Modelo Random Forest + PCA
│── notebooks/
│   ├── CSE-CIC-IDS2018.ipynb      # Proyecto de pipelines de análisis y entrenamiento de los modelos
│── README.md
│── requirements.txt

---

## 📦 Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/usuario/streamlimit.git
cd streamlimit

### 2. Ejecutar requirements.txt

pip install -r requirements.txt

### 3. Ejecutar aplicación

```bash
streamlit run Inicio.py