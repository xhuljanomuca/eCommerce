from django.urls import path
from myapp import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('user/', views.user, name='user'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('home/', views.dashboard, name='dashboard'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/add/', views.product_create, name='product_create'),
    path('product/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('trending_product/<int:product_id>/', views.trending_product_detail, name='trending_product_detail'),
    path('cart/', views.view_cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('profile/', views.profile_user, name='profile_user'),
    path('update_card/', views.update_card, name='update_card'),
    path('checkout/', views.checkout, name='checkout'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)