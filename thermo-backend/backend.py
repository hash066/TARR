from flask import Flask, jsonify
from data_simulator import get_data

app = Flask(__name__)

@app.route('/data')
def data():
    try:
        return jsonify(get_data())
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Important for Render
