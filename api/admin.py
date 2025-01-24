from django.contrib import admin

from api.models import WhitelistedUser


@admin.register(WhitelistedUser)
class WhitelistedUserAdmin(admin.ModelAdmin):
    list_display = (
        "telegram_id",
        "created_at",
    )
    list_filter = (
        "telegram_id",
    )
    search_fields = (
        "telegram_id",
    )
