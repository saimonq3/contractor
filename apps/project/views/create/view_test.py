from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.company.models import Company
from apps.company.models import Members as CompanyMembers
from ...models import Project
from .view import ProjectCreateViewV1
from apps.user.models import User


class CompanyCreateTest(TestCase):

	@classmethod
	def setUpTestData(cls):
		cls.user_1 = User.objects.create(username='test_1')
		cls.user_2 = User.objects.create(username='test_2')
		cls.user_3 = User.objects.create(username='test_3')
		cls.company_1 = Company.objects.create(name='test_1', owner=cls.user_1, created_by=cls.user_1)
		cls.company_2 = Company.objects.create(name='test_2', owner=cls.user_1, created_by=cls.user_1)
		CompanyMembers.objects.create(company=cls.company_1, user=cls.user_1, is_admin=True)
		CompanyMembers.objects.create(company=cls.company_1, user=cls.user_2, is_admin=False)
		CompanyMembers.objects.create(company=cls.company_2, user=cls.user_1, is_admin=True)

	def setUp(self):
		self.factory = APIRequestFactory()

	def test_success_create(self):
		request = self.factory.post(
			'/',
			data={'name': 'test_project', 'description': 'test', 'add_company_members': True},
			format='json'
		)
		request.session = {}
		request.user = self.user_1

		force_authenticate(request, self.user_1)

		response = ProjectCreateViewV1().as_view()(request, company_uuid=str(self.company_1.uuid))

		self.assertEqual(200, response.status_code)
		response = response.data

		self.assertEqual(Project.objects.count(), 1)
		project = Project.objects.first()
		self.assertEqual(project.owner, self.user_1)
		self.assertEqual(project.project_members.count(), 2)
		self.assertEqual(project.project_members.filter(user=self.user_1, is_admin=True).exists(), True)
		self.assertEqual(project.project_members.filter(user=self.user_2, is_admin=False).exists(), True)

		self.assertEqual(response['results']['uuid'], str(project.uuid))
		self.assertEqual(response['results']['company']['uuid'], str(self.company_1.uuid))

	def test_fail_create(self):
		request = self.factory.post(
			'/',
			data={'name': 'test_project', 'description': 'test', 'add_company_members': True},
			format='json'
		)
		request.session = {}
		request.user = self.user_2

		force_authenticate(request, self.user_2)

		response = ProjectCreateViewV1().as_view()(request, company_uuid=self.company_2.uuid)

		self.assertEqual(403, response.status_code)