from flask import Flask, request, send_file
from rembg import remove
from io import BytesIO

app = Flask(__name__)

@app.route("/", methods=["POST"])
def remove_bg():
    if 'image' not in request.files:
        return "No image uploaded", 400

    image = request.files['image'].read()
    output = remove(image)
    return send_file(BytesIO(output), mimetype='image/png')

@app.route("/", methods=["GET"])
def hello():
    return "Rembg server is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)