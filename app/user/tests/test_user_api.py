from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    '''Test the users API (public)'''

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_successful(self):
        '''Test that creating a valid user is successful.'''

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
        create_user(**payload)

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
            email=payload['email']
        ).exists()

        self.assertFalse(user_exists)

    def test_create_user_token_passes(self):
        '''Test that a token can be created for a user.'''
        payload = {'email': 'new@admin.com', 'password': 'newpass12'}
        create_user(**payload)

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_with_invalid_credentials_fails(self):
        '''Test that token will not be created given invalid credentials.'''
        payload = {'email': 'you@admin.com', 'password': 'correctone'}
        create_user(**payload)
        payload['password'] = 'wrong_password'  # change the password

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_without_user(self):
        '''Test that the token creation fails if user doesn't exist.'''
        payload = {'email': 'none@none.com', 'password': 'dontbother'}

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field_fails(self):
        '''Test that both email and password fields are required.'''
        payload = {'email': 'missing@password.com', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        payload['email'] = ''
        payload['password'] = 'missing_email'

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        '''Test that authentication is required.'''

        res = self.client.post(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITests(TestCase):
    '''Test API requests that require authentication.'''

    def setUp(self):
        self.user = create_user(
            email='test@admin.com',
            password='seriousP@ss',
            name='Auth Tester'
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_can_retrieve_profile(self):
        '''Test can retrieve the profile of an authenticated User.'''
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_method_not_allowed(self):
        '''Test that POST is not allowed on the user me url.'''
        res = self.client.post(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile_works(self):
        '''Test that User profile can be updated.'''
        payload = {'name': 'Working Tester', 'password': 'More$ecure123'}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
