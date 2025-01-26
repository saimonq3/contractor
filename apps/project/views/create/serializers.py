from rest_framework import serializers


class ProjectCreateV1RequestQuery(serializers.Serializer):
	name = serializers.CharField()
	description = serializers.CharField(required=False)
	# Флаг который сообщает что надо всех сотрудников компании подключить к проекту
	add_company_members = serializers.BooleanField(default=False, required=False)
	base_url = serializers.CharField(default='', required=False)

