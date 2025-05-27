import json
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from product.factories import ProductFactory, CategoryFactory
from product.models import Product

class TestProductViewSet(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='user', password='user')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.product = ProductFactory(title="Book", price=100)
        
    def test_get_all_product(self):
        response = self.client.get(
            reverse('product-list', kwargs={'version': 'v1'})
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        product_data = json.loads(response.content)['results']
        self.assertIsInstance(product_data, list)
        self.assertGreaterEqual(len(product_data), 1)
        self.assertEqual(product_data[0]['title'], self.product.title)
        self.assertEqual(product_data[0]['price'], self.product.price)
        self.assertEqual(product_data[0]['active'], self.product.active)
        
    def test_create_product(self):
        category = CategoryFactory()
        data = json.dumps({
            'title': 'New Book',
            'price': 150,
            'categories_id': [category.id]
        })
        
        response = self.client.post(
            reverse('product-list', kwargs={'version': 'v1'}),
            data=data,
            content_type='application/json'
        )
        
        print(f"Request data: {data}")
        print(f"Response content: {response.content}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        created_product = Product.objects.get(title='New Book')
        self.assertEqual(created_product.title, 'New Book')
        self.assertEqual(created_product.price, 150)