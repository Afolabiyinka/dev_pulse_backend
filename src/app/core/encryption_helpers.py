import os
from app.core.config import envVariables
from cryptography.fernet import Fernet


key = envVariables.github_token_encryption_key
fernet = Fernet(key.encode())


def encrypt_token(token: str) -> str:
    return fernet.encrypt(token.encode()).decode()


def decrypt_token(encrypted_token: str) -> str:
    return fernet.decrypt(encrypted_token.encode()).decode()