from django.urls import path
from myapp import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('user/', views.user, name='user'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home/', views.dashboard, name='dashboard'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('trending_product/<int:product_id>/', views.trending_product_detail, name='trending_product_detail'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]