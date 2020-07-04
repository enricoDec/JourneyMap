from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase, Client


class TestModels(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='TEST_USER',
            email='test@journey-map.eu',
            password='testing321',
            first_name='TEST',
            last_name='TEST_LAST_NAME'
        )
        self.assertEqual(user.email, 'test@journey-map.eu')
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_same_email(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='TEST_USER',
            email='test@journey-map.eu',
            password='testing321',
            first_name='TEST',
            last_name='TEST_LAST_NAME'
        )
        with self.assertRaises(IntegrityError):
            user2 = User.objects.create_user(
                username='TEST_USER2',
                email='test@journey-map.eu',
                password='testing321',
                first_name='TEST',
                last_name='TEST_LAST_NAME'
            )

    def test_create_user_same_username(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='TEST_USER',
            email='test@journey-map.eu',
            password='testing321',
            first_name='TEST',
            last_name='TEST_LAST_NAME'
        )
        with self.assertRaises(IntegrityError):
            user2 = User.objects.create_user(
                username='TEST_USER',
                email='test2@journey-map.eu',
                password='testing321',
                first_name='TEST',
                last_name='TEST_LAST_NAME'
            )

    def test_create_user_default_is_inactive(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='TEST_USER',
            email='test@journey-map.eu',
            password='testing321',
            first_name='TEST',
            last_name='TEST_LAST_NAME'
        )
        self.assertFalse(user.is_active)

    def test_create_user_default_no_email(self):
        User = get_user_model()

        with self.assertRaises(TypeError):
            user = User.objects.create_user(
                username='TEST_USER',
                password='testing321',
                first_name='TEST',
                last_name='TEST_LAST_NAME'
            )

    def test_create_user_default_no_username(self):
        User = get_user_model()

        with self.assertRaises(TypeError):
            user = User.objects.create_user(
                email='test@journey-map.eu',
                password='testing321',
                first_name='TEST',
                last_name='TEST_LAST_NAME'
            )

    def test_login_user_not_active(self):
        User = get_user_model()

        user = User.objects.create_user(
            username='TEST_USER',
            email='test@journey-map.eu',
            password='testing321',
            first_name='TEST',
            last_name='TEST_LAST_NAME'
        )

        client = Client()
        self.assertFalse(client.login(username='TEST_USER', password='testing321'))

    def test_login_user_active(self):
        User = get_user_model()

        user = User.objects.create_user(
            username='TEST_USER',
            email='test@journey-map.eu',
            password='testing321',
            first_name='TEST',
            last_name='TEST_LAST_NAME'
        )
        user.is_active = True

        client = Client()
        self.assertTrue(client.login(username='TEST_USER', password='testing321'))
