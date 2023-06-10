from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, Layout, Submit


class FileToFileForm(forms.Form):
    file1 = forms.FileField(label="Файл 1")
    file2 = forms.FileField(label="Файл 2")
    gram_size = forms.IntegerField(
        label="Размер K-граммы", initial=8, min_value=0, max_value=256
    )
    window_size = forms.IntegerField(
        label="Размер окна", initial=3, min_value=0, max_value=32
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "file1",
            "file2",
            "gram_size",
            "window_size",
            Submit("submit", "Обработать", css_class="btn btn-warning btn-lg btn-m"),
        )


class MFInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MFField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MFInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ManyFilesForm(forms.Form):
    files = MFField(label="Файлы")
    gram_size = forms.IntegerField(
        label="Размер K-граммы", initial=8, min_value=0, max_value=256
    )
    window_size = forms.IntegerField(
        label="Размер окна", initial=3, min_value=0, max_value=32
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "files",
            "gram_size",
            "window_size",
            Submit("submit", "Обработать", css_class="btn btn-warning btn-lg btn-m"),
        )
