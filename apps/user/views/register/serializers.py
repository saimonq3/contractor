from rest_framework import serializers

from apps.user.models import User


class RegisterSerializer(serializers.ModelSerializer):
	phone_number = serializers.CharField(required=False)
	first_name = serializers.CharField(required=False)
	last_name = serializers.CharField(required=False)

	class Meta:
		model = User
		fields = [
			'email',
			'password',
			'phone_number',
			'first_name',
			'last_name'
		]
		extra_kwargs = {
			'password': {'write_only': True},
		}

	def create(self, validated_data):
		password = validated_data.pop('password')
		user = User(**validated_data)
		user.set_password(password)
		user.save()
		return user

	def validate_phone_number(self, value):
		if User.objects.filter(phone_number=value).exists():
			raise serializers.ValidationError('Пользователь с таким phone_number уже существует.')
		return value
