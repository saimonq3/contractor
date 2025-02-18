from rest_framework import serializers

from apps.project.models import Project
from ...models import DTO


class ProjectSerializerV1(serializers.ModelSerializer):
	class Meta:
		model = Project
		fields = [
			'uuid',
			'name'
		]


class DTOSerializerV1(serializers.ModelSerializer):
	project = ProjectSerializerV1()
	class Meta:
		model = DTO
		fields = [
			'uuid',
			'name',
			'project',
			'description',
			'base_url'
		]