import json
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from .models import House
from .serializers import HouseSerializer


class HouseEstimatorTest(APITestCase):
    def setUp(self):
        self.valid = {"area": 120, "location": ' فرشته', "room": 2, "year": 1390}
        self.invalid = {"area": "", "location": ' فرشته', "room": 2, "year": 1390}
        self.invalid2 = {"area": 120, "location": ' فرشته', "room": 2}

    def test_valid_data(self):
        response = self.client.post("/HEstimator/House/",
                                    data=json.dumps(self.valid), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_data(self):
        response = self.client.post("/HEstimator/House/",
                                    data=json.dumps(self.invalid), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_data2(self):
        response = self.client.post("/HEstimator/House/",
                                    data=json.dumps(self.invalid2), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_main_page(self):
        response = self.client.get("/HEstimator/House/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
