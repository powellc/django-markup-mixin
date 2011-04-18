from django.utils import unittest
from models import TestModel

class MarkupMixinTest(unittest.TestCase):
    def setUp(self):
        obj = TestModel.objects.create(title='Test case', content='Test case content\n============================\n\nA simple example case using markdown.')
        obj.save()

    def test_rendering(self):
        "Basic test of rendering ability."

        assert self.obj.rendered_content == '<h1>Test case content</h1>\n\r\n\r<p>A simple example case using markdown.</p>'
    
