from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Address(models.Model):
    HOME = "home"
    OFFICE = "office"
    SCHOOL = "school"
    ADDRESSTYPES = (
        (HOME, "Home"),
        (OFFICE, "Office"),
        (SCHOOL, "School"),
    )
    is_default = models.BooleanField(default=False)
    address = models.CharField(max_length=255, blank=False)
    phone = models.CharField(max_length=255, blank=False)
    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    address_type = models.CharField(max_length=10, choices=ADDRESSTYPES, default=HOME)
    
    def __str__(self):
        return "{}/{}".format(self.user_id.username, self.address_type, self.phone)
    

