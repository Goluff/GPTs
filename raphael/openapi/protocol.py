from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
import base64

# Clé publique chargée depuis le code GPT
public_key_pem = """-----BEGIN PUBLIC KEY-----
... ta clé ici ...
-----END PUBLIC KEY-----"""

public_key = serialization.load_pem_public_key(
    public_key_pem.encode(),
    backend=default_backend()
)

# Donnée à encrypter
data = b"journal entry: Priscilla felt anxious this morning."

# Encryption
encrypted = public_key.encrypt(
    data,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Encodage base64 pour envoi via API
encrypted_b64 = base64.b64encode(encrypted).decode("utf-8")
