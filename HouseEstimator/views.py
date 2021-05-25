from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import House
from .serializers import HouseSerializer
from User.models import UserHistory, UserWallet, UserTransactions
import pickle
import zipfile
from datetime import datetime
from datetime import date
import jdatetime
import numpy as np
from rest_framework.permissions import IsAuthenticated


with zipfile.ZipFile("HouseEstimator/Model/houseestimator.zip", "r") as zip_ref:
    zip_ref.extractall("HouseEstimator/Model")

with open('HouseEstimator/Model/lableencoder.pkl', 'rb') as file:
    L_encoder = pickle.load(file)

with open('HouseEstimator/Model/houseestimator.pkl', 'rb') as file:
    pickled_model = pickle.load(file)


class Houseview(viewsets.ModelViewSet):
    serializer_class = HouseSerializer
    queryset = House.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        return Response({"area": "", "room": "", "year": "", "location": ""}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = HouseSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        user_wallet = UserWallet.objects.get(user=user)

        if user_wallet.trial <= 0:
            if user_wallet.amount < 300:
                return Response({"massage": "please charge your account for using services"},
                                status=status.HTTP_402_PAYMENT_REQUIRED)

        headers = self.get_success_headers(serializer.data)
        area = serializer.data.get("area")
        room = serializer.data.get("room")
        year = serializer.data.get("year")
        location = serializer.data.get("location")
        location = f'{location} '

        L_encoder.fit(list(location))
        loc = L_encoder.transform(list(location))[0]

        price = pickled_model.predict(np.array([loc, area, room, year]).reshape(1, -1))
        price = int(price[0])
        # price = 3000000000

        qs = list(House.objects.filter(location=location).values())
        data = {
            "currenthouse": serializer.data,
            "price": price,
            "houses": qs,
        }
        # date_ = today.strftime("%d/%m/%Y")
        # jdate = jdatetime.datetime.now()
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        date_time = jdatetime.datetime.now().strftime("%d/%m/%Y")
        time = f"{date_time}  {current_time}"
        history_data = f"area: {area}, room: {room}, year: {year}, location: {location}"
        history = UserHistory(user=user, model="سرویس خانه", data=history_data, price=price, date=time)
        history.save()
        if user_wallet.trial > 0:
            user_wallet.trial -= 1
        else:
            user_wallet.amount -= 300
        user_wallet.save()

        transaction = UserTransactions(user=user, type="استفاده از سرویس",
                                       service="تخمین قیمت خانه", amount=300, date=time)
        transaction.save()

        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    # house = House(area=area, location=location, room=room, year=year, price=price)
    # house.save()

    '''
    def list(self, request):
        pass

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass
    '''
