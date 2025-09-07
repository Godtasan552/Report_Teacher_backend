"""
URL configuration for Report_Teacher project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path,include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from Admin_Report.views import ReportViewSet
from users_AM import views as user_views
from django.conf import settings
from django.conf.urls.static import static


router = DefaultRouter()
router.register(r"reports", ReportViewSet, basename="report")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/admin_report/", include("users_AM.urls")),  # admin router
    path("api/users_report/", include("Admin_Report.urls")),  # search / user APIs
    path("api/auth/", include("users_AM.urls")),
]

# ถ้า DEBUG=True ให้ serve media files ทำให้สามารถเข้าถึงไฟล์ที่อัพโหลดผ่าน URL ได้
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)