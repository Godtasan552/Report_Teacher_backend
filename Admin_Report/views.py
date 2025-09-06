from rest_framework import viewsets,permissions
from rest_framework.response import Response
from .models import Admin_Report
from .serializers import ReportSerializer
import random, string

# สร้าง tracking_id แบบสุ่ม
def generate_tracking_id():
    return '#' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Admin_Report.object.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.AllowAny]  # อนุญาตให้ทุกคนเข้าถึง API นี้ได้
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["tracking_id"] = generate_tracking_id()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"tracking_id": serializer.data["tracking_id"]})

    def retrieve(self, request, *args, **kwargs):
        report = self.get_object()
        return Response({
            "tracking_id": report.tracking_id,
            "status": report.status,
            "response": report.response
        })