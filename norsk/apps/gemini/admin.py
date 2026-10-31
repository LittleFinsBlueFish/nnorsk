from django.contrib import admin

from norsk.apps.gemini.models import GeminiTask


# Register your models here.
@admin.register(GeminiTask)
class GeminiTaskAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "created_at", "updated_at")
    list_filter = ("status",)
    search_fields = ("id",)
