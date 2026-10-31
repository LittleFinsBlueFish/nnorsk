from google import genai

from norsk.apps.gemini.models import GeminiTask

__all__ = ["BaseGeminiService"]


class Handler:
    """A context manager for handling Gemini tasks."""

    def __init__(self, gemini_task: GeminiTask):
        self.gemini_task = gemini_task

    def __enter__(self):
        self.gemini_task.status = GeminiTask.Status.IN_PROGRESS
        self.gemini_task.save()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            self.gemini_task.status = GeminiTask.Status.FAILED
            self.gemini_task.response = str(exc_value)
        else:
            self.gemini_task.status = GeminiTask.Status.COMPLETED
        self.gemini_task.save()


class BaseGeminiService:
    """
    Base class for services that interact with the Gemini API.

    It contains handler logic for managing Gemini tasks and provides a
    structure for subclasses to implement specific functionality.

    To create a new service, subclass this class and implement the required
    methods. Use the `Handler` context manager to manage the lifecycle of Gemini tasks.

    For example, you can use it as follows:
        class MyGeminiService(BaseGeminiService):
            def perform_task(self):
                ...
                with Handler(gemini_task) as handler:
                    # Your logic here
                    pass
                ...
    """

    def __init__(self, client: genai.Client):
        self.client = client

    def __enter__(self):
        self.gemini_task = GeminiTask.objects.create(
            name=f"{self.__class__.__name__} Task"
        )
        self.handler = Handler(self.gemini_task)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.handler = None

        if exc_type is not None:
            self.gemini_task.status = GeminiTask.Status.FAILED
            self.gemini_task.response = str(exc_value)

    def get_handler(self) -> Handler:
        if self.handler is None:
            raise RuntimeError(
                "Handler is not initialized. Use the context manager to manage the lifecycle of the Gemini task."
            )
        return self.handler
