from django.contrib import admin

from ..models import Pact, QueryParams, Header
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
		'created_by',
		'directory'
	]
	fields = [
		'uuid',
		'dto',
		'method',
		'base_url',
		'body',
		'created_by',
		'directory'
	]

	readonly_fields = [
		'uuid',
		'id',
		'created_by'
	]