from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    country = models.CharField(max_length=255, blank=True, null=True)
    account_reference = models.CharField(max_length=500, blank=True, null=True)
    account_number = models.IntegerField(blank=True, null=True)
    account_balance = models.FloatField(blank=True, null=True, default=0)
    

    def increment_account_balance(self, amount):
        self.account_balance = float(amount)
        self.save()
    
    


    def __str__(self):
        return f"{self.username}, Phone number: {self.phone_number}, Verified: {self.is_verified}, account_balance: {self.account_balance} account_reference: {self.account_reference}, account_number: {self.account_number}"


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


  
