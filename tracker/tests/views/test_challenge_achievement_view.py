from django.urls import reverse
from django.utils import timezone
from tracker.models import User, Challenge, UserChallenge, Achievement, UserAchievement, Level, UserLevel, Activity
from django.test import TestCase
from django.db import IntegrityError

class ChallengeViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User'
        )
        self.challenge = Challenge.objects.create(
            name='Test Challenge',
            description='Test description',
            points=50,
            start_date='2023-01-01',
            end_date='2023-12-31'
        )
        self.wise_spender_achievement = Achievement.objects.create(
            name='Wise spender',
            description='Test achievement description',
            criteria='Test criteria',
            badge='test_badge.png'
        )
        self.superstar_achievement = Achievement.objects.create(
            name='Superstar',
            description='Test achievement description',
            criteria='Test criteria',
            badge='test_badge.png'
        )
        self.level = Level.objects.create(
            name='Level 1',
            description='Test level description',
            required_points=0
        )
        self.client.login(email='testuser@example.com', password='testpassword')

    def test_challenge_list_view(self):
        url = reverse('challenge_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Challenge')

    def test_achievement_list_view(self):
        url = reverse('achievement_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Wise spender')

    def test_challenge_details_view(self):
        url = reverse('challenge_details', args=[self.challenge.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Challenge')
        self.assertContains(response, 'Test description')

    def test_enter_challenge_view(self):
        url = reverse('enter_challenge')
        response = self.client.post(url, {'challenge_id': self.challenge.id})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(UserChallenge.objects.filter(user=self.user, challenge=self.challenge).exists())
        response = self.client.post(url, {'challenge_id': self.challenge.id})
        self.assertEqual(response.status_code, 302)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_my_challenges_view(self):
        UserChallenge.objects.create(user=self.user, challenge=self.challenge)
        url = reverse('my_challenges')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Challenge')

    def test_superstar_challenge_achievement(self):
        for id in range (10, 21):
            test_challenge = self.challenge
            test_challenge.id = id
            test_challenge.save()
            UserChallenge.objects.create(user=self.user, challenge=test_challenge)
            url = reverse('complete_challenge', args=[test_challenge.id])
            response = self.client.post(url)
            self.assertEqual(response.status_code, 302)

    def test_deleted_challenge_achievement(self):
        self.wise_spender_achievement.delete()
        UserChallenge.objects.create(user=self.user, challenge=self.challenge)
        url = reverse('complete_challenge', args=[self.challenge.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(UserChallenge.objects.filter(user=self.user, challenge=self.challenge).exists())
        self.assertEqual(Achievement.objects.filter(name='Wise spender').count(), 0)

    def test_challenge_already_completed(self):
        user_challenge = UserChallenge.objects.create(user=self.user, challenge=self.challenge)
        user_challenge.date_completed = timezone.now()
        user_challenge.save()
        url = reverse('complete_challenge', args=[self.challenge.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(UserChallenge.objects.filter(user=self.user, challenge=self.challenge).exists())

    def test_complete_not_existing_challenge(self):
        url = reverse('complete_challenge', args=[10])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

