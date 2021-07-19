from django.contrib import admin
from .models import Order, OrderDetails

admin.site.register(Order)
admin.site.register(OrderDetails)