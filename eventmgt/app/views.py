from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import VendorRegistrationForm, LoginForm, ProductForm, UserRegistrationForm, UserLoginForm
from .models import Product, Vendor, Cart
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q

# Home page view
def home(request):
    return render(request, "app/home.html")

def vendor(request):
    return render(request, "app/vendor.html")

def UserView(request):
    return render(request, "app/user.html")

@login_required
def order_status_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_amount = sum(item.product.Price * item.quantity for item in cart_items)
    shipping_cost = 40
    final_total = total_amount + shipping_cost

    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
        'final_total': final_total,
    }
    return render(request, 'app/orderstatus.html', context)

def order_view(request):
    cart = request.session.get('cart', [])
    return redirect('order_status') if cart else redirect('showcart')

# About page view
def about(request):
    return render(request, "app/about.html")

# Contact page view
def contact(request):
    return render(request, "app/contact.html")

class VendorResistrationaView(View):
    def get(self, request):
        form = VendorRegistrationForm()
        return render(request, "app/vendorregistration.html", locals())

    def post(self, request):
        form = VendorRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! Successfully Registered.")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, "app/vendorregistration.html", locals())

def LoginView(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                auth_login(request, user)
                messages.success(request, "You have successfully logged in.")
                return redirect('vendor')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, "app/login.html", locals())

@login_required
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'app/add_product.html', {'form': form})

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'app/product_list.html', locals())

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        return HttpResponseRedirect(reverse('product_list'))
    return render(request, 'app/confirm_delete.html', locals())

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('user_home')
    else:
        form = UserRegistrationForm()
    return render(request, 'app/register.html', locals())

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('user_home')
    else:
        form = UserLoginForm()
    return render(request, 'app/ulogin.html', locals())

@login_required
def user_home(request):
    return render(request, 'app/user_home.html')

def vendor_list(request):
    users = User.objects.all()
    return render(request, 'app/vendors.html', {'users': users})

def vendor_products(request, vendor_id):
    vendor = get_object_or_404(User, id=vendor_id)
    products = Product.objects.filter(vendor=vendor)
    return render(request, 'app/vendor_products.html', {'vendor': vendor, 'products': products})

@login_required
def add_to_cart(request, vendor_id):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to add items to the cart.")
        return redirect('login')

    product_id = request.GET.get('prod_id')
    product = get_object_or_404(Product, id=product_id, vendor_id=vendor_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, "Product added to cart.")
    return redirect('vendor_products', vendor_id=vendor_id)

def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = sum(item.total_cost for item in cart)
    totalamount = amount + 40
    return render(request, 'app/addtocart.html', {'cart': cart, 'amount': amount, 'totalamount': totalamount})

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        try:
            cart_item = Cart.objects.get(product_id=prod_id, user=request.user)
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Cart item not found'}, status=404)

        cart_item.quantity += 1
        cart_item.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = sum(item.total_cost for item in cart)
        totalamount = amount + 40

        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'totalamount': totalamount,
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        try:
            cart_item = Cart.objects.get(Q(product_id=prod_id) & Q(user=request.user))
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Cart item not found'}, status=404)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = sum(item.total_cost for item in cart)
        totalamount = amount + 40

        data = {
            'quantity': cart_item.quantity if cart_item.quantity > 0 else 0,
            'amount': amount,
            'totalamount': totalamount,
        }
        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        carts = Cart.objects.filter(Q(product_id=prod_id) & Q(user=request.user))

        if carts.exists():
            carts.delete()
            user = request.user
            cart_items = Cart.objects.filter(user=user)
            amount = sum(item.total_cost for item in cart_items)
            totalamount = amount + 40
            data = {
                'quantity': 0,
                'amount': amount,
                'totalamount': totalamount
            }
        else:
            data = {
                'quantity': 0,
                'amount': 0,
                'totalamount': 40
            }

        return JsonResponse(data)
