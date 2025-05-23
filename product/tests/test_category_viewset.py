import json
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from django.urls import reverse

from product.factories import CategoryFactory
from order.factories import UserFactory
from product.models import Category

class TestCategoryViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user = UserFactory()  # Criar usuário para autenticação
        self.category = CategoryFactory(title='Books', slug='books', description='Book category', active=True)

    def test_get_all_category(self):
        response = self.client.get(
            reverse('category-list', kwargs={'version': 'v1'})
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        category_data = json.loads(response.content)
        
        self.assertEqual(category_data[0]['title'], self.category.title)
        self.assertEqual(category_data[0]['slug'], self.category.slug)
        self.assertEqual(category_data[0]['description'], self.category.description)
        self.assertEqual(category_data[0]['active'], self.category.active)
        
    def test_create_category(self):
        data = json.dumps({
            'title': 'Tech',
            'slug': 'tech',
            'description': 'Technology books',
            'active': True
        })
        
        # Autenticar o usuário
        self.client.force_authenticate(user=self.user)
        
        response = self.client.post(
            reverse('category-list', kwargs={'version': 'v1'}),
            data=data,
            content_type='application/json'
        )
        
        print(f"Request data: {data}")  # Depuração
        print(f"Response content: {response.content}")  # Depuração
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        created_category = Category.objects.get(title='Tech')
        self.assertEqual(created_category.title, 'Tech')
        self.assertEqual(created_category.slug, 'tech')
        self.assertEqual(created_category.description, 'Technology books')
        self.assertEqual(created_category.active, True)