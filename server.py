import os

from flask import Flask, send_from_directory

app = Flask(__name__, static_folder="ui")


@app.route("/")
def serve_ui():
    return send_from_directory("ui", "index.html")


@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory("ui", path)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
