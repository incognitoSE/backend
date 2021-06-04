from rest_framework.test import APITestCase
from rest_framework import status


class CarEstimatorTest(APITestCase):
    def setUp(self):
        self.valid = {"brand": "سمند", "model": "LX", "mileage": 80000, "year": 2017, "body_status": 'بدون رنگ'}
        self.invalid = {"brand": "سمند", "model": "LX", "mileage": 80000, "year": 2017}
        self.invalid2 = {"brand": "", "model": "LX", "mileage": 80000, "year": 2017, "body_status": 'بدون رنگ'}

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
        response = self.client.post("/CEstimator/Car/", self.valid)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_data(self):
        response = self.client.post("/CEstimator/Car/", self.invalid)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_data2(self):
        response = self.client.post("/CEstimator/Car/", self.invalid2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_price_data(self):
        price = self.client.post("/CEstimator/Car/", self.valid).data.get("price")
        self.assertIsInstance(price, int)

    def test_cars_data(self):
        cars = self.client.post("/CEstimator/Car/", self.valid).data.get("cars")
        self.assertIsInstance(cars, list)

    def test_current_data(self):
        our_data = self.client.post("/CEstimator/Car/", self.valid)

        brand = our_data.data.get("currentcar").get("brand")
        self.assertEqual(brand, self.valid.get("brand"))
        model = our_data.data.get("currentcar").get("model")
        self.assertEqual(model, self.valid.get("model"))
        mileage = our_data.data.get("currentcar").get("mileage")
        self.assertEqual(mileage, self.valid.get("mileage"))
        year = our_data.data.get("currentcar").get("year")
        self.assertEqual(year, self.valid.get("year"))
        body_status = our_data.data.get("currentcar").get("body_status")
        self.assertEqual(body_status, self.valid.get("body_status"))

    def test_main_page(self):
        response = self.client.get("/CEstimator/Car/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
