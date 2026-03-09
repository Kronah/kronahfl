from flask import Flask, request, jsonify

app = Flask(__name__)

ultimo_alerta = {
    "zona": "",
    "mensagem": "",
    "timestamp": "",
    "novo": False
}

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "ok": True,
        "mensagem": "API online funcionando"
    })

@app.route("/alerta", methods=["POST"])
def alerta():
    global ultimo_alerta
    data = request.get_json(silent=True) or {}

    ultimo_alerta = {
        "zona": str(data.get("zona", "")),
        "mensagem": str(data.get("mensagem", "")),
        "timestamp": str(data.get("timestamp", "")),
        "novo": True
    }

    return jsonify({
        "ok": True,
        "alerta": ultimo_alerta
    })

@app.route("/ultimo_alerta", methods=["GET"])
def get_ultimo_alerta():
    return jsonify(ultimo_alerta)

@app.route("/marcar_lido", methods=["POST"])
def marcar_lido():
    global ultimo_alerta
    ultimo_alerta["novo"] = False
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
