import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, messaging

app = Flask(__name__)
CORS(app)

# ===== Inicializar Firebase =====
firebase_json = os.environ.get("FIREBASE_SERVICE_ACCOUNT")

if firebase_json:
    cred_dict = json.loads(firebase_json)
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "ok": True,
        "mensagem": "API KRONAH online"
    })

@app.route("/alerta", methods=["POST"])
def alerta():
    data = request.get_json(silent=True) or {}

    zona = data.get("zona", "")
    mensagem_texto = data.get("mensagem", "")
    token = data.get("token", "")

    if not token:
        return jsonify({
            "ok": False,
            "erro": "Token FCM não informado"
        }), 400

    titulo = "Alerta Perimetral"

    message = messaging.Message(
        token=token,
        notification=messaging.Notification(
            title=titulo,
            body=mensagem_texto
        ),
        data={
            "zona": str(zona),
            "mensagem": str(mensagem_texto)
        }
    )

    response = messaging.send(message)

    return jsonify({
        "ok": True,
        "zona": zona,
        "mensagem": mensagem_texto,
        "firebase": response
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
