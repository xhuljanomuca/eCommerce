from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Myuser, Product, TrendingProduct, House, Car, Category, Order, Photo, Cart, Card, Transaction, ProductReview
from .forms import UserRegistrationForm, ProductForm, Product, ReviewForm
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
            password = form.cleaned_data.get('password')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            phone = form.cleaned_data.get('phone')
            address = form.cleaned_data.get('address')

            # Check if email already exists
            if User.objects.filter(email=email).exists():
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
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


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
    reviews = ProductReview.objects.filter(product=product)

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('login')

        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, "Review submitted successfully!")
            return redirect('product_detail', product_id=product.id)
    else:
        form = ReviewForm()

    return render(request, 'product_detail.html', {
        'product': product,
        'reviews': reviews,
        'form': form,
    })

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        files = request.FILES.getlist('images')

        if form.is_valid():
            product = form.save(commit=False)  # Don't save yet
            
            # Ensure the category exists
            if not product.category:
                messages.error(request, "Please select a valid category.")
                return redirect('add_product')

            # Assign the logged-in user as the seller
            product.seller = request.user  

            # Now save the product
            product.save()

            # Save images
            for file in files:
                Photo.objects.create(product=product, image=file)

            messages.success(request, "Product added successfully!")
            return redirect('dashboard')

    else:
        form = ProductForm()

    return render(request, 'product_create.html', {'form': form})


@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)

    if product.is_sold:
        messages.error(request, "You cannot edit a sold product.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect('dashboard')
    else:
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {'form': form})



@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product, defaults={'quantity': 1, 'card': None})
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"{product.name} added to cart!")
    return redirect('cart')


@login_required
def remove_from_cart(request, cart_id):
    cart_item = Cart.objects.get(id=cart_id, user=request.user)
    cart_item.delete()
    return redirect('cart')


@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})


import logging
logger = logging.getLogger(__name__)

@login_required
def profile_user(request):
    logger.info(f"Request user: {request.user} (Type: {type(request.user)})")
    myuser = Myuser.objects.get(user=request.user)
    
    # Fetch user's card details
    card = Card.objects.filter(user=request.user).first()

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        product = get_object_or_404(Product, id=product_id)

        # Get or create user's Myuser profile
        user_profile, created = Myuser.objects.get_or_create(user=request.user)

        # Get or create a cart item
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
        cart_item.quantity = quantity
        cart_item.save()

        messages.success(request, 'Cart updated successfully.')
        return redirect('profile_user')

    return render(request, 'profile_user.html', {'myuser': myuser, 'card': card})



@login_required
def checkout(request):
    user_profile = request.user.myuser
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    if user_profile.funds < total_price:
        messages.error(request, "Insufficient funds!")
        return redirect('cart')

    # Deduct funds from buyer
    user_profile.funds -= total_price
    user_profile.save()

    # Transfer funds and mark products as sold
    for item in cart_items:
        item.product.is_sold = True
        item.product.save()

        # Transfer funds to the seller
        seller_profile = item.product.seller.myuser
        seller_profile.funds += item.product.price * item.quantity
        seller_profile.save()

        # Create transaction log
        Transaction.objects.create(
            buyer=request.user,
            seller=item.product.seller,
            product=item.product,
            amount=item.product.price * item.quantity
        )

        item.delete()  # Remove item from cart after purchase

    messages.success(request, "Purchase successful!")
    return redirect('dashboard')



@login_required
def update_card(request):
    myuser = Myuser.objects.get(user=request.user)
    
    if request.method == 'POST':
        card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')
        cardholder_name = request.POST.get('cardholder_name')
        amount = request.POST.get('amount')
        # Here you would save the card information to the user's profile or another model
        messages.success(request, 'Card information updated successfully.')
        Card.objects.create(user=request.user, card_number=card_number, expiration_date=expiry_date, cvv=cvv, cardholder_name=cardholder_name, amount=amount)
        return redirect('profile')
    return render(request, 'profile_user.html', {'myuser': myuser})


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


""" def add_to_cart(request, product_id):
@login_required
   
    # Create an order entry
    Order.objects.create(user=user, product=product, quantity=cart_item.quantity, total_price=product.price * cart_item.quantity)
    
    messages.success(request, 'Product added to cart and order created successfully.')
    return redirect('dashboard') """