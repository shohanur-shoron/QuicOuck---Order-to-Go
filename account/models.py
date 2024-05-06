from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='proPic', null=True, blank=True)
    phone = models.CharField(max_length=20)
    
    
    isStore = models.BooleanField(default=False)
    storeName = models.CharField(max_length=100, blank=True, null=True)
    storeDescription = models.TextField(null=True, blank=True)
    storeAddress = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.first_name

