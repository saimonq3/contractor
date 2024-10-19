from rest_framework.test import APIRequestFactory, APITestCase

from apps.user.models import User
from .view import LoginView


class LoginV1Test(APITestCase):
	@classmethod
	def setUpTestData(cls):
		cls.user = User.objects.create(email='test@test.ru', phone_number='+71234567890')
		cls.test_user = User.objects.create(email='test_user@test.ru', phone_number='+70987654321')
		cls.password = 'TesT!Passwd123'

	def setUp(self):
		self.factory = APIRequestFactory()

	def test_create_token(self):
		self.test_user.set_password(self.password)
		self.test_user.save()

		data = {
			'email': self.test_user.email,
			'password': self.password
		}

		request = self.factory.post('/', data=data, format='json')
		response = LoginView.as_view()(request)

		self.assertEqual(200, response.status_code)
		self.assertIn('token', response.data.keys())
		self.assertEqual(
			User.objects.get(email=self.test_user.email).auth_token.__str__(),
			response.data.get('token')
		)

	def test_wrong_password(self):
		self.test_user.set_password(self.password)
		self.test_user.save()

		data = {
			'email': self.test_user.email,
			'password': 'WrongPassword'
		}

		request = self.factory.post('/', data=data, format='json')
		response = LoginView.as_view()(request)

		self.assertEqual(403, response.status_code)
		self.assertEqual(
			{
				"detail": "Неверные логин или пароль"
			},
			response.data
		)