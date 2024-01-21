# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from live.models import Lecture
from report.models import Reaction, Feedback
from user.models import User


class ReportViewsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            userid='testuser',
            password='testpassword123!',
            name='Test User',
            email='testuser@example.com'
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpassword123!')

        self.lecture = Lecture.objects.create(
            user=self.user,
            topic='Test Lecture',
            start_time=timezone.now(),
            end_time=timezone.now()
        )

        self.reaction = Reaction.objects.create(
            lecture=self.lecture,
            time=10,
            concentration=50,
            negative=0,
            neutral=30,
            positive=20
        )

        self.feedback = Feedback.objects.create(
            reaction=self.reaction,
            content='Good lecture'
        )

    def test_list_lectures(self):
        response = self.client.get(reverse('report:list_lectures'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'report/storage_list.html')

    def test_result(self):
        url = reverse('report:detail', kwargs={'id': self.lecture.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'report/report_page.html')

    def test_delete_lecture(self):
        response = self.client.post(reverse('report:delete_lecture'), {'lecture_id': self.lecture.id})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'message': 'Lecture deleted successfully'})
        self.assertEqual(Lecture.objects.filter(pk=self.lecture.id).count(), 0)
