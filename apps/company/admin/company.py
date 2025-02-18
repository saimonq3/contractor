from django.contrib import admin

from apps.company.models import Company, Members
from utils.admin_mixin import CreatedByModelAdminMixin


class MemberInLine(admin.TabularInline):
	model = Members
	extra = 0

@admin.register(Company)
class CompanyAdmin(CreatedByModelAdminMixin):
	inlines = [MemberInLine, ]
	list_display = [
		'uuid',
		'name',
		'owner',
		'created_by'
	]
	fields = [
		'uuid',
		'name',
		'owner',
		'id',
		'created_by'
	]

	readonly_fields = [
		'id',
		'uuid',
		'created_by'
	]