from datetime import datetime

from django.db import models

from accounts.models import Users


class SoftDeleteManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, default=None)
    objects = models.Manager()
    undeleted_objects = SoftDeleteManager()

    def soft_delete(self):
        self.deleted_at = datetime.now()
        self.is_deleted = True
        self.save()

    def restore(self):
        self.deleted_at = None
        self.is_deleted = False
        self.save()

    class Meta:
        abstract = True


class Category(SoftDeleteModel):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    is_opened = models.BooleanField(default=False)
    depth1 = models.CharField(max_length=20, null=False, unique=True)
    depth2 = models.CharField(max_length=20, null=True)
    depth3 = models.CharField(max_length=20, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = "category"


class Board(SoftDeleteModel):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=1)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=250)
    created_at = models.DateTimeField(default=datetime.now, null=False)
    updated_at = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = "board"


class Comment(SoftDeleteModel):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    board_id = models.ForeignKey(Board, on_delete=models.CASCADE)
    content = models.CharField(max_length=200, null=False)
    created_at = models.DateTimeField(default=datetime.now, null=False)
    updated_at = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = "comment"
