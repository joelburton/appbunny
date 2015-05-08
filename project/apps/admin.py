from django.contrib import admin
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.http import HttpResponseRedirect

from .models import ApplicationTemplate, Course, Question, ApplicationTemplateSection
from .forms import QuestionForm


class ApplicationTemplateInline(admin.TabularInline):
    """Inline to just show links to survey templates on semester form."""

    fields = ['name']
    readonly_fields = ['name']
    extra = 0
    model = ApplicationTemplate
    show_change_link = True
    can_delete = False
    has_add_permission = lambda x, y: False  # don't allow adding


# noinspection PyMethodMayBeStatic
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Course admin form."""

    fields = [
        'code',
        'name',
        'description',
        'num_templates',
        'num_applications'
    ]

    list_display = [
        'code',
        'name',
        'num_templates',
        'num_applications'
    ]

    list_display_links = ['code', 'name']

    inlines = [ApplicationTemplateInline]

    readonly_fields = [
        'num_templates',
        'num_applications'
    ]

    # ordering = ['start_date']

    def num_templates(self, obj):
        url = '/admin/feedback/applicationtemplate/?course_code__exact=%s' % obj.code
        return u'%s <a href="%s" target="_blank">(view)</a>' % (obj.num_templates, url)

    num_templates.short_description = '# Templates'
    num_templates.allow_tags = True

    def num_applications(self, obj):
        url = '/admin/feedback/application/?template_course__code__exact=%s' % obj.code
        return u'%s <a href="%s" target="_blank">(view)</a>' % (obj.num_applications, url)

    num_applications.short_description = '# Applications'
    num_applications.allow_tags = True

    def get_queryset(self, request):
        """Add counts for phones, templates, and applications."""

        qs = super(CourseAdmin, self).get_queryset(request)
        return qs.annotate(
            num_templates=Count('applicationtemplate', distinct=True),
            num_applications=Count('applicationtemplate__application', distinct=True)
        )


class ApplicationTemplateSectionInline(admin.StackedInline):
    """Inline for questions for application template sections."""

    model = ApplicationTemplateSection
    # form = QuestionForm
    extra = 0


# noinspection PyMethodMayBeStatic
@admin.register(ApplicationTemplate)
class ApplicationTemplateAdmin(admin.ModelAdmin):
    """Application template form."""

    def copy_templates(modeladmin, request, queryset):
        """Copy application template to a different course."""

        ids = ",".join(str(template.id) for template in queryset.all())
        return HttpResponseRedirect(reverse("template.copy") + "?ids=%s" % ids)

    copy_templates.short_description = "Copy templates to a different course"

    actions = [copy_templates]

    fields = [
        'course',
        'name',
        'description',
        'num_applications',
    ]

    list_display = [
        'id',
        'name',
        'course',
        'description',
        'num_applications',
    ]

    list_display_links = ['id', 'name']

    list_filter = ['course']

    readonly_fields = ['num_applications']

    inlines = [ApplicationTemplateSectionInline]

    def num_applications(self, obj):
        url = '/admin/feedback/application/?template__id__exact=%s' % obj.id
        return u'%s <a href="%s" target="_blank">(view)</a>' % (obj.num_applications, url)

    num_applications.short_description = '# Surveys'
    num_applications.allow_tags = True

    # def results(self, obj):
    #     """Show links to results page."""
    #
    #     if obj and obj.id:
    #         url = reverse("survey.template", kwargs={'pk': obj.id})
    #         return "<a href='%s'>Results</a>" % url
    #     return "(None)"
    #
    # results.allow_tags = True

    def get_queryset(self, request):
        """Get counts for applications."""

        qs = super(ApplicationTemplateAdmin, self).get_queryset(request)
        return qs.annotate(
            num_applications=Count('application', distinct=True),
        )


class QuestionInline(admin.StackedInline):
    """Inline for questions for survey template form."""

    model = Question
    form = QuestionForm
    extra = 0


@admin.register(ApplicationTemplateSection)
class ApplicationTemplateSectionAdmin(admin.ModelAdmin):
    """Application template section form."""

    fields = [
        'template',
        'code',
        'name',
        'help_html',
    ]

    list_display = [
        'code',
        'name',
                'template',

    ]

    list_display_links = ['code', 'name']

    list_filter = ['template']

    inlines = [QuestionInline]
