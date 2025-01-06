from rest_framework import serializers


class CompanyUpdateQuerySerializer(serializers.Serializer):
	name = serializers.CharField()


class CompanyChangeOwnerQuerySerializer(serializers.Serializer):
	user = serializers.UUIDField()