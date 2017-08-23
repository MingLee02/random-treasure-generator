from django.test import TestCase
from django.urls import reverse


class TestUrls(TestCase):
    def test_main(self):
        url = reverse('frostgrave_main')
        self.assertEqual(url, '/')
