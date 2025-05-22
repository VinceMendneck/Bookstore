from django.test import TestCase
from django.core.exceptions import ValidationError
from product.models import Category, Product
from product.factories import CategoryFactory, ProductFactory

class CategoryModelTest(TestCase):
    def test_create_category(self):
        # Testa a criação de uma categoria
        category = CategoryFactory()
        self.assertTrue(isinstance(category, Category))
        self.assertEqual(str(category), category.title)
        self.assertTrue(category.active)

    def test_category_title_max_length(self):
        # Testa o limite de comprimento do campo title
        category = CategoryFactory(title='a' * 255)
        self.assertEqual(len(category.title), 255)
        with self.assertRaises(ValidationError):
            CategoryFactory(title='a' * 256).full_clean()

    def test_category_slug_unique(self):
        # Testa a restrição de unicidade do slug
        category1 = CategoryFactory(slug='test-slug')
        with self.assertRaises(Exception):
            CategoryFactory(slug='test-slug').full_clean()

    def test_category_description_nullable(self):
        # Testa que description pode ser null ou blank
        category = CategoryFactory(description=None)
        self.assertIsNone(category.description)
        category = CategoryFactory(description='')
        self.assertEqual(category.description, '')

    def test_category_active_default(self):
        # Testa o valor padrão de active
        category = CategoryFactory(active=False)
        self.assertFalse(category.active)
        category = CategoryFactory()
        self.assertTrue(category.active)

    def test_category_unicode_method(self):
        # Testa o método __unicode__
        category = CategoryFactory(title="Fiction")
        self.assertEqual(str(category), "Fiction")

class ProductModelTest(TestCase):
    def test_create_product(self):
        # Testa a criação de um produto
        product = ProductFactory()
        self.assertTrue(isinstance(product, Product))
        self.assertTrue(product.active)
        self.assertTrue(product.price > 0)
        self.assertTrue(str(product), product.title)

    def test_product_title_max_length(self):
        # Testa o limite de comprimento do campo title
        product = ProductFactory(title='a' * 255)
        self.assertEqual(len(product.title), 255)
        with self.assertRaises(ValidationError):
            ProductFactory(title='a' * 256).full_clean()

    def test_product_description_nullable(self):
        # Testa que description pode ser null ou blank
        product = ProductFactory(description=None)
        self.assertIsNone(product.description)
        product = ProductFactory(description='')
        self.assertEqual(product.description, '')

    def test_product_price_nullable(self):
        # Testa que price pode ser null
        product = ProductFactory(price=None)
        self.assertIsNone(product.price)
        product = ProductFactory(price=100)
        self.assertEqual(product.price, 100)

    def test_product_category_relation(self):
        # Testa a relação ManyToMany com Category
        category1 = CategoryFactory()
        category2 = CategoryFactory()
        product = ProductFactory(category=[category1, category2])
        self.assertEqual(product.category.count(), 2)
        self.assertIn(category1, product.category.all())
        self.assertIn(category2, product.category.all())

    def test_product_category_blank(self):
        # Testa que category pode ser vazio (blank=True)
        product = ProductFactory(category=[])
        self.assertEqual(product.category.count(), 0)

    def test_product_active_default(self):
        # Testa o valor padrão de active
        product = ProductFactory(active=False)
        self.assertFalse(product.active)
        product = ProductFactory()
        self.assertTrue(product.active)