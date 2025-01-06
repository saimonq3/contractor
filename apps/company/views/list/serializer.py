from rest_framework import serializers


class CompanyListSerializerV1(serializers.Serializer):
	name = serializers.CharField(source='company.name')
	uuid = serializers.UUIDField(source='company.uuid')