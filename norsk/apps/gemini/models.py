from django.db import models

from norsk.apps.core.models import TimeStampedModel


class GeminiTask(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"

    name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    response = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
