from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import viewsets
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authentication import TokenAuthentication
from django.contrib import auth
import jwt
from .serializers import UserProfileSerializer
from .models import UserProfile
from .permissions import UpdatingProfilePermission
from django.conf import settings


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (UpdatingProfilePermission,)


class LoginView(GenericAPIView):
    serializer_class = AuthTokenSerializer
    permission_classes = UpdatingProfilePermission

    def post(self, requset):
        data = requset.data

        username = data.get("username").lower()

        password = data.get("password")

        user = auth.authenticate(username=username, password=password)
        if user:
            serializer = UserProfileSerializer(user)
            auth_token = jwt.encode({'username': user.email}, settings.JWT_SECRET_KEY)

            data = {
                "user": serializer.data,
                "token": auth_token
            }
            return Response(data, status=status.HTTP_200_OK)

        return Response({'detail': 'invalid credentials or may have not signed up yet'},
                        status=status.HTTP_401_UNAUTHORIZED)