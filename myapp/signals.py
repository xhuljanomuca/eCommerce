from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Category

@receiver(post_migrate)
def create_default_categories(sender, **kwargs):
    if sender.name == "myapp":  # Replace "myapp" with your app's name
        default_categories = [
            ('real_estate', 'Real Estate'),
            ('cars', 'Cars'),
            ('tech', 'Tech Products'),
            ('furniture', 'Furniture'),
            ('clothing', 'Clothing'),
            ('sports', 'Sports'),
            ('books', 'Books'),
            ('toys', 'Toys'),
        ]
        for code, name in default_categories:
            Category.objects.get_or_create(name=code)
