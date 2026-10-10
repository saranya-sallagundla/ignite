from flask import Flask, jsonify

APP_VERSION = "2.1"

app = Flask(__name__)


@app.route("/health")
def health():
    return jsonify(status="ok", version=APP_VERSION), 200


@app.route("/ready")
def ready():
    return jsonify(ready=True, version=APP_VERSION), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
