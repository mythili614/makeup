import razorpay
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Product, Category, Cart, Order

client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)


def home(request):
    products = Product.objects.all()[:6]
    categories = Category.objects.all()
    return render(request, "glowify/home.html", {
        "products": products,
        "categories": categories
    })


def shop(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, "glowify/shop.html", {
        "products": products,
        "categories": categories
    })


def category_products(request, id):
    category = get_object_or_404(Category, id=id)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()
    return render(request, "glowify/shop.html", {
        "products": products,
        "categories": categories,
        "category": category
    })


def cart(request):
    items = []
    total = 0

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            total += item.product.price * item.quantity
            items.append(item)
    else:
        cart = request.session.get('cart', {})
        for product_id, qty in cart.items():
            product = Product.objects.get(id=product_id)
            total += product.price * qty
            items.append({
                'product': product,
                'quantity': qty
            })

    return render(request, 'glowify/cart.html', {
        'items': items,
        'total': total
    })


def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)

    if request.user.is_authenticated:
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
    else:
        cart = request.session.get('cart', {})
        cart[str(id)] = cart.get(str(id), 0) + 1
        request.session['cart'] = cart

    return redirect('cart')


@login_required(login_url='login')
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        return redirect('cart')

    total = sum(item.product.price * item.quantity for item in cart_items)
    amount = int(total * 100)

    payment = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": "1"
    })

    return render(request, "glowify/checkout.html", {
        "items": cart_items,
        "total": total,
        "payment": payment,
        "razorpay_key": settings.RAZORPAY_KEY_ID
    })


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # ✅ NEXT HANDLE (IMPORTANT)
            next_url = request.POST.get('next')

            if next_url:
                return redirect(next_url)
            else:
                return redirect('home')

        else:
            return render(request, "glowify/login.html", {"error": "Invalid Username or Password"})

    return render(request, "glowify/login.html")
def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "glowify/my_orders.html", {"orders": orders})


@login_required
def cancel_order(request, id):
    order = Order.objects.get(id=id, user=request.user)
    order.status = "Cancelled"
    order.save()
    return redirect("my_orders")


def payment_success(request):
    request.session['cart'] = {}
    return render(request, "glowify/order_success.html")


def track_order(request, id):
    order = Order.objects.get(id=id)
    return render(request, "glowify/track_order.html", {"order": order})


def increase_qty(request, id):
    item = Cart.objects.filter(user=request.user, product_id=id).first()
    if item:
        item.quantity += 1
        item.save()
    return redirect('cart')


def decrease_qty(request, id):
    item = Cart.objects.filter(user=request.user, product_id=id).first()
    if item and item.quantity > 1:
        item.quantity -= 1
        item.save()
    return redirect('cart')


def remove_from_cart(request, id):
    item = Cart.objects.filter(user=request.user, product_id=id).first()
    if item:
        item.delete()
    return redirect('cart')


def about(request):
    return render(request, "glowify/about.html")


def contact(request):
    return render(request, "glowify/contact.html")


def offers(request):
    return render(request, "glowify/offers.html")




def payment_success(request):
    request.session['cart'] = {}

    # ✅ latest order fetch
    order = Order.objects.last()

    return render(request, "glowify/order_success.html", {
        "order": order
    })