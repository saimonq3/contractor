from rest_framework.test import APIRequestFactory, APITestCase

from apps.user.models import User
from .view import RegisterUser


class LoginV1Test(APITestCase):

	def setUp(self):
		self.factory = APIRequestFactory()

	def test_register(self):
		user1 = {
			'username': 'test_user1',
			'password': 'TesT!Passwd1'
		}

		user2 = {
			'username': 'test_user2',
			'password': 'TesT!Passwd1',
			'phone_number': '+71234567890'
		}

		user3 = {
			'username': 'test_user3',
			'password': 'TesT!Passwd1',
			'phone_number': '+71234567890'
		}

		user4 = {
			'username': 'test_user2',
			'password': 'TesT!Passwd1',
			'phone_number': '+71234567890'
		}

		user5 = {
			'password': 'TesT!Passwd1',
			'phone_number': '+71234567899'
		}

		# Проверяем что можно зарегистрироваться только по почте
		request1 = self.factory.post('/', data=user1, format='json')
		response1 = RegisterUser.as_view()(request1)
		self.assertEqual(200, response1.status_code)
		self.assertEqual(
			{
				'username': 'test_user1',
			},
			response1.data
		)

		# Проверяем что можно зарегистрироваться по почте и номеру телефона
		request2 = self.factory.post('/', data=user2, format='json')
		response2 = RegisterUser.as_view()(request2)
		self.assertEqual(200, response2.status_code)
		self.assertEqual(
			{
				'username': 'test_user2',
				'phone_number': '+71234567890'
			},
			response2.data
		)

		# Проверяем что будет ошибка при попытке зарегистрировать пользователя по уже существующему номеру телефона
		request3 = self.factory.post('/', data=user3, format='json')
		response3 = RegisterUser.as_view()(request3)
		self.assertEqual(400, response3.status_code)
		self.assertEqual(
			{
				"phone_number": [
					"Пользователь с таким phone_number уже существует."
				]
			},
			response3.data
		)

		# Проверяем что будет ошибка при попытке зарегистрировать пользователя по уже существующим username
		request4 = self.factory.post('/', data=user4, format='json')
		response4 = RegisterUser.as_view()(request4)
		self.assertEqual(400, response4.status_code)
		self.assertEqual(
			{
				"username": [
					"Пользователь с таким username уже существует."
				],
				"phone_number": [
					"Пользователь с таким phone_number уже существует."
				]
			},
			response4.data
		)

		# Проверяем что будет ошибка при попытке зарегистрировать без username
		request5 = self.factory.post('/', data=user5, format='json')
		response5 = RegisterUser.as_view()(request5)
		self.assertEqual(400, response5.status_code)
		self.assertEqual({'username': ['Обязательное поле.']}, response5.data)

		# Проверяем что зарегистрировалось 2 пользователя
		self.assertEqual(User.objects.count(), 2)