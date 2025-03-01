# from django.test import TestCase
# from rest_framework.test import APIRequestFactory, force_authenticate
#
# from apps.company.models import Company, Members
# from apps.user.models import User
# from .view import CompanyUpdateNameViewV1, CompanyChangeOwnerViewV1, CompanyAddMembersViewV1 ,CompanyRemoveMembersViewV1, CompanyChangeMemberPermissionViewV1
#
#
# class CompanyListTest(TestCase):
#
# 	@classmethod
# 	def setUpTestData(cls):
# 		cls.user_1 = User.objects.create(username='test1')
# 		cls.user_2 = User.objects.create(username='test2')
# 		cls.company_1 = Company.objects.create(
# 			name='test_company_1',
# 			owner=cls.user_1,
# 			created_by=cls.user_1
# 		)
# 		cls.company_2 = Company.objects.create(
# 			name='test_company_2',
# 			owner=cls.user_2,
# 			created_by=cls.user_2
# 		)
# 		cls.company_3 = Company.objects.create(
# 			name='test_company_3',
# 			owner=cls.user_2,
# 			created_by=cls.user_2
# 		)
# 		cls.members = Members.objects.create(
# 			user=cls.user_1,
# 			is_admin=True,
# 			company=cls.company_1
# 		)
# 		cls.members = Members.objects.create(
# 			user=cls.user_1,
# 			is_admin=True,
# 			company=cls.company_2
# 		)
# 		cls.members = Members.objects.create(
# 			user=cls.user_2,
# 			is_admin=True,
# 			company=cls.company_3
# 		)
#
# 	def setUp(self):
# 		self.factory = APIRequestFactory()
