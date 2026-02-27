from rest_framework import viewsets
from .models import Invoice
from .serializers import InvoiceSerializer
from users.permissions import IsAdmin, IsPatient

class InvoiceViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        user = self.request.user
        base_queryset = Invoice.objects.select_related('appointment__patient__user', 'appointment__doctor__user')
        if user.role == 'ADMIN':
            return base_queryset.all()
        elif user.role == 'PATIENT':
            return base_queryset.filter(appointment__patient__user=user)
        return Invoice.objects.none()
