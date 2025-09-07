from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    file = serializers.SerializerMethodField()  # เปลี่ยนเป็น method field

    class Meta:
        model = Report
        fields = '__all__'

    def get_file(self, obj):
        request = self.context.get('request')
        if obj.file:
            return request.build_absolute_uri(obj.file.url)  # จะได้ URL เต็ม เช่น http://127.0.0.1:8000/media/xxx.pdf
        return None
