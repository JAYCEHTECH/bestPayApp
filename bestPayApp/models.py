from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


# Create your models here.
class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    username = models.CharField(max_length=100, null=False, blank=False, unique=True)
    email = models.EmailField(max_length=250, null=False, blank=False)
    phone = models.PositiveIntegerField(null=True, blank=True)
    password1 = models.CharField(max_length=100, null=False, blank=False)
    password2 = models.CharField(max_length=100, null=False, blank=False)


class AirtimeTransaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField(max_length=250, null=False, blank=True)
    airtime_number = models.PositiveIntegerField(null=False, blank=False)
    airtime_amount = models.FloatField(null=False, blank=True)
    provider = models.CharField(max_length=20, null=False, blank=True)
    reference = models.CharField(max_length=20, null=False, blank=True)
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_status = models.CharField(max_length=100, null=False)

    def __str__(self):
        return f"{self.user.username} - {self.airtime_number} - {self.reference}"


class MTNBundleTransaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField(max_length=250, null=False, blank=True)
    bundle_number = models.PositiveIntegerField(null=False, blank=False)
    offer = models.CharField(max_length=250, null=False, blank=False)
    reference = models.CharField(max_length=20, null=False, blank=True)
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_status = models.CharField(max_length=100, null=False)

    def __str__(self):
        return f"{self.user.username} - {self.bundle_number} - {self.reference}"


class OtherMTNBundleTransaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField(max_length=250, null=False, blank=True)
    bundle_number = models.PositiveIntegerField(null=False, blank=False)
    offer = models.CharField(max_length=250, null=False, blank=False)
    reference = models.CharField(max_length=20, null=False, blank=True)
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_status = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.bundle_number} - {self.reference}"


class VodafoneBundleTransaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField(max_length=250, null=False, blank=True)
    bundle_number = models.PositiveIntegerField(null=False, blank=False)
    offer = models.CharField(max_length=250, null=False, blank=False)
    reference = models.CharField(max_length=20, null=False, blank=True)
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_status = models.CharField(max_length=100, null=False)

    def __str__(self):
        return f"{self.user.username} - {self.bundle_number} - {self.reference}"


class AirtelTigoBundleTransaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField(max_length=250, null=False, blank=True)
    bundle_number = models.PositiveIntegerField(null=False, blank=False)
    offer = models.CharField(max_length=250, null=False, blank=False)
    reference = models.CharField(max_length=20, null=False, blank=True)
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_status = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.bundle_number} - {self.reference}"


class IShareBundleTransaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField(max_length=250, null=False, blank=True)
    bundle_number = models.PositiveIntegerField(null=False, blank=False)
    offer = models.CharField(max_length=250, null=False, blank=False)
    batch_id = models.CharField(max_length=250, null=False, blank=False)
    message = models.CharField(max_length=250, null=False, blank=False)
    reference = models.CharField(max_length=20, null=False, blank=True)
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_status = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.bundle_number} - {self.reference}"


class SikaKokooBundleTransaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField(max_length=250, null=False, blank=True)
    bundle_number = models.PositiveIntegerField(null=False, blank=False)
    offer = models.CharField(max_length=250, null=False, blank=False)
    reference = models.CharField(max_length=20, null=False, blank=True)
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_status = models.CharField(max_length=100, null=False)

    def __str__(self):
        return f"{self.user.username} - {self.bundle_number} - {self.reference}"


class TvTransaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField(max_length=250, null=False, blank=True)
    account_number = models.PositiveIntegerField(null=False, blank=False)
    amount = models.PositiveIntegerField(null=False, blank=False)
    provider = models.CharField(max_length=250, null=False, blank=False)
    reference = models.CharField(max_length=20, null=False, blank=True)
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_status = models.CharField(max_length=100, null=False)

    def __str__(self):
        return f"{self.user.username} - {self.account_number} - {self.reference}"


# ========================== SHOP ============================


class Product(models.Model):
    name = models.CharField(max_length=250, null=False, blank=True)
    product_image = models.CharField(max_length=300, null=False, blank=False)
    description = models.TextField(max_length=600, null=False, blank=False)
    quantity = models.PositiveIntegerField(null=False, blank=False)
    original_price = models.FloatField(null=False, blank=False)
    selling_price = models.FloatField(null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0=default, 1=Hidden")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty = models.PositiveIntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order_name = models.CharField(max_length=300, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    phone = models.PositiveIntegerField(null=False, blank=False)
    address = models.CharField(max_length=400, null=False, blank=False)
    total_price = models.FloatField(null=False, blank=False)
    payment_reference = models.CharField(max_length=100, null=False, blank=False)
    order_statuses = (
        ('Pending', 'Pending'),
        ('Out for Shipping', 'Out for Shipping'),
        ('Completed', 'Completed')
    )
    status = models.CharField(max_length=100, choices=order_statuses, default="Pending")
    tracking_number = models.CharField(max_length=150, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tracking_number} - {self.user} - {self.order_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    tracking_number = models.CharField(max_length=150, null=True)
    quantity = models.PositiveIntegerField(null=False)

    def __str__(self):
        return f"{self.order.tracking_number} - {self.order.user} - {self.order.order_name}"















