from cryptography.fernet import Fernet


key = Fernet.generate_key()
print(f"Сохраните этот ключ для использования: {key.decode()}")
