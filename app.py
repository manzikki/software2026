from flask import Flask, render_template, jsonify
from logic import get_random_drill
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/next")
def next_drill():
    drill = get_random_drill()
    return jsonify(drill)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
