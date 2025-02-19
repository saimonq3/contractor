from rest_framework import serializers

from apps.company.models import Company
from utils.serializers import UserSerializerV1, MembersSerializerV1


class CompanyDetailSerializerV1(serializers.ModelSerializer):
	owner = UserSerializerV1(help_text='Владелец компании')
	members = MembersSerializerV1(many=True, source='company_members', help_text='Сотрудники компании')

	class Meta:
		model = Company
		fields = [
			'uuid',
			'name',
			'owner',
			'members'
		]


class CompanyListSerializerV1(serializers.ModelSerializer):
	owner = UserSerializerV1(help_text='Владелец компании')

	class Meta:
		model = Company
		fields = [
			'uuid',
			'name',
			'owner'
		]