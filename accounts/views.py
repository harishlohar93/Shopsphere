from django.shortcuts import render , redirect
from django.http import HttpResponseRedirect , HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from .models import Profile
import uuid
from base.emails import send_account_sctivation_email
import time



def login_page(request):
    if request.method == 'POST':
        # Retrieve email and password from the form
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        # Check if both fields are provided
        if not email:
            messages.warning(request, 'Email is required.')
            return HttpResponseRedirect(request.path_info)
        if not password:
            messages.warning(request, 'Password is required.')
            return HttpResponseRedirect(request.path_info)

        try:
            # Find the user by email (email is saved as username in registration)
            user = User.objects.get(username=email)
        except User.DoesNotExist:
            messages.error(request, 'Account not found. Please register.')
            return HttpResponseRedirect(request.path_info)

        # Authenticate the user
        user_obj = authenticate(request, username=user.username, password=password)
        if user_obj:
            # Check email verification
            if hasattr(user_obj, 'profile') and not user_obj.profile.is_email_verified:
                messages.warning(request, 'Your email address is not verified.')
                return HttpResponseRedirect(request.path_info)

            # Log in the user
            login(request, user_obj)
            messages.success(request, 'You are successfully logged in!')
            return redirect('/')

        # Incorrect password case
        messages.error(request, 'Invalid credentials. Please try again.')
        return HttpResponseRedirect(request.path_info)

    return render(request, 'accounts/login.html')

def register_page(request):
    if request.method == 'POST':
        fullname = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        # Check for empty fields
        if not fullname or not email or not password:
            messages.warning(request, 'All fields are required.')
            return HttpResponseRedirect(request.path_info)

        # Password confirmation
        if password != confirm_password:
            messages.warning(request, 'Passwords do not match.')
            return HttpResponseRedirect(request.path_info)

        # Check if the user already exists
        if User.objects.filter(username=email).exists():
            messages.warning(request, 'Email is already registered.')
            return HttpResponseRedirect(request.path_info)

        # Split fullname into first and last name
        first_name, last_name = (fullname.split(' ', 1) + [''])[:2]

        # Create the user
        user_obj = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # Add a profile for the user (email verification token)
        email_token = str(uuid.uuid4())
        Profile.objects.create(user=user_obj, email_token=email_token)

        # Send email verification
        send_account_sctivation_email(email_token, email)

        messages.success(request, 'Registration successful. Please check your email to verify your account.')
        time.sleep(5)
        return redirect('/login')  # Redirect to login page after registration

    return render(request, 'accounts/register.html')

def activate_email(request, email_token):
    try:
        # Look for the profile with the given token
        profile = Profile.objects.get(email_token=email_token)
        
        # If the email is already verified, return a message
        if profile.is_email_verified:
            messages.info(request, 'Your email is already verified.')
            return redirect('/')

        # Mark the profile as email verified
        profile.is_email_verified = True
        profile.save()

        # Optionally, mark the user as email verified (if you're using an attribute on the User model for email verification)
        profile.user.is_email_verified = True
        profile.user.save()

        messages.success(request, 'Email verified successfully. You can now log in.')
        return redirect('/')  # Redirect to home page or login page
    except Profile.DoesNotExist:
        # Handle invalid or expired token
        messages.error(request, 'Invalid or expired token.')
        return redirect('/login')  # Redirect to login page or error page