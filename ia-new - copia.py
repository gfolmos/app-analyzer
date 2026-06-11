import streamlit as st
import pandas as pd
import os
from langchain_groq import ChatGroq
from langchain_experimental.agents import create_pandas_dataframe_agent
# MODIFICACIÓN: Importamos el manejador de memoria
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain.memory import ConversationBufferWindowMemory

API_KEY = st.secrets["GROQ_API_KEY"]
st.set_page_config(page_title="IA Sales Analyzer", layout="wide")
os.environ["GROQ_API_KEY"] = API_KEY

st.title("🚀 App de LangChain con Memoria")

# ### MODIFICACIÓN: Inicializar la memoria en la sesión de Streamlit
# Usamos k=5 para que recuerde las últimas 5 interacciones (ahorra tokens)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = ConversationBufferWindowMemory(
        k=5, 
        return_messages=True, 
        memory_key="chat_history"
    )

archivos_csv = [f for f in os.listdir('.') if f.endswith('.csv')]

if not archivos_csv:
    st.error("No se encontraron archivos CSV.")
else:
    archivo_seleccionado = st.selectbox("Selecciona el archivo:", archivos_csv)
    df = pd.read_csv(archivo_seleccionado)

    with st.expander("Ver vista previa"):
        st.write(df.head(5))

    # ### MODIFICACIÓN: Mostrar el historial de chat visualmente (estilo ChatGPT)
    for msg in st.session_state.chat_history.buffer:
        with st.chat_message("user" if msg.type == "human" else "assistant"):
            st.write(msg.content)

    # 3ra PARTE: INPUT DE PREGUNTA (Cambiado a chat_input para mejor experiencia)
    pregunta = st.chat_input("Escribe tu pregunta sobre los datos...")

    if pregunta:
        # Mostrar pregunta del usuario inmediatamente
        with st.chat_message("user"):
            st.write(pregunta)

        with st.spinner("Analizando..."):
            try:
                llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0)

                # ### MODIFICACIÓN: Creamos el agente pasando la memoria
                agente = create_pandas_dataframe_agent(
                    llm, 
                    df, 
                    verbose=False, 
                    allow_dangerous_code=True,
                    agent_executor_kwargs={
                        "memory": st.session_state.chat_history,
                        "handle_parsing_errors": True # Útil para que no truene si la IA se confunde
                    } # AQUÍ se inyecta la memoria
                )

                # Ejecutar con el historial incluido
                resultado = agente.invoke({"input": pregunta})
                respuesta = resultado["output"]

                # Mostrar respuesta
                with st.chat_message("assistant"):
                    st.success(respuesta)
                
                # RECARGAR para que el historial se vea actualizado (opcional en versiones nuevas)
                # st.rerun()

            except Exception as e:
                st.error(f"Error: {e}")

st.sidebar.info("La memoria está activa. Puedes hacer preguntas de seguimiento como '¿y de esos cuáles son los más caros?'")