from rest_framework import serializers


class CompanyUpdateQuerySerializer(serializers.Serializer):
	name = serializers.CharField()


class CompanyMemberV1Serializer(serializers.Serializer):
	user = serializers.UUIDField()

class CompanyChangeMemberV1Serializer(serializers.Serializer):
	user = serializers.UUIDField()
	is_admin = serializers.BooleanField()