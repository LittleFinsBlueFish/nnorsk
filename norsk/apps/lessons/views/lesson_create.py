from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView

from norsk.apps.lessons.models import Lesson


class LessonCreateForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ("title", "description", "content")


class LessonCreateView(LoginRequiredMixin, CreateView):
    model = Lesson
    template_name = "lessons/lesson_create.html"
    form_class = LessonCreateForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, _("Lesson created."))
        return response
