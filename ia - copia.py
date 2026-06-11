# App que utiliza LangChain para hacr preguntas sobre los datos de un archivo
# 1.- Selecciona 
# Utiliza streamlit
# Se corre: streamlit run app.py (desde terminal)
import streamlit as st
import pandas as pd
import os
from langchain_groq import ChatGroq
from langchain_experimental.agents import create_pandas_dataframe_agent

API_KEY = st.secrets["GROQ_API_KEY"]
# Configuración de la página
st.set_page_config(page_title="IA Sales Analyzer", layout="wide")

# 1. TÍTULO
st.title("🚀 App de LangChain de Ventas")
st.markdown("---")

# Configuración de la API Key (puedes usar secretos de Streamlit o variable de entorno)
os.environ["GROQ_API_KEY"] = API_KEY

# 2. SELECCIÓN DE ARCHIVOS
# Buscamos todos los archivos .csv en la carpeta actual
archivos_csv = [f for f in os.listdir('.') if f.endswith('.csv')]

if not archivos_csv:
    st.error("No se encontraron archivos CSV en la carpeta actual.")
else:
    archivo_seleccionado = st.selectbox("Selecciona el archivo de ventas que deseas analizar:", archivos_csv)
    
    # Cargar el dataframe
    df = pd.read_csv(archivo_seleccionado)

    # 2da PARTE: MOSTRAR CONTENIDO (Desplegable)
    with st.expander(f"Ver vista previa de {archivo_seleccionado} (10 filas)"):
        st.write(df.head(10))

    st.markdown("---")

    # 3ra PARTE: INPUT DE PREGUNTA
    pregunta = st.text_input("Escribe tu pregunta sobre los datos:", placeholder="Ej: ¿Cuál es la suma de la columna importe por region?")

    if pregunta:
        with st.spinner("El agente está pensando y analizando los datos..."):
            # Le damos una instrucción de formato adicional a la pregunta del usuario
            instruccion_formato = "\nResponde siempre usando formato de tablas de Markdown si muestras múltiples datos."
            try:
                # Inicializar el modelo de Groq
                llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0)

                # Crear el agente para el archivo específico
                agente = create_pandas_dataframe_agent(
                    llm, 
                    df, 
                    verbose=False, 
                    allow_dangerous_code=True
                )

                # Ejecutar la consulta
                # resultado = agente.invoke(pregunta)
                resultado = agente.invoke(pregunta + " Si el resultado es una tabla, devuélvela en formato Markdown.")

                respuesta_texto = resultado["output"]
                
                # Si la respuesta contiene una tabla Markdown (detectada por los pipes '|')
                #if "|" in respuesta_texto:
                #    st.markdown(respuesta_texto)
                #else:
                #    st.write(respuesta_texto)
                
                # Mostrar la respuesta
                st.subheader("Respuesta del Asistente:")
                st.success(resultado["output"])

            except Exception as e:
                st.error(f"Hubo un error al procesar la consulta: {e}")

# Pie de página
st.sidebar.info("Esta app utiliza Groq Cloud para el procesamiento de lenguaje natural y Pandas para el análisis local.")