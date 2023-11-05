from django.db import models  # import models from django.db
import uuid  # import uuid
from django.db import models  # import models from django.db


class BaseModel(models.Model):  # create BaseModel class
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True, db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class File(BaseModel):  # create File class
    resource_type = models.CharField(max_length=255)  # set mime_type field

    def __str__(self):
        return self.name


class GuestUser(BaseModel):
    def __str__(self) -> str:
        return str(self.id)

    @property
    def is_authenticated(self):
        return True
