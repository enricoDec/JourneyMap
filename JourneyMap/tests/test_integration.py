from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from django.utils.translation import gettext as _
from selenium.webdriver.firefox.webdriver import WebDriver


class SeleniumTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(SeleniumTests, cls).setUpClass()
        cls.selenium = WebDriver()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(SeleniumTests, cls).tearDownClass()

    def test_contact_us_resolvable(self):
        url = self.live_server_url + reverse('JourneyMap_contact_us')
        self.selenium.get(url)

        self.assertEqual(self.selenium.title, 'Journey Map - ' + _('Contact Us'))

    def test_contact_us_form_valid(self):
        url = self.live_server_url + reverse('JourneyMap_contact_us')
        self.selenium.get(url)

        # Content to insert in the form
        name = 'Test'
        message = 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, ' \
                  'sed diam nonumy eirmod tempor invidunt ut labore et dolore ' \
                  'magna aliquyam erat, sed diam voluptua. ' \
                  'At vero eos et accusam et justo duo dolores et ea rebum. '
        email = 'contact@journey-map.eu'

        # Form fields
        name_field = self.selenium.find_element_by_name('name')
        message_field = self.selenium.find_element_by_name('message')
        email_field = self.selenium.find_element_by_name('email')

        # Insert content
        name_field.send_keys(name)
        message_field.send_keys(message)
        email_field.send_keys(email)

        # Send form
        self.selenium.find_element_by_xpath('/html/body/main/div[2]/form/div/button').click()

        # Assert redirect
        self.assertEqual(self.selenium.title, 'Journey Map - ' + _('Home'))

        # Assert success message
        confirm_message = self.selenium.find_element_by_class_name('alert-success')
        self.assertIsNotNone(confirm_message.text)

    def test_contact_us_form_short_message(self):
        url = self.live_server_url + reverse('JourneyMap_contact_us')
        self.selenium.get(url)

        # Content to insert in the form
        name = 'Test'
        message = 'Hi'
        email = 'contact@journey-map.eu'

        # Form fields
        name_field = self.selenium.find_element_by_name('name')
        message_field = self.selenium.find_element_by_name('message')
        email_field = self.selenium.find_element_by_name('email')

        # Insert content
        name_field.send_keys(name)
        message_field.send_keys(message)
        email_field.send_keys(email)

        # Send form
        self.selenium.find_element_by_xpath('/html/body/main/div[2]/form/div/button').click()

        # Assert no redirect
        self.assertEqual(self.selenium.title, 'Journey Map - ' + _('Contact Us'))

    def test_contact_us_form_invalid_email(self):
        url = self.live_server_url + reverse('JourneyMap_contact_us')
        self.selenium.get(url)

        # Content to insert in the form
        name = 'Test'
        message = 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, ' \
                  'sed diam nonumy eirmod tempor invidunt ut labore et dolore ' \
                  'magna aliquyam erat, sed diam voluptua. ' \
                  'At vero eos et accusam et justo duo dolores et ea rebum. '
        email = 'contact@journey-map'

        # Form fields
        name_field = self.selenium.find_element_by_name('name')
        message_field = self.selenium.find_element_by_name('message')
        email_field = self.selenium.find_element_by_name('email')

        # Insert content
        name_field.send_keys(name)
        message_field.send_keys(message)
        email_field.send_keys(email)

        # Send form
        self.selenium.find_element_by_xpath('/html/body/main/div[2]/form/div/button').click()

        # Assert no redirect
        self.assertEqual(self.selenium.title, 'Journey Map - ' + _('Contact Us'))
