import openai
from flask import Flask, request, jsonify

app = Flask(__name__)

# API Key de OpenAI (Reemplaza con la tuya)
OPENAI_API_KEY = "TU_API_KEY"

def ask_chatgpt(question):
    """Consulta a ChatGPT y devuelve la respuesta"""
    openai.api_key = OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Eres un asistente virtual para empleados en Odoo."},
                  {"role": "user", "content": question}]
    )
    return response["choices"][0]["message"]["content"]

@app.route("/chat", methods=["POST"])
def chat():
    """Recibe preguntas de Odoo y devuelve respuestas"""
    data = request.json
    question = data.get("question", "")
    if not question:
        return jsonify({"error": "Pregunta vacía"}), 400
    answer = ask_chatgpt(question)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
