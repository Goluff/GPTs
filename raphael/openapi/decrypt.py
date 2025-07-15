import base64
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend

# Chargement de ta clé privée
with open("private_key.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,  # Si la clé est protégée, ajoute le mot de passe ici
        backend=default_backend()
    )

def decrypt_b64_message(encrypted_b64):
    encrypted_bytes = base64.b64decode(encrypted_b64)
    decrypted = private_key.decrypt(
        encrypted_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted.decode("utf-8")

# Exemple d’usage :
if __name__ == "__main__":
    # Message chiffré reçu par GPT (encodé en base64)
    b64_input = input("Message base64 à déchiffrer : ").strip()
    print("Déchiffré :", decrypt_b64_message(b64_input))
