from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Simcard
from User.models import UserHistory, UserWallet, UserTransactions
from rest_framework.permissions import IsAuthenticated
from .serializers import SimcardSerializer
import jdatetime
from datetime import datetime
import base64


images = []


yesorno = {
    'بله': 1,
    'خیر': 0
}

yesorno_rev = {
    1: 'بله',
    0: 'خیر'
}


# with open('SimCardEstimator/Model/Screenshot from 2021-06-02 14-25-00.png', "rb") as f:
#     # images.append(f.read().decode('utf8', 'ignore'))
#     images.append(base64.b64encode(f.read()))
#     # img = f"{bytes(f.read())}"
#
# with open('SimCardEstimator/Model/Screenshot from 2021-05-29 20-36-49.png', "rb") as f:
#     # images.append(f.read().decode('utf8', 'ignore'))
#     images.append(base64.b64encode(f.read()))
#     # img = f"{bytes(f.read())}"


class SimcardView(viewsets.ModelViewSet):
    serializer_class = SimcardSerializer
    queryset = Simcard.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        data = {
            "images": images
        }
        return Response(data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = SimcardSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        user_wallet = UserWallet.objects.get(user=user)
        if user_wallet.trial <= 0:
            if user_wallet.amount < 300:
                return Response({"massage": "please charge your account for using services"},
                                status=status.HTTP_402_PAYMENT_REQUIRED)

        headers = self.get_success_headers(serializer.data)
        number = serializer.data.get("number")
        rond = serializer.data.get("rond")
        stock = serializer.data.get("stock")
        daemi = serializer.data.get("daemi")

        qs = list(Simcard.objects.filter(rond=yesorno[rond], daemi=yesorno[daemi]).values())
        for element in qs:
            element['rond'] = yesorno_rev[element['rond']]
            element['stock'] = yesorno_rev[element['stock']]
            element['daemi'] = yesorno_rev[element['daemi']]

        # TODO: price is fake
        price = 15000
        data = {
            "currentsimcard": serializer.data,
            "price": price,
            "simcards": qs,
        }

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        date_time = jdatetime.datetime.now().strftime("%d/%m/%Y")
        time = f"{date_time}  {current_time}"

        history_data = f"number: {number}, rond: {rond}, stock: {stock}, daemi: {daemi}"
        history = UserHistory(user=user, model="سرویس سیم‌کارت", data=history_data, price=price, date=time)
        history.save()

        if user_wallet.trial > 0:
            user_wallet.trial -= 1
        else:
            user_wallet.amount -= 300
        user_wallet.save()

        transaction = UserTransactions(user=user, type="استفاده از سرویس",
                                       service="تخمین قیمت سیم‌کارت", amount=300, date=time)
        transaction.save()

        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

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