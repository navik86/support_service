from django.urls import reverse
from rest_framework.test import APITestCase


class TicketsApiTestCase(APITestCase):
    def test_get(self):
        url = reverse('tickets-list')
        print(url)
        response = self.client.get(url)
        print(response)