from django.test import TestCase
from store.forms import ProductAdminForm

class ProductFormTest(TestCase):
    def test_negative_price_invalid(self):
        form = ProductAdminForm(data={'price': -100})
        self.assertFalse(form.is_valid())
