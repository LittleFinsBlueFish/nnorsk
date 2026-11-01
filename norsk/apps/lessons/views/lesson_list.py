from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.views.generic import ListView

from norsk.apps.lessons.models import Lesson


class LessonListView(LoginRequiredMixin, ListView):
    model = Lesson
    template_name = "lessons/lesson_list.html"
    context_object_name = "lessons"

    def get_queryset(self):
        queryset = super().get_queryset()
        return (
            queryset.filter(user=self.request.user)
            .annotate(
                word_count=Count("words", distinct=True),
                material_count=Count("materials", distinct=True),
            )
            .order_by("-created_at")
        )
