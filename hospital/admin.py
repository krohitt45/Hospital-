from django.contrib import admin
from .models import Doctor, Patient, Appointment, Prescription

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'experience_years', 'consultation_fee')
    search_fields = ('user__username', 'specialization')

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'blood_group')
    search_fields = ('user__username', 'blood_group')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'time', 'status')
    list_filter = ('status', 'date')
    search_fields = ('patient__user__username', 'doctor__user__username')

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'created_at')
    search_fields = ('appointment__patient__user__username',)
