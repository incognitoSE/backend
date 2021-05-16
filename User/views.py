from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import viewsets
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authentication import TokenAuthentication
from django.contrib import auth
import jwt
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer, UserhistorySerializer
from .models import UserProfile, UserHistory
from .permissions import UpdatingProfilePermission
from django.conf import settings


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (UpdatingProfilePermission,)


class UserSignup (APIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    
    def post (self, *args, **kwargs):
        data = self.request.data
        try:
            user = UserProfile(
                        email=data['email'],
                        name=data['name']
                    )
            user.set_password(data['password'])
            user.save()
            # new_user = UserProfile.objects.create_user(email=data['snn'], password=pass_)
            refresh = RefreshToken.for_user(user)
            return Response(data={
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "message": "User successfuly inserted!"
            }, status=status.HTTP_201_CREATED)

        except Exception as exc:
            return Response(data={
                "message": str(exc)
                }, status=status.HTTP_400_BAD_REQUEST)


class UserHistoryViewset(viewsets.ModelViewSet):
    serializer_class = UserhistorySerializer
    queryset = UserHistory.objects.all()
    # TODO: check authentication
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        qs = list(UserHistory.objects.filter(user=self.request.user).values())

        return Response(qs, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        return Response({"Message: Nothing to post"}, status=status.HTTP_201_CREATED)


# class LoginView(GenericAPIView):
#     serializer_class = AuthTokenSerializer
#
#     def post(self, requset):
#         data = requset.data
#         username = data.get("username").lower()
#         password = data.get("password")
#
#         user = auth.authenticate(username=username, password=password)
#
#         if user:
#             serializer = UserProfileSerializer(user)
#             auth_token = jwt.encode({'username': user.email}, "SMT")
#
#             data = {
#                 "user": serializer.data,
#                 "token": auth_token
#             }
#             return Response(data, status=status.HTTP_200_OK)
#
#         return Response({'detail': 'invalid credentials or may have not signed up yet'},
#                         status=status.HTTP_401_UNAUTHORIZED)