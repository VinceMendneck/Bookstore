from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from product.models import Product
from order.models import Order
from product.factories import ProductFactory
from order.factories import OrderFactory, UserFactory

class OrderModelTest(TestCase):
    def test_create_order(self):
        product = ProductFactory()
        user = UserFactory()
        order = OrderFactory(product=[product], user=user)
        self.assertTrue(isinstance(order, Order))
        self.assertTrue(isinstance(order.user, User))
        self.assertEqual(order.product.count(), 1)
        self.assertEqual(str(order), f"Order for {order.user.username}")

    def test_order_product_not_empty(self):
        with self.assertRaises(ValidationError):
            order = OrderFactory(product=[])
            order.clean()

    def test_order_product_relation(self):
        product1 = ProductFactory()
        product2 = ProductFactory()
        user = UserFactory()
        order = OrderFactory(product=[product1, product2], user=user)
        self.assertEqual(order.product.count(), 2)
        self.assertIn(product1, order.product.all())
        self.assertIn(product2, order.product.all())

    def test_order_user_relation(self):
        user = UserFactory(username="testuser")
        order = OrderFactory(user=user, product=[ProductFactory()])
        self.assertEqual(order.user, user)
        self.assertEqual(order.user.username, "testuser")

    def test_order_user_not_nullable(self):
        product = ProductFactory()
        temp_user = UserFactory()
        order = Order(user=temp_user)
        order.save()
        order.product.add(product)
        order.user = None
        with self.assertRaises(ValidationError):
            order.full_clean()

    def test_order_cascade_delete(self):
        user = UserFactory()
        product = ProductFactory()
        order = OrderFactory(user=user, product=[product])
        user_id = user.id
        user.delete()
        self.assertFalse(Order.objects.filter(id=order.id).exists())