import unittest
from django.test import Client


class HomeTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_details(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
