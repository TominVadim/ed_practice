from django.test import TestCase
from store.models import Product, Category

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Тест')
    
    def test_product_creation(self):
        product = Product.objects.create(
            article='TEST001',
            name='Тестовый товар',
            category=self.category,
            price=1000,
            stock_quantity=10
        )
        self.assertEqual(product.article, 'TEST001')
