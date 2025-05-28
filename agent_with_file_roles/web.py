import streamlit as st
import requests
import uuid

st.set_page_config(
    page_title="Agentes IA con roles externos",
    page_icon="🤖",
    layout="wide"
)

if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'current_agent' not in st.session_state:
    st.session_state.current_agent = {'id': 'techbot', 'name': 'TechBot', 'description': 'Agente techbot'}
if 'available_agents' not in st.session_state:
    st.session_state.available_agents = {}

API_URL = 'http://127.0.0.1:5050'

def get_available_agents():
    try:
        response = requests.get(f'{API_URL}/agents')
        if response.status_code == 200:
            return response.json()['available_agents']
    except:
        return {}
    return {}

def set_agent(agent_id):
    try:
        response = requests.post(f'{API_URL}/set_agent',
            json={
                'session_id': st.session_state.session_id,
                'agent_id': agent_id
            })
        if response.status_code == 200:
            data = response.json()
            st.session_state.current_agent = data['agent']
            st.session_state.messages = []
            return True
    except:
        return False
    return False

def send_message(message, agent_id):
    try:
        response = requests.post(f'{API_URL}/chat',
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

def create_custom_agent_from_file(agent_name, filename):
    try:
        response = requests.post(f'{API_URL}/create_custom_agent_from_file',
            json={
                'session_id': st.session_state.session_id,
                'name': agent_name,
                'filename': filename
            })
        if response.status_code == 200:
            return response.json()
    except:
        return {'error': 'Error al crear agente desde archivo'}
    return {'error': 'Error de conexión'}

if not st.session_state.available_agents:
    st.session_state.available_agents = get_available_agents()

st.title('🤖 Agentes IA')
st.markdown("**Personalidades y roles definidos por archivos en la carpeta `/roles`**")

with st.sidebar:
    st.header("🎭 Selector de Agentes")
    st.success(f"**Agente Actual:** {st.session_state.current_agent['name']}")
    st.info(f"**Descripción:** {st.session_state.current_agent['description']}")
    st.markdown("---")
    st.subheader("🤖 Agentes Disponibles")
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
    st.subheader("🛠️ Crear Agente Personalizado desde Archivo")
    with st.expander("➕ Nuevo Agente desde Archivo"):
        custom_name = st.text_input("Nombre del agente:", key="custom_name_file")
        filename = st.text_input("Nombre del archivo de rol (ej: fitness.txt):", key="custom_file")
        if st.button("🚀 Crear Agente desde Archivo"):
            if custom_name and filename:
                result = create_custom_agent_from_file(custom_name, filename)
                if 'error' not in result:
                    st.session_state.current_agent = result['agent']
                    st.session_state.messages = []
                    st.success(f"¡Agente {custom_name} creado desde {filename}!")
                    st.rerun()
                else:
                    st.error(f"Error: {result['error']}")
            else:
                st.warning("Completa nombre y archivo de rol")
    st.markdown("---")
    st.subheader("📊 Info de Sesión")
    st.text(f"ID: {st.session_state.session_id[:8]}...")
    st.text(f"Mensajes: {len(st.session_state.messages)}")
    if st.button("🗑️ Nueva Sesión"):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()

chat_container = st.container()
with chat_container:
    if not st.session_state.messages:
        welcome_msg = f"""
        ¡Hola! Soy **{st.session_state.current_agent['name']}** 🤖
        **Descripción:** {st.session_state.current_agent['description']}
        Tengo memoria completa de nuestra conversación y puedo ayudarte según mi especialidad.
        ¿En qué puedo ayudarte hoy?
        """
        st.chat_message("assistant").markdown(welcome_msg)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
user_input = st.chat_input(f"Escribe tu mensaje para {st.session_state.current_agent['name']}...")
if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("assistant"):
        with st.spinner(f"{st.session_state.current_agent['name']} está pensando..."):
            result = send_message(user_input, st.session_state.current_agent['id'])
            if 'error' not in result:
                assistant_reply = result['reply']
                st.markdown(assistant_reply)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_reply
                })
                if 'current_agent' in result:
                    st.session_state.current_agent = result['current_agent']
            else:
                error_msg = f"❌ Error: {result['error']}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })
st.markdown("---")
st.markdown(
    "💡 **Tip:** Puedes crear nuevos agentes agregando archivos de texto en la carpeta `/roles` y usarlos desde la interfaz.\n"
    "Ejemplo: crea un archivo llamado `aitutor.txt` con instrucciones para un tutor experto en IA generativa y Python."
)
