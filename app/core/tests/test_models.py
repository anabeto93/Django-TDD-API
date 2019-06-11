from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        '''Test creating a new user with an email is successful.'''

        email = 'test@admin.com'
        password = 'TestPass1234$'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        '''Test the email of a new user is normalized.'''
        email = 'test1@AdmiN.com'
        user = get_user_model().objects.create_user(email, 'pass1234')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email_fails(self):
        '''Test creating a new user without an email will fail'''
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'pass1234')

    def test_super_user_is_created_successfully(self):
        '''Test creating a new superuser works'''

        user = get_user_model().objects.create_superuser(
            'you@mybuz.com', 'haha1234'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
