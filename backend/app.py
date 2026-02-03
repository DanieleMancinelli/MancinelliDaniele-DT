from flask import Flask, jsonify, request
from flask_cors import CORS
from DatabaseWrapper import DatabaseWrapper

app = Flask(__name__)
# Abilitiamo CORS per permettere ad Angular di comunicare con Flask
CORS(app)

# Inizializziamo il Database Wrapper
db = DatabaseWrapper()

@app.route('/deliveries', methods=['GET'])
def get_deliveries():
    """Ritorna la lista di tutte le consegne in formato JSON"""
    try:
        data = db.get_all_deliveries()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/deliveries', methods=['POST'])
def add_delivery():
    """Riceve una nuova consegna, la valida e la salva nel DB"""
    data = request.json
    
    # Validazione base: controlliamo che ci siano tutti i campi richiesti
    required_fields = ['tracking_code', 'recipient', 'address', 'time_slot', 'priority']
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Dati incompleti"}), 400

    try:
        db.add_delivery(
            tracking=data['tracking_code'],
            recipient=data['recipient'],
            address=data['address'],
            time_slot=data['time_slot'],
            priority=data['priority']
        )
        return jsonify({"message": "Consegna inserita correttamente"}), 201
    except Exception as e:
        # Gestione errore se il codice tracking (UNIQUE) esiste già
        if "Duplicate entry" in str(e):
            return jsonify({"error": "Il codice tracking esiste già"}), 409
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Avviamo sulla porta 5000
    app.run(host='0.0.0.0', port=5000, debug=True)