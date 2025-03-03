from django.contrib import admin

from utils.admin_mixin import CreatedByModelAdminMixin
from ..models import DTO, Field


class FieldsInLine(admin.TabularInline):
	model = Field
	extra = 0
	fields = [
		'created_by',
		'type',
		'value',
	]
	readonly_fields = [
		'created_by'
	]


@admin.register(DTO)
class DTOAdmin(CreatedByModelAdminMixin):
	list_display = [
		'uuid',
		'name',
		'project',
		'description',
		'id',
		'created_by'
	]
	fields = [
		'uuid',
		'name',
		'project',
		'description',
		'base_url',
		'id',
		'created_by'
	]
	readonly_fields = [
		'uuid',
		'id',
		'created_by'
	]

	inlines = [FieldsInLine, ]