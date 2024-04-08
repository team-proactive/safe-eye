import graphene
from graphene_django import DjangoObjectType
from .models import MediaFile
from .serializers import MediaFileSerializer

class MediaFileType(DjangoObjectType):
    class Meta:
        model = MediaFile
        fields = ('id', 'file', 'created_at')
        serializer_class = MediaFileSerializer

class Query(graphene.ObjectType):
    media_files = graphene.List(MediaFileType)

    def resolve_media_files(self, info):
        return MediaFile.objects.all()