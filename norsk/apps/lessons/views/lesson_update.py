from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView

from norsk.apps.lessons.models import Lesson


class LessonUpdateForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ("title", "description", "content")


class LessonUpdateView(LoginRequiredMixin, UpdateView):
    model = Lesson
    template_name = "lessons/lesson_update.html"
    form_class = LessonUpdateForm

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, _("Lesson updated."))
        return response
