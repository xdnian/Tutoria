from django.contrib import admin

# Register your models here.
from .models import Wallet, Transaction, Coupon

admin.site.register(Wallet)
admin.site.register(Transaction)
admin.site.register(Coupon)