from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from authentication.models import User

@api_view(['POST'])
def check_username_availability(request):
    username = request.data.get("username")
    
    if username and User.objects.filter(username=username).exists():
        return Response({"detail": "Ushbu username allaqachon mavjud."}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"detail": "Ushbu username allaqachon mavjud."}, status=status.HTTP_200_OK)