from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('shop/', views.shop, name='shop'),

    path('category/<int:id>/', views.category_products, name='category_products'),

    path('cart/', views.cart, name='cart'),

    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),

    path('offers/', views.offers, name="offers"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('login/', views.login_view, name='login'),

    path('checkout/', views.checkout, name='checkout'),

    path("payment-success/", views.payment_success, name="payment_success"),

    path('track-order/<int:id>/', views.track_order, name='track_order'),

    path("increase/<int:id>/", views.increase_qty, name="increase_qty"),
    path("decrease/<int:id>/", views.decrease_qty, name="decrease_qty"),

    path('remove-from-cart/<int:id>/', views.remove_from_cart, name='remove_from_cart'),

    path('my-orders/', views.my_orders, name="my_orders"),
    path('cancel-order/<int:id>/', views.cancel_order, name="cancel_order"),
]