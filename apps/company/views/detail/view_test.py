import uuid

from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from ...models import Company, Members
from .view import CompanyDetailViewV1
from apps.user.models import User


class CompanyDetailTest(TestCase):

	@classmethod
	def setUpTestData(cls):
		cls.user = User.objects.create(username='test')
		cls.company = Company.objects.create(
			name='test_company',
			owner=cls.user,
			created_by=cls.user
		)
		cls.members = Members.objects.create(
			user=cls.user,
			is_admin=True,
			company=cls.company
		)

	def setUp(self):
		self.factory = APIRequestFactory()

	def test_success_detail(self):
		request = self.factory.get('/')
		request.session = {}
		request.user = self.user

		force_authenticate(request, self.user)

		response = CompanyDetailViewV1().as_view()(request, company_uuid=self.company.uuid)

		self.assertEqual(200, response.status_code)
		response = response.data

		self.assertEqual(response['results']['uuid'], str(self.company.uuid))
		self.assertEqual(response['results']['name'], self.company.name)
		self.assertEqual(response['results']['owner']['fio'], self.user.fio)
		self.assertEqual(response['results']['members'][0]['is_admin'], True)

	def test_not_found_detail(self):
		request = self.factory.get('/')
		request.session = {}
		request.user = self.user

		force_authenticate(request, self.user)

		response = CompanyDetailViewV1().as_view()(request, company_uuid=uuid.uuid4())

		self.assertEqual(403, response.status_code)
