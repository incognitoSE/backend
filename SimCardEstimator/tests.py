from rest_framework.test import APITestCase
from rest_framework import status


class SimcardEstimatorTest(APITestCase):
    def setUp(self):
        self.valid = {"number": 9120959336, "rond": "خیر", "stock": 'بله', "daemi": "بله"}
        self.invalid = {"number": 9120959336, "rond": "", "stock": 'بله', "daemi": "بله"}
        self.invalid2 = {"number": 9120959336, "rond": "خیر", "stock": 'بله'}

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
        response = self.client.post("/SEstimator/Simcard/", self.valid)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_data(self):
        response = self.client.post("/SEstimator/Simcard/", self.invalid)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_data2(self):
        response = self.client.post("/SEstimator/Simcard/", self.invalid2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_price_data(self):
        price = self.client.post("/SEstimator/Simcard/", self.valid).data.get("price")
        self.assertIsInstance(price, int)

    def test_simcards_data(self):
        simcards = self.client.post("/SEstimator/Simcard/", self.valid).data.get("simcards")
        self.assertIsInstance(simcards, list)

    def test_current_data(self):
        our_data = self.client.post("/SEstimator/Simcard/", self.valid)

        number = our_data.data.get("currentsimcard").get("number")
        self.assertEqual(number, self.valid.get("number"))
        rond = our_data.data.get("currentsimcard").get("rond")
        self.assertEqual(rond, self.valid.get("rond"))
        stock = our_data.data.get("currentsimcard").get("stock")
        self.assertEqual(stock, self.valid.get("stock"))
        daemi = our_data.data.get("currentsimcard").get("daemi")
        self.assertEqual(daemi, self.valid.get("daemi"))

    def test_main_page(self):
        response = self.client.get("/CEstimator/Car/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
