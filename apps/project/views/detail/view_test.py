from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.company.models import Company
from apps.company.models import Members as CompanyMembers
from .view import ProjectDetailViewV1
from ...models import Project
from apps.user.models import User


class ProjectDetailTestV1(TestCase):

	@classmethod
	def setUpTestData(cls):
		cls.user = User.objects.create(username='test')
		cls.company = Company.objects.create(name='test', owner=cls.user, created_by=cls.user)
		cls.project = Project.objects.create(name='test', company=cls.company, owner=cls.user, created_by=cls.user)

	def setUp(self):
		self.factory = APIRequestFactory()

	def test_detail(self):
		request = self.factory.get('/')
		request.session = {}
		request.user = self.user

		force_authenticate(request, self.user)

		response = ProjectDetailViewV1().as_view()(request, self.project.uuid)

		self.assertEqual(200, response.status_code)
		response = response.data

		self.assertEqual(response['results']['uuid'], str(self.project.uuid))
		self.assertEqual(response['results']['name'], self.project.name)
		self.assertEqual(response['results']['owner']['fio'], self.user.fio)