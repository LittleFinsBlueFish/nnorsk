from django import forms


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    """
    A custom form field that allows multiple file uploads. It uses the MultipleFileInput widget to render the input field and overrides the clean method to handle multiple files.

    Source: https://stackoverflow.com/questions/77212709/django-clearablefileinput-does-not-support-uploading-multiple-files-error
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result
