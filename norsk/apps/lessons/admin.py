from django.contrib import admin

from norsk.apps.lessons.models import Lesson


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "created_at", "updated_at")
    search_fields = ("title", "description")
