from rest_framework import serializers

from apps.user.models import User


class UpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = [
			'first_name',
			'last_name',
			'patronymic',
			'country_code',
			'sex',
			'avatar'
		]