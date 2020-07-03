from django.test import TestCase, Client
from django.urls import reverse


class TestView(TestCase):

    def setUp(self):
        self.client = Client()
        self.home_url = reverse('JourneyMap_home')
        self.contact_us_url = reverse('JourneyMap_contact_us')

    def test_home_GET(self):
        response = self.client.get(self.home_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'JourneyMap/home.html')

    def test_contact_us_GET(self):
        response = self.client.get(self.contact_us_url)

        self.assertEqual(response.status_code, 200)

    def test_contact_us_POST(self):
        data = {
            'name': 'Test',
            'email': 'contact@journey-map.eu',
            'message': 'Hi my name is Test, I have a question. Does this work?',
        }
        response = self.client.post(self.contact_us_url, data=data)

        self.assertEqual(response.status_code, 302)
