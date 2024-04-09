from rest_framework import viewsets
from .mixins import Custom404Mixin, IsAuthorOrReadOnly
from .models import Tag, Status
from .serializers import TagSerializer, StatusSerializer
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CustomPageNumberPagination(PageNumberPagination):
    def get_page_size(self, request):
        if "page_size" in request.query_params:
            return min(int(request.query_params["page_size"]), 100)
        return self.page_size


class TagViewSet(Custom404Mixin, viewsets.ModelViewSet):
    queryset = Tag.objects.order_by("-id")  # 정렬 조건 추가
    serializer_class = TagSerializer
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = CustomPageNumberPagination
    filter_fields = ["id", "tag_type", "tag_content"]
    custom_404_message = "해당 태그를 찾을 수 없습니다."

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

    def perform_create(self, serializer):
        serializer.save()


class StatusViewSet(Custom404Mixin, viewsets.ModelViewSet):
    queryset = Status.objects.order_by("-created_at")
    serializer_class = StatusSerializer
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = CustomPageNumberPagination
    filter_fields = ["id", "available"]
    custom_404_message = "해당 상태를 찾을 수 없습니다."

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

    def perform_create(self, serializer):
        serializer.save()
