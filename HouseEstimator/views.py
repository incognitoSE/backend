from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import House
from .serializers import HouseSerializer
import pickle
import numpy as np
from rest_framework import permissions


with open('HouseEstimator/Model/lableencoder.pkl', 'rb') as file:
    L_encoder = pickle.load(file)

with open('HouseEstimator/Model/houseestimator.pkl', 'rb') as file:
    pickled_model = pickle.load(file)


class Houseview(viewsets.ModelViewSet):
    serializer_class = HouseSerializer
    queryset = House.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        return Response({"area": "", "room": "", "year": "", "location": ""}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = HouseSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
            "houses": len(qs),
        }

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
