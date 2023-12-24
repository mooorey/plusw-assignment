from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Feature 
from django.http import JsonResponse
from django.conf import settings
import openai, os
# from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
import typer
import re
import random



openai.api_key = os.getenv("OPENAI_KEY")
app = typer.Typer()

# Create your views here.
def index(request):
    return render(request, 'home.html')


    


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']

        if confirm_password == password:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already in use')
                return redirect('register')
            elif not re.match(r'^[a-zA-Z0-9._%+-]+@(gmail\.com|hotmail\.com|yahoo\.com|live\.com)$', email):
                messages.info(request, 'Invalid email syntax')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already in use')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                return redirect('login')
        else:
            messages.info(request, 'Password is not the same')
            return redirect('register')

    else:
        return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')  # Use get method with a default value
        password = request.POST.get('password', '')  # Use get method with a default value

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')  # Redirect to home page if login is successful
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')
    
    else:
        return render(request, 'login-page.html')



def logout(request):
    auth.logout(request)
    return redirect('login')

def home(request):
    return render(request, 'home.html', {'user': request.user})


def recommendations(request):
    if request.method == "POST":
        user_input = request.POST.get('user-input')

        # Define a list of possible system messages for more variety
        system_messages = [
            "You are a helpful assistant.",
            "You are an expert in book recommendations.",
            "You love suggesting great books to read.",
            # Add more system messages as needed
        ]

        # Randomly select a system message
        selected_system_message = random.choice(system_messages)

        # Construct the prompt with the selected system message
        prompt = f"{selected_system_message}\n\nRecommend 5 books in the genre of {user_input}. Do not give description or anything else of the books, only recommend them in this form: book-name by author, etc etc"

        # Define the temperature value (adjust as needed)
        temperature = 0.7

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": selected_system_message},
                {"role": "user", "content": prompt},
            ],
            temperature=temperature  # Add the temperature parameter
        )

        # Extract recommended books from the response
        recommended_books = response['choices'][0]['message']['content']

        # Split the recommended books into a list
        recommended_books_list = recommended_books.split('\n\n')

        # Store the recommended books in a dictionary
        books_dict = {'books': recommended_books_list}

        # Print the dictionary for debugging
        print("Recommended Books Dictionary:", books_dict)

        # Pass the dictionary to the HTML template
        return render(request, 'home.html', {'books_dict': books_dict})

    return render(request, 'home.html', {})