from flask import Flask, render_template, request, jsonify
import serial
import time

app = Flask(__name__)

PORT = "COM4"

arduino = None

try:
    arduino = serial.Serial(PORT, 9600, timeout=1)
    time.sleep(2)
    print("Arduino connected")
except Exception as e:
    print("Arduino error:", e)
    arduino = None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/water", methods=["POST"])
def water():
    try:
        data = request.json
        state = data.get("state")

        cmd = ""

        if state == "ON":
            cmd = "WATER_ON\n"
        elif state == "OFF":
            cmd = "WATER_OFF\n"

        if arduino is not None:
            arduino.write(cmd.encode())
            arduino.flush()   # 🔥 IMPORTANT FIX

        return jsonify({"status": "ok", "sent": cmd})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)