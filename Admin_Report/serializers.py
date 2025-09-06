from rest_framework import serializers
from .models import Admin_Report

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin_Report
        fields = '__all__'