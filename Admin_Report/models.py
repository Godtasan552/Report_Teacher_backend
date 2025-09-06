from django.db import models

# Create your models here.
STATUS_CHOICES = [
    ("ReportSent", "ทำการส่งรายงานแล้ว"), 
    ("Received", "ได้รับรายงานแล้ว"),
    ("Forwarding", "กำหลังส่งให้หน่วยงานที่เกี่ยวข้อง"),
    ("Pending", "กำลังการตรวจสอบ"),
    ("Checked", "ตรวจสอบเรียบร้อยแล้ว"),
    ("Completed", "ทำการแก้ไขปัญหาเรียบร้อยแล้ว"),
] 

class Report(models.Model):
    tracking_id =models.CharField(max_length=100, unique=True)
    teacher = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    detail = models.TextField()
    file = models.FileField(upload_to="uploads/", blank=True, null=True)
    status = models.CharField(
        max_length=50, 
        choices=STATUS_CHOICES, 
        default="ReportSent")
    respones  = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.tracking_id} - {self.teacher} - {self.subject}"
    