from rest_framework import viewsets
from .mixins import Custom404Mixin, IsAuthorOrReadOnly
from .models import Tag, Status
from .serializers import TagSerializer, StatusSerializer
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CustomPageNumberPagination(PageNumberPagination):
    """
    사용자 정의 페이지네이션 클래스.
    PageNumberPagination을 상속받아 페이지 크기를 동적으로 조정하는 기능을 제공.

    Methods
        get_page_size(request): 요청에 따라 페이지 크기를 결정하는 메서드.
    """

    def get_page_size(self, request):
        """
        요청에 따라 페이지 크기를 결정하는 메서드.
        이 메서드는 요청 매개변수 'page_size'를 확인하여 페이지 크기를 동적으로 조정.
        'page_size' 매개변수가 존재하면 해당 값을 정수로 변환하여 리턴, 최대 100을 초과하지 않도록 제한.
        'page_size' 매개변수가 없으면 기본 페이지 크기를 리턴.

        Parameters
            request (HttpRequest): HTTP 요청 객체.

        Returns
            int: 결정된 페이지 크기.
        """
        if "page_size" in request.query_params:
            return min(int(request.query_params["page_size"]), 100)
        return self.page_size


class TagViewSet(Custom404Mixin, viewsets.ModelViewSet):
    """
    Tag 모델에 대한 ViewSet.
    이 ViewSet은 Tag 모델에 대한 CRUD 작업을 제공.

    Attributes
        queryset: Tag 모델의 쿼리셋으로, 'id' 필드를 기준으로 내림차순으로 정렬.
        serializer_class: TagSerializer 클래스를 사용하여 직렬화/역직렬화를 수행.
        permission_classes: IsAuthorOrReadOnly 권한 클래스를 사용하여 접근 권한을 제어.
        pagination_class: CustomPageNumberPagination을 사용하여 페이지네이션을 구현.
        filter_fields: 필터링을 위한 필드로 'id', 'tag_type', 'tag_content'를 지정.
        custom_404_message: 404 에러 발생 시 표시할 사용자 정의 메시지.

    Methods
        list(request, *args, **kwargs): tag 목록을 반환하는 메서드.
        perform_create(serializer): 새로운 tag를 생성하는 메서드.
    """

    queryset = Tag.objects.order_by("-id")  # 정렬 조건 추가
    serializer_class = TagSerializer
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = CustomPageNumberPagination
    filter_fields = ["id", "tag_type", "tag_content"]
    custom_404_message = "해당 tag를 찾을 수 없습니다."

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
        """
        tag 목록을 반환하는 메서드.

        Parameters
            request (HttpRequest): HTTP 요청 객체.
            *args: 추가 위치 인수.
            **kwargs: 추가 키워드 인수.

        Returns
            Response: tag 목록이 포함된 HTTP 응답 객체.
        """
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        """
        새로운 tag를 생성하는 메서드.

        Parameters
            serializer (TagSerializer): tag 데이터가 포함된 serializer 객체.
        """
        serializer.save()


class StatusViewSet(Custom404Mixin, viewsets.ModelViewSet):
    """
    Status 모델에 대한 ViewSet.
    이 ViewSet은 Status 모델에 대한 CRUD 작업을 제공.

    Attributes
        queryset: Status 모델의 쿼리셋으로, 'created_at' 필드를 기준으로 내림차순으로 정렬.
        serializer_class: StatusSerializer 클래스를 사용하여 직렬화/역직렬화를 수행.
        permission_classes: IsAuthorOrReadOnly 권한 클래스를 사용하여 접근 권한을 제어.
        pagination_class: CustomPageNumberPagination을 사용하여 페이지네이션을 구현.
        filter_fields: 필터링을 위한 필드로 'id'와 'available'을 지정.
        custom_404_message: 404 에러 발생 시 표시할 사용자 정의 메시지.

    Methods
        list(request, *args, **kwargs): status 목록을 반환하는 메서드.
        perform_create(serializer): 새로운 status를 생성하는 메서드.
    """

    queryset = Status.objects.order_by("-created_at")
    serializer_class = StatusSerializer
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = CustomPageNumberPagination
    filter_fields = ["id", "available"]
    custom_404_message = "해당 status 를 찾을 수 없습니다."

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
        """
        status 목록을 반환하는 메서드.

        Parameters
            request (HttpRequest): HTTP 요청 객체.
            *args: 추가 위치 인수.
            **kwargs: 추가 키워드 인수.

        Returns
            Response: status 목록이 포함된 HTTP 응답 객체.
        """
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        """
        새로운 status를 생성하는 메서드.

        Parameters
            serializer (StatusSerializer): status 데이터가 포함된 serializer 객체.
        """
        serializer.save()
