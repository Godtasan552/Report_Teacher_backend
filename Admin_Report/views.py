from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Report
from .serializers import ReportSerializer
import random, string

# สร้าง tracking_id แบบสุ่ม
def generate_tracking_id():
    return "#" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))

# Permission สำหรับ admin เท่านั้น
class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    authentication_classes = [JWTAuthentication]  # เพิ่ม JWT authentication
    
    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy", "get_reports"]:
            return [IsAdminUser()]
        return [permissions.AllowAny()]

    # เพิ่มบรรทัดนี้เพื่อให้ serializer ใช้ request ในการสร้าง URL ของไฟล์
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def list(self, request, *args, **kwargs):
        return Response(
            {"error": "ใช้ POST /reports/get_reports/ แทน"}, 
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @action(detail=False, methods=['POST'], url_path='get_reports')
    def get_reports(self, request):
        # ... โค้ดเหมือนเดิม ...
        serializer = self.get_serializer(paginated_reports, many=True)
        return Response({
            'data': serializer.data,
            'pagination': {
                'page': page,
                'page_size': page_size,
                'total_count': total_count,
                'total_pages': (total_count + page_size - 1) // page_size
            },
            'filters_applied': filters
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["tracking_id"] = generate_tracking_id()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "tracking_id": serializer.data["tracking_id"],
            "message": "สร้างรายงานสำเร็จ"
        }, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def search_report(request, tracking_id):
    try:
        report = Report.objects.get(tracking_id=tracking_id)
        data = {
            "tracking_id": report.tracking_id,
            "teacher": report.teacher,
            "subject": report.subject,
            "detail": report.detail,
            "status": report.status,
            "status_display": report.get_status_display(),
            "response": report.response,
            "created_at": report.created_at,
            "file": report.file.url if report.file else None  # <-- แก้ตรงนี้
        }
        return Response(data, status=status.HTTP_200_OK)
    except Report.DoesNotExist:
        return Response({"error": "ไม่พบรายงาน"}, status=status.HTTP_404_NOT_FOUND)
