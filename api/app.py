# Flask app for å servere Angular frontend og API-endepunkter
# Denne filen blir startet ved å kjøre 'py -m api.app' fra root.
import os
from flask import Flask, send_from_directory, jsonify                           # jsonify for API-et
from flask_cors import CORS                                                     # For å håndtere CORS (Cross-Origin Resource Sharing)

from api.database import hent_varer # Antar at denne funksjonen er klar

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))                        # Stien til 'api'-mappen
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, '..'))                 # Stien til 'ITPROGDB-Gruppe-8'
ANGULAR_DIST_DIR = os.path.join(PROJECT_ROOT, 'www', 'varelager', 'dist', 'varelager', 'browser') # Stien til Angular-dist-mappen
app = Flask(__name__, static_folder=None)

# Konfigurer CORS for API-endepunktene:
CORS(app, resources={r"/api/*": {"origins": "*"}})

# === API Endepunkt ===
@app.route('/api/varer', methods=['GET'])
def api_get_varer():
    try:
        varer_data = hent_varer() # Din funksjon fra api.database
        return jsonify(varer_data)
    except Exception as e:
        print(f"Feil i /api/varer: {e}")
        return jsonify({"error": "Intern serverfeil ved henting av varer"}), 500

# === Ruter for å servere Angular-appen ===

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_angular(path):
    requested_file_path = os.path.join(ANGULAR_DIST_DIR, path)

    if path != "" and os.path.exists(requested_file_path) and os.path.isfile(requested_file_path):
        return send_from_directory(ANGULAR_DIST_DIR, path)                      # Returner filen hvis den finnes i Angular-dist-mappen  
    else:
        index_path = os.path.join(ANGULAR_DIST_DIR, 'index.html')
        if not os.path.exists(index_path):
            return "Angular app's index.html not found in " + ANGULAR_DIST_DIR, 404
        return send_from_directory(ANGULAR_DIST_DIR, 'index.html')

if __name__ == '__main__':
    print("Webserver kjører på http://localhost:5000")
    app.run(host='127.0.0.1', port=5000, debug=False)
# For å kjøre denne appen, bruk kommandoen:
# python -m api.app