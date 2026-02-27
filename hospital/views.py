from rest_framework import viewsets, permissions
from .models import Doctor, Patient, Appointment, Prescription
from .serializers import DoctorSerializer, PatientSerializer, AppointmentSerializer, PrescriptionSerializer
from users.permissions import IsAdmin, IsDoctor, IsPatient, IsDoctorOrAdmin

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.select_related('user').all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAdmin] 

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.select_related('user').all()
    serializer_class = PatientSerializer
    
    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.AllowAny()]
        return [IsDoctorOrAdmin()]

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        user = self.request.user
        base_queryset = Appointment.objects.select_related('doctor__user', 'patient__user')
        if user.role == 'ADMIN':
            return base_queryset.all()
        elif user.role == 'DOCTOR':
            return base_queryset.filter(doctor__user=user)
        elif user.role == 'PATIENT':
            return base_queryset.filter(patient__user=user)
        return Appointment.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if user.role == 'PATIENT':
            serializer.save(patient=user.patient_profile)
        else:
            serializer.save()

class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsDoctorOrAdmin]
