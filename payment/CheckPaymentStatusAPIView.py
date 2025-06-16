from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Transaction
from education.models import Module, FoundationCourse, Tariff

class CheckPaymentStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        module_id = request.query_params.get('module_id')
        course_id = request.query_params.get('course_id')
        tariff_id = request.query_params.get('tariff_id')

        if not module_id and not course_id and not tariff_id:
            return Response({"error": "Either module_id, course_id, or tariff_id is required"}, status=400)

        if module_id:
            try:
                module = Module.objects.get(id=module_id)
            except Module.DoesNotExist:
                return Response({"error": "Module not found"}, status=404)

            transaction = Transaction.objects.filter(user=request.user, module=module, state='paid').first()
            return Response({"status": "paid" if transaction else "not_paid", "module": module.title})

        if course_id:
            try:
                course = FoundationCourse.objects.get(id=course_id)
            except FoundationCourse.DoesNotExist:
                return Response({"error": "Course not found"}, status=404)

            transaction = Transaction.objects.filter(user=request.user, course=course, state='paid').first()
            return Response({"status": "paid" if transaction else "not_paid", "course": course.title})

        if tariff_id:
            try:
                tariff = Tariff.objects.get(id=tariff_id)
            except Tariff.DoesNotExist:
                return Response({"error": "Tariff not found"}, status=404)

            transaction = Transaction.objects.filter(user=request.user, tariff=tariff, state='paid').first()
            return Response({"status": "paid" if transaction else "not_paid", "tariff": tariff.title})
