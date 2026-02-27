from rest_framework import serializers
from .models import Doctor, Patient, Appointment, Prescription
from users.serializers import UserSerializer

class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Doctor
        fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Patient
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    doctor_name = serializers.ReadOnlyField(source='doctor.user.get_full_name')
    patient_name = serializers.ReadOnlyField(source='patient.user.get_full_name')

    class Meta:
        model = Appointment
        fields = '__all__'
        extra_kwargs = {'patient': {'required': False}}

class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'
