from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Myuser
from .forms import UserRegistrationForm
from django.contrib.auth.models import User

@login_required
def user(request):
    users = Myuser.objects.all()
    return render(request, 'user.html', {'users': users})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            # Check if email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, 'This email is already registered. Please use a different email or login.')
                return render(request, 'register.html', {'form': form})
            
            try:
                # Create the user
                user = form.save()
                # Create MyUser profile
                Myuser.objects.create(user=user)
                # Log the user in
                login(request, user)
                return redirect('user')
            except Exception as e:
                print(f"Registration error: {str(e)}")  # For debugging
                messages.error(request, f'Registration error: {str(e)}')
        else:
            # Form is not valid, show field-specific errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        # Since we're using email as username
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('user')
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'login.html')