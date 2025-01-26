from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.company.models import Company
from apps.user.models import User
from utils import api
from .serializers import ProjectMemberSerializerV1, ProjectUpdateInfoSerializerV1
from ...models import Project, Members


class ProjectAddMemberViewV1(APIView):
	permission_classes = [IsAuthenticated, ]

	def post(self, request, project_uuid):
		check_query_serializer = ProjectMemberSerializerV1(data=request.data)
		if not check_query_serializer.is_valid():
			return api.error_response(
				status=400,
				message=str(check_query_serializer.error_messages)
			)
		try:
			project = Project.objects.get(uuid=project_uuid)
		except Project.DoesNotExist:
			return api.error_response(
				status=404,
				message='Проект не найден'
			)
		try:
			Members.objects.get(user=request.user, is_admin=True)
		except Members.DoesNotExist:
			return api.error_response(
				status=403,
				message='Вы не являетесь администратором'
			)

		try:
			new_member = User.objects.get(uuid=request.data.get('user_uuid'))
		except User.DoesNotExist:
			return api.error_response(
				status=404,
				message='Пользователь не найден'
			)

		new_member_is_admin = request.data.get('is_admin')

		# TODO создание надо будет вынести в отдельный сервис, пока делаю кстылем во вьюхе
		Members.objects.create(
			project=project,
			user=new_member,
			is_admin=new_member_is_admin if new_member_is_admin else False
		)

		project_members = (
			Members.objects
			.filter(project=project)
			.order_by('-is_admin', 'user__first_name', 'user__last_name')
			.select_related('user')
		)

		return api.response(
			{
				'uuid': project.uuid,
				'name': project.name,
				'description': project.description,
				'owner': project.owner.fio,
				'company': project.company.name,
				'base_url': project.base_url,
				'members': [
					{
						'user': member.user.fio,
						'is_admin': member.is_admin
					}
					for member in project_members
				]
			}
		)


class ProjectRemoveMemberViewV1(APIView):
	permission_classes = [IsAuthenticated, ]

	def post(self, request, project_uuid):
		check_query_serializer = ProjectMemberSerializerV1(data=request.data)
		if not check_query_serializer.is_valid():
			return api.error_response(
				status=400,
				message=str(check_query_serializer.error_messages)
			)
		try:
			project = Project.objects.get(uuid=project_uuid)
		except Project.DoesNotExist:
			return api.error_response(
				status=404,
				message='Проект не найден'
			)
		try:
			Members.objects.get(user=request.user, is_admin=True)
		except Members.DoesNotExist:
			return api.error_response(
				status=403,
				message='Вы не являетесь администратором'
			)

		try:
			remove_member = User.objects.get(uuid=request.data.get('user_uuid'))
		except User.DoesNotExist:
			return api.error_response(
				status=404,
				message='Пользователь не найден'
			)
		try:
			Members.objects.get(project=project, user=remove_member).delete()
		except Members.DoesNotExist:
			return api.error_response(
				status=404,
				message='Пользователь не являеться участкником проекта'
			)

		project_members = (
			Members.objects
			.filter(project=project)
			.order_by('-is_admin', 'user__first_name', 'user__last_name')
			.select_related('user')
		)

		return api.response(
			{
				'uuid': project.uuid,
				'name': project.name,
				'description': project.description,
				'owner': project.owner.fio,
				'company': project.company.name,
				'base_url': project.base_url,
				'members': [
					{
						'user': member.user.fio,
						'is_admin': member.is_admin
					}
					for member in project_members
				]
			}
		)


class ProjectChangeMemberPermissionViewV1(APIView):
	permission_classes = [IsAuthenticated, ]

	def post(self, request, project_uuid):
		check_query_serializer = ProjectMemberSerializerV1(data=request.data)
		if not check_query_serializer.is_valid():
			return api.error_response(
				status=400,
				message=str(check_query_serializer.error_messages)
			)
		try:
			project = Project.objects.get(uuid=project_uuid)
		except Project.DoesNotExist:
			return api.error_response(
				status=404,
				message='Проект не найден'
			)
		try:
			Members.objects.get(user=request.user, is_admin=True)
		except Members.DoesNotExist:
			return api.error_response(
				status=403,
				message='Вы не являетесь администратором'
			)

		try:
			member_to_change = User.objects.get(uuid=request.data.get('user_uuid'))
		except User.DoesNotExist:
			return api.error_response(
				status=404,
				message='Пользователь не найден'
			)

		member_is_admin = request.data.get('is_admin')
		try:
			member = Members.objects.get(project=project, user=member_to_change)
			member.is_admin = member_is_admin if member_is_admin else False
			member.save()
		except Members.DoesNotExist:
			return api.error_response(
				status=404,
				message='Пользователь не являеться участкником проекта'
			)

		project_members = (
			Members.objects
			.filter(project=project)
			.order_by('-is_admin', 'user__first_name', 'user__last_name')
			.select_related('user')
		)

		return api.response(
			{
				'uuid': project.uuid,
				'name': project.name,
				'description': project.description,
				'owner': project.owner.fio,
				'company': project.company.name,
				'base_url': project.base_url,
				'members': [
					{
						'user': member.user.fio,
						'is_admin': member.is_admin
					}
					for member in project_members
				]
			}
		)


class ProjectUpdateInfoViewV1(APIView):
	permission_classes = [IsAuthenticated, ]

	def post(self, request, project_uuid):
		try:
			project = Project.objects.get(uuid=project_uuid)
		except Project.DoesNotExist:
			return api.error_response(
				status=404,
				message='Проект не найден'
			)
		try:
			Members.objects.get(project=project, user=request.user, is_admin=True)
		except Members.DoesNotExist:
			return api.error_response(
				status=403,
				message='Вы не являетесь администратором'
			)
		serializer = ProjectUpdateInfoSerializerV1(data=request.data)
		serializer.update(project, validated_data=request.data)

		project_members = (
			Members.objects
			.filter(project=project)
			.order_by('-is_admin', 'user__first_name', 'user__last_name')
			.select_related('user')
		)

		return api.response(
			{
				'uuid': project.uuid,
				'name': project.name,
				'description': project.description,
				'owner': project.owner.fio,
				'company': project.company.name,
				'base_url': project.base_url,
				'members': [
					{
						'user': member.user.fio,
						'is_admin': member.is_admin
					}
					for member in project_members
				]
			}
		)


class ProjectChangeCompanyViewV1(APIView):
	permission_classes = [IsAuthenticated, ]

	def post(self, request, project_uuid):
		try:
			project = Project.objects.get(uuid=project_uuid)
		except Project.DoesNotExist:
			return api.error_response(
				status=404,
				message='Проект не найден'
			)
		try:
			Members.objects.get(project=project, user=request.user, is_admin=True)
		except Members.DoesNotExist:
			return api.error_response(
				status=403,
				message='Вы не являетесь администратором'
			)

		try:
			company = Company.objects.get(uuid=request.data.get('company'))
		except Company.DoesNotExist:
			return api.error_response(
				status=404,
				message='Компания не найдена'
			)
		project.company = company
		project.owner = company.owner
		project.save()

		# Удаляем текущих пользователей проекта
		Members.objects.filter(project=project).delete()
		# Добавляем текущего владельца новой компании в пользователи проекта и даем права админа
		Members.objects.create(project=project, user=company.owner, is_admin=True)

		project.refresh_from_db()

		project_members = (
			Members.objects
			.filter(project=project)
			.order_by('-is_admin', 'user__first_name', 'user__last_name')
			.select_related('user')
		)

		return api.response(
			{
				'uuid': project.uuid,
				'name': project.name,
				'description': project.description,
				'owner': project.owner.fio,
				'company': project.company.name,
				'base_url': project.base_url,
				'members': [
					{
						'user': member.user.fio,
						'is_admin': member.is_admin
					}
					for member in project_members
				]
			}
		)


class ProjectChangeOwnerViewV1(APIView):
	permission_classes = [IsAuthenticated, ]

	def post(self, request, project_uuid):
		try:
			project = Project.objects.get(uuid=project_uuid)
		except Project.DoesNotExist:
			return api.error_response(
				status=404,
				message='Проект не найден'
			)
		try:
			old_owner = Members.objects.get(project=project, user=request.user, is_admin=True)
			old_owner.is_admin = False
			old_owner.save()
		except Members.DoesNotExist:
			return api.error_response(
				status=403,
				message='Вы не являетесь администратором'
			)

		try:
			new_owner = User.objects.get(uuid=request.data.get('user'))
		except Company.DoesNotExist:
			return api.error_response(
				status=404,
				message='Компания не найдена'
			)
		project.owner = new_owner
		project.save()

		Members.objects.get_or_create(
			project=project,
			user=new_owner,
			is_admin=True
		)

		project.refresh_from_db()

		project_members = (
			Members.objects
			.filter(project=project)
			.order_by('-is_admin', 'user__first_name', 'user__last_name')
			.select_related('user')
		)

		return api.response(
			{
				'uuid': project.uuid,
				'name': project.name,
				'description': project.description,
				'owner': project.owner.fio,
				'company': project.company.name,
				'base_url': project.base_url,
				'members': [
					{
						'user': member.user.fio,
						'is_admin': member.is_admin
					}
					for member in project_members
				]
			}
		)
