from rest_framework import serializers

class ProjectRemoveOrChangeOwnerMemberQuerySerializer(serializers.Serializer):
	user_uuid = serializers.CharField(help_text='UUID пользователя')


class ProjectMemberQuerySerializer(serializers.Serializer):
	user_uuid = serializers.CharField(help_text='UUID пользователя')
	is_admin = serializers.BooleanField(help_text='Является администратором', default=False, required=False)


class ProjectChangeCompanyQuerySerializer(serializers.Serializer):
	company_uuid = serializers.CharField(help_text='UUID компании')


class ProjectUpdateInfoSerializerV1(serializers.Serializer):
	name = serializers.CharField(required=False, help_text='Название проекта')
	description = serializers.CharField(required=False, help_text='Описание проекта')
	base_url = serializers.CharField(required=False, help_text='Базовый URL')

	def update(self, instance, validated_data):
		instance.name = validated_data.get('name', instance.name)
		instance.description = validated_data.get('description', instance.description)
		instance.base_url = validated_data.get('base_url', instance.base_url)
		instance.save()
		return instance