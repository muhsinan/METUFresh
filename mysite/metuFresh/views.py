from django.shortcuts import render, redirect
from .models import Product, Customer, Restaurant
from .forms import ProductForm
from django.contrib import messages


def main_view(request):
    return render(request, "metuFresh/main.html")


def home_view(request):
    products = Product.objects.all()

    if 'user_type' in request.session and request.session['user_type'] == 'restaurant' and 'email' in request.session:
        restaurant = Restaurant.objects.filter(
            email=request.session['email']).first()
        products = Product.objects.filter(restaurant=restaurant)
    else:
        products = Product.objects.all()
    return render(request, "metuFresh/home.html", {"products": products})


def navbar_view(request):
    return render(request, "metuFresh/navbar.html")


def product_view(request, pk):
    product = Product.objects.get(id=pk)
    context = {"product": product}

    return render(request, "metuFresh/product.html", context)


# def create_product(request):
#     form = ProductForm()
#     if request.method == "POST":
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("home")
#     context = {'form': form}
#     return render(request, "metuFresh/product_form.html", context)


def create_product(request):
    form = ProductForm()
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            if Product.objects.filter(name=name).exists():
                messages.error(
                    request, 'A product with this name already exists.')
            else:
                form.save()
                return redirect("home")
    context = {'form': form}
    return render(request, "metuFresh/product_form.html", context)


def update_product(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {'form': form}
    return render(request, "metuFresh/product_form.html", context)


def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == "POST":
        product.delete()
        return redirect("home")

    context = {'product': product}
    return render(request, "metuFresh/delete.html", context)


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Replace the following line with your own authentication logic
        is_restaurant = request.POST.get('is_restaurant')
        if is_restaurant:
            restaurant = Restaurant.objects.filter(
                email=email, password=password).first()
            if restaurant is not None:
                request.session['is_logged_in'] = True
                request.session['user_type'] = 'restaurant'
                request.session['email'] = email
                return redirect('home')
        else:
            customer = Customer.objects.filter(
                email=email, password=password).first()
            if customer is not None:
                request.session['is_logged_in'] = True
                request.session['user_type'] = 'customer'
                return redirect('home')
    # If the login attempt failed, render the login form again
    return render(request, "metuFresh/login.html")


def logout_view(request):
    if 'is_logged_in' in request.session:
        del request.session['is_logged_in']
    if 'cart' in request.session:
        del request.session['cart']
    if 'user_type' in request.session:
        del request.session['user_type']
    return redirect('home')


def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone_number')
        address = request.POST.get('address')
        email = request.POST.get('username')
        password = request.POST.get('password')
        is_restaurant = request.POST.get('is_restaurant')
        if Customer.objects.filter(email=email).exists():
            # Handle case where username already exists
            return render(request, 'metuFresh/register.html', {'error': 'Username already exists'})
        else:
            if is_restaurant:
                restaurant = Restaurant.objects.create(
                    name=first_name, address=address, email=email, password=password, phone=phone)
                if restaurant is not None:
                    return redirect('home')
            else:
                customer = Customer.objects.create(
                    first_name=first_name, last_name=last_name, address=address, email=email, password=password, phone=phone)
                if customer is not None:
                    return redirect('home')
    return render(request, 'metuFresh/register.html')


def cart_view(request):
    cart = []
    if 'cart' in request.session:
        cart = [int(id) for id in request.session['cart']]  # Convert to int
    products = Product.objects.filter(id__in=cart)
    return render(request, "metuFresh/cart.html", {"products": products})


def add_to_cart(request):
    if request.method == 'POST':
        product_id = int(request.POST.get('product_id'))  # Convert to int
        if 'cart' not in request.session:
            request.session['cart'] = []
        request.session['cart'].append(product_id)
        request.session.save()
        print(request.session['cart'])
        messages.add_message(request, messages.INFO, 'Product added to cart')
        return redirect('home')
    return render(request, "metuFresh/cart.html")


def remove_from_cart(request):
    if request.method == 'POST':
        product_id = int(request.POST.get('product_id'))  # Convert to int
        print(f"Product ID: {product_id}")  # Print the product ID
        if 'cart' in request.session:
            # Print the cart before removal
            print(f"Cart before removal: {request.session['cart']}")
            request.session['cart'].remove(product_id)
            # Print the cart after removal
            print(f"Cart after removal: {request.session['cart']}")
            request.session.save()  # Save the session
            messages.add_message(request, messages.INFO,
                                 'Product removed from cart')
        return redirect('cart')
    return render(request, "metuFresh/cart.html")


def checkout_view(request):
    if request.method == 'POST':

        cart = []
        if 'cart' in request.session:
            cart = [int(id)
                    for id in request.session['cart']]  # Convert to int
        products = Product.objects.filter(id__in=cart)
        for product in products:
            product.stock_quantity -= 1
            product.save()
        request.session['cart'] = []
        request.session.save()
        return redirect('home')
    return render(request, "metuFresh/home.html")


def search_view(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()
    return render(request, 'metuFresh/search.html', {'products': products})
