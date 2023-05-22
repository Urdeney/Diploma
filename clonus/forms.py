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
