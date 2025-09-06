from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Report
from .serializers import ReportSerializer
import random, string

# สร้าง tracking_id แบบสุ่ม
def generate_tracking_id():
    return "#" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))

# Permission สำหรับ admin
class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def get_permissions(self):
        # สำหรับ update, partial_update, destroy, list → admin เท่านั้น
        if self.action in ["update", "partial_update", "destroy", "list"]:
            return [IsAdminUser()]
        # สำหรับ create, retrieve → ทุกคน
        return [permissions.AllowAny()]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["tracking_id"] = generate_tracking_id()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # ส่งกลับเฉพาะ tracking_id
        return Response({"tracking_id": serializer.data["tracking_id"]})

    def retrieve(self, request, *args, **kwargs):
        report = self.get_object()
        return Response({
            "tracking_id": report.tracking_id,
            "status": report.status,
            "response": report.response
        })
