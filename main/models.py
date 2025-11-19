from django.db import models
from django.contrib.auth.models import User

# ---------------------------
# Product Model
# ---------------------------
class Product(models.Model):
    name = models.CharField(max_length=255)
    image_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# ---------------------------
# Retailer Model
# ---------------------------
class Retailer(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.name

# ---------------------------
# Price History Model
# ---------------------------
class PriceHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE)
    price = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.product.name} - {self.retailer.name} - {self.price}"

# ---------------------------
# User Profile Model (for OTP verification)
# ---------------------------
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
