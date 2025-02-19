from rest_framework import serializers


class CompanyUpdateQuerySerializer(serializers.Serializer):
	name = serializers.CharField(help_text='Новое название')


class CompanyMemberV1Serializer(serializers.Serializer):
	user_uuid = serializers.UUIDField(help_text='UUID пользователя')

class CompanyChangeMemberV1Serializer(serializers.Serializer):
	user_uuid = serializers.UUIDField(help_text='UUID пользователя')
	is_admin = serializers.BooleanField(help_text='Является администратором')