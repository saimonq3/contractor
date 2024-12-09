from django.contrib import admin

from apps.company.models import Company, Members


class MemberInLine(admin.TabularInline):
	model = Members
	extra = 0

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
	inlines = [MemberInLine]
	list_display = [
		'uuid',
		'name',
		'owner',
		'arhived'
	]
	fields = [
		'uuid',
		'name',
		'owner',
		'arhived',
		'id'
	]

	readonly_fields = [
		'id',
		'uuid',
	]

	def delete_model(self, request, obj):
		if not request.user.is_superuser:
			obj.arhived = True
			obj.save()
			return
		return super().delete_model(request, obj)

	def delete_queryset(self, request, queryset):
		if not request.user.is_superuser:
			for company in queryset.iterator(chunk_size=50):
				company.arhived =True
			Company.objects.bulk_update(queryset, ['arhived'], batch_size=100)
			return
		return super().delete_queryset(request, queryset)
