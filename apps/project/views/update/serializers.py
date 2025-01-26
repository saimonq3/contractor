from rest_framework import serializers


class ProjectMemberSerializerV1(serializers.Serializer):
	user_uuid = serializers.UUIDField()
	is_admin = serializers.BooleanField(default=False, required=False)


class ProjectUpdateInfoSerializerV1(serializers.Serializer):
	name = serializers.CharField(required=False)
	description = serializers.CharField(required=False)
	base_url = serializers.CharField(required=False)

	def update(self, instance, validated_data):
		instance.name = validated_data.get('name', instance.name)
		instance.description = validated_data.get('description', instance.description)
		instance.base_url = validated_data.get('base_url', instance.base_url)
		instance.save()
		return instance