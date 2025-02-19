from rest_framework import serializers

from ...models import Company


class CompanyCreateV1RequestQuery(serializers.Serializer):
	name = serializers.CharField(help_text='Название компании')


class CompanyCreateSerializerV1(serializers.ModelSerializer):
	class Meta:
		model = Company
		fields = [
			'uuid',
			'name'
		]
