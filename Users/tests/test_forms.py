from django.test import TestCase

from Users.forms import UserRegister


class TestForms(TestCase):

    def test_register_form_valid_data(self):
        form = UserRegister(data={
            'first_name': 'Test',
            'last_name': 'Test',
            'email': 'test@journey-map.eu',
            'username': 'testUser',
            'password1': 'testing321',
            'password2': 'testing321',
        })

        self.assertTrue(form.is_valid())

    def test_register_form_nodata(self):
        form = UserRegister(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 6)

    def test_register_form_invalid_password(self):
        form = UserRegister(data={
            'first_name': 'Test',
            'last_name': 'Test',
            'email': 'test@journey-map.eu',
            'username': 'testUser',
            'password1': 'testing321',
            'password2': 'testingNOT321',
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_register_form_simple_password(self):
        form = UserRegister(data={
            'first_name': 'Test',
            'last_name': 'Test',
            'email': 'test@journey-map.eu',
            'username': 'testUser',
            'password1': 'password',
            'password2': 'password',
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_register_form_password_similar_to_name(self):
        form = UserRegister(data={
            'first_name': 'MyName',
            'last_name': 'MyName',
            'email': 'test@journey-map.eu',
            'username': 'testUser',
            'password1': 'MyName98',
            'password2': 'MyName98',
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_register_form_email_invalid(self):
        form = UserRegister(data={
            'first_name': 'Test',
            'last_name': 'Test',
            'email': 'testjourney-map.eu',
            'username': 'testUser',
            'password1': 'testing321',
            'password2': 'testing321',
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
