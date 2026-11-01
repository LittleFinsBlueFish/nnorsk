from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from norsk.apps.lessons.models import Lesson


class LessonDetailView(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = "lessons/lesson_detail.html"
    context_object_name = "lesson"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user).prefetch_related(
            "materials", "words"
        )
