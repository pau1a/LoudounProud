from django.test import Client, TestCase


class HomeViewTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_home_renders(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ready to build")

# Create your tests here.
