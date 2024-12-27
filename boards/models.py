from datetime import datetime

from django.db import models

from accounts.models import Users


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    is_opened = models.BooleanField(default=False)
    depth1 = models.CharField(max_length=20, null=False)
    depth2 = models.CharField(max_length=20, null=True)
    depth3 = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.id

    class Meta:
        db_table = "category"


class Board(models.Model):
    uuid = models.UUIDField(primary_key=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=1)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=250)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.now, null=False)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.uuid)

    class Meta:
        db_table = "board"


class Comment(models.Model):
    uuid = models.UUIDField(primary_key=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    board_id = models.ForeignKey(Board, on_delete=models.CASCADE)
    content = models.CharField(max_length=200, null=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.now, null=False)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.uuid)

    class Meta:
        db_table = "comment"
