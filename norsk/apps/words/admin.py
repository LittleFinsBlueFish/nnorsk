from django.contrib import admin

from norsk.apps.words.models import Word


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ("id", "lesson", "word_type", "word", "translation")
    list_filter = ("word_type",)
    search_fields = ("word", "translation")
