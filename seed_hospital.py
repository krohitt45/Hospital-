import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from hospital.models import Doctor, Patient, Appointment
from django.utils import timezone

User = get_user_model()

def seed_data():
    print("Seeding Hospital Data...")
    
    # 1. Create Doctors
    specializations = ['Cardiology', 'Neurology', 'Pediatrics', 'Orthopedics', 'Dermatology']
    for i in range(1, 6):
        email = f"doctor{i}@medicore.com"
        username = f"doctor{i}"
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username,
                email=email,
                password="password123",
                first_name=f"Dr.",
                last_name=f"Specialist {i}",
                role='DOCTOR'
            )
            Doctor.objects.create(
                user=user,
                specialization=random.choice(specializations),
                experience_years=random.randint(5, 20),
                consultation_fee=random.randint(500, 2000),
                bio=f"Highly experienced specialist in {random.choice(specializations)}."
            )
            print(f"Created Doctor: {username}")

    # 2. Create Patients
    for i in range(1, 6):
        email = f"patient{i}@example.com"
        username = f"patient{i}"
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username,
                email=email,
                password="password123",
                first_name=f"Patient",
                last_name=f"User {i}",
                role='PATIENT'
            )
            Patient.objects.create(
                user=user,
                date_of_birth="1990-01-01",
                address=f"Flat {i}, Medi Street, City",
                blood_group=random.choice(['A+', 'B+', 'O+', 'AB+'])
            )
            print(f"Created Patient: {username}")

    print("Seeding Complete!")

if __name__ == "__main__":
    seed_data()
