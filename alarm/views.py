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
    """
    Alarm 모델에 대한 ViewSet.
    이 ViewSet은 Alarm 모델에 대한 CRUD 작업을 제공.

    Attributes
        queryset: Alarm 모델의 쿼리셋으로, 'created_at' 필드를 기준으로 내림차순으로 정렬.
        serializer_class: AlarmSerializer 클래스를 사용하여 직렬화/역직렬화를 수행.
        permission_classes: IsAuthorOrReadOnly 권한 클래스를 사용하여 접근 권한을 제어.
        pagination_class: CustomPageNumberPagination을 사용하여 페이지네이션을 구현.
        filter_backends: DjangoFilterBackend와 SearchFilter를 사용하여 필터링을 수행.
        filterset_fields: 필터링을 위한 필드로 'camera_id', 'alarm_type__code', 'risk__level'을 지정.
        search_fields: 검색을 위한 필드로 'alarm_content'와 'custom_message'를 지정.
        custom_404_message: 404 에러 발생 시 표시할 사용자 정의 메시지.

    Methods
        list(request, *args, **kwargs): 알람 목록을 반환하는 메서드.
        perform_create(serializer): 새로운 알람을 생성하는 메서드.
        update(request, *args, **kwargs): 기존 알람을 업데이트하는 메서드.
        perform_update(serializer): 알람을 업데이트하는 메서드.
        receive_alarm_data(request): GPT 모델 앱에서 알람 데이터를 받아 처리하는 메서드.
    """

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
        """
        알람 목록을 반환하는 메서드.

        Parameters
            request (HttpRequest): HTTP 요청 객체.
            *args: 추가 위치 인수.
            **kwargs: 추가 키워드 인수.

        Returns
            Response: 알람 목록이 포함된 HTTP 응답 객체.
        """
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        """
        새로운 알람을 생성하는 메서드.
        인증된 사용자가 'admin' 또는 'superuser' 역할을 가진 경우에만 알람을 생성 가능.
        인증되지 않은 경우 PermissionDenied 예외를 발생.

        Parameters
            serializer (AlarmSerializer): 알람 데이터가 포함된 serializer 객체.

        Raises
            PermissionDenied: 사용자가 알람을 생성할 수 있는 권한이 없는 경우 발생하는 예외.
        """
        admin = self.request.user
        if admin.is_authenticated and admin.role in ["admin", "superuser"]:
            serializer.save(admin=admin)
        else:
            raise PermissionDenied("이 작업을 수행할 권한이 없습니다.")

    def update(self, request, *args, **kwargs):
        """
        기존 알람을 업데이트하는 메서드.
        부분 업데이트를 지원하며, 업데이트된 알람 정보를 직렬화하여 응답.

        Parameters
            request (HttpRequest): HTTP 요청 객체.
            *args: 추가 위치 인수.
            **kwargs: 추가 키워드 인수.

        Returns
            Response: 업데이트된 알람 정보가 포함된 HTTP 응답 객체.
        """
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        """
        알람을 업데이트하는 메서드.
        인증된 사용자가 'admin' 또는 'superuser' 역할을 가진 경우에만 알람을 업데이트할 수 있음.
        인증되지 않은 경우 PermissionDenied 예외를 발생.

        Parameters
            serializer (AlarmSerializer): 알람 데이터가 포함된 serializer 객체.

        Raises
            PermissionDenied: 사용자가 알람을 업데이트할 수 있는 권한이 없는 경우 발생하는 예외.
        """
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
        """
        GPT 모델 앱에서 알람 데이터를 받아 처리하는 메서드.
        요청 데이터에서 알람 정보를 추출하고, 해당 정보를 사용하여 새로운 알람을 생성.
        생성된 알람을 직렬화하여 응답. 알람 유형 또는 위험 수준이 유효하지 않은 경우 적절한 오류 응답을 리턴.

        Parameters
            request (HttpRequest): HTTP 요청 객체.

        Returns
            Response: 생성된 알람 정보가 포함된 HTTP 응답 객체.
        """
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
    """
    Risk 모델에 대한 ViewSet.
    이 ViewSet은 Risk 모델에 대한 CRUD 작업을 제공.

    Attributes
        queryset: Risk 모델의 모든 객체를 쿼리셋으로 리턴.
        serializer_class: RiskSerializer 클래스를 사용하여 직렬화/역직렬화를 수행.
    """

    queryset = Risk.objects.all()
    serializer_class = RiskSerializer


class AlarmTypeViewSet(viewsets.ModelViewSet):
    """
    AlarmType 모델에 대한 ViewSet.
    이 ViewSet은 AlarmType 모델에 대한 CRUD 작업을 제공.

    Attributes
        queryset: AlarmType 모델의 모든 객체를 쿼리셋으로 리턴.
        serializer_class: AlarmTypeSerializer 클래스를 사용하여 직렬화/역직렬화를 수행.
    """

    queryset = AlarmType.objects.all()
    serializer_class = AlarmTypeSerializer
