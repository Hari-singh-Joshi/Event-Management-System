from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm
urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path('users/', views.UserView, name='users'),
    path("contact/", views.contact, name="contact"),
    path("vendor/", views.vendor, name="vendor"),
    path('vendor/add_product/', views.add_product, name='add_product'),
    path('vendor/products/', views.product_list, name='product_list'),
    path('vendor/delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('register/', views.register, name='register'),
    path('ulogin/', views.user_login, name='ulogin'),
    path('user_home/', views.user_home, name='user_home'),
    path('order/', views.order_view, name='order'),  
    path('order-status/', views.order_status_view, name='order_status'),
    path('vendors/', views.vendor_list, name='vendor_list'),
    path('vendor/<str:vendor_id>/', views.vendor_products, name='vendor_products'),
    path('add_to_cart/<str:vendor_id>/', views.add_to_cart, name='add_to_cart'),
    path("cart/", views.show_cart, name="showcart"),
    path("pluscart/", views.plus_cart),
    path("minuscart/", views.minus_cart),
    path("removecart/", views.remove_cart),
    


    #Authentication and Password management
    path("vregistration/", views.VendorResistrationaView.as_view(), name="vregistration"),
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='app/login.html',
        authentication_form=LoginForm
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
        
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
