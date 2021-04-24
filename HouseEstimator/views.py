from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import House
from .serializers import HouseSerializer
import pickle
import numpy as np


class Houseview(viewsets.ModelViewSet):

    def list(self, request, *args, **kwargs):
        return Response({"Message": "Every thing is Ok"}, status=status.HTTP_201_CREATED)


    serializer_class = HouseSerializer
    queryset = House.objects.all()

    # not main
    def create(self, request, *args, **kwargs):

        serializer = HouseSerializer(data=request.data)

        if serializer.is_valid():
            with open('Model/houseestimator.pkl', 'rb') as file:
                pickled_model = pickle.load(file)

            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            location = serializer.data.get("location")
            area = serializer.data.get("area")
            room = serializer.data.get("room")
            yaer = serializer.data.get("yaer")
            price = pickled_model.predict(np.array([location, area, room, yaer]).reshape(1, -1))
            house = House(area=area, location=location, room=room, yaer=yaer, price=price)

            house.save()

            return Response({"price": price}, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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