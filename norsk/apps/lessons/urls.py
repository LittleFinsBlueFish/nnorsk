from django.urls import include, path

from . import views

app_name = "lessons"
urlpatterns = [
    path("", views.LessonListView.as_view(), name="lesson_list"),
    path("create/", views.LessonCreateView.as_view(), name="lesson_create"),
    path("<uuid:pk>/", views.LessonDetailView.as_view(), name="lesson_detail"),
    path("<uuid:pk>/delete/", views.LessonDeleteView.as_view(), name="lesson_delete"),
    path("<uuid:pk>/update/", views.LessonUpdateView.as_view(), name="lesson_update"),
    path(
        "<uuid:pk>/upload-materials/",
        views.LessonMaterialsCreateView.as_view(),
        name="lesson_upload_materials",
    ),
    path(
        "materials/<uuid:pk>/delete/",
        views.LessonMaterialsDeleteView.as_view(),
        name="lesson_delete_materials",
    ),
    path("<uuid:pk>/words/", include("norsk.apps.words.urls", namespace="words")),
]
