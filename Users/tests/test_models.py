from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase, Client

from Users.models import Profile

import logging, logging.config
import sys

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO'
    }
}

logging.config.dictConfig(LOGGING)


class TestModels(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='TEST_USER1',
            email='test1@journey-map.eu',
            password='testing321',
            first_name='TEST',
            last_name='TEST_LAST_NAME'
        )
        self.assertEqual(user.email, 'test1@journey-map.eu')
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_same_email(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='TEST_USER2',
            email='test2@journey-map.eu',
            password='testing321',
            first_name='TEST',
            last_name='TEST_LAST_NAME'
        )
        with self.assertRaises(IntegrityError):
            user2 = User.objects.create_user(
                username='TEST_USER3',
                email='test2@journey-map.eu',
                password='testing321',
                first_name='TEST',
                last_name='TEST_LAST_NAME'
            )

    def test_create_user_same_username(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='TEST_USER4',
            email='test3@journey-map.eu',
            password='testing321',
            first_name='TEST',
            last_name='TEST_LAST_NAME'
        )
        with self.assertRaises(IntegrityError):
            user2 = User.objects.create_user(
                username='TEST_USER4',
                email='test4@journey-map.eu',
                password='testing321',
                first_name='TEST',
                last_name='TEST_LAST_NAME'
            )

    def test_create_user_default_is_inactive(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='TEST_USER5',
            email='test5@journey-map.eu',
            password='testing321',
            first_name='TEST',
            last_name='TEST_LAST_NAME'
        )
        self.assertFalse(user.is_active)

    def test_create_user_default_no_email(self):
        User = get_user_model()

        with self.assertRaises(TypeError):
            user = User.objects.create_user(
                username='TEST_USER6',
                password='testing321',
                first_name='TEST',
                last_name='TEST_LAST_NAME'
            )

    def test_create_user_default_no_username(self):
        User = get_user_model()

        with self.assertRaises(TypeError):
            user = User.objects.create_user(
                email='test6@journey-map.eu',
                password='testing321',
                first_name='TEST',
                last_name='TEST_LAST_NAME'
            )

    def test_login_user_not_active(self):
        User = get_user_model()

        user = User.objects.create_user(
            username='TEST_USER7',
            email='test7@journey-map.eu',
            password='testing321',
            first_name='TEST',
            last_name='TEST_LAST_NAME'
        )

        client = Client()
        self.assertFalse(client.login(username='TEST_USER7', password='testing321'))

    def test_login_user_active(self):
        User = get_user_model()

        user = User.objects.create_user(
            username='TEST_USER8',
            email='test8@journey-map.eu',
            password='testing321',
            first_name='TEST',
            last_name='TEST_LAST_NAME'
        )
        user.is_active = True
        user.save()

        client = Client()
        self.assertTrue(client.login(username='TEST_USER8', password='testing321'))

    def test_profile_create(self):
        User = get_user_model()

        user = User.objects.create_user(
            username='TEST_USER9',
            email='test9@journey-map.eu',
            password='testing321',
            first_name='TEST',
            last_name='TEST_LAST_NAME'
        )
        user.is_active = True

        profile = Profile.objects.get(user_id=user.id)

        self.assertEqual(profile.user_id, user.id)

    def test_profile_default_image(self):
        User = get_user_model()

        user = User.objects.create_user(
            username='TEST_USER10',
            email='test10@journey-map.eu',
            password='testing321',
            first_name='TEST',
            last_name='TEST_LAST_NAME'
        )
        user.is_active = True

        profile = Profile.objects.get(user_id=user.id)

        self.assertEqual(profile.image.name, 'profile_pics/default.jpg')

    def test_profile_no_override_image(self):
        User = get_user_model()

        user = User.objects.create_user(
            username='TEST_USER11',
            email='test11@journey-map.eu',
            password='testing321',
            first_name='TEST',
            last_name='TEST_LAST_NAME'
        )
        user.is_active = True
        user.save()

        profile = Profile.objects.get(user_id=user.id)

        logging.info(settings.MEDIA_ROOT + '/test_image/Canon_40D.jpg')

        profile.image = open(settings.MEDIA_ROOT + '/test_image/Canon_40D.jpg', 'r')
        #profile.save()

        assert True
