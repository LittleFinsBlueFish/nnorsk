from .lesson_create import LessonCreateView
from .lesson_delete import LessonDeleteView
from .lesson_detail import LessonDetailView
from .lesson_list import LessonListView
from .lesson_material_create import LessonMaterialsCreateView
from .lesson_material_delete import LessonMaterialsDeleteView
from .lesson_update import LessonUpdateView

__all__ = [
    "LessonCreateView",
    "LessonDeleteView",
    "LessonDetailView",
    "LessonListView",
    "LessonMaterialsCreateView",
    "LessonMaterialsDeleteView",
    "LessonUpdateView",
]
