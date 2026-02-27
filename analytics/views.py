from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache
from django.db.models import Count, Sum
from hospital.models import Appointment, Doctor, Patient
from billing.models import Invoice
from users.permissions import IsAdmin

class DashboardStatsView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        cache_key = 'dashboard_stats'
        stats = cache.get(cache_key)

        if not stats:
            total_appointments = Appointment.objects.count()
            total_doctors = Doctor.objects.count()
            total_patients = Patient.objects.count()
            total_revenue = Invoice.objects.filter(status='PAID').aggregate(Sum('total_amount'))['total_amount__sum'] or 0

            stats = {
                'total_appointments': total_appointments,
                'total_doctors': total_doctors,
                'total_patients': total_patients,
                'total_revenue': float(total_revenue),
            }
            # Cache for 15 minutes
            cache.set(cache_key, stats, 15 * 60)

        return Response(stats)
