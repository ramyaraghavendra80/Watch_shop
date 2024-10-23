from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Email field as unique identifier
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True)

    def __str__(self):
        return self.user.username


class Watchlist(models.Model):
    brand = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='watches/')
    stock = models.IntegerField(default=0)
    available = models.BooleanField(default=True)
    discount = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00)  # in percentage

    def __str__(self):
        return f"{self.brand}"


class Wishlist(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    watches = models.ManyToManyField(Watchlist, related_name='wishlists')

    def __str__(self):
        return f"{self.user.username}'s Wishlist"

# class Order(models.Model):
#     user = models.Fore
# ignKey(User, on_delete=models.CASCADE)
#     watches = models.ManyToManyField(Watch, through='OrderItem')
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Order #{self.id} by {self.user.username}"

# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     watch = models.ForeignKey(Watch, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1)
#     price = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f"{self.watch.name} in order #{self.order.id}"

# class Cart(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Cart of {self.user.username}"

# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
#     watch = models.ForeignKey(Watch, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1)

#     def __str__(self):
#         return f"{self.quantity}x {self.watch.name} in {self.cart.user.username}'s cart"
