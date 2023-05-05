from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


#----------------#
class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class UserInfo(models.Model):

    ACCOUNT_TYPE_CHOICES = [
        ('User', 'User'),
        ('Mediator', 'Mediator'),   
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_info")
    fullname = models.CharField(max_length=100, blank=True)
    account_type = models.CharField(choices=ACCOUNT_TYPE_CHOICES, max_length=5)
    profile_photo = models.ImageField(upload_to="profile_photo", blank=True, null=True) #Use Cloudinary here
    dob = models.DateField()
    
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
