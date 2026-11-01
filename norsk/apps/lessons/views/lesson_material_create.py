from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView

from norsk.apps.core.forms.fields import MultipleFileField
from norsk.apps.lessons.models import Lesson


class LessonMaterialsCreateForm(forms.ModelForm):
    materials = MultipleFileField(label=_("Materials"))

    class Meta:
        model = Lesson
        fields = ("materials",)


class LessonMaterialsCreateView(LoginRequiredMixin, UpdateView):
    model = Lesson
    template_name = "lessons/lesson_material_create.html"
    form_class = LessonMaterialsCreateForm

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def form_valid(self, form):
        uploaded_files = self.request.FILES.getlist("materials")

        for file in uploaded_files:
            self.object.materials.create(
                file=file, title=file.name, user=self.request.user
            )

        response = super().form_valid(form)
        messages.success(self.request, _("Materials uploaded."))
        return response
