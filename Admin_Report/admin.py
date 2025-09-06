from django.contrib import admin
from .models import Admin_Report

@admin.register(Admin_Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ["tracking_id", "teacher", "subject", "status", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["tracking_id", "teacher", "subject"]

# Register your models here.
