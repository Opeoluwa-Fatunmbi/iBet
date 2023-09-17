from django.db import models
from core.models import BaseModel
from django.contrib.auth.models import AbstractBaseUser
from cloudinary.models import CloudinaryField

# Create your models here.

class User(BaseModel):
    profile_pic = CloudinaryField("image",default=None,null=True)

