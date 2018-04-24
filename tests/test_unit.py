from unittest.mock import Mock
from django.test import TestCase

from app.templatetags.app_tags import footer_promotions, logo


class TestLogoTemplateTag(TestCase):
    def setUp(self):
        obj = Mock()
        obj.site = Mock()
        obj.site.root_page = Mock()
        obj.site.root_page.specific = {}
        self.context = {'request': obj}

    def test_logo_returns_empty_string_with_no_context_for_logo_image(self):
        logo_dict = logo(self.context)
        assert logo_dict['logo_image'] == ''

    def test_logo_returns_empty_string_with_no_context_for_logo_text(self):
        logo_dict = logo(self.context)
        assert logo_dict['logo_text'] == ''

class TestFooterPromotionsTemplateTag(TestCase):
    def setUp(self):
        obj = Mock()
        obj.site = Mock()
        obj.site.root_page = Mock()
        obj.site.root_page.specific = {}
        self.context = {'request': obj}

    def test_footer_promotions_returns_empty_string_with_no_context(self):
        footer_dict = footer_promotions(self.context)
        assert footer_dict['footer_promotions'] == ''
