from django.db import models

from norsk.apps.core.models import BaseModel
from norsk.apps.users.models import UserOwnedModel


class Lesson(BaseModel, UserOwnedModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    content = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("lessons:lesson_detail", kwargs={"pk": self.pk})


def get_material_upload_path(instance, filename):
    return (
        f"lesson_materials/{instance.lesson.id}/{instance.id}.{filename.split('.')[-1]}"
    )


class LessonMaterial(BaseModel, UserOwnedModel):
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="materials"
    )
    title = models.CharField(max_length=255)
    file = models.ImageField(upload_to=get_material_upload_path)

    def __str__(self):
        return self.title
