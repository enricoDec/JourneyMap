from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from django.utils import translation
from django.utils.translation import gettext as _
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.webdriver import WebDriver


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

    def test_login_form_uid_success(self):
        self.create_user(username='TEST_USER', email='test@journey-map.eu', active=True)

        url = self.live_server_url + reverse('login')
        self.selenium.get(url)

        self.selenium.find_element_by_id('id_username').send_keys('TEST_USER')
        self.selenium.find_element_by_id('id_password').send_keys('testing321')
        self.selenium.find_element_by_xpath('//button[@class="btn btn-outline-info" and @type="submit"]').click()

        try:
            alert = self.selenium.find_element_by_xpath('//div[@class="alert alert-block alert-danger"]')
            raise AssertionError('Alert should not be found.')
        except NoSuchElementException:
            self.assertEqual(self.selenium.title, 'Journey Map - ' + _('Home'))

    def test_login_form_email_success(self):
        self.create_user(username='TEST_USER2', email='test2@journey-map.eu', active=True)

        url = self.live_server_url + reverse('login')
        self.selenium.get(url)

        self.selenium.find_element_by_id('id_username').send_keys('test2@journey-map.eu')
        self.selenium.find_element_by_id('id_password').send_keys('testing321')
        self.selenium.find_element_by_xpath('//button[@class="btn btn-outline-info" and @type="submit"]').click()

        try:
            alert = self.selenium.find_element_by_xpath('//div[@class="alert alert-block alert-danger"]')
            raise AssertionError('Alert should not be found.')
        except NoSuchElementException:
            self.assertEqual(self.selenium.title, 'Journey Map - ' + _('Home'))

    def test_login_form_fail(self):
        self.create_user(username='TEST_USER3', email='test3@journey-map.eu', active=True)

        url = self.live_server_url + reverse('login')
        self.selenium.get(url)

        self.selenium.find_element_by_id('id_username').send_keys('TEST')
        self.selenium.find_element_by_id('id_password').send_keys('testing321')
        self.selenium.find_element_by_xpath('//button[@class="btn btn-outline-info" and @type="submit"]').click()

        alert = self.selenium.find_element_by_xpath('//div[@class="alert alert-block alert-danger"]')
        self.assertTrue(alert is not None)

    def create_user(self, username, email, active):
        User = get_user_model()

        user = User.objects.create_user(
            username=username,
            email=email,
            password='testing321',
            first_name='TEST',
            last_name='TEST_LAST_NAME'
        )
        user.is_active = active
        user.save()

    def test_profile_if_logged(self):
        self.create_user(username='TEST_USER_2', email='test@journey-map.eu', active=True)

        url = self.live_server_url + reverse('login')
        self.selenium.get(url)

        self.selenium.find_element_by_id('id_username').send_keys('TEST_USER_2')
        self.selenium.find_element_by_id('id_password').send_keys('testing321')
        self.selenium.find_element_by_xpath('//button[@class="btn btn-outline-info" and @type="submit"]').click()

        profile_url = self.live_server_url + reverse('profile')
        self.selenium.get(profile_url)

        self.assertEqual(self.selenium.title, 'Journey Map - ' + _('Profile'))

    def test_profile_if_not_logged(self):
        profile_url = self.live_server_url + reverse('profile')
        self.selenium.get(profile_url)

        self.assertNotEqual(self.selenium.title, 'Journey Map - ' + _('Profile'))

    def test_profile_change_password(self):
        self.create_user(username='TEST_USER', email='test@journey-map.eu', active=True)

        url = self.live_server_url + reverse('login')
        self.selenium.get(url)

        self.selenium.find_element_by_id('id_username').send_keys('TEST_USER')
        self.selenium.find_element_by_id('id_password').send_keys('testing321')
        self.selenium.find_element_by_xpath('//button[@class="btn btn-outline-info" and @type="submit"]').click()

        profile_url = self.live_server_url + reverse('profile')
        self.selenium.get(profile_url)
        self.selenium.find_element_by_xpath('//*[@id="id_old_password"]').send_keys('testing321')
        self.selenium.find_element_by_xpath('//*[@id="id_new_password1"]').send_keys('testing9876')
        self.selenium.find_element_by_xpath('//*[@id="id_new_password2"]').send_keys('testing9876')
        self.selenium.find_element_by_xpath('/html/body/main/div[2]/div[2]/form[2]/div/button').click()
        confirm_message = self.selenium.find_element_by_xpath('/html/body/main/div[1]/div')

        self.assertEqual(confirm_message.text, 'Password information Updated!')
