from celery import shared_task
from django.conf import settings
from google import genai

from norsk.apps.words.services.word_extractor import WordExtractorService


@shared_task
def parse_words_from_materials(lesson_id: str, material_ids: list[str]):
    from norsk.apps.lessons.models import Lesson, LessonMaterial
    from norsk.apps.words.models import Word

    # Preload all materials to minimize database hits
    lesson = Lesson.objects.get(id=lesson_id)
    materials = LessonMaterial.objects.filter(
        id__in=material_ids, lesson_id=lesson_id
    ).select_related("lesson")

    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    uploaded_files = [
        client.files.upload(file=material.file.path) for material in materials
    ]

    with WordExtractorService(client=client, files=uploaded_files) as extractor:
        Word.objects.bulk_create(
            [
                Word(
                    lesson=lesson,
                    user=lesson.user,
                    word=word.word,
                    translation=word.translation,
                    word_type=word.type,
                )
                for word in extractor.extract_words().response
            ]
        )
