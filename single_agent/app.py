from flask import Flask, request, jsonify
import ollama

app = Flask(__name__)

# Almacenamiento en memoria para el historial de conversaciones
# En producción, esto debería estar en una base de datos
conversation_history = {}

# Configuración del agente - Define la personalidad y rol
AGENT_SYSTEM_MESSAGE = {
    'role': 'system',
    'content': '''Eres un Asistente de Soporte Técnico especializado en programación y tecnología. 
    Tu personalidad es:
    - Amigable y paciente
    - Explicas conceptos técnicos de manera clara y sencilla
    - Siempre proporcionas ejemplos prácticos
    - Te enfocas en resolver problemas paso a paso
    - Mantienes un tono profesional pero cercano
    - Recuerdas el contexto de la conversación anterior
    
    Siempre te identificas como "TechBot" y ofreces ayuda adicional al final de cada respuesta.'''
}

def get_or_create_conversation(session_id='default'):
    """Obtiene o crea una nueva conversación con memoria"""
    if session_id not in conversation_history:
        # Inicializar conversación con el mensaje del sistema (agente)
        conversation_history[session_id] = [AGENT_SYSTEM_MESSAGE]
    return conversation_history[session_id]

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json['message']
        session_id = request.json.get('session_id', 'default')
        
        # Obtener historial de conversación (MEMORIA)
        messages = get_or_create_conversation(session_id)
        
        # Agregar mensaje del usuario al historial
        messages.append({
            'role': 'user',
            'content': user_message
        })
        
        model = "llama3.2:1b"
        
        # Llamar a Ollama con TODO el historial de conversación
        response = ollama.chat(
            model=model, 
            messages=messages  # Aquí se pasa toda la memoria
        )
        
        # Extraer respuesta del asistente
        assistant_reply = response['message']['content']
        
        # Agregar respuesta del asistente al historial (MEMORIA)
        messages.append({
            'role': 'assistant',
            'content': assistant_reply
        })
        
        # Opcional: Limitar el historial para evitar tokens excesivos
        # Mantener solo los últimos 20 mensajes + el mensaje de sistema
        if len(messages) > 21:
            messages = [messages[0]] + messages[-20:]
            conversation_history[session_id] = messages
        
        return jsonify({
            'reply': assistant_reply,
            'session_id': session_id,
            'message_count': len(messages) - 1  # -1 para no contar el mensaje de sistema
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/reset', methods=['POST'])
def reset_conversation():
    """Endpoint para reiniciar la conversación"""
    session_id = request.json.get('session_id', 'default')
    if session_id in conversation_history:
        del conversation_history[session_id]
    return jsonify({'message': 'Conversación reiniciada'})

@app.route('/history', methods=['GET'])
def get_history():
    """Endpoint para obtener el historial de conversación"""
    session_id = request.args.get('session_id', 'default')
    messages = get_or_create_conversation(session_id)
    # Retornar solo mensajes de usuario y asistente (sin el sistema)
    user_messages = [msg for msg in messages if msg['role'] in ['user', 'assistant']]
    return jsonify({'history': user_messages})

if __name__ == '__main__':
    print("🤖 TechBot - Asistente de Soporte Técnico iniciado")
    print("💾 Memoria de conversación activada")
    print("🚀 Servidor corriendo en http://127.0.0.1:5050")

    app.run(debug=True, port=5050)