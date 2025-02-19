from rest_framework import serializers

from apps.company.models import Company
from utils.serializers import UserSerializerV1, MembersSerializerV1


class CompanyDetailSerializerV1(serializers.ModelSerializer):
	owner = UserSerializerV1()
	members = MembersSerializerV1(many=True, source='company_members')

	class Meta:
		model = Company
		fields = [
			'uuid',
			'name',
			'owner',
			'members'
		]