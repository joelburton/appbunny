from django.forms import ModelForm, Textarea, CharField
from django.contrib.postgres.forms import SimpleArrayField

from .models import Question


class QuestionForm(ModelForm):
    """Question form; used by admin.

    This form overrides the default one we'd get; this is used for the likert field to
    show as a textarea with each answer on a line, rather than as a text input with each
    answer separated by commas.
    """

    vocabulary = SimpleArrayField(
        CharField(max_length=50),
        delimiter="\r",
        widget=Textarea(attrs={'cols': 50, 'rows': 8}),
        required=False,
        help_text="Put each option on a separate line."
    )

    def clean_vocabulary(self):
        """There may be newlines left on the values; strip these off."""

        return [label.strip("\n") for label in self.cleaned_data['vocabulary']]

    class Meta:
        model = Question
        exclude = []
