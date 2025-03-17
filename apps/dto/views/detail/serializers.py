from rest_framework import serializers

from ..list.serializers import ProjectSerializerV1
from ...models import DTO, Field


class FieldsSerializerV1(serializers.ModelSerializer):
	class Meta:
		model = Field
		fields = [
			'uuid',
			'type',
			'value',
			'description'
		]


class DTODetailSerializer(serializers.ModelSerializer):
	project = ProjectSerializerV1()
	fields = FieldsSerializerV1(source='dto_fields', many=True)

	class Meta:
		model = DTO
		fields = [
			'uuid',
			'name',
			'description',
			'project',
			'base_url',
			'fields'
		]