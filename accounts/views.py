from django.shortcuts import render , redirect
from django.http import HttpResponseRedirect , HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from .models import Profile

def login_page(request):
    if request.method == 'POST':
        fullname = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        
        
        # Check if the user already exists
        if not User.objects.filter(username=email).exists():
            messages.warning(request, 'Account not found')
            return HttpResponseRedirect(request.path_info)
        
        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, 'Email is not verified')
            return HttpResponseRedirect(request.path_info)
        
        user_obj = authenticate(username=email, password=password)
        if user_obj:
            login(request, user_obj)
            return HttpResponseRedirect('/')
        
        messages.warning(request, 'Invalid Credentials')
        return HttpResponseRedirect(request.path_info)

    return render(request, 'accounts/login.html')

def register_page(request):
    if request.method == 'POST':
        fullname = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        
        # Check if the user already exists
        if User.objects.filter(username=email).exists():
            messages.warning(request, 'Email is already registered')
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
        messages.success(request, 'Registration successful. Please verify your email address.')
        return HttpResponseRedirect(request.path_info)

    return render(request, 'accounts/register.html')

def activate_email(request , email_token):
    try:
        user = User.objects.get(profile_email_token=email_token)
        user.is_email_verified = True
        user.save()
        return redirect('/')
    except Exception as e:
        return HttpResponse('Invalid token')