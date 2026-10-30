from django.contrib import admin

from norsk.apps.lessons.models import Lesson, LessonMaterial


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "created_at", "updated_at")
    search_fields = ("title", "description")


@admin.register(LessonMaterial)
class LessonMaterialAdmin(admin.ModelAdmin):
    list_display = ("lesson", "file", "created_at", "updated_at")
    search_fields = ("lesson__title",)
