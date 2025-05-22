from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from product.models import Product
from order.models import Order
from product.factories import ProductFactory
from order.factories import OrderFactory, UserFactory

class OrderModelTest(TestCase):
    def test_create_order(self):
        # Testa a criação de um pedido
        product = ProductFactory()
        order = OrderFactory(product=[product])
        self.assertTrue(isinstance(order, Order))
        self.assertTrue(isinstance(order.user, User))
        self.assertEqual(order.product.count(), 1)
        self.assertEqual(str(order), f"Order for {order.user.username}")

    def test_order_product_not_empty(self):
        # Testa a restrição blank=False no ManyToManyField
        with self.assertRaises(ValidationError):
            order = OrderFactory(product=[])
            order.clean()

    def test_order_product_relation(self):
        # Testa a relação ManyToMany com Product
        product1 = ProductFactory()
        product2 = ProductFactory()
        order = OrderFactory(product=[product1, product2])
        self.assertEqual(order.product.count(), 2)
        self.assertIn(product1, order.product.all())
        self.assertIn(product2, order.product.all())

    def test_order_user_relation(self):
        # Testa a relação ForeignKey com User
        user = UserFactory(username="testuser")
        order = OrderFactory(user=user, product=[ProductFactory()])
        self.assertEqual(order.user, user)
        self.assertEqual(order.user.username, "testuser")

    def test_order_user_not_nullable(self):
        # Testa que user não pode ser null (null=False)
        with self.assertRaises(Exception):
            order = Order(user=None, product=[ProductFactory()])
            order.full_clean()

    def test_order_cascade_delete(self):
        # Testa o comportamento on_delete=CASCADE para User
        user = UserFactory()
        product = ProductFactory()
        order = OrderFactory(user=user, product=[product])
        user_id = user.id
        user.delete()
        self.assertFalse(Order.objects.filter(id=order.id).exists())