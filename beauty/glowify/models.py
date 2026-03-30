from django.db import models
from django.contrib.auth.models import User


# CATEGORY

class Category(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



# PRODUCT

class Product(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    name = models.CharField(max_length=200)

    description = models.TextField()

    brand = models.CharField(max_length=100, default="Glowify")

    color = models.CharField(max_length=100, default="Red")

    price = models.IntegerField()

    offer_price = models.IntegerField(null=True, blank=True)

    stock = models.IntegerField(default=10)

    image = models.ImageField(upload_to="products/")

    rating = models.FloatField(default=4.5)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



# CART

class Cart(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.IntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product.name)



# ORDER

class Order(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    address = models.TextField()

    total_price = models.IntegerField()

    razorpay_order_id = models.CharField(max_length=200, null=True, blank=True)

    paid = models.BooleanField(default=False)

    status = models.CharField(
        max_length=50,
        default="Ordered"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Order " + str(self.id)