"""
Unit tests for Item app
Tests item creation, listing, and cart functionality
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from item.models import Category, Item


class ItemModelTestCase(TestCase):
    """Test Item model functionality"""

    def setUp(self):
        """Create test user and category"""
        self.user = User.objects.create_user(
            username='seller',
            password='sellerpass123'
        )
        self.category = Category.objects.create(name='Electronics')

    def test_create_item(self):
        """Test item creation"""
        item = Item.objects.create(
            category=self.category,
            name='Test Phone',
            description='A test phone',
            price=500.00,
            created_by=self.user
        )
        self.assertEqual(item.name, 'Test Phone')
        self.assertEqual(item.price, 500.00)
        self.assertEqual(item.created_by, self.user)

    def test_item_string_representation(self):
        """Test item __str__ method"""
        item = Item.objects.create(
            category=self.category,
            name='Test Laptop',
            description='A test laptop',
            price=1000.00,
            created_by=self.user
        )
        self.assertEqual(str(item), 'Test Laptop')


class ItemViewsTestCase(TestCase):
    """Test item views"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testbuyer',
            password='buyerpass123'
        )
        self.category = Category.objects.create(name='Books')
        self.item = Item.objects.create(
            category=self.category,
            name='Test Book',
            description='A test book',
            price=20.00,
            created_by=self.user
        )

    def test_items_page_loads(self):
        """Test items listing page loads"""
        response = self.client.get(reverse('item:items'))
        self.assertEqual(response.status_code, 200)

    def test_item_detail_page_loads(self):
        """Test individual item page loads"""
        response = self.client.get(
            reverse('item:detail', kwargs={'pk': self.item.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_create_item_requires_login(self):
        """Test that creating item requires authentication"""
        response = self.client.get(reverse('item:new'))
        # Should redirect to login
        self.assertEqual(response.status_code, 302)


class CategoryTestCase(TestCase):
    """Test Category model"""

    def test_create_category(self):
        """Test category creation"""
        category = Category.objects.create(name='Clothing')
        self.assertEqual(category.name, 'Clothing')
        self.assertEqual(str(category), 'Clothing')

    def test_category_ordering(self):
        """Test categories are ordered by name"""
        Category.objects.create(name='Zebra')
        Category.objects.create(name='Apple')
        categories = Category.objects.all()
        self.assertEqual(categories[0].name, 'Apple')
        self.assertEqual(categories[1].name, 'Zebra')
