# Flask app for å servere Angular frontend og API-endepunkter
# Denne filen blir startet ved å kjøre 'python api/app.py' fra root.
import os
from flask import Flask, send_from_directory, jsonify                           # jsonify for API-et
from flask_cors import CORS                                                     # For å håndtere CORS (Cross-Origin Resource Sharing)

from api.database import hent_varer # Antar at denne funksjonen er klar

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))                        # Stien til 'api'-mappen
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, '..'))                 # Stien til 'ITPROGDB-Gruppe-8'
ANGULAR_DIST_DIR = os.path.join(PROJECT_ROOT, 'www', 'varelager', 'dist', 'varelager', 'browser') # Stien til Angular-dist-mappen
# Initialiser Flask-appen. Vi setter static_folder til None for å håndtere alt manuelt,
# eller du kan sette den direkte til ANGULAR_DIST_DIR og static_url_path til ''.
app = Flask(__name__, static_folder=None)

# Konfigurer CORS for API-endepunktene dine.
# For enkelhetens skyld, tillater alle origins for /api/*, juster for produksjon.
CORS(app, resources={r"/api/*": {"origins": "*"}})

# === API Endepunkt ===
@app.route('/api/varer', methods=['GET'])
def api_get_varer():
    try:
        # Her kaller du funksjonen som henter og formaterer varene dine
        # Sørg for at denne funksjonen returnerer en liste med dictionaries
        # og at 'Pris' og 'Antall' er numeriske typer (float/int).
        varer_data = hent_varer() # Din funksjon fra api.database
        return jsonify(varer_data)
    except Exception as e:
        print(f"Feil i /api/varer: {e}")
        return jsonify({"error": "Intern serverfeil ved henting av varer"}), 500

# === Ruter for å servere Angular-appen ===

# Denne ruten serverer filer direkte hvis de finnes (f.eks. main.js, styles.css, assets).
# For alle andre stier (inkludert rot '/'), serveres index.html slik at Angular kan håndtere rutingen.
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_angular(path):
    # Sjekk om den forespurte stien (path) er en fil i Angulars distribusjonsmappe
    requested_file_path = os.path.join(ANGULAR_DIST_DIR, path)

    if path != "" and os.path.exists(requested_file_path) and os.path.isfile(requested_file_path):
        # Hvis det er en eksisterende fil, server den
        return send_from_directory(ANGULAR_DIST_DIR, path)
    else:
        # Ellers, server index.html for Angular routing (håndterer /, /en-angular-rute, etc.)
        index_path = os.path.join(ANGULAR_DIST_DIR, 'index.html')
        if not os.path.exists(index_path):
            return "Angular app's index.html not found in " + ANGULAR_DIST_DIR, 404
        return send_from_directory(ANGULAR_DIST_DIR, 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)