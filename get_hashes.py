from dotenv import load_dotenv
load_dotenv()  # Loads your DATABASE_URL so the DB engine doesn't crash

from app.auth.repository import AuthRepository

# Define the passwords we want to hash
provider_pass = "Provider@123"
patient_pass = "Patient@123"
frontdesk_pass = "Frontdesk@123"

# Generate the hashes using your repository logic
provider_hash = AuthRepository.hash_password(provider_pass)
patient_hash = AuthRepository.hash_password(patient_pass)
frontdesk_hash = AuthRepository.hash_password(frontdesk_pass)

print("-" * 30)
print(f"Provider Hash:\n{provider_hash}\n")
print(f"Patient Hash:\n{patient_hash}\n")
print(f"Front Desk Hash:\n{frontdesk_hash}")
print("-" * 30)
