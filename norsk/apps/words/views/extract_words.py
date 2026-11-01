from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView

from norsk.apps.lessons.models import Lesson
from norsk.apps.words.tasks import parse_words_from_materials


class DummyForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ()  # No fields needed for this form


class ExtractWordsView(LoginRequiredMixin, UpdateView):
    model = Lesson
    template_name = "words/extract_words.html"
    form_class = DummyForm

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def form_valid(self, form):
        materials = self.object.materials.all()
        material_ids = [str(material.id) for material in materials]

        # Call the Celery task to parse words from materials
        parse_words_from_materials.delay(str(self.object.id), material_ids)

        response = super().form_valid(form)
        messages.success(self.request, _("Word extraction started."))
        return response
