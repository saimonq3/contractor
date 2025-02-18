from rest_framework import serializers

from apps.company.models import Members
from apps.user.models import User


class UserSerializerV1(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = [
			'fio'
		]


class MembersSerializerV1(serializers.ModelSerializer):
	user = UserSerializerV1()
	class Meta:
		model = Members
		fields = [
			'user',
			'is_admin'
		]
