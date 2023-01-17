from time import timezone

from django.db import models
import uuid


# Create your models here.

class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True


class Todo(BaseModel):
    todo_title = models.CharField(max_length=100)
    todo_description = models.TextField()
    is_done = models.BooleanField(default=False)


class TimingTodo(BaseModel):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE)
    timing = models.DateField(default='2022-01-20')
