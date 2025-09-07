from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
     # เพิ่ม field status_display เพื่อดึงค่าที่เป็นภาษาไทย
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    class Meta:
        model = Report
        fields = '__all__'