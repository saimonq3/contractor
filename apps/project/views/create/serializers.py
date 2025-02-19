from rest_framework import serializers


class ProjectCreateV1RequestQuery(serializers.Serializer):
	name = serializers.CharField(help_text='Название проекта')
	description = serializers.CharField(required=False, help_text='Описание прокета')
	# Флаг который сообщает что надо всех сотрудников компании подключить к проекту
	add_company_members = serializers.BooleanField(default=False, required=False, help_text='Добавить всех сотрудников компании в проект')
	base_url = serializers.CharField(default='', required=False, help_text='Базовый URL')

