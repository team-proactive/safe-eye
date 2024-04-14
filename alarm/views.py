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
from django.core.exceptions import PermissionDenied
from rest_framework.decorators import action


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
                description="페이지당 결과 수를 지정합니다.",
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        admin = self.request.user
        if admin.is_authenticated and admin.role in ["admin", "superuser"]:
            serializer.save(admin=admin)
        else:
            raise PermissionDenied("이 작업을 수행할 권한이 없습니다.")

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        admin = self.request.user
        if admin.is_authenticated and admin.role in ["admin", "superuser"]:
            serializer.save(admin=admin)
        else:
            raise PermissionDenied("이 작업을 수행할 권한이 없습니다.")

    @action(detail=False, methods=["post"])
    @swagger_auto_schema(
        operation_description="GPT 모델 앱에서 알람 데이터 받기",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(type=openapi.TYPE_STRING),
                "risk_level": openapi.Schema(type=openapi.TYPE_STRING),
                "alarm_type_code": openapi.Schema(type=openapi.TYPE_STRING),
                "custom_message": openapi.Schema(type=openapi.TYPE_STRING),
                "camera_id": openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=["status", "risk_level", "alarm_type_code"],
        ),
        responses={200: "알람 데이터가 성공적으로 수신되고 처리되었습니다."},
    )
    def receive_alarm_data(self, request):
        alarm_data = request.data

        status = alarm_data.get("status")
        risk_level = alarm_data.get("risk_level")
        alarm_type_code = alarm_data.get("alarm_type_code")
        custom_message = alarm_data.get("custom_message", "")
        camera_id = alarm_data.get("camera_id", 1)

        try:
            alarm_type = AlarmType.objects.get(code=alarm_type_code)
            risk = Risk.objects.get(level=risk_level)
        except (AlarmType.DoesNotExist, Risk.DoesNotExist):
            return Response(
                {"detail": "유효하지 않은 알람 유형 또는 위험 수준입니다."}, status=400
            )

        alarm = Alarm.objects.create(
            admin=request.user,
            camera_id=camera_id,
            alarm_type=alarm_type,
            alarm_content=status,
            risk=risk,
            custom_message=custom_message,
        )

        serializer = self.get_serializer(alarm)

        return Response(serializer.data, status=200)


class RiskViewSet(viewsets.ModelViewSet):
    queryset = Risk.objects.all()
    serializer_class = RiskSerializer


class AlarmTypeViewSet(viewsets.ModelViewSet):
    queryset = AlarmType.objects.all()
    serializer_class = AlarmTypeSerializer
