# schema.py
import graphene
from graphene_django import DjangoObjectType
from .models import Notice
from .serializers import NoticeSerializer


class NoticeType(DjangoObjectType):
    class Meta:
        model = Notice
        fields = ("id", "title", "content", "created_at", "updated_at")
        serializer_class = NoticeSerializer


class Query(graphene.ObjectType):
    notices = graphene.List(NoticeType)

    def resolve_notices(self, info):
        queryset = Notice.objects.all()
        return queryset
