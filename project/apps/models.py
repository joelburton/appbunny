from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models


class Course(models.Model):
    """A course offering for Hackbright."""

    code = models.SlugField(
        max_length=15,
        primary_key=True,
        help_text="Unique code for this course.",
    )

    name = models.CharField(
        max_length=40,
        unique=True,
        help_text='Name of offering (e.g., "Fellowship")',
    )

    description = models.TextField(
        blank=True,
    )

    def __str__(self):
        return self.name


class ApplicationTemplate(models.Model):
    """A template for an application.

    Applications are semester-specific and tie together a group of questions. For example,
    a template might be for the Spring 2016 Fellowship.
    """

    course = models.ForeignKey(Course)

    name = models.CharField(
        max_length=40,
        unique=True,
        help_text='Name of the template (e.g., "Spring 2016 Fellowship")'
    )

    description = models.TextField(
        blank=True,
    )

    def __str__(self):
        return self.name


class ApplicationTemplateSection(models.Model):
    """A section of an application template.

    The longer applications are divided into multiple sections.
    """

    template = models.ForeignKey(ApplicationTemplate)

    code = models.SlugField(
        max_length=15,
        help_text="Abbreviated unique code for this section.",
    )

    name = models.CharField(
        max_length=50,
        help_text='Name for this section.',
    )

    help_html = models.TextField(
    )


class Question(models.Model):
    """A question on an application."""

    section = models.ForeignKey(ApplicationTemplateSection)

    label = models.CharField(
        max_length=25,
        help_text='Short label to identify this question on reports.',
    )

    question = models.CharField(
        max_length=100,
        help_text='Question as it will be phrased on application',
    )

    position = models.IntegerField(
        help_text='Order of this question as it should appear on survey (low #s appear first)'
    )

    question_type = models.CharField(
        max_length=10,
        choices=[
            ('boolean', 'Yes/No'),
            ('text', 'Text'),
            ('select', 'Select'),
            ('multiselect', 'Select-Multiple'),
            ('file', 'File Upload'),
        ]
    )

    required = models.BooleanField(
        default=True,
    )

    min_words = models.PositiveSmallIntegerField(
        name='Minumum number of words.',
        null=True,
        blank=True,
    )

    vocabulary = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        help_text='Labels for select and select-multiple questions.',
        name='Select/Select-Multiple Options',
    )

    filetypes_allowed = ArrayField(
        models.CharField(max_length=25),
        blank=True,
        help_text='File extensions allowed for uploaded file.',
        default=['pdf', 'doc', 'docx', 'odt']
    )

    class Meta:
        unique_together = [['section', 'label']]
        ordering = ['section', 'position']

    def __str__(self):
        return self.question

    def clean(self):
        """Validate."""

        super(Question, self).clean()
        qt = self.question_type
        vocab = getattr(self, 'vocabulary', None)

        ### FIXME: these don't work, not getting vocab

        if (qt == 'Select' or qt == 'Select-Multiple') and not vocab:
            raise ValidationError(u"Select and Select-Multiple fields must provide a vocabulary.")

        if (qt != 'Select' and qt != 'Select-Multiple' and vocab):
            raise ValidationError(
                u"Only Select and Select-Multiple fields can provide a vocabulary.")


class Application(models.Model):
    """An application."""

    template = models.ForeignKey(ApplicationTemplate)