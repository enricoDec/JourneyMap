from django.utils.translation import gettext as _
from django.utils import translation

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By

from WebApplication import settings

import requests


# Create your tests here.


class SeleniumTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(SeleniumTests, cls).setUpClass()
        cls.selenium = WebDriver()

        lang_cookie = cls.selenium.get_cookie('django_language')
        browser_lang = cls.selenium.execute_script("return window.navigator.userLanguage || window.navigator.language")

        translation.activate(lang_cookie if lang_cookie != None else browser_lang)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(SeleniumTests, cls).tearDownClass()

    def test_routes(self):
        self.selenium.get('http://localhost:8000/')
        self.assertEqual(self.selenium.title, 'Journey Map - ' + _('Home'))

        element = self.selenium.find_element_by_xpath('//a[@class="nav-link" and .=\'' + _('Contact Us') + '\']')

        self.selenium.get(element.get_attribute('href'))
        self.assertEqual(self.selenium.title, 'Journey Map - ' + _('Contact Us'))

    def test_images_for_200_response(self):
        self.selenium.get('http://localhost:8000/')
        example_images = self.selenium.find_elements(By.TAG_NAME, 'img')

        for image in example_images:
            self.check_200_response(image.get_attribute("src"))

        bg_div_style = self.selenium.find_element_by_xpath(
            '//div[@class="position-relative overflow-hidden p-3 p-md-5 m-md-3 text-center bg-light"]').get_attribute(
            'style')
        self.check_200_response('http://localhost:8000' + bg_div_style.split('url("', 1)[1].split('"', 1)[0])

    def check_200_response(self, url):
        r = requests.get(url)
        try:
            self.assertEqual(r.status_code, 200)
        except AssertionError as e:
            self.verificationErrors.append(url + ' delivered response code of ' + r.status_code)

    def test_translation_select(self):
        self.selenium.find_element_by_xpath('//button[@class="btn dropdown-toggle btn-default"]').click()

        dropdown = self.selenium.find_element_by_xpath('//div[@class="dropdown-menu open show"]')
        dropdown_anchors = dropdown.find_elements(By.TAG_NAME, 'a')

        for anchor in dropdown_anchors:
            self.check_translation(anchor)

    def check_translation(self, anchor):
        anchor.click()
        self.assertEquals(self.get_cookie('http://localhost:8000/', 'django_language'),
                          settings.LANGUAGES[int(anchor.get_attribute('tabindex'))][0])

    def get_cookie(self, url, name):
        with requests.Session() as s:
            s.get(url)
            return s.cookies.get_dict()[name]
