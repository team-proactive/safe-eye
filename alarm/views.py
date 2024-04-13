from rest_framework import viewsets, filters
from .models import Alarm, Risk, AlarmType
from .serializers import AlarmSerializer, RiskSerializer, AlarmTypeSerializer
from utils.mixins import Custom404Mixin
from django_filters.rest_framework import DjangoFilterBackend
from utils.views import CustomPageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from utils.mixins import IsAuthorOrReadOnly


class AlarmViewSet(Custom404Mixin, viewsets.ModelViewSet):
    queryset = Alarm.objects.order_by("-created_at")
    serializer_class = AlarmSerializer
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["camera_id", "alarm_type__code", "risk__level"]
    search_fields = ["alarm_content", "custom_message"]
    custom_404_message = "해당 알람을 찾을 수 없습니다."

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
        user = self.request.user
        if user.is_authenticated:
            serializer.save(user=user)
        else:
            serializer.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        user = self.request.user
        if user.is_authenticated:
            serializer.save(user=user)
        else:
            serializer.save()


class RiskViewSet(viewsets.ModelViewSet):
    queryset = Risk.objects.all()
    serializer_class = RiskSerializer


class AlarmTypeViewSet(viewsets.ModelViewSet):
    queryset = AlarmType.objects.all()
    serializer_class = AlarmTypeSerializer
