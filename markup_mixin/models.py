import logging
import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.markup.templatetags import markup


MARKUP_HTML = 'h'
MARKUP_MARKDOWN = 'm'
MARKUP_REST = 'r'
MARKUP_TEXTILE = 't'
MARKUP_OPTIONS = getattr(settings, 'MARKUP_OPTIONS', (
        (MARKUP_HTML, _('HTML/Plain Text')),
        (MARKUP_MARKDOWN, _('Markdown')),
        (MARKUP_REST, _('ReStructured Text')),
        (MARKUP_TEXTILE, _('Textile'))
    ))
MARKUP_DEFAULT = getattr(settings, 'MARKUP_DEFAULT', MARKUP_MARKDOWN)

MARKUP_HELP = _("""Select the type of markup you are using with this model.
<ul>
<li><a href="http://daringfireball.net/projects/markdown/basics" target="_blank">Markdown Guide</a></li>
<li><a href="http://docutils.sourceforge.net/docs/user/rst/quickref.html" target="_blank">ReStructured Text Guide</a></li>
<li><a href="http://thresholdstate.com/articles/4312/the-textile-reference-manual" target="_blank">Textile Guide</a></li>
</ul>""")

class MarkupOptions(object):
    """ Class handling per-model markup options. """
    rendered_field = None
    source_field = None

    def __init__(self, opts):
        for key, value in opts.__dict__.iteritems():
            setattr(self, key, value)

class MarkupBase(models.base.ModelBase):
    def __init__(cls, name, bases, attrs):
        parents = [b for b in bases if isinstance(b, MarkupBase)]
        if not parents:
            return
        ''' Parse MarkupOptions and store them under _markup on the object. '''
        user_opts = getattr(cls, 'MarkupOptions', None)
        opts = MarkupOptions(user_opts)
        setattr(cls, '_markup', opts)

class MarkupMixin(models.Model):
    markup = models.CharField(max_length=1, choices=MARKUP_OPTIONS, default=MARKUP_DEFAULT, help_text=MARKUP_HELP)

    __metaclass__  = MarkupBase
    class Meta:
        abstract=True

    class MarkupOptions:
        pass

    def save(self, *args, **kwargs):
        ''' Only try to pre-render if the options have been set.'''
        if self._markup.rendered_field and self._markup.source_field:
            logging.debug('Rendering markup for %s to %s.' % (self._markup.source_field, self._markup.rendered_field))
            self.do_render_markup()
        super(MarkupMixin, self).save(*args, **kwargs)

    def do_render_markup(self):
        """Turns any markup into HTML"""

        original = self._rendered
        if self.markup == MARKUP_MARKDOWN:
            rendered = markup.markdown(self._source)
        elif self.markup == MARKUP_REST:
            rendered = markup.restructuredtext(self._source)
        elif self.markup == MARKUP_TEXTILE:
            rendered = markup.textile(self._source)
        else:
            rendered = self._source

        setattr(self, self._markup.rendered_field, rendered)
        return (rendered != original)

    @property
    def _source(self):
        return getattr(self, self._markup.source_field)

    @property
    def _rendered(self):
        return getattr(self, self._markup.rendered_field)

