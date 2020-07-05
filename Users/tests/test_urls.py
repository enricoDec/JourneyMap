import uuid

from django.contrib.auth.views import LoginView
from django.test import SimpleTestCase
from django.urls import resolve, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from Users.views import sign_up, sign_out, ActivateUser


class TestUrls(SimpleTestCase):

    def test_register_url_is_resolves(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func, sign_up)

    def test_activation_url_is_resolves(self):
        url = reverse('activate', args=[urlsafe_base64_encode(force_bytes(uuid.uuid4())), '5hs-a6b79825b01749d91e1c'])
        self.assertEqual(resolve(url).func.view_class, ActivateUser)

    def test_login_url_is_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, LoginView)

    def test_logout_url_is_resolves(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func.view_class, sign_out)
