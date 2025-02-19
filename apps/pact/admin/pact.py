from django.contrib import admin
from apps.pact.models import Pact, QueryParams, Header
from utils.admin_mixin import CreatedByModelAdminMixin


class QueryParamsInLine(admin.TabularInline):
	model = QueryParams
	extra = 0


class HeadersInLine(admin.TabularInline):
	model = Header
	extra = 0


@admin.register(Pact)
class PactAdmin(CreatedByModelAdminMixin):
	inlines = [
		QueryParamsInLine,
		HeadersInLine
	]
	list_display = [
		'uuid',
		'method',
		'created_by'
	]
	fields = [
		'uuid',
		'dto',
		'method',
		'base_url',
		'body',
		'created_by'
	]

	readonly_fields = [
		'uuid',
		'id',
		'created_by'
	]