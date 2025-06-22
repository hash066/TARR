from flask import Flask, request, jsonify

app = Flask(__name__)
sensor_data = {"hot": 0, "cold": 0, "power": 0, "pressure": 0}

@app.route("/data", methods=["POST"])
def update_data():
    global sensor_data
    sensor_data = request.json
    return {"status": "received"}

@app.route("/data", methods=["GET"])
def get_data():
    return jsonify(sensor_data)

if __name__ == "__main__":
    app.run(app.run(host="0.0.0.0", port=5000)
)
