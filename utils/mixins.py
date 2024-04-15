from django.http import Http404
from django.shortcuts import render
from rest_framework import permissions


class Custom404Mixin:
    """
    사용자 정의 404 에러 페이지를 제공하는 mixin 클래스.
    404 에러가 발생했을 때, 기본 404 페이지 대신 사용자 정의 404 페이지를 리턴.
    custom_404_message 속성을 통해 사용자 정의 에러 메시지를 지정 가능.

    Attributes
    custom_404_message (str): 사용자 정의 404 에러 메시지.
    """

    custom_404_message = None

    def dispatch(self, request, *args, **kwargs):
        """
        HTTP 요청을 처리하고 응답을 반환하는 메서드.
        요청 처리 중에 Http404 예외가 발생하면, 사용자 정의 404 페이지 리턴.
        custom_404_message 속성이 설정되어 있으면 해당 메시지를 사용하고, 그렇지 않으면 기본 메시지를 사용.

        Parameters
        request (HttpRequest): HTTP 요청 객체.
        *args: 추가 위치 인수.
        **kwargs: 추가 키워드 인수.

        Returns
        HttpResponse: HTTP 응답 객체.
        """
        try:
            return super().dispatch(request, *args, **kwargs)
        except Http404:
            message = self.custom_404_message or "페이지를 찾을 수 없습니다."
            context = {"message": message}
            return render(request, "custom_404.html", context, status=404)


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    사용자 정의 권한 클래스.
    요청 메서드가 안전한 메서드(GET, HEAD, OPTIONS)인 경우에는 모든 사용자에게 권한을 허용.
    인증된 사용자가 admin 또는 superuser 역할을 가지고 있고, 해당 객체의 작성자(admin)와 일치하는 경우에만 쓰기 권한을 부여.
    """

    def has_object_permission(self, request, view, obj):
        """
        객체 수준에서 사용자의 권한을 확인하는 메서드.

        Parameters
        request (HttpRequest): HTTP 요청 객체.
        view (View): 호출된 뷰.
        obj (Model): 확인할 모델 객체.

        Returns
        bool: 사용자에게 권한이 있는 경우 True, 그렇지 않은 경우 False.
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_authenticated:
            if request.user.role in ["admin", "superuser"]:
                return obj.admin == request.user
            else:
                return False

        return False
