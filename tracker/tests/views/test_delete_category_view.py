from django.test import TestCase, Client
from django.urls import reverse
from tracker.models import User, Category

"""Unit tests for the delete_category view"""
class DeleteCategoryViewTestCase(TestCase):

    def setUp(self):
        self.c = Client()
        self.url = reverse('delete_category')
        self.user = User.objects.create_user(email='user@email.com', password='Password123')
        self.category = Category.objects.create(name = 'Category', week_limit = 10, is_binned=True)

    def test_url(self):
        self.assertEqual(self.url, '/delete_category')

    def test_successful_delete(self):
        self.c.login(email='user@email.com', password='Password123')
        before_count = Category.objects.count()
        response = self.c.post(self.url, {'radio_pk': self.category.pk})
        after_count = Category.objects.count()
        self.assertEqual(after_count, before_count-1)
        self.assertRedirects(response, reverse('category_bin'))

    def test_delete_category_without_radio_pk(self):
        self.c.login(email='user@email.com', password='Password123')
        before_count = Category.objects.count()
        response = self.c.post(self.url)
        after_count = Category.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 302)

    def test_delete_category_get_request(self):
        self.c.login(email='user@email.com', password='Password123')
        response = self.c.get(self.url)
        self.assertEqual(response.status_code, 302)
