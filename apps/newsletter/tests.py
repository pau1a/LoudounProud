from django.test import Client, TestCase

from .models import Subscriber


class SubscribeViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_subscribe_page_renders(self):
        response = self.client.get("/subscribe/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Subscribe")

    def test_subscribe_creates_subscriber(self):
        response = self.client.post("/subscribe/", {
            "email": "test@example.com",
            "first_name": "Test",
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Subscriber.objects.filter(email="test@example.com").exists())

    def test_subscribe_duplicate_confirmed_email_rejected(self):
        Subscriber.objects.create(
            email="taken@example.com",
            is_confirmed=True,
        )
        response = self.client.post("/subscribe/", {
            "email": "taken@example.com",
        })
        self.assertEqual(response.status_code, 200)  # Re-renders form with error

    def test_confirm_valid_token(self):
        sub = Subscriber.objects.create(email="confirm@example.com")
        response = self.client.get(f"/subscribe/confirm/{sub.confirmation_token}/")
        self.assertEqual(response.status_code, 200)
        sub.refresh_from_db()
        self.assertTrue(sub.is_confirmed)
