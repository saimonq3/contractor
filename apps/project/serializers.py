from rest_framework import serializers

from .models import Project
from utils.serializers import UserSerializerV1, MembersSerializerV1
from ..company.serializers import CompanyDetailSerializerV1


class ProjectDetailSerializerV1(serializers.ModelSerializer):
	owner = UserSerializerV1()
	members = MembersSerializerV1(many=True, source='project_members')
	company = CompanyDetailSerializerV1()

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