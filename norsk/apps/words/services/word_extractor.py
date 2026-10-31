from google import genai
from google.genai import types
from pydantic import BaseModel, Field

from norsk.apps.gemini.models import GeminiTask
from norsk.apps.gemini.services import BaseGeminiService
from norsk.apps.words.models import Word


class WordModel(BaseModel):
    type: Word.WordType = Field(
        description="The type of the word, e.g., verb, substantiv, adjektiv, uttrykk, or other."
    )
    word: str = Field(description="The base or citation form of the word.")
    translation: str = Field(
        description="The translation of the word. If no translation is available, it will be '<<translation_required>>'."
    )


class OutputModel(BaseModel):
    response: list[WordModel]


class WordExtractorService(BaseGeminiService):
    model = "gemma-4-26b-a4b-it"
    system_prompt = """You are an expert linguistic data extraction assistant. Your task is to accurately extract words, parts of speech, and translations from the provided study sheets containing Norwegian (Nynorsk) vocabulary and their translations.
# Extraction Rules
## 1. Type Mapping
Map the section headers from the source material to one of the following standardized categories:
* `verb` (includes verbs and verb phrases like \"Verb og verbuttrykk\")
* `substantiv` (nouns)
* `adjektiv` (adjectives)
* `uttrykk` (expressions, phrases, ord og uttrykk)
* `other` (for any words that do not fit into the above categories)
## 2. Word Formatting
* Extract the base or citation form of the word.
* For verbs, include the infinitive marker (e.g., \"å begynne\").
* For nouns, if the word is presented in a declension/inflection table, extract **only** the base ubestemt eintal (indefinite singular) form (e.g., \"Ei barneoppdraging\", \"Eit faktum\"), dropping other case/definiteness forms from the entry.
* If a word is composite or separated, combine or represent the core word correctly based on the entry.
## 3. Translation Handling
* Extract the handwritten or printed translation provided in the image.
* If no translation is available or legible, output precisely: `<<translation_required>>`."""

    def __init__(self, client: genai.Client, files: list[types.File]):
        self.client = client
        self.gemini_task: GeminiTask | None = None
        self.contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_uri(
                        file_uri=uploaded_file.uri, mime_type=uploaded_file.mime_type
                    )
                    for uploaded_file in files
                ],
            ),
        ]

        self.tools = [
            types.Tool(googleSearch=types.GoogleSearch()),
        ]

        self.generate_content_config = types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(
                thinking_level="MINIMAL",
            ),
            audio_transcription_config=types.AudioTranscriptionConfig(),
            tools=self.tools,
            response_mime_type="application/json",
            response_schema=OutputModel,
            system_instruction=[
                types.Part.from_text(
                    text=self.system_prompt,
                ),
            ],
        )

    def extract_words(self) -> OutputModel:
        with self.get_handler():
            response = self.client.models.generate_content(
                model=self.model,
                contents=self.contents,
                config=self.generate_content_config,
            )

            return response.parsed
