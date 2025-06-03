from django.test import TestCase
from django.core.exceptions import ValidationError
from product.models import Category, Product
from product.factories import ProductFactory, CategoryFactory

class CategoryModelTest(TestCase):
    def test_create_category(self):
        category = CategoryFactory()
        self.assertTrue(isinstance(category, Category))
        self.assertEqual(str(category), category.title)
        self.assertTrue(category.active)

    def test_category_title_max_length(self):
        category = CategoryFactory(title='a' * 255)
        self.assertEqual(len(category.title), 255)
        with self.assertRaises(ValidationError):
            category = Category(title='a' * 255)
            category.full_clean()

    def test_category_slug_unique(self):
        CategoryFactory(slug='test-slug')
        category = Category(slug='test-slug')
        with self.assertRaises(ValidationError):
            category.full_clean()

    def test_category_description_nullable(self):
        category = CategoryFactory(description=None)
        self.assertIsNone(category.description)
        category = CategoryFactory(description='')
        self.assertEqual(category.description, '')

    def test_category_active_default(self):
        category = CategoryFactory(active=False)
        self.assertFalse(category.active)
        category = CategoryFactory()
        self.assertTrue(category.active)

    def test_category_unicode_method(self):
        category = CategoryFactory(title="Fiction")
        self.assertEqual(str(category), "Fiction")

class ProductModelTest(TestCase):
    def test_create_product(self):
        product = ProductFactory()
        self.assertTrue(isinstance(product, Product))
        self.assertTrue(product.active)
        self.assertTrue(product.price > 0)
        self.assertEqual(str(product), product.title)

    def test_product_title_max_length(self):
        product = ProductFactory(title='a' * 255)
        self.assertEqual(len(product.title), 255)
        with self.assertRaises(ValidationError):
            product = ProductFactory.build(title='a' * 256)  # Use build() here
            product.full_clean()

    def test_product_description_nullable(self):
        product = ProductFactory(description=None)
        self.assertIsNone(product.description)
        product = ProductFactory(description='')
        self.assertEqual(product.description, '')

    def test_product_price_nullable(self):
        product = ProductFactory(price=None)
        self.assertIsNone(product.price)
        product = ProductFactory(price=100)
        self.assertEqual(product.price, 100)

    def test_product_category_relation(self):
        category1 = CategoryFactory()
        category2 = CategoryFactory()
        product = ProductFactory(category=[category1, category2])
        self.assertEqual(product.category.count(), 2)
        self.assertIn(category1, product.category.all())
        self.assertIn(category2, product.category.all())

    def test_product_category_blank(self):
        product = ProductFactory(category=[])
        self.assertEqual(product.category.count(), 0)

    def test_product_active_default(self):
        product = ProductFactory(active=False)
        self.assertFalse(product.active)
        product = ProductFactory()
        self.assertTrue(product.active)