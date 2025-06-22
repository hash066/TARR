from flask import Flask, jsonify
from data_simulator import get_data
import os

app = Flask(__name__)

@app.route('/data')
def data():
    try:
        return jsonify(get_data())
    except Exception as e:
        return jsonify({'error': str(e)})

# Health check endpoint for Render (so it doesn’t timeout)
@app.route('/healthz')
def health_check():
    return "OK", 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use the PORT Render provides
    app.run(host='0.0.0.0', port=port)
