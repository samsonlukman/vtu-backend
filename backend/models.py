from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    profile_pics = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    country = models.CharField(max_length=255, blank=True, null=True)
    account_reference = models.CharField(max_length=500, blank=True, null=True)
    account_number = models.IntegerField(blank=True, null=True)
    account_balance = models.FloatField(blank=True, null=True, default=0)
    flutter_secret_key = models.CharField(max_length=200, default="Bearer FLWSECK-fab12578d0fa352253f89fd6a7b7b713-18f55ce05d4vt-X")

    def increment_account_balance(self, amount):
        self.account_balance = float(amount)
        self.save()
    
    


    def __str__(self):
        return f"{self.username}, Phone number: {self.phone_number}, Verified: {self.is_verified}, account_balance: {self.account_balance} account_reference: {self.account_reference}, account_number: {self.account_number}, secret_key: {self.flutter_secret_key}"


class Airtime(models.Model):
    NETWORK_CHOICES = [
        ('MTN', 'MTN'),
        ('AIRTEL', 'AIRTEL'),
        ('GLO', 'GLO'),
        ('9MOBILE', '9MOBILE'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    network = models.CharField(max_length=100, choices=NETWORK_CHOICES)
    phone_number = models.CharField(max_length=20)
    successful = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.amount} to {self.network} number: {self.phone_number}"
    

class Transactions(models.Model):
    tx_ref = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    
    def __str__(self):
        return f"status: {self.status}, transaction_id: {self.transaction_id}, tx_ref: {self.tx_ref}"

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f"{self.user.username}: {self.text}"


  
