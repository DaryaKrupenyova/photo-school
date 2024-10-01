from django.contrib.auth.models import User
from django.test import TestCase, Client

# Create your tests here.
from django.urls import reverse


class UserPageTestCase(TestCase):
    fixtures = ['database_for_tests.json']

    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.get(username='pavel4')
        self.client.force_login(self.user)
        self.response = self.client.get(reverse('account', args=['pavel4']))

    def test_response(self):
        self.assertEqual(self.response.status_code, 200)

    def test_response_logout(self):
        self.client.logout()
        self.response = self.client.get(reverse('account', args=['pavel4']))
        self.assertEqual(self.response.status_code, 302)

    def test_first_and_last_names(self):
        self.assertEqual(self.response.context['first_name'], 'Pavel')
        self.assertEqual(self.response.context['last_name'], 'Vishnyakov')

    def test_expected_302_url(self):
        self.client.logout()
        self.response = self.client.get(reverse('account', args=['pavel4']))
        self.assertRedirects(self.response, reverse('login'), status_code=302)


class SettingsPageTestCase(TestCase):
    fixtures = ['database_for_tests.json']

    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.get(username='pavel4')
        self.client.force_login(self.user)
        self.response = self.client.get(reverse('settings'))

    def test_response(self):
        self.assertEqual(self.response.status_code, 200)

    def test_response_logout(self):
        self.client.logout()
        self.response = self.client.get(reverse('settings'))
        self.assertEqual(self.response.status_code, 302)

    def test_first_and_last_names(self):
        self.assertEqual(self.response.context['first_name'], 'Pavel')
        self.assertEqual(self.response.context['last_name'], 'Vishnyakov')

    def test_change_to_existing_name(self):
        self.response = self.client.post(reverse('settings'), {'username': 'pavel'})
        self.assertEqual(self.response.context['alert_state'], 'block')

    def test_change_to_existing_name_response(self):
        self.response = self.client.post(reverse('settings'), {'username': 'pavel'})
        self.assertEqual(self.response.status_code, 200)

    def test_change_gmail(self):
        self.response = self.client.post(reverse('settings'), {'email': '1234@gmail.com'})
        self.assertEqual(self.response.context['email'], 'visnyakovp@gmail.com')

    def test_change_gmail_response(self):
        self.response = self.client.post(reverse('settings'), {'email': '1234@gmail.com'})
        self.assertEqual(self.response.status_code, 200)


class CoursePageTestCase(TestCase):
    fixtures = ['database_for_tests.json']

    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.get(username='pavel4')
        self.client.force_login(self.user)
        self.response = self.client.get(reverse('courses'))

    def test_response(self):
        self.assertEqual(self.response.status_code, 200)

    def test_response_logout(self):
        self.client.logout()
        self.response = self.client.get(reverse('courses'))
        self.assertEqual(self.response.status_code, 302)

    def test_first_and_last_names(self):
        self.assertEqual(self.response.context['first_name'], 'Pavel')
        self.assertEqual(self.response.context['last_name'], 'Vishnyakov')


class LandingPageTestCase(TestCase):
    fixtures = ['database_for_tests.json']

    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.get(username='pavel4')
        self.client.force_login(self.user)
        self.response = self.client.get(reverse('lending'))

    def test_response(self):
        self.assertEqual(self.response.status_code, 200)

    def test_response_logout(self):
        self.client.logout()
        self.response = self.client.get(reverse('lending'))
        self.assertEqual(self.response.status_code, 200)


class FinancePageTestCase(TestCase):
    fixtures = ['database_for_tests.json']

    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.get(username='pavel4')
        self.client.force_login(self.user)
        self.response = self.client.get(reverse('finances'))

    def test_response(self):
        self.assertEqual(self.response.status_code, 200)

    def test_response_logout(self):
        self.client.logout()
        self.response = self.client.get(reverse('finances'))
        self.assertEqual(self.response.status_code, 302)


class LoginPageTestCase(TestCase):
    fixtures = ['database_for_tests.json']

    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.get(username='pavel4')
        self.client.force_login(self.user)
        self.response = self.client.get(reverse('login'))

    def test_response(self):
        self.assertRedirects(self.response, reverse('account', args=['pavel4']))

    def test_response_logout(self):
        self.client.logout()
        self.response = self.client.get(reverse('login'))
        self.assertEqual(self.response.status_code, 200)


class LogoutTestCase(TestCase):
    fixtures = ['database_for_tests.json']

    def test_logout(self):
        self.client = Client()
        self.user = User.objects.get(username='pavel4')
        self.client.force_login(self.user)
        self.response = self.client.get(reverse('logout'))
        self.assertEqual(self.response.status_code, 302)


class SignupTestCase(TestCase):
    fixtures = ['database_for_tests.json']

    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.get(username='pavel4')
        self.client.force_login(self.user)
        self.response = self.client.get(reverse('signup'))

    def test_response(self):
        self.assertEqual(self.response.status_code, 200)

    def test_response_logout(self):
        self.assertEqual(self.  response.status_code, 200)


class SignupCompleteTestCase(TestCase):
    fixtures = ['database_for_tests.json']

    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.get(username='pavel4')
        self.client.force_login(self.user)
        self.response = self.client.get(reverse('signup_complete'))

    def test_response(self):
        self.assertEqual(self.response.status_code, 200)

    def test_response_logout(self):
        self.assertEqual(self.  response.status_code, 200)


class PasswordResetTestCase(TestCase):
    fixtures = ['database_for_tests.json']

    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.get(username='pavel4')
        self.client.force_login(self.user)
        self.response = self.client.get(reverse('password_reset'))

    def test_response(self):
        self.assertEqual(self.response.status_code, 200)

    def test_response_logout(self):
        self.assertEqual(self.  response.status_code, 200)


class PasswordResetDoneTestCase(TestCase):
    fixtures = ['database_for_tests.json']

    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.get(username='pavel4')
        self.client.force_login(self.user)
        self.response = self.client.get(reverse('password_reset_done'))

    def test_response(self):
        self.assertEqual(self.response.status_code, 200)

    def test_response_logout(self):
        self.assertEqual(self.  response.status_code, 200)
