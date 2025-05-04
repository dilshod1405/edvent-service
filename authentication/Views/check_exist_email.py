from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from authentication.models import User

@api_view(['POST'])
def check_email_availability(request):
    email = request.data.get("email")
    
    if email and User.objects.filter(email=email).exists():
        return Response({"detail": "Ushbu email allaqachon mavjud."}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"detail": "Ushbu email allaqachon mavjud."}, status=status.HTTP_200_OK)