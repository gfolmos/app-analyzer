# Version moderna de ia
from langchain_groq import ChatGroq
from langchain_experimental.agents import create_pandas_dataframe_agent
# 1. Importa el enum de AgentType
from langchain.agents import AgentType

# 2. Inicializa tu modelo Llama 3.3
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

# 3. Crea el agente estructurado
agent_executor = create_pandas_dataframe_agent(
    llm=llm,
    df=df,  # Tu DataFrame de pandas
    verbose=True,
    # 4. Define el nuevo tipo de agente aquí:
    agent_type=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    # Al ser un agente estructurado, es altamente recomendable mantener esto activo:
    handle_parsing_errors=True 
)

# 5. Ejecuta tu consulta
# Nota: Si usas una versión reciente de LangChain, se recomienda usar .invoke() en lugar de .run()
response = agent_executor.invoke({"input": "Muestra los 5 productos con las mayores ventas"})
print(response["output"])