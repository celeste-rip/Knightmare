from flask import Flask, render_template, request, redirect, Response
import serial
import os

app = Flask(__name__)
LOG_FILE = "logs/knightmare.log"
SERIAL_PORT = "/dev/ttyUSB0"  # Update for Windows: COM3 or similar
BAUD_RATE = 115200

pillars = {
    "I": "Integrated Threat Intelligence",
    "C": "Cybersecurity TTPs",
    "A": "Aerial and Aquatic Defense",
    "R": "Robotic System Resilience",
    "U": "Unmanned System Operations",
    "S": "Systems Monitoring & Response"
}

@app.route("/", methods=["GET", "POST"])
def index():
    log_output = open(LOG_FILE).read() if os.path.exists(LOG_FILE) else "No logs yet."
    if request.method == "POST":
        cmd = request.form.get("cmd")
        try:
            with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2) as ser:
                ser.write((cmd + "\n").encode())
                response = ser.readline().decode().strip()
            with open(LOG_FILE, "a") as f:
                f.write(f"[CMD] {cmd} -> {response}\n")
            log_output = response
        except Exception as e:
            log_output = f"Error: {e}"
    return render_template("index.html", log_output=log_output)

@app.route("/icarus")
def icarus():
    return render_template("icarus.html", pillars=pillars)

@app.route("/video_feed")
def video_feed():
    def gen():
        import cv2
        cam = cv2.VideoCapture(0)
        while True:
            ret, frame = cam.read()
            if not ret:
                break
            _, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        cam.release()
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')
