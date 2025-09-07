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
        # admin เท่านั้นที่แก้ไข / ดู list / ลบได้
        if self.action in ["update", "partial_update", "destroy", "get_reports"]:
            return [IsAdminUser()]
        # คนทั่วไปสามารถส่ง report ได้
        return [permissions.AllowAny()]
    
    # ปิดการใช้งาน list method เดิม
    def list(self, request, *args, **kwargs):
        return Response(
            {"error": "ใช้ POST /reports/get_reports/ แทน"}, 
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    @action(detail=False, methods=['POST'], url_path='get_reports')
    def get_reports(self, request):
        """ดึงรายการ reports ด้วย POST พร้อมรับเงื่อนไขการกรอง"""
        # รับพารามิเตอร์จาก request body
        filters = {}
        
        # กรองตามสถานะ
        if 'status' in request.data:
            filters['status'] = request.data['status']
        
        # กรองตามอาจารย์
        if 'teacher' in request.data:
            filters['teacher__icontains'] = request.data['teacher']
        
        # กรองตามวิชา
        if 'subject' in request.data:
            filters['subject__icontains'] = request.data['subject']
        
        # กรองตามช่วงเวลา
        if 'date_from' in request.data:
            filters['created_at__gte'] = request.data['date_from']
        
        if 'date_to' in request.data:
            filters['created_at__lte'] = request.data['date_to']
        
        # Query ข้อมูล
        reports = Report.objects.filter(**filters)
        
        # เรียงลำดับ
        order_by = request.data.get('order_by', '-created_at')
        reports = reports.order_by(order_by)
        
        # Pagination
        page_size = request.data.get('page_size', 20)
        page = request.data.get('page', 1)
        
        start = (page - 1) * page_size
        end = start + page_size
        
        paginated_reports = reports[start:end]
        total_count = reports.count()
        
        # Serialize ข้อมูล
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
        """สร้าง report ใหม่ พร้อม gen tracking_id"""
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
    """ค้นหารายงานด้วย tracking_id"""
    try:
        report = Report.objects.get(tracking_id=tracking_id)
        data = {
            "tracking_id": report.tracking_id,
            "teacher": report.teacher,
            "subject": report.subject,
            "detail": report.detail,
            "status": report.status,
            "response": report.response,
            "created_at": report.created_at,
        }
        return Response(data, status=status.HTTP_200_OK)
    except Report.DoesNotExist:
        return Response({"error": "ไม่พบรายงาน"}, status=status.HTTP_404_NOT_FOUND)