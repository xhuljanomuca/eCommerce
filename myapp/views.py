from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Myuser, Product, TrendingProduct, House, Car, Category
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

def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    
    return render(request, 'dashboard.html', {'categories': categories, 'products': products})


def dashboard(request):
    products = Product.objects.all()
    trending_products = TrendingProduct.objects.all()
    return render(request, 'trending_product_detail.html', {'products': products}, {'trending_products': trending_products})

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'product_detail.html', {'product': product})

def product_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        product = Product(name=name, description=description, price=price)
        product.save()
        Product.objects.create(name=name, description=description, price=price)
    return render(request, 'product_create.html')

def house(request):
    house= House.objects.all()
    return render(request, 'property.html', {'property': property})

def property_detail(request, property_id):
    house=House.objects.get(id=property_id)
    return render(request, 'property_detail.html', {'property': property})

def house_create(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        city = request.POST.get('city')
        rooms = request.POST.get('rooms')
        property_surface = request.POST.get('property_surface')
        price = request.POST.get('price')
        description = request.POST.get('description')
        title = request.POST.get('title')
        type = request.POST.get('type')
        house = House(address=address, city=city, rooms=rooms, property_surface=property_surface, price=price, description=description, title=title, type=type)
        house.save()
        House.objects.create(address=address, city=city, rooms=rooms, property_surface=property_surface, price=price, description=description, title=title, type=type)
    return render(request, 'property_create.html')

def cars(request):
    cars = Car.objects.all()
    return render(request, 'cars.html', {'cars': cars})

def car_detail(request, car_id):
    car = Car.objects.get(id=car_id)
    return render(request, 'car_detail.html', {'car': car})

def car_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        color = request.POST.get('color')
        model = request.POST.get('model')
        year = request.POST.get('year')
        price = request.POST.get('price')
        car = Car(title=title, color=color, model=model, year=year, price=price)
        car.save()
        Car.objects.create(title=title, color=color, model=model, year=year, price=price)
    return render(request, 'car_create.html')

def car_delete(request, car_id):
    car = Car.objects.get(id=car_id)
    car.delete()
    return redirect('cars')

def house_delete(request, house_id):
    house = House.objects.get(id=house_id)
    house.delete()
    return redirect('property')

def product_delete(request, product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    return redirect('dashboard')
