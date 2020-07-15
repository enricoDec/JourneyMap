from django.test import TestCase, Client

from JourneyMap.forms import ContactForm


class TestForms(TestCase):

    def test_contact_us_form_valid_data(self):
        self.client = Client()
        form = ContactForm(data={
            'name': 'Test',
            'email': 'contact@journey-map.eu',
            'message': 'Hi my name is Test, I have a question. Does this work?',
        })

        response = self.client.get('/contact_us', follow=True)
        self.assertTrue(form.is_valid())
        self.assertRedirects(response, '', status_code=301)

    def test_contact_us_form_no_data(self):
        form = ContactForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

    def test_contact_us_form_invalid_email(self):
        form = ContactForm(data={
            'name': 'Test',
            'email': 'contactjourney-map.eu',
            'message': 'Hi my name is Test, I have a question. Does this work?',
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_contact_us_form_no_message(self):
        form = ContactForm(data={
            'name': 'Test',
            'email': 'contact@journey-map.eu',
            'message': '',
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_contact_us_form_short_message(self):
        form = ContactForm(data={
            'name': 'Test',
            'email': 'contact@journey-map.eu',
            'message': 'Hi',
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_contact_us_form_no_name(self):
        form = ContactForm(data={
            'name': '',
            'email': 'contact@journey-map.eu',
            'message': 'Hi my name is Test, I have a question. Does this work?',
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
