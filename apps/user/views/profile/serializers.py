from rest_framework import serializers

from apps.user.models import User


class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = [
			'first_name',
			'last_name',
			'patronymic',
			'username',
			'email',
			'email_verified'
		]