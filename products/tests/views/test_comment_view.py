import json
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from ...models.product import Product
from ...models.category import Category
from ...models.user import User
from ...models.comment import Comment


class ProductCommentViewTestCase(APITestCase):
    """Test cases for ProductCommentView API endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.category = Category.objects.create(name="Energy Drink")
        self.user = User.objects.create(telegram_id=123456789, username="testuser")
        self.product = Product.objects.create(
            category=self.category,
            user=self.user,
            variant='Test Product'
        )
    
    def test_add_comment_success(self):
        """Test successful comment creation"""
        data = {
            'product_id': self.product.id,
            'telegram_id': 123456789,
            'comment': 'This is a great product!'
        }
        
        url = reverse('product-comment')
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        
        comment = Comment.objects.first()
        self.assertEqual(comment.text, 'This is a great product!')
        self.assertEqual(comment.product, self.product)
        self.assertEqual(comment.user, self.user)
    
    def test_add_comment_missing_fields(self):
        """Test comment creation with missing fields"""
        data = {
            'product_id': self.product.id,
            'telegram_id': 123456789
            # Missing comment
        }
        
        url = reverse('product-comment')
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_comment_invalid_product(self):
        """Test comment creation with invalid product ID"""
        data = {
            'product_id': 999,
            'telegram_id': 123456789,
            'comment': 'Test comment'
        }
        
        url = reverse('product-comment')
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, 400)
    
    def test_add_comment_invalid_user(self):
        """Test comment creation with invalid user"""
        data = {
            'product_id': self.product.id,
            'telegram_id': 999999999,
            'comment': 'Test comment'
        }
        
        url = reverse('product-comment')
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, 400)
    
    def test_add_multiple_comments(self):
        """Test adding multiple comments to the same product"""
        # Add first comment
        data1 = {
            'product_id': self.product.id,
            'telegram_id': 123456789,
            'comment': 'First comment'
        }
        
        url = reverse('product-comment')
        response1 = self.client.post(url, data1, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        
        # Add second comment
        data2 = {
            'product_id': self.product.id,
            'telegram_id': 123456789,
            'comment': 'Second comment'
        }
        
        response2 = self.client.post(url, data2, format='json')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        
        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(self.product.comments.count(), 2)
