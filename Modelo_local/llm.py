from flask import Flask, render_template_string, request, session
import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma:2b"

app = Flask(__name__)
app.secret_key = "clave_secreta_para_sesiones_123"  


HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Gemma 2B - Ollama Chat</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #23272f; color: #f5f6fa; margin: 0; padding: 0; }
        .container { max-width: 800px; margin: auto; padding: 20px; }
        h1 { text-align: center; }
        .chat-container {
            background-color: #2c313c; border-radius: 8px; padding: 20px; margin: 20px 0;
            height: 400px; overflow-y: auto; border: 2px solid #3d4553;
        }
        .mensaje {
            margin: 15px 0; padding: 10px; border-radius: 8px; line-height: 1.5;
        }
        .usuario {
            background-color: #4f8cff; color: white; margin-left: 50px; text-align: right;
        }
        .asistente {
            background-color: #40444b; color: #f5f6fa; margin-right: 50px;
        }
        .form-container {
            display: flex; gap: 10px; margin-top: 20px;
        }
        input[type=text] {
            flex: 1; padding: 12px; background-color: #2c313c; color: #f5f6fa; 
            border: 2px solid #3d4553; border-radius: 8px; font-size: 16px;
        }
        input[type=text]:focus {
            outline: none; border-color: #4f8cff;
        }
        button {
            background-color: #4f8cff; color: #ffffff; padding: 12px 20px;
            border: none; border-radius: 8px; cursor: pointer; font-size: 16px;
            min-width: 80px;
        }
        button:hover { background-color: #3574d4; }
        .clear-btn {
            background-color: #e74c3c; margin-left: 10px;
        }
        .clear-btn:hover { background-color: #c0392b; }
        .empty-chat {
            text-align: center; color: #7289da; font-style: italic; margin-top: 150px;
        }
    </style>
    <script>
        function scrollToBottom() {
            var chatContainer = document.querySelector('.chat-container');
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        window.onload = function() {
            scrollToBottom();
        }
    </script>
</head>
<body>
    <div class="container">
        <h1>Gemma 2B - Ollama Chat</h1>
        
        <div class="chat-container">
            {% if historial %}
                {% for mensaje in historial %}
                    <div class="mensaje {{ mensaje.tipo }}">
                        <strong>{% if mensaje.tipo == 'usuario' %}Tú:{% else %}Gemma:{% endif %}</strong><br>
                        {{ mensaje.contenido }}
                    </div>
                {% endfor %}
            {% else %}
                <div class="empty-chat">¡Escribe un mensaje para comenzar!</div>
            {% endif %}
        </div>
        
        <form method="post" class="form-container">
            <input type="text" name="prompt" placeholder="Escribe tu pregunta..." required autofocus>
            <button type="submit">Enviar</button>
            <button type="submit" name="limpiar" value="true" class="clear-btn">Limpiar</button>
        </form>
    </div>
</body>
</html>
"""

def consultar_ollama(prompt):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": True
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload, stream=True)
        if response.status_code == 200:
            respuesta = ""
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode('utf-8'))
                        if 'response' in data:
                            respuesta += data['response']
                        if data.get('done', False):
                            break
                    except json.JSONDecodeError:
                        continue
            return respuesta.strip() if respuesta else "Sin respuesta del modelo."
        else:
            return f"Error HTTP {response.status_code}: {response.text}"
    except requests.exceptions.ConnectionError:
        return "Error: No se pudo conectar con Ollama. ¿Está ejecutándose en localhost:11434?"
    except Exception as e:
        return f"Error inesperado: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    # Inicializar historial si no existe
    if 'historial' not in session:
        session['historial'] = []
    
    if request.method == "POST":
        
        if request.form.get("limpiar"):
            session['historial'] = []
            return render_template_string(HTML_TEMPLATE, historial=session['historial'])
        
        prompt = request.form.get("prompt", "").strip()
        if prompt:
            # Agregar mensaje del usuario al historial
            session['historial'].append({
                'tipo': 'usuario',
                'contenido': prompt
            })
            
            # Obtener respuesta del modelo
            respuesta = consultar_ollama(prompt)
            
            # Agregar respuesta del asistente al historial
            session['historial'].append({
                'tipo': 'asistente',
                'contenido': respuesta
            })
            
            if len(session['historial']) > 20:
                session['historial'] = session['historial'][-20:]
            
            session.modified = True
    
    return render_template_string(HTML_TEMPLATE, historial=session['historial'])

if __name__ == "__main__":
    app.run(port=5000, debug=True)
