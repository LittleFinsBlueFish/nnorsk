from django.db import models

from norsk.apps.core.models import BaseModel


class Lesson(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    content = models.TextField()

    def __str__(self):
        return self.title
