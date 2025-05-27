import json
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from product.factories import CategoryFactory
from product.models import Category

class TestCategoryViewSet(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='adminuser', password='adminuser')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.category = CategoryFactory(title='Books', slug='books', description='Book category', active=True)

    def test_get_all_category(self):
        response = self.client.get(
            reverse('category-list', kwargs={'version': 'v1'})
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        category_data = json.loads(response.content)['results']
        self.assertIsInstance(category_data, list)
        self.assertGreaterEqual(len(category_data), 1)
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
        
        response = self.client.post(
            reverse('category-list', kwargs={'version': 'v1'}),
            data=data,
            content_type='application/json'
        )
        
        print(f"Request data: {data}")
        print(f"Response content: {response.content}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        created_category = Category.objects.get(title='Tech')
        self.assertEqual(created_category.title, 'Tech')
        self.assertEqual(created_category.slug, 'tech')
        self.assertEqual(created_category.description, 'Technology books')
        self.assertEqual(created_category.active, True)