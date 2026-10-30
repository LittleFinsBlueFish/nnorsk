from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DeleteView

from norsk.apps.lessons.models import LessonMaterial


class LessonMaterialsDeleteView(LoginRequiredMixin, DeleteView):
    model = LessonMaterial
    template_name = "lessons/lesson_material_delete.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def get_success_url(self):
        lesson_id = self.object.lesson.id
        return reverse("lessons:lesson_detail", kwargs={"pk": lesson_id})
