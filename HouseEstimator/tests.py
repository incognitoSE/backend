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
        self.valid = {"area": 120, "room": 2, "year": 1390, "location": 'فرشته'}
        self.invalid = {"area": "", "location": ' فرشته', "room": 2, "year": 1390}
        self.invalid2 = {"area": 120, "location": ' فرشته', "room": 2}

    def test_valid_data(self):
        response = self.client.Post("/HEstimator/House/")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_data(self):
        response = self.client.Post("/HEstimator/House/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_data2(self):
        response = self.client.Post("/HEstimator/House/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_price_data(self):
        price = self.client.Post("/HEstimator/House/").data.get("price")
        self.assertIsInstance(price, int)

    def test_houses_data(self):
        houses = self.client.Post("/HEstimator/House/").data.get("houses")
        self.assertIsInstance(houses, list)

    def test_current_data(self):
        room = self.client.Post("/HEstimator/House/").data.get("currenthouse").get("room")
        location = self.client.Post("/HEstimator/House/").data.get("currenthouse").get("location")
        area = self.client.Post("/HEstimator/House/").data.get("currenthouse").get("area")
        year = self.client.Post("/HEstimator/House/").data.get("currenthouse").get("year")
        self.assertEqual(room, self.valid.get("room"))
        self.assertEqual(year, self.valid.get("year"))
        self.assertEqual(location, self.valid.get("location"))
        self.assertEqual(area, self.valid.get("area"))

    def test_main_page(self):
        response = self.client.get("/HEstimator/House/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
