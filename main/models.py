from django.db import models
from django.contrib.auth.models import User

# ---------------------------
# Product Model
# ---------------------------
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True)


    def __str__(self):
        return self.name

# ---------------------------
# Retailer Model (optional, keep if you want to track multiple retailers)
# ---------------------------
# class Retailer(models.Model):
#     name = models.CharField(max_length=100)
#     url = models.URLField(blank=True, null=True)

#     def __str__(self):
#         return self.name

# ---------------------------
# Price History Model
# ---------------------------
# class PriceHistory(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prices')
#     merchant = models.CharField(max_length=64)  # 'ebay', 'amazon', etc.
#     price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
#     currency = models.CharField(max_length=8, default='EUR')
#     url = models.URLField(max_length=1024, null=True, blank=True)
#     image = models.URLField(max_length=1024, null=True, blank=True)
#     scraped_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['-scraped_at']

#     def __str__(self):
#         return f"{self.product.title} - {self.merchant} - {self.price}"

# ---------------------------
# User Profile Model (for OTP verification)
# ---------------------------
# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     otp_verified = models.BooleanField(default=False)

#     def __str__(self):
#         return self.user.username



class ProductPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prices')
    store_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    url_to_store = models.URLField(blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.store_name} - {self.price}"