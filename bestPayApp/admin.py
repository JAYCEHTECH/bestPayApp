from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models
from .models import CustomUser
# Register your models here.


class CustomUserAdmin(UserAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone']

    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }))


class AirtimeTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'airtime_amount', 'airtime_number', 'reference', 'provider', 'transaction_date']
    search_fields = ['reference']


class MTNBundleTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'bundle_number', 'offer', 'reference', 'transaction_date', "transaction_status"]
    search_fields = ['reference']


class VodafoneBundleTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'bundle_number', 'offer', 'reference', 'transaction_date', "transaction_status"]
    search_fields = ['reference']


class OtherMTNBundleTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'bundle_number', 'offer', 'reference', 'transaction_date', "transaction_status"]
    search_fields = ['reference']


class AirtelTigoBundleTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'bundle_number', 'offer', 'reference', 'transaction_date', "transaction_status"]
    search_fields = ['reference']


class SikaKokooBundleTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'bundle_number', 'offer', 'reference', 'transaction_date', "transaction_status"]
    search_fields = ['reference']


class IShareBundleTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'bundle_number', 'offer', 'reference', 'transaction_date', 'message']
    search_fields = ['reference']


class TvTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'account_number', 'amount', 'reference', 'transaction_date', "transaction_status"]
    search_fields = ['reference']


class ProductAdmin(admin.ModelAdmin):
    ...


class CartAdmin(admin.ModelAdmin):
    ...


class OrderAdmin(admin.ModelAdmin):
    ...


class OrderItemAdmin(admin.ModelAdmin):
    ...


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(models.AirtimeTransaction, AirtimeTransactionAdmin)
admin.site.register(models.MTNBundleTransaction, MTNBundleTransactionAdmin)
admin.site.register(models.VodafoneBundleTransaction, VodafoneBundleTransactionAdmin)
admin.site.register(models.OtherMTNBundleTransaction, OtherMTNBundleTransactionAdmin)
admin.site.register(models.AirtelTigoBundleTransaction, AirtelTigoBundleTransactionAdmin)
admin.site.register(models.SikaKokooBundleTransaction, SikaKokooBundleTransactionAdmin)
admin.site.register(models.IShareBundleTransaction, IShareBundleTransactionAdmin)
admin.site.register(models.TvTransaction, TvTransactionAdmin)

admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Cart, CartAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderItem, OrderItemAdmin)


