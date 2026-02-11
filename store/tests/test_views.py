from django.test import TestCase
from django.urls import reverse

class ProductListViewTest(TestCase):
    def test_view_url_exists(self):
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
