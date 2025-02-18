from django.contrib import admin


class CreatedByModelAdminMixin(admin.ModelAdmin):

    def __init__(self, *args, **kwargs):
        self.readonly_fields = list(self.readonly_fields) + ['created_by']
        super().__init__(*args, **kwargs)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)