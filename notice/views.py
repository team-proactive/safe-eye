from rest_framework import viewsets
from .models import Notice
from .serializers import NoticeSerializer
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CustomPageNumberPagination(PageNumberPagination):
    def get_page_size(self, request):
        if "page_size" in request.query_params:
            return min(int(request.query_params["page_size"]), 100)
        return self.page_size


class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.order_by("-created_at")
    serializer_class = NoticeSerializer
    pagination_class = CustomPageNumberPagination
    filter_fields = ["id", "title"]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="page_size",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Number of results to return per page.",
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
