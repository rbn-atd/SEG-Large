from django.test import TestCase, Client
from django.urls import reverse
from tracker.models import User, Post, Comment, Reply, Forum_Category, UserLevel, Level
from django.core.files.uploadedfile import SimpleUploadedFile


class EditReplyViewTests(TestCase):

    fixtures = ['tracker/tests/fixtures/default_user.json']

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(email='galin@email.com')
        self.forum_category = Forum_Category.objects.create(title='Test Category', slug='test-category', description='Description')
        self.post = Post.objects.create(user=self.user, title='Test Post', content='Test content')
        self.comment = Comment.objects.create(user=self.user, content='Test commet content')
        self.reply = Reply.objects.create(user=self.user, content='Test reply content')
        self.post.forum_categories.add(self.forum_category)
        self.post.comments.add(self.comment)
        self.comment.replies.add(self.reply)
        self.url = reverse('edit_reply', kwargs={'id': self.reply.id})
        self.level = Level.objects.create(name='level', description='description', required_points=10)
        self.userlevel = UserLevel.objects.create(user=self.user, level=self.level, points=20)

    def test_post_request_with_valid_data_updates_reply(self):
        self.client.login(email='galin@email.com', password='Password123')
        data = {
            'content': 'Edited Content',
        }
        response = self.client.post(self.url, data)
        self.reply.refresh_from_db()
        self.assertEqual(self.reply.content, 'Edited Content')
        self.assertRedirects(response, self.post.get_url())

    def test_post_request_with_media_updates_reply(self):
        media_file = SimpleUploadedFile("test_image.txt", b"test content", content_type="text/plain")
        self.client.login(email='galin@email.com', password='Password123')
        data = {
            'content': 'Edited Content',
            'media': media_file,
        }
        response = self.client.post(self.url, data)
        self.reply.refresh_from_db()
        self.assertEqual(self.reply.content, 'Edited Content')
        self.assertIsNotNone(self.comment.media)
        self.assertRedirects(response, self.post.get_url())

    def test_post_request_with_media_clear_updates_comment(self):
        media_file = SimpleUploadedFile("test_image.txt", b"test content", content_type="text/plain")
        self.reply.media = media_file
        self.client.login(email='galin@email.com', password='Password123')
        data = {
            'content': 'Edited Content',
            'media-clear': 'a',
        }
        response = self.client.post(self.url, data)
        self.reply.refresh_from_db()
        self.assertEqual(self.reply.content, 'Edited Content')
        self.assertRedirects(response, self.post.get_url())

    def test_reply_does_not_exist(self):
        self.client.login(email='galin@email.com', password='Password123')
        non_existent_reply_url = reverse('edit_reply', kwargs={'id': self.reply.id + 1})
        response = self.client.post(non_existent_reply_url)
        self.assertRedirects(response, reverse('forum_home'))

    def test_edit_reply_get_request(self):
        self.client.login(email='galin@email.com', password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
