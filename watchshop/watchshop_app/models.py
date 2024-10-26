from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.exceptions import ValidationError

# Custom user model
# new_admin_username, your_secure_password


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username

# Profile model associated with CustomUser


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True)
    fullname = models.CharField(max_length=100, blank=True)
    dob = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.user.username


class Watchlist(models.Model):
    brand = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='static\watchshop_app\watches')
    stock = models.IntegerField(default=0)
    available = models.BooleanField(default=True)
    discount = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00)  # in percentage

    def __str__(self):
        return f"{self.brand}"


class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    watch = models.ForeignKey(Watchlist, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s Wishlist - {self.watch.brand}"


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    watch = models.ForeignKey(Watchlist, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username}'s Cart - {self.watch.brand}"


class Review(models.Model):
    watch = models.ForeignKey(
        'Watchlist', related_name='reviews', on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    rating = models.PositiveIntegerField(default=1)
    review_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Only check for user and watch if they are already assigned
        if hasattr(self, 'user') and hasattr(self, 'watch'):
            if Review.objects.filter(user=self.user, watch=self.watch).exists():
                raise ValidationError("You have already reviewed this watch.")

    def __str__(self):
        return f"{self.user.username} - {self.watch.brand} ({self.rating} stars)"
