from flask import Flask, request, jsonify
from flask_cors import CORS

from database import hent_varer

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def index():
    if(request.method == 'GET'):
        return jsonify(hent_varer())
    else:
        return jsonify({"error": "Method not allowed"}), 405
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)