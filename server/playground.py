from cryptography.fernet import Fernet

k = Fernet.generate_key()
print(k)