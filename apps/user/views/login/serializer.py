from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
	username = serializers.CharField(write_only=True)
	password = serializers.CharField(trim_whitespace=False, write_only=True)
	token = serializers.CharField(read_only=True)

	def validate(self, attrs):
		username = attrs.get('username')
		password = attrs.get('password')

		if username and password:
			user_obj = get_user_model().objects.filter(username__iexact=username).first()

			if not user_obj:
				raise serializers.ValidationError()

			user = authenticate(
				request=self.context.get('request'),
				username=user_obj.get_username(),
				password=password
			)

			if not user:
				raise serializers.ValidationError()

		else:
			raise serializers.ValidationError()

		attrs['user'] = user
		return attrs