import razorpay
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Cart, Order

client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)


def home(request):

    products = Product.objects.all()[:6]
    categories = Category.objects.all()

    return render(request,"glowify/home.html",{
        "products":products,
        "categories":categories
    })


def shop(request):

    products = Product.objects.all()
    categories = Category.objects.all()

    sort = request.GET.get("sort")

    if sort == "low":
        products = products.order_by("price")

    if sort == "high":
        products = products.order_by("-price")

    return render(request,"glowify/shop.html",{
        "products":products,
        "categories":categories
    })


def category_products(request, id):

    category = get_object_or_404(Category, id=id)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()

    return render(request,"glowify/shop.html",{
        "products":products,
        "categories":categories,
        "category":category
    })


def cart(request):

    items = []
    total = 0

    if request.user.is_authenticated:
        items = Cart.objects.filter(user=request.user)

        for item in items:
            total += item.product.price * item.quantity

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




def checkout(request):

    items = []
    total = 0

    cart_items = Cart.objects.filter(user=request.user)

    for item in cart_items:

        total += item.product.price * item.quantity

        items.append({
            "product": item.product,
            "quantity": item.quantity
        })

    if total == 0:
        return redirect('cart')

    amount = int(total * 100)

    payment = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": "1"
    })

    return render(request,"glowify/checkout.html",{
        "items":items,
        "total":total,
        "payment":payment,
        "razorpay_key":settings.RAZORPAY_KEY_ID
    })


def track_order(request, id):

    order = Order.objects.get(id=id)

    return render(request,"glowify/track_order.html",{
        "order":order
    })


def offers(request):
    return render(request,'glowify/offers.html')


def about(request):
    return render(request,"glowify/about.html")


def contact(request):
    return render(request,'glowify/contact.html')


def login_view(request):
    return render(request,'glowify/login.html')


def increase_qty(request, id):

    item = Cart.objects.filter(product_id=id).first()

    if item:
        item.quantity += 1
        item.save()

    return redirect('cart')

def decrease_qty(request, id):

    item = Cart.objects.filter(product_id=id).first()

    if item:
        if item.quantity > 1:
            item.quantity -= 1
            item.save()

    return redirect('cart')

def remove_cart(request, id):

    item = Cart.objects.filter(product_id=id).first()

    if item:
        item.delete()

    return redirect('cart')

def cart_count(request):

    if request.user.is_authenticated:
        count = Cart.objects.filter(user=request.user).count()
    else:
        count = 0

    return {'cart_count': count}

@login_required
def my_orders(request):

    orders = Order.objects.filter(user=request.user).order_by("-created_at")

    return render(request,"glowify/my_orders.html",{
        "orders":orders
    })


@login_required
def cancel_order(request,id):

    order = Order.objects.get(id=id,user=request.user)

    order.status = "Cancelled"
    order.save()

    return redirect("my_orders")

def payment_success(request):

    request.session['cart'] = {}   # cart clear

    order_id = request.GET.get('order_id')

    if not order_id:
        return redirect('home')

    order = Order.objects.get(id=order_id)

    return render(request,"glowify/order_success.html",{
        "order":order
    })
def remove_from_cart(request, id):

    cart = request.session.get('cart', {})

    if str(id) in cart:
        del cart[str(id)]

    request.session['cart'] = cart

    return redirect('checkout')   # cart இல்லை checkout