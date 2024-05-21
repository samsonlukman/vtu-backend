from django.contrib import admin
from .models import User, Airtime, History, Transactions

# Register your models here.
admin.site.register(User)
admin.site.register(Airtime)
admin.site.register(History)
admin.site.register(Transactions)
