from flask import Flask, request, jsonify
import ollama

app = Flask(__name__)

# Almacenamiento en memoria para conversaciones
conversation_history = {}
current_agents = {}  # Para almacenar el agente actual por sesión

# ============================================
# BIBLIOTECA DE AGENTES PREDEFINIDOS
# ============================================

AVAILABLE_AGENTS = {
    "techbot": {
        "name": "TechBot",
        "description": "Asistente de Soporte Técnico",
        "system_message": '''Eres TechBot, un asistente de soporte técnico especializado en programación y tecnología. 
        Eres amigable, paciente, explicas paso a paso y siempre proporcionas ejemplos prácticos.'''
    },
    
    "mathtutor": {
        "name": "MathBot",
        "description": "Tutor de Matemáticas",
        "system_message": '''Eres MathBot, un tutor de matemáticas paciente y motivador. 
        Explicas conceptos paso a paso, usas analogías cotidianas y siempre verificas la comprensión del estudiante.'''
    },
    
    "chef": {
        "name": "ChefBot",
        "description": "Chef Personal",
        "system_message": '''Eres ChefBot, un chef personal experto en cocina internacional. 
        Eres apasionado, creativo, adaptas recetas según restricciones dietéticas y siempre incluyes tips profesionales.'''
    },
    
    "fitness": {
        "name": "FitBot",
        "description": "Entrenador Personal",
        "system_message": '''Eres FitBot, un entrenador personal certificado. 
        Creas rutinas personalizadas, explicas técnicas correctas, motivas constantemente y priorizas la seguridad.'''
    },
    
    "creative": {
        "name": "CreativeBot", 
        "description": "Asistente Creativo",
        "system_message": '''Eres CreativeBot, un compañero creativo para proyectos artísticos. 
        Inspiras sin juzgar, sugieres técnicas específicas y ayudas a superar bloqueos creativos.'''
    },
    
    "business": {
        "name": "BizBot",
        "description": "Consultor de Negocios", 
        "system_message": '''Eres BizBot, un consultor empresarial con experiencia. 
        Analizas viabilidad, propones estrategias accionables y hablas en términos orientados a resultados.'''
    }
}

def get_agent_system_message(agent_id):
    """Obtiene el mensaje del sistema para un agente específico"""
    if agent_id in AVAILABLE_AGENTS:
        return {
            'role': 'system',
            'content': AVAILABLE_AGENTS[agent_id]['system_message']
        }
    else:
        # Agente por defecto
        return {
            'role': 'system', 
            'content': 'Eres un asistente IA útil y amigable.'
        }

def get_or_create_conversation(session_id, agent_id='techbot'):
    """Obtiene o crea una conversación con un agente específico"""
    if session_id not in conversation_history:
        conversation_history[session_id] = [get_agent_system_message(agent_id)]
        current_agents[session_id] = agent_id
    return conversation_history[session_id]

@app.route('/agents', methods=['GET'])
def list_agents():
    """Endpoint para listar todos los agentes disponibles"""
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
    """Endpoint para cambiar el agente de una sesión"""
    data = request.json
    session_id = data.get('session_id', 'default')
    agent_id = data.get('agent_id', 'techbot')
    
    if agent_id not in AVAILABLE_AGENTS:
        return jsonify({'error': f'Agente {agent_id} no encontrado'}), 400
    
    # Reiniciar conversación con nuevo agente
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
        
        # Si se especifica un agente diferente, cambiar
        if session_id in current_agents and current_agents[session_id] != agent_id:
            conversation_history[session_id] = [get_agent_system_message(agent_id)]
            current_agents[session_id] = agent_id
        
        # Obtener historial de conversación
        messages = get_or_create_conversation(session_id, agent_id)
        
        # Agregar mensaje del usuario
        messages.append({
            'role': 'user',
            'content': user_message
        })
        
        model = "llama3.2:1b"
        
        # Llamar a Ollama con contexto completo
        response = ollama.chat(model=model, messages=messages)
        assistant_reply = response['message']['content']
        
        # Agregar respuesta al historial
        messages.append({
            'role': 'assistant',
            'content': assistant_reply
        })
        
        # Gestión de memoria (limitar historial)
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

@app.route('/create_custom_agent', methods=['POST'])
def create_custom_agent():
    """Endpoint para crear un agente personalizado temporal"""
    data = request.json
    session_id = data.get('session_id', 'default')
    custom_instructions = data.get('instructions', '')
    agent_name = data.get('name', 'CustomAgent')
    
    if not custom_instructions:
        return jsonify({'error': 'Se requieren instrucciones para el agente'}), 400
    
    # Crear mensaje de sistema personalizado
    custom_system_message = {
        'role': 'system',
        'content': f'''Eres {agent_name}. 
        
        Instrucciones específicas:
        {custom_instructions}
        
        Mantén estas instrucciones durante toda la conversación y adapta tu comportamiento según lo especificado.'''
    }
    
    # Reiniciar conversación con agente personalizado
    conversation_history[session_id] = [custom_system_message]
    current_agents[session_id] = 'custom'
    
    return jsonify({
        'message': f'Agente personalizado {agent_name} creado exitosamente',
        'agent': {
            'id': 'custom',
            'name': agent_name,
            'description': 'Agente personalizado'
        }
    })

@app.route('/reset', methods=['POST'])
def reset_conversation():
    """Reinicia la conversación manteniendo el agente actual"""
    data = request.json
    session_id = data.get('session_id', 'default')
    
    if session_id in conversation_history:
        current_agent_id = current_agents.get(session_id, 'techbot')
        conversation_history[session_id] = [get_agent_system_message(current_agent_id)]
    
    return jsonify({'message': 'Conversación reiniciada'})

if __name__ == '__main__':
    print("🤖 Sistema de Agentes IA Avanzado")
    print("📋 Agentes disponibles:")
    for agent_id, info in AVAILABLE_AGENTS.items():
        print(f"   - {agent_id}: {info['name']} ({info['description']})")
    print("\n🚀 Servidor iniciado en http://127.0.0.1:5000")
    print("\n📡 Endpoints disponibles:")
    print("   GET  /agents - Listar agentes")
    print("   POST /set_agent - Cambiar agente")
    print("   POST /create_custom_agent - Crear agente personalizado")
    print("   POST /chat - Enviar mensaje")
    print("   POST /reset - Reiniciar conversación")
    
    app.run(debug=True, port=5050)