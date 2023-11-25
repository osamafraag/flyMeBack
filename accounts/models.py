from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from countries.models import city,country
from cities_light.abstract_models import AbstractRegion

class MyUser(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'Prefer not to say'),
    ]
    passport_number = models.CharField(max_length=20)
    passport_expire_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20)
    image = models.ImageField(upload_to='accounts/', blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    activation_link_created_at = models.DateTimeField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    country = models.ForeignKey(country, on_delete=models.SET_NULL, null=True, blank=True,related_name='users')
    city = models.ForeignKey(city, on_delete=models.SET_NULL, null=True, blank=True,related_name='users')
    region = models.ForeignKey(AbstractRegion, on_delete=models.SET_NULL, null=True, blank=True,related_name='users')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    post_code = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email_verification_code = models.CharField(max_length=6, blank=True, null=True)
    activation_code = models.CharField(max_length=6, blank=True, null=True)


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            if not self.wallet:
                pass
        except:
            wallet = Wallet()
            wallet.user = self
            wallet.save()
        

    @classmethod
    def get_all_users(cls):
        return cls.objects.all()
    

class PaymentCard(models.Model):
    TYPES = [
        ('VISA', 'Visa'),
        ('MASTER', 'Master Card'),
        ('MEZA', 'Meza')
    ]
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    type = models.CharField(choices=TYPES)
    cardholder_name = models.CharField(max_length=100)
    card_number = models.CharField(max_length=16)
    expiration_date = models.DateField()
    CVV = models.CharField(max_length=4)

    class Meta:
        unique_together = ('user', 'type',)


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAWAL', 'Withdrawal'),
        ('WPURCHASE', 'Wallet Purchase'),
        ('CPURCHASE', 'Card Purchase'),
    ]
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    amount = models.FloatField(default=0, validators=[MinValueValidator(0)])
    date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)

    def save(self, *args, **kwargs):
        if self.type == 'WPURCHASE':
            if self.amount <=  0 : 
                raise ValidationError({'totalCost':'amount must be greater than Zero'})
            if self.user.wallet.available_balance < self.amount:
                raise ValidationError({'totalCost':'amount is bigger than your balance'})
            self.user.wallet.available_balance -= self.amount
            self.user.wallet.save()
        elif self.type == 'WITHDRAWAL':
            if self.amount <=  0 : 
                raise ValidationError({'totalCost':'amount must be greater than Zero'})
            if self.user.wallet.available_balance < self.amount:
                raise ValidationError({'totalCost':'amount is bigger than your balance'})
            self.user.wallet.available_balance -= self.amount
            self.user.wallet.withdrawal += self.amount
            self.user.wallet.save()
        elif self.type == 'DEPOSIT':
            self.user.wallet.available_balance += self.amount
            self.user.wallet.save()
        super().save(*args, **kwargs)



class Wallet(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE,related_name='wallet')
    available_balance = models.FloatField(default=0, null=True, blank=True)
    pendding_balance = models.FloatField(default=0, null=True, blank=True)
    withdrawal = models.FloatField(default=0, null=True, blank=True)

    def clean(self) :
        pass
        
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Complaint(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),  
        ('RESOLVED', 'Resolved'), 
        ('CLOSED', 'Closed'),  
        ('REOPENED', 'Reopened'),  
    ]
    user_id = models.ForeignKey(MyUser, on_delete=models.CASCADE,null=True)
    description = models.TextField()
    answer = models.TextField(blank=True)
    status = models.CharField(choices=STATUS_CHOICES)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.answer != '' and self.user_id:
            notification = Notification()
            notification.user = self.user_id
            notification.title = "Your Complaint Answer!"
            notification.description = f"{self.answer}  \n Reply For -> {self.description}"
            notification.save()
    
        super().save(*args, **kwargs)


class Notification(models.Model):
    statuses = [
        ('READ', 'Read'),
        ('UNREAD', 'Unread')
    ]
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,related_name='notifications')
    title = models.CharField()
    description = models.CharField()
    date = models.DateTimeField(auto_now_add=True)
    readDate = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=statuses, default='UNREAD')

    def clean(self) :
        if self.status == 'UNREAD':
            self.readDate = None
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class PasswordResetToken(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


