from django.test import TestCase
from app.models import  Logo


class TestLogo(TestCase):
    def setUp(self):
        self.logo = Logo.objects.create(image=None, caption='foo', is_active=True)
        self.logo.save()

    def test_string_representation(self):
        self.assertEqual(self.logo.__str__(), 'foo (Active)')

    def test_only_one_logo_active(self):
        self.assertTrue(self.logo.is_active)

        logo2 = Logo.objects.create(image=None, caption='bar', is_active=True)
        logo2.save()
        self.logo.refresh_from_db()

        self.assertTrue(logo2.is_active)
        self.assertFalse(self.logo.is_active)
