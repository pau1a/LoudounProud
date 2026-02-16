from django.test import Client, TestCase

from .models import SiteSettings


class HomeViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_renders(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Loudoun")

    def test_about_renders(self):
        response = self.client.get("/about/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Brian")

    def test_robots_txt(self):
        response = self.client.get("/robots.txt")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/plain")
        self.assertContains(response, "Sitemap")


class SiteSettingsTests(TestCase):
    def test_singleton(self):
        s1 = SiteSettings.load()
        s2 = SiteSettings.load()
        self.assertEqual(s1.pk, s2.pk)
        self.assertEqual(s1.pk, 1)
