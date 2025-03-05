import os
from dotenv import load_dotenv
import openai
from flask import Flask, request, jsonify

# Cargar variables de entorno desde el archivo clave.env.txt
load_dotenv("clave.env.txt")

# Inicializar la aplicación Flask
app = Flask(__name__)

# Obtener la clave API de OpenAI desde las variables de entorno
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("No se encontró la API Key de OpenAI en las variables de entorno.")

def ask_chatgpt(question):
    """
    Consulta a ChatGPT y devuelve la respuesta.
    """
    try:
        openai.api_key = OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Puedes cambiar a "gpt-3.5-turbo" si lo prefieres
            messages=[
                {"role": "system", "content": "Eres un asistente virtual para empleados en Odoo."},
                {"role": "user", "content": question}
            ]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error al consultar ChatGPT: {str(e)}"

@app.route("/chat", methods=["POST"])
def chat():
    """
    Endpoint para recibir preguntas de Odoo y devolver respuestas.
    """
    data = request.json
    question = data.get("question", "").strip()

    # Validar que la pregunta no esté vacía
    if not question:
        return jsonify({"error": "Pregunta vacía"}), 400

    # Obtener la respuesta de ChatGPT
    answer = ask_chatgpt(question)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    # Obtener el modo de depuración desde las variables de entorno
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"

    # Iniciar el servidor Flask
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)
