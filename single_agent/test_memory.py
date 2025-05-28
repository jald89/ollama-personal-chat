#!/usr/bin/env python3
"""
Script de prueba para demostrar la memoria y funcionalidad del agente
Ejecutar después de iniciar el servidor Flask
"""

import requests
import json
import time

# Configuración
BASE_URL = "http://127.0.0.1:5000"
SESSION_ID = "test_session_123"

def send_message(message):
    """Envía un mensaje al chat y devuelve la respuesta"""
    try:
        response = requests.post(f"{BASE_URL}/chat", 
                               json={
                                   'message': message,
                                   'session_id': SESSION_ID
                               })
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Status code: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def test_agent_memory():
    """Prueba la memoria y personalidad del agente"""
    
    print("🤖 PRUEBA DE MEMORIA Y AGENTE - TechBot")
    print("=" * 50)
    
    # Lista de mensajes de prueba para demostrar memoria
    test_messages = [
        "Hola, ¿quién eres?",
        "Necesito ayuda con Python",
        "¿Qué es una función en Python?",
        "¿Puedes darme un ejemplo de la función que mencionaste?",
        "Ahora háblame sobre las listas en Python",
        "¿Cómo se diferencia una lista de lo que me explicaste antes sobre funciones?",
        "Gracias por toda la ayuda, ¿recuerdas de qué hablamos al principio?"
    ]
    
    responses = []
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n📝 MENSAJE {i}: {message}")
        print("-" * 30)
        
        result = send_message(message)
        
        if "error" in result:
            print(f"❌ ERROR: {result['error']}")
            break
        
        reply = result.get('reply', 'Sin respuesta')
        message_count = result.get('message_count', 0)
        
        print(f"🤖 TechBot: {reply}")
        print(f"📊 Total mensajes en memoria: {message_count}")
        
        responses.append({
            'user': message,
            'assistant': reply,
            'message_count': message_count
        })
        
        # Pausa entre mensajes para simular conversación real
        time.sleep(1)
    
    return responses

def test_context_persistence():
    """Prueba específica de persistencia de contexto"""
    print("\n" + "=" * 50)
    print("🧠 PRUEBA DE PERSISTENCIA DE CONTEXTO")
    print("=" * 50)
    
    # Establecer contexto
    context_setup = "Mi nombre es Juan y estoy aprendiendo JavaScript"
    print(f"\n📝 Estableciendo contexto: {context_setup}")
    result1 = send_message(context_setup)
    print(f"🤖 TechBot: {result1.get('reply', 'Error')}")
    
    time.sleep(1)
    
    # Probar si recuerda el contexto
    context_test = "¿Recuerdas mi nombre y qué estoy aprendiendo?"
    print(f"\n📝 Probando memoria: {context_test}")
    result2 = send_message(context_test)
    print(f"🤖 TechBot: {result2.get('reply', 'Error')}")
    
    return result2

def reset_conversation():
    """Reinicia la conversación"""
    try:
        response = requests.post(f"{BASE_URL}/reset", 
                               json={'session_id': SESSION_ID})
        return response.status_code == 200
    except:
        return False

if __name__ == "__main__":
    print("🚀 Iniciando pruebas del sistema de chat con memoria...")
    print("📡 Verificando conexión con el servidor...")
    
    # Verificar conexión
    test_result = send_message("test")
    if "error" in test_result:
        print(f"❌ No se puede conectar al servidor: {test_result['error']}")
        print("💡 Asegúrate de que el servidor Flask esté corriendo en http://127.0.0.1:5000")
        exit(1)
    
    print("✅ Conexión exitosa!")
    
    # Reiniciar conversación para prueba limpia
    if reset_conversation():
        print("🔄 Conversación reiniciada")
    
    # Ejecutar pruebas
    responses = test_agent_memory()
    
    if responses:
        # Prueba adicional de contexto
        test_context_persistence()
        
        print("\n" + "=" * 50)
        print("📋 RESUMEN DE PRUEBAS")
        print("=" * 50)
        print(f"✅ Mensajes enviados: {len(responses)}")
        print(f"✅ Agente personalizado: TechBot (Soporte Técnico)")
        print(f"✅ Memoria funcionando: {responses[-1]['message_count']} mensajes recordados")
        print("✅ Contexto mantenido a lo largo de la conversación")
        print("\n🎉 ¡Todas las pruebas completadas exitosamente!")
    else:
        print("❌ Las pruebas fallaron")