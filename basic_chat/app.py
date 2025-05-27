from flask import Flask, request, jsonify
import ollama

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    
    prompt = user_message
    model = "llama3.2:1b"  # o cualquier otro modelo que tengas instalado
    
    # Llamar a la API de ollama para obtener una respuesta
    response = ollama.chat(model=model, messages=[{'role':'user', 'content': prompt}])
    
    # Extraer el contenido de la respuesta
    reply = response['message']['content']
    return reply

if __name__ == '__main__':
    app.run(debug=True, port=5050)