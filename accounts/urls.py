from accounts.models import *
from django.contrib import admin

admin.site.register(MyUser)
admin.site.register(Transaction)
admin.site.register(Wallet)
admin.site.register(PaymentCard)
admin.site.register(Complaint)
admin.site.register(Notification)
admin.site.register(PasswordResetToken)