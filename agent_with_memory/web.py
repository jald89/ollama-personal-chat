import streamlit as st
import requests
import json
import uuid

# Configuración de la página
st.set_page_config(
    page_title="🤖 Sistema de Agentes IA",
    page_icon="🤖",
    layout="wide"
)

# Inicializar session state
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'current_agent' not in st.session_state:
    st.session_state.current_agent = {'id': 'techbot', 'name': 'TechBot', 'description': 'Asistente de Soporte Técnico'}
if 'available_agents' not in st.session_state:
    st.session_state.available_agents = {}

# Funciones auxiliares
def get_available_agents():
    """Obtiene la lista de agentes disponibles"""
    try:
        response = requests.get('http://127.0.0.1:5050/agents')
        if response.status_code == 200:
            return response.json()['available_agents']
    except:
        return {}
    return {}

def set_agent(agent_id):
    """Cambia el agente actual"""
    try:
        response = requests.post('http://127.0.0.1:5050/set_agent', 
                               json={
                                   'session_id': st.session_state.session_id,
                                   'agent_id': agent_id
                               })
        if response.status_code == 200:
            data = response.json()
            st.session_state.current_agent = data['agent']
            st.session_state.messages = []  # Limpiar mensajes al cambiar agente
            return True
    except:
        return False
    return False

def send_message(message, agent_id):
    """Envía mensaje al agente"""
    try:
        response = requests.post('http://127.0.0.1:5050/chat',
                               json={
                                   'message': message,
                                   'session_id': st.session_state.session_id,
                                   'agent_id': agent_id
                               })
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        return {'error': str(e)}
    return {'error': 'Error de conexión'}

def create_custom_agent(name, instructions):
    """Crea un agente personalizado"""
    try:
        response = requests.post('http://127.0.0.1:5050/create_custom_agent',
                               json={
                                   'session_id': st.session_state.session_id,
                                   'name': name,
                                   'instructions': instructions
                               })
        if response.status_code == 200:
            return response.json()
    except:
        return {'error': 'Error al crear agente'}
    return {'error': 'Error de conexión'}

# Obtener agentes disponibles al inicio
if not st.session_state.available_agents:
    st.session_state.available_agents = get_available_agents()

# ============================================
# INTERFAZ PRINCIPAL
# ============================================

st.title('🤖 Sistema de Agentes IA Avanzado')
st.markdown("**Múltiples personalidades especializadas con memoria persistente**")

# ============================================
# SIDEBAR - SELECTOR DE AGENTES
# ============================================

with st.sidebar:
    st.header("🎭 Selector de Agentes")
    
    # Información del agente actual
    st.success(f"**Agente Actual:** {st.session_state.current_agent['name']}")
    st.info(f"**Especialidad:** {st.session_state.current_agent['description']}")
    
    st.markdown("---")
    
    # Selector de agentes predefinidos
    st.subheader("🤖 Agentes Predefinidos")
    
    agent_options = {}
    for agent_id, info in st.session_state.available_agents.items():
        display_name = f"{info['name']} - {info['description']}"
        agent_options[display_name] = agent_id
    
    if agent_options:
        current_display = f"{st.session_state.current_agent['name']} - {st.session_state.current_agent['description']}"
        
        selected_agent_display = st.selectbox(
            "Selecciona un agente:",
            options=list(agent_options.keys()),
            index=list(agent_options.keys()).index(current_display) if current_display in agent_options else 0
        )
        
        selected_agent_id = agent_options[selected_agent_display]
        
        if st.button("🔄 Cambiar Agente", type="primary"):
            if set_agent(selected_agent_id):
                st.success("¡Agente cambiado exitosamente!")
                st.rerun()
            else:
                st.error("Error al cambiar agente")
    
    st.markdown("---")
    
    # Creador de agente personalizado
    st.subheader("🛠️ Crear Agente Personalizado")
    
    with st.expander("➕ Nuevo Agente Custom"):
        custom_name = st.text_input("Nombre del agente:", placeholder="Ej: Dr. MedBot")
        
        custom_instructions = st.text_area(
            "Instrucciones y personalidad:",
            placeholder="""Ejemplo:
Eres un médico virtual especializado en primeros auxilios.
- Siempre aclaras que no reemplazas consulta médica
- Das instrucciones claras y paso a paso
- Preguntas por síntomas específicos
- Eres calmado y profesional en emergencias""",
            height=150
        )
        
        if st.button("🚀 Crear Agente"):
            if custom_name and custom_instructions:
                result = create_custom_agent(custom_name, custom_instructions)
                if 'error' not in result:
                    st.session_state.current_agent = result['agent']
                    st.session_state.messages = []
                    st.success(f"¡Agente {custom_name} creado!")
                    st.rerun()
                else:
                    st.error(f"Error: {result['error']}")
            else:
                st.warning("Completa nombre e instrucciones")
    
    st.markdown("---")
    
    # Información de sesión
    st.subheader("📊 Info de Sesión")
    st.text(f"ID: {st.session_state.session_id[:8]}...")
    st.text(f"Mensajes: {len(st.session_state.messages)}")
    
    if st.button("🗑️ Nueva Sesión"):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()

# ============================================
# CHAT PRINCIPAL
# ============================================

# Contenedor del chat
chat_container = st.container()

with chat_container:
    # Mensaje de bienvenida
    if not st.session_state.messages:
        welcome_msg = f"""
        ¡Hola! Soy **{st.session_state.current_agent['name']}** 🤖
        
        **Mi especialidad:** {st.session_state.current_agent['description']}
        
        Tengo memoria completa de nuestra conversación y puedo ayudarte con todo lo relacionado a mi área de expertise.
        ¿En qué puedo ayudarte hoy?
        """
        st.chat_message("assistant").markdown(welcome_msg)
    
    # Mostrar historial de mensajes
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Input del usuario
user_input = st.chat_input(f"Escribe tu mensaje para {st.session_state.current_agent['name']}...")

if user_input:
    # Mostrar mensaje del usuario
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Agregar al historial
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Enviar al agente
    with st.chat_message("assistant"):
        with st.spinner(f"{st.session_state.current_agent['name']} está pensando..."):
            result = send_message(user_input, st.session_state.current_agent['id'])
            
            if 'error' not in result:
                assistant_reply = result['reply']
                st.markdown(assistant_reply)
                
                # Agregar respuesta al historial
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": assistant_reply
                })
                
                # Actualizar info del agente si cambió
                if 'current_agent' in result:
                    st.session_state.current_agent = result['current_agent']
                
            else:
                error_msg = f"❌ Error: {result['error']}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": error_msg
                })

# ============================================
# EJEMPLOS DE USO
# ============================================

st.markdown("---")

with st.expander("💡 Ejemplos de Uso por Agente"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🔧 TechBot (Soporte Técnico)**
        - "¿Cómo instalo Python?"
        - "Explícame qué son las APIs"
        - "Tengo un error en mi código JavaScript"
        """)
        
        st.markdown("""
        **🧮 MathBot (Tutor de Matemáticas)**
        - "¿Cómo resuelvo ecuaciones cuadráticas?"
        - "Explícame el teorema de Pitágoras"
        - "Necesito ayuda con cálculo diferencial"
        """)
    
    with col2:
        st.markdown("""
        **👨‍🍳 ChefBot (Chef Personal)**
        - "Receta para pasta sin gluten"
        - "¿Cómo preparar un risotto perfecto?"
        - "Ideas para cena romántica vegetariana"
        """)
        
        st.markdown("""
        **💪 FitBot (Entrenador Personal)**
        - "Rutina para principiantes en casa"
        - "Ejercicios para mejorar resistencia"
        - "Plan de alimentación para ganar músculo"
        """)
    
    with col3:
        st.markdown("""
        **🎨 CreativeBot (Asistente Creativo)**
        - "Ideas para un proyecto de fotografía"
        - "¿Cómo superar el bloqueo creativo?"
        - "Técnicas de pintura para principiantes"
        """)
        
        st.markdown("""
        **💼 BizBot (Consultor de Negocios)**
        - "¿Cómo crear un plan de negocios?"
        - "Estrategias de marketing digital"
        - "Consejos para una startup tecnológica"
        """)