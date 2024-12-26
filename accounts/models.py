from django.db import models


# Create your models here.
class Users(models.Model):
    uuid = models.UUIDField(primary_key=True)
    password = models.CharField(null=False, max_length=50)
    nickname = models.CharField(null=False, max_length=50)

    def __str__(self):
        return self.uuid
