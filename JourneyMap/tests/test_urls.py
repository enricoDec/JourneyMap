from django.test import SimpleTestCase
from django.urls import resolve, reverse

from JourneyMap.views import home, contact


class TestUrls(SimpleTestCase):

    def test_home_url_is_resolves(self):
        url = reverse('JourneyMap_home')
        self.assertEqual(resolve(url).func, home)

    def test_contact_us_url_is_resolves(self):
        url = reverse('JourneyMap_contact_us')
        self.assertEqual(resolve(url).func, contact)
