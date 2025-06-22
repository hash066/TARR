from flask import Flask, jsonify
import random
import time

app = Flask(__name__)

@app.route('/data')
def get_data():
    data = {
        "hot": round(random.uniform(35.0, 45.0), 2),
        "cold": round(random.uniform(20.0, 30.0), 2),
        "power": round(random.uniform(3.0, 6.0), 2),
        "pressure": round(random.uniform(0.3, 1.2), 2)
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
