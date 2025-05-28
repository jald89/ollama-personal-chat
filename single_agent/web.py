import streamlit as st
import requests
import json
import uuid

# Configuración de la página
st.set_page_config(
    page_title="TechBot - Asistente IA",
    page_icon="🤖",
    layout="wide"
)

# Inicializar session state para mantener estado
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'first_interaction' not in st.session_state:
    st.session_state.first_interaction = True

# Header de la aplicación
st.title('🤖 TechBot - Asistente de Soporte Técnico')
st.markdown("**Tu asistente IA especializado en programación y tecnología**")
st.markdown("---")

# Sidebar con información del agente
with st.sidebar:
    st.header("📋 Información del Agente")
    st.markdown("""
    **Personalidad:**
    - 🎯 Especialista en soporte técnico
    - 💡 Explica conceptos de forma sencilla
    - 🔧 Enfoque práctico y paso a paso
    - 🧠 Mantiene memoria de la conversación
    - ✨ Amigable y profesional
    """)
    
    st.markdown("---")
    st.markdown(f"**ID Sesión:** `{st.session_state.session_id[:8]}...`")
    st.markdown(f"**Mensajes:** {len(st.session_state.messages)}")
    
    # Botón para reiniciar conversación
    if st.button("🔄 Nueva Conversación", type="secondary"):
        try:
            response = requests.post('http://127.0.0.1:5000/reset', 
                                   json={'session_id': st.session_state.session_id})
            if response.status_code == 200:
                st.session_state.messages = []
                st.session_state.session_id = str(uuid.uuid4())
                st.session_state.first_interaction = True
                st.rerun()
        except:
            st.error("Error al conectar con el servidor")

# Mostrar historial de mensajes
chat_container = st.container()

with chat_container:
    # Mensaje de bienvenida inicial
    if st.session_state.first_interaction:
        st.chat_message("assistant").markdown(
            "¡Hola! Soy **TechBot**, tu asistente de soporte técnico. "
            "Estoy aquí para ayudarte con programación, tecnología y resolver tus dudas técnicas. "
            "Tengo memoria, así que puedo recordar nuestra conversación. ¿En qué puedo ayudarte hoy?"
        )
    
    # Mostrar mensajes del historial
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Input del usuario
user_input = st.chat_input("Escribe tu pregunta técnica aquí...")

if user_input:
    # Mostrar mensaje del usuario
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Agregar mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.first_interaction = False
    
    # Enviar mensaje al servidor Flask
    with st.chat_message("assistant"):
        with st.spinner("TechBot está pensando..."):
            try:
                response = requests.post('http://127.0.0.1:5050/chat', 
                                       json={
                                           'message': user_input,
                                           'session_id': st.session_state.session_id
                                       },
                                       timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    assistant_reply = data['reply']
                    
                    # Mostrar respuesta
                    st.markdown(assistant_reply)
                    
                    # Agregar respuesta al historial
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": assistant_reply
                    })
                    
                    # Mostrar información de debug en sidebar
                    with st.sidebar:
                        st.success(f"✅ Respuesta recibida")
                        if 'message_count' in data:
                            st.info(f"📊 Total mensajes: {data['message_count']}")
                
                else:
                    error_msg = "❌ Error del servidor. Verifica que Flask esté ejecutándose."
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": error_msg
                    })
                    
            except requests.exceptions.ConnectionError:
                error_msg = "🔌 No se puede conectar al servidor. Asegúrate de que Flask esté corriendo en http://127.0.0.1:5000"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": error_msg
                })
            except requests.exceptions.Timeout:
                error_msg = "⏱️ Tiempo de espera agotado. El servidor tardó demasiado en responder."
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": error_msg
                })
            except Exception as e:
                error_msg = f"❌ Error inesperado: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": error_msg
                })

# Footer
st.markdown("---")
st.markdown(
    "💡 **Tip:** TechBot tiene memoria y puede recordar nuestra conversación completa. "
    "Puedes hacer preguntas de seguimiento que dependan del contexto anterior."
)