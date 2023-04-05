from rest_framework.decorators import api_view
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from .serializers import *


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
        print(serializer.items())
        for key, value in serializer.items():
            data[key] = value
        return data



class MyToken(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(["GET"])
@permission_classes([IsAdminUser])
def index(request):
    return Response({"message": "Hello, world!"})


@api_view(["POST"])
def register(request):
    if request.method == "POST":    
        data = request.data
        print(data)
        try:
            user = User.objects.create(
                username=data["email"],
                email=data["email"],
                password=make_password(data["password"])
            )
            serializer = UserSerializerWithToken(user, many=False)
            return Response(serializer.data)
        except:
            message = {"detail": "User with this email already exists"}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
 
