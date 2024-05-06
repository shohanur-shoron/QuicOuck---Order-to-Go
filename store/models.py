from django.db import models
from django.contrib.auth.models import User
from account.models import Profile


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images', null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.PositiveIntegerField(default=0)
    discountPersentage = models.DecimalField(max_digits=3, decimal_places=1)
    discountPrice = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='product_images', null=True, blank=True)
    store = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='products', limit_choices_to={'isStore': True})
    avgReviewPoint = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    totalReviews = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='placed_orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    pickup_time = models.CharField(max_length=100, default='Now')
    store = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='store_orders', limit_choices_to={'isStore': True})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('ready', 'Ready'), ('picked_up', 'Picked Up'), ('cancelled', 'Cancelled')], default='pending')
    cancelReason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.user.first_name}"


class CartItem(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, limit_choices_to={'isStore': False})
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.product.name} in cart of {self.user.user.username}"

class WishList(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, limit_choices_to={'isStore': False})
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.product.name} in cart of {self.user.user.username}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    ratingValue = models.PositiveIntegerField(default=0)
    ratingStar = models.CharField(max_length=100, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} reviewed {self.product.name}"


class UserMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read_by_admin = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject} from {self.user.username}"