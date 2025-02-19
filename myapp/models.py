from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Myuser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, default='Unknown')
    last_name = models.CharField(max_length=255, default='Unknown')
    email = models.EmailField(unique=True,default='Unknown')
    phone = models.CharField(max_length=255, default='Unknown')
    funds = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    address = models.TextField()

    def User(self):
        return self.user

class Category(models.Model):
    CATEGORY_CHOICES = [
        ('real_estate', 'Real Estate'),
        ('cars', 'Cars'),
        ('tech', 'Tech Products'),
        ('furniture', 'Furniture'),
        ('clothing', 'Clothing'),
        ('sports', 'Sports'),
        ('books', 'Books'),
        ('toys', 'Toys'),
    ]
    name = models.CharField(max_length=255, choices=CATEGORY_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    #photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='product_photos', null=True, blank=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    is_sold = models.BooleanField(default=False)
    #quantity = models.IntegerField()

    def __str__(self): 
        return self.name

class Photo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_photos')
    image = models.ImageField(upload_to='photos/')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.description

class TrendingProduct(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='trending_product_photos', default=1)
    quantity = models.IntegerField()

    def __str__(self):
        return self.name

class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return self.review

class Car(models.Model):
    title = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='car_photos', default=1)

    def __str__(self):
        return self.title
    
class House(models.Model):
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100, default='Unknown')
    rooms = models.CharField(max_length=100, default='Unknown')
    property_surface = models.DecimalField(max_digits=7, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    title = models.CharField(max_length=255, default='Unknown')
    type = models.CharField(max_length=100, default='Unknown')
    created_at = models.DateTimeField(auto_now=True)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='house_photos', default=1)

    def __str__(self):
        return self.title
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):  
        return self.product.name

class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    expiration_date = models.DateField()
    cvv = models.CharField(max_length=3)
    cardholder_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)

    def Card(self):
        return self.Card

class Transaction(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions_made', default=1)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions_received', default=1)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, null=True, blank=True)
    transaction_date = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.buyer.username} bought {self.product.name}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
    
