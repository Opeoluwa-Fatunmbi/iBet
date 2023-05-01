from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


#----------------#
class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['email']

class UserInfo(models.Model):

    ACCOUNT_TYPE_CHOICES = [
        ('User', 'User'),
        ('Rider', 'Rider'),   
    ]
    VEHICLE_TYPE_CHOICES = [
        ('Bicycle', 'Bicycle'),
        ('Car', 'Car'),
        ('Electric Bicycle', 'Electric Bicycle'),
        ('Scooter', 'Scooter')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_info")
    fullname = models.CharField(max_length=100, blank=True)
    cpf = models.CharField(max_length=11, unique=True)
    account_type = models.CharField(choices=ACCOUNT_TYPE_CHOICES, max_length=5)
    profile_photo = models.ImageField(upload_to="profile_photo", blank=True, null=True)
    dob = models.DateField()
    postal_code = models.CharField(max_length=10)
    vehicle_type = models.CharField(choices=VEHICLE_TYPE_CHOICES,max_length=20)
    verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username}'s User Info"
    
class UserContact(models.Model):
    CONTACT_TYPE_CHOICES = (
        ("Email", "Email"),
        ("Phone", "Phone")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_contact")
    contact_type = models.CharField(max_length=7, choices=CONTACT_TYPE_CHOICES)
    contact_detail = models.CharField(max_length=70)
    
    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "contact_type", "contact_detail"], name="unique_user_contact")]
