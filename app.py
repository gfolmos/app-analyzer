# App que utiliza LangChain para hacer preguntas sobre los datos de un archivo
# automatic analyzer
# Autor: Gerardo Figueroa
# Fecha: 08/06/26
import streamlit as st
import pandas as pd
import os
from langchain_groq import ChatGroq
from langchain_experimental.agents import create_pandas_dataframe_agent
API_KEY = st.secrets["GROQ_API_KEY"]
# Configuración de la página
st.set_page_config(layout="wide")

# Configuración de la API Key (puedes usar secretos de Streamlit o variable de entorno)
os.environ["GROQ_API_KEY"] = API_KEY
    
# ***************** manejo data frame ************************  
 
# *************Deficion pagina principal******************
st.set_page_config(layout="wide")
col1, col2 = st.columns([1, 2])  # proporción: más espacio para el título
with col1:
    st.image("images/img_ia.png", width=150)
with col2:
    st.header("Analizador Automático (Automatic Analyzer)")
    st.write("🚀 Utiliza un agente de IA que es realmente sorprendente!")

# Explicacion del programa
with st.expander("Explicación del Programa"):
    st.write("""
            Practicamente esta herramienta es un analista eficaz, solo realiza la pregunta como si la ralizaras al analista y ya no tendras que esperar dias para recibir la informes. \n
            Como realizar la pregunta simple (ejemplos): \n
            'Muestra la suma de ventas', 'Muestra las ventas por region', 'Muestra numero de Total_Transacciones por genero' (fijarse en el nombre de la columna). \n
            Nota: Si manda un error, no reconoce alguna palabre, recostruye la pregunta. \n
             Nota Final: \n
            Al utilizar la IA no se recomendaría analizar los documentos de la empresa por propia política de la empresa o por seguridad.
            Para poder utilizar una herramienta como esta corriendo con un agente de IA por internet, se puede utilizar localmente (on-premise)
            en una computadora moderna para que la información no salga por internet y este segura la información. \n
            """)

# 1ra: Seleccion archvivos
archivos_csv = [f for f in os.listdir('.') if f.endswith('.csv')]

if not archivos_csv:
    st.error("No se encontraron archivos CSV en la carpeta actual.")
else:
    archivo_seleccionado = st.selectbox("Selecciona el archivo que deseas analizar:", archivos_csv)
    df = pd.read_csv(archivo_seleccionado, encoding="utf-8-sig")

    # 2da PARTE: MOSTRAR CONTENIDO (Desplegable)
    with st.expander(f"Ver vista previa de {archivo_seleccionado}"):
        st.dataframe(df)

    #st.markdown("---")

    # 3ra PARTE: INPUT DE PREGUNTA
    #pregunta = st.text_input("Escribe tu pregunta sobre los datos:", placeholder="Ej: ¿Cuál es la suma de la columna importe por region?")
    pregunta = st.chat_input("Haz una pregunta sobre los datos...")

    if pregunta:
        with st.spinner("El agente está pensando y analizando los datos..."):
            # Le damos una instrucción de formato adicional a la pregunta del usuario
            instruccion_formato = "\nResponde siempre usando formato de tablas de Markdown si muestras múltiples datos."
            try:
                # Inicializar el modelo de Groq
                llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0)
                agente = create_pandas_dataframe_agent(
                    llm, 
                    df, 
                    verbose=False, 
                    allow_dangerous_code=True,
                    handle_parsing_errors=True
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
                st.write(f"Pregunta: {pregunta}")
                st.subheader("Respuesta del Asistente:")
                st.success(resultado["output"])

            except Exception as e:
                st.error(f"Hubo un error al procesar la consulta: {e}")

# Pie de página
#st.sidebar.info("Esta app utiliza Groq Cloud para el procesamiento de lenguaje natural y Pandas para el análisis local.")
#st.sidebar.info("Estado: Conectado a Groq | Memoria: Activa")
#******************* fin programa ppal ***************************

# ******************Definicion panel lateral*************
   
# *****************fin lateral ***********************

