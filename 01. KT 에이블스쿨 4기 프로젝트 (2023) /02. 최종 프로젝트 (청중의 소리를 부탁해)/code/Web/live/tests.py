# Create your tests here.

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from user.models import User
from .models import Lecture


class LiveViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            userid='testuser',
            password='testpassword123!',
            name='Test User',
            email='testuser@example.com'
        )
        self.client.login(username='testuser', password='testpassword123!')

        self.lecture = Lecture.objects.create(
            user=self.user,
            topic='Test Lecture',
            start_time=timezone.now(),
            end_time=timezone.now()
        )

    def test_info_GET(self):
        response = self.client.get(reverse('live:info'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'live/lecture_preset.html')

    def test_info_POST_missing_data(self):
        response = self.client.post(reverse('live:info'), kwargs={})
        self.assertEqual(response.status_code, 400)

    def test_info_POST_with_data(self):
        response = self.client.post(reverse('live:info'), {
            'topic': 'New Topic',
            'term': '1',
            'category': 'Test Category'
        })
        self.assertEqual(response.status_code, 302)

    def test_record_GET(self):
        response = self.client.get(reverse('live:record', kwargs={'id': self.lecture.id, 'term': 1}))
        self.assertRedirects(response, '/live/info/', status_code=302, target_status_code=200)

        session = self.client.session
        session['lecture_id'] = self.lecture.id
        session.save()

        response = self.client.get(reverse('live:record', kwargs={'id': self.lecture.id, 'term': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'live/analysis_page.html')

    def test_process_media_POST_missing_files(self):
        response = self.client.post(reverse('live:process_media', kwargs={}))
        self.assertEqual(response.status_code, 400)

    def test_update_lecture_time_POST_missing_data(self):
        response = self.client.post(reverse('live:update_lecture_time'), kwargs={})
        self.assertEqual(response.status_code, 400)

    def test_update_lecture_time_POST_with_data(self):
        response = self.client.post(reverse('live:update_lecture_time'), {
            'lecture_id': self.lecture.id,
            'start_time': timezone.now().time(),
            'end_time': timezone.now().time()
        })
        self.assertEqual(response.status_code, 200)
