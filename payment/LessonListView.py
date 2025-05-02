from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from education.models import Lesson
from education.serializers import LessonSerializer
from payment.CheckPaymentStatusAPIView import CheckPaymentStatusAPIView
from rest_framework.permissions import IsAuthenticated

class LessonListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        module_id = request.query_params.get('module_id')

        if not module_id:
            return Response({"error": "module_id is required"}, status=400)

        # Check if the user has paid for the module
        payment_status_response = CheckPaymentStatusAPIView().get(request)
        if payment_status_response.data.get('status') != 'paid':
            raise PermissionDenied("You need to pay for the module to access its lessons.")

        # Return lessons for the module
        lessons = Lesson.objects.filter(module_id=module_id)
        # Serialize and return lessons
        lesson_serializer = LessonSerializer(lessons, many=True)
        return Response(lesson_serializer.data)
