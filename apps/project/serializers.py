from rest_framework import serializers

from .models import Project
from utils.serializers import UserSerializerV1, MembersSerializerV1
from ..company.serializers import CompanyDetailSerializerV1


class ProjectDetailSerializerV1(serializers.ModelSerializer):
	owner = UserSerializerV1(help_text='Владелец проекта')
	members = MembersSerializerV1(many=True, source='project_members', help_text='Участники проекта')
	company = CompanyDetailSerializerV1(help_text='Компания')

	class Meta:
		model = Project
		fields = [
			'uuid',
			'name',
			'company',
			'owner',
			'description',
			'base_url',
			'members'
		]