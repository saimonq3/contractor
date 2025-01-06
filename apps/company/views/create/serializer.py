from rest_framework import serializers

from apps.company.models import Company


class CompanyCreateV1RequestQuery(serializers.Serializer):
	name = serializers.CharField()


class CompanyCreateSerializerV1(serializers.ModelSerializer):
	class Meta:
		model = Company
		fields = [
			'uuid',
			'name'
		]
