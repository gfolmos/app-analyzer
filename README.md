# 🤖 Automatic Analyzer: Agente de IA para Análisis de Datos con LangChain y Groq

Automatic Analyzer es una potente plataforma web interactiva que transforma archivos CSV estructurados en paneles de respuesta inteligente en tiempo real. 
Utilizando un agente avanzado de **LangChain** y el motor de inferencia ultra rápido de **Groq (Llama 3.3)**, la aplicación actúa como un analista de datos 
virtual bajo demanda: solo escribe tu pregunta en lenguaje natural y obtén respuestas, cálculos matemáticos y tablas estructuradas de forma inmediata.
---
## ✨ Características Principales

* **Consultas en Lenguaje Natural:** Olvídate de escribir consultas SQL complejas o scripts en Pandas. Pregunta cosas como *"Muestra las ventas por región"* o *"Muestra el total de transacciones por género"*.
* **Agente de Ejecución de Código Estricto:** Integra `create_pandas_dataframe_agent` configurado con un ciclo de razonamiento rígido (*Thought -> Action -> Observation -> Final Answer*) para garantizar respuestas lógicas y formateadas automáticamente en tablas Markdown.
* **Procesamiento de Ultra Baja Latencia:** Potenciado por el modelo `llama-3.3-70b-versatile` a través de la infraestructura cloud de Groq.
* **Ecosistema Seguro y Escalable:** Incluye advertencias de cumplimiento normativo de datos corporativos, permitiendo entender cómo migrar la arquitectura actual hacia entornos locales o despliegues *on-premise* por motivos de seguridad.
* **Carga de Datos Dinámica:** Escaneo automático del directorio raíz para detectar, seleccionar y previsualizar en tiempo real cualquier conjunto de datos CSV (`abandono_banco.csv`, `pronostico-ventas.csv`, etc.).
---
## 📂 Estructura del Proyecto
El repositorio cuenta con un diseño de arquitectura minimalista y plano, ideal para ejecuciones rápidas y contenedores:

```text
├── /images
│   └── img_ia.png             # Recursos y logotipos de la interfaz gráfica
├── .streamlit
│   └── secrets.toml           # Almacenamiento local seguro de credenciales (Omitido en Git)
├── abandono_banco.csv         # Dataset de prueba: Comportamiento y fuga de clientes
├── app.py                     # Archivo núcleo: Orquestación de interfaz de usuario y Agente LLM
├── pronostico-ventas.csv      # Dataset de prueba: Datos históricos de rendimiento comercial
└── requirements.txt           # Definición de dependencias del sistema y paquetería técnica
```
🛠️ Requisitos Previos e Instalación
Sigue estos pasos para desplegar el entorno virtual y poner en marcha la aplicación de manera local:

1. Clonar el repositorio
Bash
git clone [https://github.com/tu-usuario/tu-repositorio.git](https://github.com/tu-usuario/tu-repositorio.git)
cd tu-repositorio
3. Configurar el Entorno Virtual
Se recomienda aislar las dependencias del sistema operativo mediante un entorno virtual (venv):
En Linux/macOS:
Bash
python3 -m venv venv
source venv/bin/activate
En Windows:
Bash
python -m venv venv
venv\Scripts\activate
4. Instalar Dependencias
Actualiza el gestor de paquetes e instala los módulos de Inteligencia Artificial requeridos:
Bash
pip install --upgrade pip
pip install -r requirements.txt
5. Configurar las Claves de API (Secrets)
Para que la aplicación conecte con Groq de forma segura, crea un directorio .streamlit/ con un archivo secrets.toml en la raíz de tu proyecto:
Bash
mkdir .streamlit
touch .streamlit/secrets.toml
Abre .streamlit/secrets.toml e inserta tu API Key personal:
Ini, TOML
GROQ_API_KEY = "tu_api_key_aqui"

💻 Cómo Ejecutar la Aplicación
Una vez configurado el entorno y el archivo de credenciales, despliega el servidor local de Streamlit mediante el siguiente comando:
Bash
streamlit run app.py
La plataforma se iniciará de forma automática en tu navegador predeterminado bajo el puerto de red local estándar: http://localhost:8501.

💡 Consejos de Uso y Buenas Prácticas

⚠️ Nota de Seguridad de Datos: Por políticas de cumplimiento y gobernanza empresarial, se desaconseja subir bases de datos corporativas confidenciales a APIs 
en la nube pública. Para entornos productivos con datos sensibles, la lógica de esta aplicación está diseñada para ser migrada a modelos de ejecución 
local (On-Premise) utilizando servidores de inferencia internos.

🔧 Reconstrucción de Consultas: Si el agente experimenta problemas de parsing o errores lógicos de ejecución, asegúrate de mencionar explícitamente los nombres de las columnas en tu pregunta tal y como aparecen en la vista previa del archivo.
