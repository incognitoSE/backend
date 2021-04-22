from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import House
from .serializers import HouseSerializer
import pickle


class Houseview(viewsets.ModelViewSet):

    serializer_class = HouseSerializer
    queryset = House.objects.all()

    # not main
    def create(self, request, *args, **kwargs):

        serializer = HouseSerializer(data=request.data)

        if serializer.is_valid():
            with open('Model/houseestimator.pkl', 'rb') as file:
                picled_model = pickle.load(file)

            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            area = serializer.data.get("area")

            return Response(area, status=status.HTTP_201_CREATED, headers=headers)
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