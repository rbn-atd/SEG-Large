from django.test import TestCase
from django.urls import reverse
from tracker.models import User, Category, Achievement
from tracker.forms import AddCategoryForm

"""Unit tests for the category_list view"""
class CategoryListViewTestCase(TestCase):

    fixtures = ['tracker/tests/fixtures/default_user.json',
                'tracker/tests/fixtures/default_category.json',
                'tracker/tests/fixtures/extra_categories.json']

    def setUp(self):
        self.url = reverse('category_list')
        self.user = User.objects.get(email = 'james@example.org')
        self.form_input = {
            'name':'New',
            'week_limit':50
        }
        self.achievement = Achievement.objects.create(name = "Budget boss", description = "Test", criteria = "Test", badge = "Test")
        cat_one = Category.objects.get(name = 'Test')
        cat_two = Category.objects.get(name = 'Test2')
        cat_three = Category.objects.get(name = 'Test3')
        cat_overall = Category.objects.get(name = 'Test4')
        self.user.available_categories.add(cat_one, cat_two, cat_three, cat_overall)

    def test_category_list_url(self):
        self.assertEqual(self.url, '/category_list')

    def test_get_category_list(self):
        self.client.login(username = self.user.email, password = 'Lu123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category_list.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, AddCategoryForm))
        self.assertFalse(form.is_bound)
        category_list = list(response.context['categories'])
        self.assertEqual(len(category_list),3)

    def test_valid_add_category(self):
        self.client.login(username = self.user.email, password = 'Lu123')
        other_user = User.objects.create_user(
            email = 'johndoe@example.org',
            first_name='John',
            last_name = 'Doe',
            password = 'Doe123',
        )
        before_count = Category.objects.count()
        correct_user_before_count = self.user.available_categories.count()
        incorrect_user_before_count = other_user.available_categories.count()
        self.client.post(self.url, self.form_input, follow=True)
        after_count = Category.objects.count()
        correct_user_after_count = self.user.available_categories.count()
        incorrect_user_after_count = other_user.available_categories.count()
        self.assertEqual(after_count, before_count+1)
        self.assertEqual(correct_user_after_count, correct_user_before_count+1)
        self.assertEqual(incorrect_user_after_count, incorrect_user_before_count)

    def test_post_invalid_add_category(self):
        self.client.login(username=self.user.email, password='Lu123')
        self.form_input['week_limit']=-100
        before_count = Category.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Category.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Weekly limit cannot be negative", response.content.decode())
