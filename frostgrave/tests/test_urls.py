from django.test import TestCase
from django.urls import reverse


class TestUrls(TestCase):

    def test_games(self):
        url = reverse('games_list')
        self.assertEqual(url, '/')
