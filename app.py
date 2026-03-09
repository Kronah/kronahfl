from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "ok": True,
        "mensagem": "API online funcionando"
    })

@app.route("/alerta", methods=["POST"])
def alerta():
    data = request.get_json(silent=True) or {}

    zona = data.get("zona", "")
    mensagem = data.get("mensagem", "")

    return jsonify({
        "ok": True,
        "recebido": True,
        "zona": zona,
        "mensagem": mensagem
    })