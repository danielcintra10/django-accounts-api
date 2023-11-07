from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from api.serializers import UserSerializer, MyTokenObtainPairSerializer
from .models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from .permissions import IsAuthenticatedAndIsOwner


# Create your views here.

class ListCreateUser(ListCreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [permissions.IsAdminUser, ]
        elif self.request.method == 'POST':
            self.permission_classes = [permissions.AllowAny, ]
        else:
            self.permission_classes = [permissions.IsAdminUser, ]
        return super().get_permissions()


class RetrieveUpdateDestroyUser(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    lookup_field = 'id'

    def get_permissions(self):
        if self.request.method in ['GET', 'PUT', 'PATCH']:
            self.permission_classes = [permissions.IsAdminUser | IsAuthenticatedAndIsOwner]
        elif self.request.method == 'DELETE':
            self.permission_classes = [permissions.IsAdminUser, ]
        else:
            self.permission_classes = [permissions.IsAdminUser, ]
        return super().get_permissions()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response({'Response': 'Se eliminó al usuario de forma correcta'}, status=status.HTTP_200_OK)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny, ]
