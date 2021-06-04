from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer, UserhistorySerializer, UserWalletSerializer\
    , UserTransactionsSerializer, NotificationsSerializer, UserPasswordSerializer
from .models import UserProfile, UserHistory, UserWallet, UserTransactions, Notifications
from .permissions import UpdatingProfilePermission
import jdatetime
from datetime import datetime


class UserSignup(APIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

    def post(self, *args, **kwargs):
        data = self.request.data
        try:
            user = UserProfile(
                email=data['email'],
                name=data['name']
            )
            user.set_password(data['password'])
            user.save()
            wallet = UserWallet(user=user)
            wallet.save()
            # new_user = UserProfile.objects.create_user(email=data['snn'], password=pass_)
            refresh = RefreshToken.for_user(user)
            return Response(data={
                "name": data['name'],
                "email": data['email'],
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "message": "User successfuly registerd :)"
            }, status=status.HTTP_201_CREATED)

        except Exception as exc:
            return Response(data={
                "message": str(exc)
            }, status=status.HTTP_400_BAD_REQUEST)


class UserHistoryViewset(viewsets.ModelViewSet):
    serializer_class = UserhistorySerializer
    queryset = UserHistory.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        qs = list(UserHistory.objects.filter(user=self.request.user).values())
        return Response(qs, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        return Response({"Message: Nothing to post"}, status=status.HTTP_201_CREATED)


class UserTransactionsViewset(viewsets.ModelViewSet):
    serializer_class = UserTransactionsSerializer
    queryset = UserTransactions.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        qs = list(UserTransactions.objects.filter(user=self.request.user).values())
        return Response(qs, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        return Response({"Message: Nothing to post"}, status=status.HTTP_201_CREATED)


class UserWalletViewset(viewsets.ModelViewSet):
    serializer_class = UserWalletSerializer
    queryset = UserWallet.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user_wallet = UserWallet.objects.get(user=request.user)
        data = {
            "current_amount": user_wallet.amount
        }
        return Response(data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        user = request.user
        user_wallet = UserWallet.objects.get(user=user)
        serializer = UserWalletSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        amount = serializer.data.get("amount")

        user_wallet.amount += amount
        user_wallet.save()

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        date_time = jdatetime.datetime.now().strftime("%d/%m/%Y")
        time = f"{date_time}  {current_time}"
        transaction = UserTransactions(user=user, type="افزایش اعتبار", amount=amount, date=time)
        transaction.save()

        data = {
            "message": f"{amount} charged",
            "current_amount": user_wallet.amount
        }
        return Response(data, status=status.HTTP_200_OK, headers=headers)


class NotificationsViewset(viewsets.ModelViewSet):
    serializer_class = NotificationsSerializer
    queryset = Notifications.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        qs = list(Notifications.objects.all().values())
        return Response(qs, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        return Response({"Message": "Nothing to post"}, status=status.HTTP_201_CREATED)


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserPasswordSerializer
    queryset = UserProfile.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        data = {
            "message": "Nothing"
        }

        return Response(data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        # user = request.user
        # serializer = UserPasswordSerializer(data=request.data)
        #
        # if serializer.is_valid():
        #     if not user.check_password(serializer.data.get('old_password')):
        #         return Response({'old_password': ['Wrong password.']},
        #                         status=status.HTTP_400_BAD_REQUEST)
        #
        #     user.set_password(serializer.data.get('new_password'))
        #     user.save()
        #     return Response({'status': 'password set'}, status=status.HTTP_200_OK)
        #
        # return Response(serializer.errors,
        #                 status=status.HTTP_400_BAD_REQUEST)

        serializer = UserPasswordSerializer(data=request.data)
        user = UserProfile.objects.get(id=request.user.id)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)

        user.set_password(serializer.data.get("password"))

        user.save()

        data = {
            "message": "password changed successfully"
        }
        return Response(data, status=status.HTTP_200_OK, headers=headers)


class UserStatsViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

    def list(self, request, *args, **kwargs):
        data = {
            "users": UserProfile.objects.all().count(),
            "history": UserHistory.objects.all().count()
        }

        return Response(data, status=status.HTTP_200_OK)

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
