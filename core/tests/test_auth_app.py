from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from auth_app.models import CustomUserModel
from django.contrib.auth import get_user_model

get_user_model = CustomUserModel


class UserRegistrationTestCase(APITestCase):
    def setUp(self):
        url = reverse('registerion')
        
        self.email = 'testuser@example.com'
        self.password = 'testpassword'
        
        self.data = {
            'username': 'testuser',
            'email': self.email,
            'password': self.password,
            'repeated_password': self.password,
        }

    def test_user_registration(self):
        
        url = reverse('registerion')
        
        response = self.client.post(url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        response = self.client.post(url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    
    def test_user_login(self):
        url = reverse('login')
        url_activate = reverse('activate_user', kwargs={'uidb64': 'testuid', 'token': 'testtoken'})
        
        # Register the user first
        self.client.post(reverse('registerion'), self.data, format="json")
        
        # Now test login
        login_data = {
            'email': self.email,
            'password': self.password,
        }
        
        response = self.client.post(url, login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        response = self.client.get(url_activate)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        
        ## response = self.client.get(url_activate, follow=True)
        ## self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        ## response = self.client.post(url, login_data, format="json")
        ## self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test login with incorrect password
        login_data['password'] = 'wrongpassword'
        response = self.client.post(url, login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    
    def test_password_reset_request(self):
        url = reverse('reset_password')
        
        # Register the user first
        self.client.post(reverse('registerion'), self.data, format="json")
        
        # Request password reset
        reset_data = {
            'email': self.email,
        }
        
        response = self.client.post(url, reset_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test with non-existent email
        reset_data['email'] = 'test@test.com'
        response = self.client.post(url, reset_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_password_reset_with_token(self):
        url = reverse('reset_password_token', kwargs={'token': 'testtoken'})
        # Register the user first
        self.client.post(reverse('registerion'), self.data, format="json")
        # Request password reset
        reset_data = {
            'email': self.email,
        }
        self.client.post(reverse('reset_password'), reset_data, format="json")
        