# webui/app.py
import cv2
from flask import Response
from flask import Flask, request, render_template, redirect, url_for
from core.knightmare_controller import KnightmareController

app = Flask(__name__)
knightmare = KnightmareController()

@app.route("/", methods=["GET", "POST"])
def index():
    output = None
    if request.method == "POST":
        cmd = request.form["cmd"]
        output = knightmare.run_payload(cmd)
    return render_template("index.html", modules=knightmare.list_modules(), output=output)

@app.route("/load_module/<path>")
def load_module(path):
    msg = knightmare.load_module(path)
    return redirect(url_for("index"))

@app.route("/connect", methods=["POST"])
def connect():
    device = request.form["device"]
    msg = knightmare.connect(device)
    return redirect(url_for("index"))
@app.route("/serial_devices")
def serial_devices():
    devices = knightmare.detect_serial_devices()
    return render_template("serial_devices.html", devices=devices)
def generate_video():
    cap = cv2.VideoCapture(0)  # Use 0 for default webcam (change index for other cams)
    while True:
        success, frame = cap.read()
        if not success:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
@app.route("/video_feed")
def video_feed():
    return Response(generate_video(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
