# myapp/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class TestViews(TestCase):
    def setUp(self):
        # Create a test user for login tests
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_login_page(self):
        response = self.client.get(reverse('login'))  # Use reverse to get the URL by its name
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login-page.html')

    def test_signup_page(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_login_functionality(self):
        # Test login functionality with valid credentials
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)  # Redirects after successful login

    def test_invalid_login(self):
        # Test login functionality with invalid credentials
        response = self.client.post(reverse('login'), {'username': 'invaliduser', 'password': 'invalidpassword'})
        self.assertEqual(response.status_code, 302)  # Redirects to another page after invalid login

    # Add more specific tests as needed
