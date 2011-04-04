django-markup-mixin
===================

A simple django reusable application to provide markup control over a field in a model. Right now this is pretty hacked together, but should become more robust over time. Either way, I've found it quite useful in many places already.

On big benefit? You can provide both a markup field, and a rendered content field, meaning expensive per-template markup rendering operations can be relegated to only the simplest of text areas. Big content areas can be re-rendered on each model save.

Installation
-------------

In three easy steps!

1. Place 'markup-mixin' in your installed apps.
2. Add:

        from markup-mixin.models import MarkupMixin

3. Make sure your model inherits the mixin: 

        class YourModel(MarkupMixin): 
            ...

4. Set the markup field options on your model:
        
        def MarkupOptions:
            source_field = <your markup content field>
            rendered_field = <your rendered content field>

That's it. One major caveat, because of the hacky nature of this project, **you must place MarkupMixin at the front of your model inheritance list!** This should be fixed eventually, but right now it has something to do with how the model's save() function is overridden.

Usage
------

With the steps above taken, managing your marked up items is fairly straightforward:

    >>> obj = YourModel.objects.get(pk=1)
    >>> obj.content
    u'This is a markdown **formated** text area.'
    >>> obj.rendered_content
    u'<p>This is a markdown <strong>formated</formated> text area.</p>'

Future
------

Figure out why it must come first in the inheritance list and perhaps even add support for multiple markup rendered fields.