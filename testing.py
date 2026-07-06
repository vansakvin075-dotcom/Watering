from flask import Flask, render_template, request, jsonify
import serial
import time
import threading

app = Flask(__name__)

PORT = "COM4"

arduino = None

# ------------------------
# CONNECT ARDUINO
# ------------------------
try:
    arduino = serial.Serial(PORT, 9600, timeout=1)
    time.sleep(2)
    print("Arduino connected on", PORT)
except Exception as e:
    print("Arduino not connected:", e)
    arduino = None


# ------------------------
# SERIAL READER (NEW ADD)
# ------------------------
def read_from_arduino():
    while True:
        if arduino is not None and arduino.in_waiting:
            try:
                line = arduino.readline().decode().strip()
                if line:
                    print("📡 Arduino:", line)
            except:
                pass
        time.sleep(0.1)


# start thread
if arduino:
    thread = threading.Thread(target=read_from_arduino, daemon=True)
    thread.start()


# ------------------------
# WEB PAGE
# ------------------------
@app.route("/")
def home():
    return render_template("index.html")


# ------------------------
# API CONTROL
# ------------------------
@app.route("/api/control", methods=["POST"])
def control():
    try:
        data = request.json
        cmd = data.get("cmd")

        if arduino is not None:
            arduino.write((cmd + "\n").encode())
            arduino.flush()

        return jsonify({
            "status": "ok",
            "cmd": cmd
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ------------------------
# RUN SERVER
# ------------------------
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)