import uuid

from django.test import TestCase, Client
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class TestView(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.activate_url = reverse('activate',
                                    args=[urlsafe_base64_encode(force_bytes(uuid.uuid4())), '5hs-a6b79825b01749d91e1c'])
        self.profile_url = reverse('profile')

    def test_register_GET(self):
        response = self.client.get(self.register_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Users/sign_up.html')

    def test_activate_GET(self):
        response = self.client.get(self.activate_url)

        self.assertEqual(response.status_code, 302)

    def test_login_GET(self):
        response = self.client.get(self.login_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Users/sign_in.html')

    def test_register_POST(self):
        response = self.client.post(self.register_url)

        self.assertEqual(response.status_code, 200)

    def test_profile_GET(self):
        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, 302)

    def test_login_POST(self):
        response = self.client.post(self.profile_url)

        self.assertEqual(response.status_code, 302)
