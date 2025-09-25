from cryptography.fernet import Fernet

# Generate a new key
key = Fernet.generate_key()

print("Your new encryption key is:")
print(key)
print("\nIMPORTANT: Copy this key (including the b'' part) and save it securely.")
