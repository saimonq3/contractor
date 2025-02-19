from rest_framework import serializers

from apps.user.models import User


class UpdateSerializer(serializers.ModelSerializer):
	first_name = serializers.CharField(required=False)
	last_name = serializers.CharField(required=False)
	class Meta:
		model = User
		fields = [
			'first_name',
			'last_name',
			'patronymic',
			'avatar'
		]