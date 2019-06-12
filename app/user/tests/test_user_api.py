from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    '''Test the users API (public)'''

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_successful(self):
        '''Test that creating a valid user with the given payload is successful.'''

        payload = {
            'email': 'test@admin.com',
            'password': 'somepass1234',
            'name': 'My Buz'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        # ensure that the user is not returned in the response res
        self.assertNotIn('password', res.data)

    def test_duplicate_user_fails(self):
        '''Test that creating a user that already exists will fail.'''

        payload = {'email': 'test@admin.com', 'password': 'pass12'}
        create_user(payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_fails(self):
        '''Test that the password must be at least 6 characters.'''

        payload = {'email': 'another@admin.com', 'passowrd': 'pass'}

        res = self.client.post(CREATE_USER_URL, payload)

        # this is supposed to fail as the password is too short
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # also check to ensure the user is not created
        user_exists = get_user_model().objects.filter(
            email = payload['email']
        ).exists()

        self.assertFalse(user_exists)
