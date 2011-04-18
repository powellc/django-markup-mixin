from django.db import models
from markup_mixin.models import MarkupMixin

class TestModel(MarkupMixin):
    title = models.CharField('Title', max_length=50)
    content = models.TextField('Content')
    rendered_content = models.TextField('Rendered content', blank=True, null=True)

    def __unicode__():
        return unicode(self.title)
