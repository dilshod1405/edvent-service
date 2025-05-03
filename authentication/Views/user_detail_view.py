from authentication.serializers.user_detail_serializer import UserDetailSerializer
from rest_framework import generics, permissions
from authentication.models import User


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]