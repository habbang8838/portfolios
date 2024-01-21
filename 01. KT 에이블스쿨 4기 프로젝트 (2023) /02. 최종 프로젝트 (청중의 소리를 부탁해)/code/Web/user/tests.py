from django.test import TestCase
from django.urls import reverse

from user.models import User


class UserViewsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            userid='testuser',
            password='testpassword123!',
            name='Test User',
            email='testuser@example.com'
        )

    def test_signup_view_get(self):
        response = self.client.get(reverse('user:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/sign_up.html')

    def test_signup_view_post(self):
        response = self.client.post(reverse('user:signup'), {
            'userid': 'newuser',
            'password': 'newpassword123!',
            'password_confirm': 'newpassword123!',
            'name': 'New User',
            'email': 'newuser@example.com'
        })
        self.assertEqual(User.objects.count(), 2)
        self.assertRedirects(response, reverse('user:login'))

    def test_login_view_get(self):
        response = self.client.get(reverse('user:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/login_page.html')

    def test_login_view_post(self):
        response = self.client.post(reverse('user:login'), {
            'userid': 'testuser',
            'password': 'testpassword123!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_logout_view(self):
        self.client.login(userid='testuser', password='testpassword123!')
        response = self.client.get(reverse('user:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('_auth_user_id' not in self.client.session)

    def test_check_userid_existence(self):
        response = self.client.get(reverse('user:check_userid'), {'userid': 'testuser'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'is_taken': True})
