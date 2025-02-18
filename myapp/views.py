from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Myuser, Product, House, Car, TrendingProduct, Category, Cart, Card, Order
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
            password = form.cleaned_data.get('password')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            phone = form.cleaned_data.get('phone')
            address = form.cleaned_data.get('address')

            # Check if email already exists
            if Myuser.objects.filter(email=email).exists():
                messages.error(request, 'This email is already registered. Please use a different email or login.')
                return render(request, 'register.html', {'form': form})

            try:
                # Create the user
                user = User.objects.create_user(username=email, email=email, password=password)
                # Create Myuser profile
                Myuser.objects.create(user=user, first_name=first_name, last_name=last_name, email=email, phone=phone, address=address)
                # Log the user in
                login(request, user)
                return redirect('dashboard')
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
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'login.html')

def dashboard(request):
    category_id = request.GET.get('category_id')
    if (category_id):
        products = Product.objects.filter(category_id=category_id)
        selected_category = get_object_or_404(Category, id=category_id)
    else:
        products = Product.objects.all()
        selected_category = None
    trending_products = TrendingProduct.objects.all()
    categories = Category.objects.all()
    return render(request, 'dashboard.html', {'products': products, 'trending_products': trending_products, 'categories': categories, 'selected_category': selected_category})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
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
    house = House.objects.all()
    return render(request, 'property.html', {'property': house})

def property_detail(request, property_id):
    house = House.objects.get(id=property_id)
    return render(request, 'property_detail.html', {'property': house})

def trending_product_detail(request, product_id):
    product = get_object_or_404(TrendingProduct, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

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

@login_required
def add_to_cart(request, product_id):
   
    # Create an order entry
    Order.objects.create(user=user, product=product, quantity=cart_item.quantity, total_price=product.price * cart_item.quantity)
    
    messages.success(request, 'Product added to cart and order created successfully.')
    return redirect('dashboard')

@login_required
def profile_user(request):
    myuser = get_object_or_404(Myuser, user=request.user)
    card = Card.objects.filter(user=myuser).first()
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        product = get_object_or_404(Product, id=product_id)
        user, created = Myuser.objects.get_or_create(user=request.user)
        cart_item, created = Cart.objects.get_or_create(user=user, product=product)
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, 'Cart updated successfully.')
        return redirect('profile_user')
    return render(request, 'profileuser.html', {'myuser': myuser, 'card': card})

@login_required
def update_card(request):
    myuser = get_object_or_404(Myuser, user=request.user)
    if request.method == 'POST':
        card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')
        cardholder_name = request.POST.get('cardholder_name')
        amount = request.POST.get('amount')
        # Here you would save the card information to the user's profile or another model
        messages.success(request, 'Card information updated successfully.')
        Card.objects.create(user=myuser, card_number=card_number, expiration_date=expiry_date, cvv=cvv, cardholder_name=cardholder_name, amount=amount)
        return redirect('profile_user')
    return render(request, 'profileuser.html', {'myuser': myuser})











