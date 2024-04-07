from rest_framework import generics
from .mixins import Custom404Mixin, IsAuthorOrReadOnly
from .models import Tag, Status
from .serializers import TagSerializer, StatusSerializer


class TagListCreateAPIView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()

    # 객체 생성 직전에 추가 로직을 실행 
#    def perform_create(self, serializer):
#        content_object = serializer.validated_data['content_object']     # content_object 의 작성자를 현재 사용자로 설정
#        content_object.author = self.request.user
#        content_object.save()
#        serializer.save()


class TagRetrieveUpdateDestroyAPIView(Custom404Mixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthorOrReadOnly]
    custom_404_message = "해당 태그를 찾을 수 없습니다."


class StatusListCreateAPIView(generics.ListCreateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()

#    # 객체 생성 직전에 추가 로직을 실행 
#    def perform_create(self, serializer):
#        content_object = serializer.validated_data['content_object']    # content_object 의 작성자를 현재 사용자로 설정
#        content_object.author = self.request.user
#        content_object.save()
#        serializer.save()


class StatusRetrieveUpdateDestroyAPIView(Custom404Mixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [IsAuthorOrReadOnly]
    custom_404_message = "해당 상태를 찾을 수 없습니다."