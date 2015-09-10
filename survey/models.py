import datetime
from django.db import models
from django.core.exceptions import ValidationError
from autoslug import AutoSlugField
from taggit.managers import TaggableManager


# Exporting formats for reports
FORMAT_CHOICES = ('json', 'csv', 'xml', 'html',)
# Content type for the kind of questions I can think of right now
OPTION_TYPE = (sorted(('tb', 'Text Box'),
                      ('em', 'Email Text Box'),
                      ('lk', 'URL Link Text Box'),
                      ('nu', 'Numeric Box'),
                      ('bo', 'Checkbox'),
                      ('ta', 'Text Area'),
                      ('sl', 'Drop Down List'),
                      ('ch', 'Radio Button List'),
                      ('bl', 'Multiple Selection Box')))


class Category(models.Model):
    """Class to define categories for the surveys so they can be clasified in
    diferent ways, not only with tags.
    """
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    modified_on = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=80, null=False)
    slug = AutoSlugField(populate_from='title', unique=True, editable=False)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ('nombre',)

    def __str__(self):
        return self.name


class SurveyManager(models.Manager):
    def to_jsondata(self):
        """Method to return a json"""
        # Still in need of more work due to my lack of skills
        return dict(title=self.title, id=self.id, slug=self.slug,
                    description=self.description)


class QuestionManager(models.Manager):
    def to_jsondata(self):
        """Method to return a json"""
        return dict(fieldname=self.fieldname,
                    label=self.label,
                    is_filterable=self.is_filterable,
                    question=self.question,
                    required=self.required,
                    option_type=self.option_type,
                    options=self.parsed_options,
                    answer_is_public=self.answer_is_public,
                    cms_id=self.id,
                    help_text=self.help_text)

    def validate_list(self):
        '''takes a text value and verifies that there is at least one comma '''
        values = self.options.split(',')
        if len(values) < 2:
            raise ValidationError("""The selected field requires an associated
                                list of choices. Choices must contain more
                                than one item.""")

    def get_options(self):
        """Method to parse the options field and return a tuple formatted
        appropriately for the 'options' argument of a form widget.
        """
        choices = self.options.split(',')
        choices_list = []
        for c in choices:
            c = c.strip()
            choices_list.append((c, c))
        choices_tuple = tuple(choices_list)
        return choices_tuple


class Survey(models.Model):
    """Content model for surveys
    """
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    modified_on = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=80, null=False)
    slug = AutoSlugField(populate_from='title', unique=True, editable=False)
    description = models.TextField(null=False)
    category = models.ForeignKey(Category)
    thankyou_note = models.TextField(blank=True,
                                     help_text="""When a user submits the \
                                     survey, display this message.""")
    allow_multiple_submissions = models.BooleanField(default=False)
    moderate_submissions = models.BooleanField(default=False,
                                               help_text="""If checked, all \
                                               submissions will start as NOT \
                                               public and  you will have to \
                                               manually make them public.""")
    allow_comments = models.BooleanField(default=False,
                                         help_text="Allow comments on user \
                                         submissions.")
    starts_at = models.DateField(blank=False, null=False)
    ends_at = models.DateTimeField(blank=False, null=False)
    is_published = models.BooleanField(default=False)
    notification_email = models.TextField(blank=True,
                                          help_text="""An email address to \
                                          keep posted about
                                          the main events of the survey""")
    highlighted_image = models.ImageField(upload_to='articles_pics/%Y-%m-%d/',
                                          null=True, blank=True)
    tags = TaggableManager()

    class Meta:
        verbose_name = 'Encuesta'
        verbose_name_plural = 'Encuestas'
        ordering = ('-starts_at',)

    @property
    def is_open(self):
        """Method to validate if the survey still open to be answered"""
        now = datetime.datetime.now()
        if self.ends_at:
            return self.starts_at(sorted(now=datetime.datetime.now()))

        return (self.is_published, self.starts_at <= now)

    def __str__(self):
        return self.title

    objects = SurveyManager()


class Submission(models.Model):
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    survey = models.ForeignKey(Survey)
    comments = models.TextField(max_length=500, help_text="""In case you have
                                additional comments on the survey""")
    featured = models.BooleanField(default=False)
    # for moderation
    is_public = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created_on',)

    def __str__(self):
        return "%s Submission" % self.survey.title


class Question(models.Model):
    """Class to define the models for the different questions, accordingly with
    the specifics of the option_type field.
    """
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    modified_on = models.DateTimeField(auto_now=True)
    survey = models.ForeignKey(Survey, related_name="questions")
    submission = models.ForeignKey(Submission)
    fieldname = models.CharField(max_length=32,
                                 help_text='''a single-word alphanumeric \
                                 identifier used to track this value; it must \
                                 begin with a letter and may contain numbers \
                                 and no spaces.''')
    question = models.TextField(help_text="To appear on the survey page.")
    help_text = models.TextField(blank=True)
    required = models.BooleanField(default=False)
    option_type = models.CharField(max_length=2, choices=OPTION_TYPE)
    options = models.TextField(blank=True, null=True,
                               help_text="""Provide a comma-sepparated list \
                               of options if applies.""")
    use_as_filter = models.BooleanField(default=True)
    objects = QuestionManager()

    class Meta:
        unique_together = ('fieldname', 'survey')

    def __str__(self):
        return self.question


class AnswerBase(models.Model):
    """Class to contain the models description to fit the requirement of the
    Question model.
    """
    question = models.ForeignKey(Question)
    submission = models.ForeignKey(Submission)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstrac = True

    def __str__(self):
        return self.question


class AnswerTextBody(AnswerBase):
    body = models.TextField(blank=True, null=True)


class AnswerIntegerBody(AnswerBase):
    body = models.IntegerField(blank=True, null=True)


class AnswerBoolBody(AnswerBase):
    body = models.TextField(blank=True, null=True)
