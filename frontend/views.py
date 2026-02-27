from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from hospital.models import Appointment, Doctor, Patient

class IndexView(TemplateView):
    template_name = 'frontend/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hero_image'] = 'static/frontend/img/hero.png'
        return context

from django.contrib.auth import authenticate, login
from django.contrib import messages

class LoginView(TemplateView):
    template_name = 'frontend/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
            return self.get(request, *args, **kwargs)

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'frontend/dashboard.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.role == 'DOCTOR':
            context['appointments'] = Appointment.objects.filter(doctor__user=user).select_related('patient__user')
            context['stat_label'] = 'Total Patients'
            from hospital.models import Patient
            context['stat_count'] = Patient.objects.filter(appointments__doctor__user=user).distinct().count()
        elif user.role == 'PATIENT':
            context['appointments'] = Appointment.objects.filter(patient__user=user).select_related('doctor__user')
            context['stat_label'] = 'Available Doctors'
            context['stat_count'] = Doctor.objects.count()
            context['all_doctors'] = Doctor.objects.select_related('user').all()
        else:
            context['appointments'] = Appointment.objects.all().select_related('doctor__user', 'patient__user')
        return context

class BookAppointmentView(LoginRequiredMixin, TemplateView):
    template_name = 'frontend/book_appointment.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['doctors'] = Doctor.objects.select_related('user').all()
        context['doctor_id'] = self.request.GET.get('doctor_id')
        return context

class RegisterView(TemplateView):
    template_name = 'frontend/register.html'

from django.contrib.auth import logout
from django.views import View

class LogoutUserView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('index')

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('index')
