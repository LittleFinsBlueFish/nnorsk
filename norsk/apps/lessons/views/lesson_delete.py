from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from norsk.apps.lessons.models import Lesson


class LessonDeleteView(LoginRequiredMixin, DeleteView):
    model = Lesson
    template_name = "lessons/lesson_delete.html"
    success_url = reverse_lazy("lessons:lesson_list")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)
