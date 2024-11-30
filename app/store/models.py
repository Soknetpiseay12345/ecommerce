from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    id = models.BigAutoField(primary_key=True) 
    name = models.CharField(max_length=255)
    image_url = models.URLField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
# Shopping Cart model
class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Use the built-in User model
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user.username}"  # Use 'username' to represent the user in string representation

# Cart Item model (products in the shopping cart)
class CartItem(models.Model):
    cart = models.ForeignKey(ShoppingCart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # This is where the quantity is defined

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"