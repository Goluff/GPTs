
import requests
import json
import hashlib
import hmac

# Configuration
API_URL = "https://api.yourdomain.com/psychtracker/record_entry"
API_KEY = "your-api-key-here"
HMAC_SECRET = b"your-hmac-secret"

# Données à envoyer
data = {
    "user_id": "UUID123",
    "date": "2025-07-14",
    "category": "anxiety",
    "score": 7,
    "note": "Fatigue mentale, troubles du sommeil"
}

# Préparation du corps JSON et signature
body = json.dumps(data).encode("utf-8")
signature = hmac.new(HMAC_SECRET, body, hashlib.sha256).hexdigest()

# En-têtes sécurisés
headers = {
    "Content-Type": "application/json",
    "X-API-Key": API_KEY,
    "X-Signature": signature
}

# Envoi de la requête
response = requests.post(API_URL, headers=headers, data=body)

# Affichage du résultat
print("Status:", response.status_code)
print("Response:", response.json())
