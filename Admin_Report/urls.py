from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReportViewSet, search_report

router = DefaultRouter()
router.register("reports", ReportViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("reports/search/<str:tracking_id>/", search_report, name="search_report"),
]