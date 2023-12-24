# myapp/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class TestLoginSignup(TestCase):
    def setUp(self):
        # Create a test user for login tests
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_login_page(self):
        response = self.client.get(reverse('login'))  # Use reverse to get the URL by its name
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login-page.html')

    def test_signup_page(self):
        # Simulate a complete signup process
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'testuser@gmail.com',
            'password': 'testpassword',
            'confirm-password': 'testpassword'
        })

        # Check if the signup process is successful
        self.assertEqual(response.status_code, 302)  # Redirects after successful signup

        # Check if the user is created in the database
        self.assertTrue(User.objects.filter(username='testuser').exists())



    def test_login_functionality(self):
        # Test login functionality with valid credentials
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)  # Redirects after successful login

    def test_invalid_login(self):
        # Test login functionality with invalid credentials
        response = self.client.post(reverse('login'), {'username': 'invaliduser', 'password': 'invalidpassword'})
        self.assertEqual(response.status_code, 302)  # Redirects to another page after invalid login
 
class TestRecommendations(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_recommendations_functionality(self):
        # Log in the test user
        self.client.login(username='testuser', password='testpassword')

        # Send a POST request to the recommendations endpoint with a sample user-input
        response = self.client.post(reverse('recommendations'), {'user-input': 'Mystery'})

        # Check if the view returns a success status code
        self.assertEqual(response.status_code, 200)

        # Add more specific checks for the content of the response if needed
        # For example, you can check if the recommended books are present in the response content

        # Example: Check if the recommended books section is present in the HTML response
        self.assertContains(response, '<div class="recommendations">')

        # Example: Check if specific book titles are present in the HTML response
        self.assertContains(response, 'Gone Girl')
        self.assertContains(response, 'The Girl with the Dragon Tattoo')

        # Add more specific checks as needed