from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Car
from rest_framework.permissions import IsAuthenticated
from .serializers import CarSerializer
import pickle
import zipfile
from User.models import UserHistory, UserWallet, UserTransactions
import jdatetime
import os
import re
from datetime import datetime
import numpy as np
import base64


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


with zipfile.ZipFile("CarEstimator/Model/carestimator.zip", "r") as zip_ref:
    zip_ref.extractall("CarEstimator/Model")

with open('CarEstimator/Model/car_lableencoder.pkl', 'rb') as file:
    L_encoder = pickle.load(file)

with open('CarEstimator/Model/carestimator.pkl', 'rb') as file:
    pickled_model = pickle.load(file)


body_status_dict = {
     "بدون رنگ": 1,
     "صافکاری بدون رنگ": 14,
     "یک لکه رنگ": 2,
     "دو لکه رنگ": 3,
     "چند لکه رنگ": 4,
     "گلگیر لکه رنگ": 5,
     "گلگیر تعویض": 6,
     "یک درب رنگ": 7,
     "دو درب رنگ": 8,
     "درب تعویض": 9,
     "کاپوت رنگ": 10,
     "کاپوت تعویض": 11,
     "دور رنگ": 12,
     "کامل رنگ": 13,
     "تصادفی": 15,
     "اتاق تعویض": 16,
     "سوخته": 17,
     "اوراقی": 18
}

body_status_rev_dict = {
     "1": "بدون رنگ",
     "14": "صافکاری بدون رنگ",
     "2": "یک لکه رنگ",
     "3": "دو لکه رنگ",
     "4": "چند لکه رنگ",
     "5": "گلگیر لکه رنگ",
     "6": "گلگیر تعویض",
     "7": "یک درب رنگ",
     "8": "دو درب رنگ",
     "9": "درب تعویض",
     "10": "کاپوت رنگ",
     "11": "کاپوت تعویض",
     "12": "دور رنگ",
     "13": "کامل رنگ",
     "15": "تصادفی",
     "16": "اتاق تعویض",
     "17": "سوخته",
     "18": "اوراقی"
}

images = explore('CarEstimator/Model/')


class CarView(viewsets.ModelViewSet):
    serializer_class = CarSerializer
    queryset = Car.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        return Response(images, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = CarSerializer(data=request.data)
        boolean = True
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        user_wallet = UserWallet.objects.get(user=user)

        if user_wallet.trial <= 0:
            boolean = False
            if user_wallet.amount < 300:
                return Response({"massage": "please charge your account for using services"},
                                status=status.HTTP_402_PAYMENT_REQUIRED)

        headers = self.get_success_headers(serializer.data)
        brand = serializer.data.get("brand")
        model = serializer.data.get("model")
        mileage = serializer.data.get("mileage")
        year = serializer.data.get("year")
        body_status = serializer.data.get("body_status")

        L_encoder.fit(list(brand))
        brand_ = L_encoder.transform(list(brand))[0]

        L_encoder.fit(list(model))
        model_ = L_encoder.transform(list(model))[0]

        body_status_ = body_status_dict[body_status]

        price = pickled_model.predict(np.array([brand_, model_, mileage, year, body_status_]).reshape(1, -1))
        price = int(price[0])

        qs = list(Car.objects.filter(brand=brand,
                                     model=model,
                                     year__gte=year - 4,
                                     mileage__lte=mileage + 5000,
                                     price__lte=price + 300000000,
                                     price__gte=price - 400000000
                                     ).values())

        for element in qs:
            element['body_status'] = body_status_rev_dict[element['body_status']]

        data = {
            "currentcar": serializer.data,
            "price": price,
            "cars": qs,
        }

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        date_time = jdatetime.datetime.now().strftime("%d/%m/%Y")
        time = f"{date_time}  {current_time}"
        history_data = f"brand: {brand}, model: {model}, mileage: {mileage}, year: {year}, body_status: {body_status}"
        history = UserHistory(user=user, model="سرویس ماشین", data=history_data, price=price, date=time)
        history.save()
        if user_wallet.trial > 0:
            user_wallet.trial -= 1
        else:
            user_wallet.amount -= 300
        user_wallet.save()

        if boolean:
            transaction = UserTransactions(user=user, type="استفاده از سرویس",
                                           service="تخمین قیمت ماشین", amount="رایگان", date=time)
            transaction.save()

        else:
            transaction = UserTransactions(user=user, type="استفاده از سرویس",
                                           service="تخمین قیمت ماشین", amount=300, date=time)
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