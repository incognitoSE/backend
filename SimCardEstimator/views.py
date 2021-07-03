from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Simcard
from User.models import UserHistory, UserWallet, UserTransactions
from rest_framework.permissions import IsAuthenticated
from .serializers import SimcardSerializer
import jdatetime
import pickle
import zipfile
import os
import pytz
import re
import numpy as np
from datetime import datetime
import base64


yesorno = {
    'بله': 1,
    'خیر': 0
}

yesorno_rev = {
    1: 'بله',
    0: 'خیر'
}


def explore(addresss):
    type_ = ["jpg", "png"]
    with open(os.path.join(addresss, 'text.txt'), 'r') as f:
        content = f.read()
    data = {'mainText': content,
            'imagesAndTexts': []}
    contents = os.walk(addresss)
    for each in contents:
        for files in each[2]:
            try:
                if files.split('.')[1].lower() in type_:
                    with open(os.path.join(each[0], files), 'rb') as f:
                        img = base64.b64encode(f.read())
                        num = int(re.findall('[0-9]', files)[0])
                        with open(os.path.join(addresss, f'text{num}.txt'), 'r') as fa:
                            cont = fa.read()
                        data['imagesAndTexts'].append(
                            {
                                'image': img,
                                'text': cont
                            }
                        )

            except IndexError:
                continue

    return data


# with zipfile.ZipFile("SimCardEstimator/Model/simestimator.zip", "r") as zip_ref:
#     zip_ref.extractall("SimCardEstimator/Model")

# with open('SimCardEstimator/Model/sim_lableencoder.pkl', 'rb') as file:
#     L_encoder = pickle.load(file)

# with open('SimCardEstimator/Model/simestimator.pkl', 'rb') as file:
#     pickled_model = pickle.load(file)


images = explore('SimCardEstimator/Model/')


class SimcardView(viewsets.ModelViewSet):
    serializer_class = SimcardSerializer
    queryset = Simcard.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        return Response(images, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = SimcardSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        boolean = True
        user = request.user
        user_wallet = UserWallet.objects.get(user=user)
        if user_wallet.trial <= 0:
            boolean = False
            if user_wallet.amount < 300:
                return Response({"massage": "please charge your account for using services"},
                                status=status.HTTP_402_PAYMENT_REQUIRED)

        headers = self.get_success_headers(serializer.data)
        number = serializer.data.get("number")
        rond = serializer.data.get("rond")
        stock = serializer.data.get("stock")
        daemi = serializer.data.get("daemi")

        L_encoder.fit(list(rond))
        rond_ = L_encoder.transform(list(rond))[0]

        L_encoder.fit(list(stock))
        stock_ = L_encoder.transform(list(stock))[0]

        L_encoder.fit(list(daemi))
        daemi_ = L_encoder.transform(list(daemi))[0]

        # price = pickled_model.predict(np.array([number, rond_, stock_, daemi_]).reshape(1, -1))
        price = [550]
        price = int(price[0])

        qs = list(Simcard.objects.filter(rond=yesorno[rond],
                                         daemi=yesorno[daemi],
                                         price__lte=price+150000,
                                         price__gte=price-200000).values())

        for element in qs:
            element['rond'] = yesorno_rev[element['rond']]
            element['stock'] = yesorno_rev[element['stock']]
            element['daemi'] = yesorno_rev[element['daemi']]

        data = {
            "currentsimcard": serializer.data,
            "price": price,
            "simcards": qs,
        }

        now = datetime.now(pytz.timezone('Asia/Tehran'))
        current_time = now.strftime("%H:%M:%S")
        date_time = jdatetime.datetime.now().strftime("%Y/%m/%d")
        time = f"{date_time}  {current_time}"

        history_data = f"number: {number}, rond: {rond}, stock: {stock}, daemi: {daemi}"
        history = UserHistory(user=user, model="سرویس سیم‌کارت", data=history_data, price=price, date=time)
        history.save()

        if user_wallet.trial > 0:
            user_wallet.trial -= 1
        else:
            user_wallet.amount -= 300
        user_wallet.save()

        if boolean:
            transaction = UserTransactions(user=user, type="استفاده از سرویس",
                                           service="تخمین قیمت سیم‌کارت", amount=0, date=time)
            transaction.save()

        else:
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