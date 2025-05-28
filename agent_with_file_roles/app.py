import os
from flask import Flask, request, jsonify
import ollama

app = Flask(__name__)

conversation_history = {}
current_agents = {}

ROLES_DIR = os.path.join(os.path.dirname(__file__), 'roles')

def load_roles_from_files():
    agents = {}
    for filename in os.listdir(ROLES_DIR):
        if filename.endswith('.txt'):
            agent_id = filename.replace('.txt', '')
            with open(os.path.join(ROLES_DIR, filename), 'r', encoding='utf-8') as f:
                content = f.read().strip()
            agents[agent_id] = {
                'name': agent_id.capitalize() + 'Bot',
                'description': f'Agente {agent_id}',
                'system_message': content
            }
    return agents

AVAILABLE_AGENTS = load_roles_from_files()
# Nota: cualquier archivo nuevo en roles/ (ej: aitutor.txt) será cargado automáticamente como agente

def get_agent_system_message(agent_id):
    if agent_id in AVAILABLE_AGENTS:
        return {
            'role': 'system',
            'content': AVAILABLE_AGENTS[agent_id]['system_message']
        }
    else:
        return {
            'role': 'system',
            'content': 'Eres un asistente IA útil y amigable.'
        }

def get_or_create_conversation(session_id, agent_id='techbot'):
    if session_id not in conversation_history:
        conversation_history[session_id] = [get_agent_system_message(agent_id)]
        current_agents[session_id] = agent_id
    return conversation_history[session_id]

@app.route('/agents', methods=['GET'])
def list_agents():
    return jsonify({
        'available_agents': {
            agent_id: {
                'name': info['name'],
                'description': info['description']
            }
            for agent_id, info in AVAILABLE_AGENTS.items()
        }
    })

@app.route('/set_agent', methods=['POST'])
def set_agent():
    data = request.json
    session_id = data.get('session_id', 'default')
    agent_id = data.get('agent_id', 'techbot')
    if agent_id not in AVAILABLE_AGENTS:
        return jsonify({'error': f'Agente {agent_id} no encontrado'}), 400
    conversation_history[session_id] = [get_agent_system_message(agent_id)]
    current_agents[session_id] = agent_id
    agent_info = AVAILABLE_AGENTS[agent_id]
    return jsonify({
        'message': f'Agente cambiado a {agent_info["name"]}',
        'agent': {
            'id': agent_id,
            'name': agent_info['name'],
            'description': agent_info['description']
        }
    })

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data['message']
        session_id = data.get('session_id', 'default')
        agent_id = data.get('agent_id', 'techbot')
        if session_id in current_agents and current_agents[session_id] != agent_id:
            conversation_history[session_id] = [get_agent_system_message(agent_id)]
            current_agents[session_id] = agent_id
        messages = get_or_create_conversation(session_id, agent_id)
        messages.append({'role': 'user', 'content': user_message})
        model = "llama3.2:1b"
        response = ollama.chat(model=model, messages=messages)
        assistant_reply = response['message']['content']
        messages.append({'role': 'assistant', 'content': assistant_reply})
        if len(messages) > 21:
            messages = [messages[0]] + messages[-20:]
            conversation_history[session_id] = messages
        current_agent = AVAILABLE_AGENTS.get(current_agents.get(session_id, agent_id), {})
        return jsonify({
            'reply': assistant_reply,
            'session_id': session_id,
            'current_agent': {
                'id': current_agents.get(session_id, agent_id),
                'name': current_agent.get('name', 'Unknown'),
                'description': current_agent.get('description', '')
            },
            'message_count': len(messages) - 1
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/create_custom_agent_from_file', methods=['POST'])
def create_custom_agent_from_file():
    data = request.json
    session_id = data.get('session_id', 'default')
    agent_name = data.get('name', 'CustomAgent')
    filename = data.get('filename')
    if not filename:
        return jsonify({'error': 'Se requiere el nombre del archivo de rol'}), 400
    filepath = os.path.join(ROLES_DIR, filename)
    if not os.path.isfile(filepath):
        return jsonify({'error': f'Archivo {filename} no encontrado'}), 400
    with open(filepath, 'r', encoding='utf-8') as f:
        custom_instructions = f.read().strip()
    custom_system_message = {
        'role': 'system',
        'content': f'''Eres {agent_name}.

{custom_instructions}

Mantén estas instrucciones durante toda la conversación.'''
    }
    conversation_history[session_id] = [custom_system_message]
    current_agents[session_id] = 'custom'
    return jsonify({
        'message': f'Agente personalizado {agent_name} creado desde archivo',
        'agent': {
            'id': 'custom',
            'name': agent_name,
            'description': f'Agente personalizado desde {filename}'
        }
    })

@app.route('/reset', methods=['POST'])
def reset_conversation():
    data = request.json
    session_id = data.get('session_id', 'default')
    if session_id in conversation_history:
        current_agent_id = current_agents.get(session_id, 'techbot')
        conversation_history[session_id] = [get_agent_system_message(current_agent_id)]
    return jsonify({'message': 'Conversación reiniciada'})

if __name__ == '__main__':
    print("🤖 Sistema de Agentes IA con roles desde archivos")
    print("📋 Agentes disponibles (según archivos en /roles):")
    for agent_id, info in AVAILABLE_AGENTS.items():
        print(f"   - {agent_id}: {info['name']} ({info['description']})")
    print("\nEjemplo: para agregar un agente IA Tutor, crea roles/aitutor.txt y reinicia el backend.")
    print("\n🚀 Servidor iniciado en http://127.0.0.1:5050")
    print("\n📡 Endpoints disponibles:")
    print("   GET  /agents - Listar agentes")
    print("   POST /set_agent - Cambiar agente")
    print("   POST /create_custom_agent_from_file - Crear agente personalizado desde archivo")
    print("   POST /chat - Enviar mensaje")
    print("   POST /reset - Reiniciar conversación")
    app.run(debug=True, port=5050)
