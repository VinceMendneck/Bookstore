import json
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from product.factories import ProductFactory, CategoryFactory
from order.factories import OrderFactory, UserFactory
from product.models import Product
from order.models import Order

class TestOrderViewSet(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # Criar o usuário adminuser
        self.user = User.objects.create_user(username='adminuser', password='adminuser')
        # Gerar token para adminuser
        self.token = Token.objects.create(user=self.user)
        # Autenticar com o token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.category = CategoryFactory(title="Fiction")
        self.product = ProductFactory(title="Book", price=100, category=[self.category])
        self.order = OrderFactory(product=[self.product], user=self.user)

    def test_order(self):
        response = self.client.get(
            reverse('order-list', kwargs={'version': 'v1'})
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        order_data = json.loads(response.content)['results']
        self.assertIsInstance(order_data, list)
        self.assertGreaterEqual(len(order_data), 1)
        self.assertEqual(order_data[0]['product'][0]['title'], self.product.title)
        self.assertEqual(order_data[0]['product'][0]['price'], self.product.price)
        self.assertEqual(order_data[0]['product'][0]['active'], self.product.active)
        self.assertEqual(order_data[0]['product'][0]['category'][0]['title'], self.category.title)
        
    def test_create_order(self):
        product = ProductFactory()
        data = json.dumps({
            'products_id': [product.id],
            'user': self.user.id
        })
        
        response = self.client.post(
            reverse('order-list', kwargs={'version': 'v1'}),
            data=data,
            content_type='application/json'
        )
        
        print(f"Request data: {data}")
        print(f"Response content: {response.content}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        created_order = Order.objects.filter(user=self.user).latest('id')