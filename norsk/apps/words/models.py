from django.db import models
from django.utils.translation import gettext_lazy as _

from norsk.apps.core.models import BaseModel
from norsk.apps.users.models import UserOwnedModel


class Word(BaseModel, UserOwnedModel):
    class WordType(models.TextChoices):
        SUBSTANTIVE = "substantive", _("Substantive")
        ADJECTIVE = "adjective", _("Adjective")
        VERB = "verb", _("Verb")
        UTTRYKK = "uttrykk", _("Uttrykk")
        OTHER = "other", _("Other")

    lesson = models.ForeignKey(
        "lessons.Lesson", on_delete=models.CASCADE, related_name="words"
    )
    word_type = models.CharField(
        max_length=50, choices=WordType.choices, default=WordType.OTHER
    )
    word = models.TextField()
    translation = models.TextField()
    example = models.TextField(blank=True)

    def __str__(self):
        return self.word
