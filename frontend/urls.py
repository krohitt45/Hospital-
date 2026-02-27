from django.urls import path
from .views import IndexView, LoginView, RegisterView, DashboardView, BookAppointmentView, LogoutUserView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('book/', BookAppointmentView.as_view(), name='book_appointment'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
]
