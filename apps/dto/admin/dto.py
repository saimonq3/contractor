from django.contrib import admin

from apps.dto.models import DTO, Field


class FieldsInLine(admin.TabularInline):
	model = Field
	extra = 0


@admin.register(DTO)
class DTOAdmin(admin.ModelAdmin):
	list_display = [
		'uuid',
		'name',
		'project',
		'description',
		'id'
	]
	fields = [
		'uuid',
		'name',
		'project',
		'description',
		'base_url',
		'id'
	]
	readonly_fields = [
		'uuid',
		'id'
	]

	inlines = [FieldsInLine,]