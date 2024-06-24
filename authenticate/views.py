from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, SignInForm
from verify_email.email_handler import send_verification_email

def signin(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', '/') 
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = SignInForm()
    return render(request, 'authenticate/signin.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                User.objects.get(email=email)
                messages.error(request, 'Email already exists.')
            except User.DoesNotExist:
                send_verification_email(request, form)  # Pass the user instance
                messages.success(request, 'Please check your email to verify your account.')
                return redirect('signin')  # Replace with your sign-in page URL name
    else:
        form = SignUpForm()
    return render(request, 'authenticate/signup.html', {'form': form})
