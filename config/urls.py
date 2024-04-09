from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from graphene_django.views import GraphQLView
from django.shortcuts import redirect
from .schema import schema

schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version="v1",
        description="API description",
    ),
    public=True,
)


def redirect_to_swagger(request):
    return redirect("/swagger/")


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/",
        include(
            [
                path("notice/", include("notice.urls")),
                # 추가적인 앱의 URL 패턴을 여기에 포함시킵니다.
                # 예: path("blog/", include("blog.urls")),
                #    path("users/", include("users.urls")),
            ]
        ),
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("graphql", GraphQLView.as_view(graphiql=True, schema=schema)),
    path("", redirect_to_swagger),
]