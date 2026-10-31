from django.urls import path

from . import views

app_name = "words"
urlpatterns = [
    path("extract/", views.ExtractWordsView.as_view(), name="extract_words"),
]
