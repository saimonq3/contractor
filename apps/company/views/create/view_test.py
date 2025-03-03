from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from ...models import Company
from .view import CompanyCreateViewV1
from apps.user.models import User


class CompanyCreateTest(TestCase):

	@classmethod
	def setUpTestData(cls):
		cls.user = User.objects.create(username='test')

	def setUp(self):
		self.factory = APIRequestFactory()

	def test_success_create(self):
		request = self.factory.post(
			'/',
			data={'name': 'test company'},
			format='json'
		)
		request.session = {}
		request.user = self.user

		force_authenticate(request, self.user)

		response = CompanyCreateViewV1().as_view()(request)

		self.assertEqual(200, response.status_code)
		response = response.data

		company = Company.objects.all()

		# Проверяем что создалась только одна компания
		self.assertEqual(company.count(), 1)

		# Проверяем что компания создалачь корректно
		self.assertEqual(company[0].company_members.all().count(), 1)
		self.assertEqual(company[0].company_members.filter(is_admin=True)[0].user, self.user)
		self.assertEqual(company[0].owner, self.user)
		self.assertEqual(company[0].name, 'test company')

		# Проверяем что в ответе пришил корректные данные
		self.assertEqual(str(company[0].uuid), response['results']['uuid'])
		self.assertEqual(company[0].name, response['results']['name'])

	def test_fail_create(self):
		request = self.factory.post(
			'/',
			data={'wrong_field': 'test company'},
			format='json'
		)
		request.session = {}
		request.user = self.user

		force_authenticate(request, self.user)

		response = CompanyCreateViewV1().as_view()(request)

		self.assertEqual(400, response.status_code)
		response = response.data

		self.assertEqual(response['results']['error']['user_message'], 'Не корректные данные запроса')

		# Проверяем что Компания не создалась
		self.assertEqual(Company.objects.count(), 0)

	def test_return_created_company(self):
		request = self.factory.post(
			'/',
			data={'name': 'test_company'},
			format='json'
		)
		Company.objects.create(
			owner=self.user,
			name='test_company',
			created_by=self.user
		)

		request.session = {}
		request.user = self.user

		force_authenticate(request, self.user)

		response = CompanyCreateViewV1().as_view()(request)

		self.assertEqual(200, response.status_code)
		response = response.data

		company = Company.objects.all()

		# Проверяем что создалась только одна компания
		self.assertEqual(company.count(), 1)

		self.assertEqual(company[0].owner, self.user)
		self.assertEqual(company[0].name, 'test_company')

		# Проверяем что в ответе пришил корректные данные
		self.assertEqual(str(company[0].uuid), response['results']['uuid'])
		self.assertEqual(company[0].name, response['results']['name'])
