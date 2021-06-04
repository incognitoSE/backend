from rest_framework.test import APITestCase
from rest_framework import status


class HouseEstimatorTest(APITestCase):
    def setUp(self):
        self.valid = {"area": 120, "room": 2, "year": 1390, "location": "جیحون"}
        self.invalid = {"area": "", "location": 'فرشته', "room": 2, "year": 1390}
        self.invalid2 = {"area": 120, "location": 'فرشته', "room": 2}

        self.user_data = {
            "email": "t@gmail.com",
            "name": "test",
            "password": "3625"
        }
        self.client.post('/User/profile/', self.user_data)  # user created
        self.user_acc = self.client.post('/User/login/', {
            "email": self.user_data.get("email"),
            "password": self.user_data.get("password")
        }).data.get('access')  # get access_token for authorization
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_acc}')

    def test_valid_data(self):
        response = self.client.post("/HEstimator/House/", self.valid)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_data(self):
        response = self.client.post("/HEstimator/House/", self.invalid)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_data2(self):
        response = self.client.post("/HEstimator/House/", self.invalid2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_price_data(self):
        price = self.client.post("/HEstimator/House/", self.valid).data.get("price")
        self.assertIsInstance(price, int)

    def test_houses_data(self):
        houses = self.client.post("/HEstimator/House/", self.valid).data.get("houses")
        self.assertIsInstance(houses, list)

    def test_current_data(self):
        our_data = self.client.post("/HEstimator/House/", self.valid)

        room = our_data.data.get("currenthouse").get("room")
        self.assertEqual(room, self.valid.get("room"))
        location = our_data.data.get("currenthouse").get("location")
        self.assertEqual(location, self.valid.get("location"))
        year = our_data.data.get("currenthouse").get("year")
        self.assertEqual(year, self.valid.get("year"))
        area = our_data.data.get("currenthouse").get("area")
        self.assertEqual(area, self.valid.get("area"))

    def test_main_page(self):
        response = self.client.get("/HEstimator/House/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
