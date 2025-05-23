import json
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from django.urls import reverse

from product.factories import ProductFactory, CategoryFactory
from order.factories import UserFactory
from product.models import Product

class TestProductViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user = UserFactory()
        self.product = ProductFactory(title="Book", price=100)
        
    def test_get_all_product(self):
        response = self.client.get(
            reverse('product-list', kwargs={'version': 'v1'})
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        product_data = json.loads(response.content)
        
        self.assertEqual(product_data[0]['title'], self.product.title)
        self.assertEqual(product_data[0]['price'], self.product.price)
        self.assertEqual(product_data[0]['active'], self.product.active)
        
    def test_create_product(self):
        category = CategoryFactory()
        data = json.dumps({
            'title': 'New Book',
            'price': 150,
            'categories_id': [category.id]  # Enviar lista de IDs
        })
        
        # Autenticar o usuario
        self.client.force_authenticate(user=self.user)
        
        response = self.client.post(
            reverse('product-list', kwargs={'version': 'v1'}),
            data=data,
            content_type='application/json'
        )
        
        print(f"Request data: {data}")  # Depuracao
        print(f"Response content: {response.content}")  # Depuracao
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        created_product = Product.objects.get(title='New Book')
        self.assertEqual(created_product.title, 'New Book')
        self.assertEqual(created_product.price, 150)