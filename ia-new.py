# App que utiliza LangChain para hacer preguntas sobre los datos de un archivo
# version mejorada con memoria
# 1.- Selecciona 
# Utiliza streamlit
# se desinstalo langchain 0.4 x 0.3 no funcionaba la memoria
import streamlit as st
import pandas as pd
import os

# Importaciones estándar de la versión 0.3.x
from langchain_groq import ChatGroq
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.memory import ConversationBufferWindowMemory

# --- CONFIGURACIÓN ---
API_KEY = st.secrets["GROQ_API_KEY"]
os.environ["GROQ_API_KEY"] = API_KEY
st.set_page_config(page_title="IA Sales Analyzer", layout="wide")

st.title("🚀 App de Ventas con Memoria (v0.3.0)")

# --- INICIALIZAR MEMORIA ---
if "chat_history" not in st.session_state:
    # k=5 permite recordar las últimas 5 preguntas/respuestas
    st.session_state.chat_history = ConversationBufferWindowMemory(
        k=5, 
        return_messages=True, 
        memory_key="chat_history"
    )

# --- SELECCIÓN DE ARCHIVOS ---
archivos_csv = [f for f in os.listdir('.') if f.endswith('.csv')]

if not archivos_csv:
    st.error("No se encontraron archivos CSV.")
else:
    archivo_seleccionado = st.selectbox("Selecciona el archivo:", archivos_csv)
    df = pd.read_csv(archivo_seleccionado)

    # Mostrar historial previo en la UI
    for msg in st.session_state.chat_history.buffer:
        role = "user" if msg.type == "human" else "assistant"
        with st.chat_message(role):
            st.write(msg.content)

    # --- ENTRADA DE USUARIO ---
    pregunta = st.chat_input("Haz una pregunta sobre los datos...")

    if pregunta:
        with st.chat_message("user"):
            st.write(pregunta)

        with st.spinner("Analizando datos..."):
            try:
                llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0)

                # Creamos el agente inyectando la memoria de la sesión
                agente = create_pandas_dataframe_agent(
                    llm, 
                    df, 
                    verbose=True, # Ponlo en True para ver en la terminal cómo "piensa"
                    allow_dangerous_code=True,
                    agent_executor_kwargs={
                        "memory": st.session_state.chat_history,
                        "handle_parsing_errors": True
                    }
                )

                # IMPORTANTE: Pasamos la pregunta dentro de un diccionario
                resultado = agente.invoke({"input": pregunta + " Si el resultado es una tabla, devuélvela en formato Markdown."})
                respuesta = resultado["output"]

                with st.chat_message("assistant"):
                    st.success(respuesta)

            except Exception as e:
                st.error(f"Error técnico: {e}")

st.sidebar.info("Estado: Conectado a Groq | Memoria: Activa")