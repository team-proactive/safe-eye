from rest_framework import status, viewsets
from rest_framework.response import Response
from .models import CustomUser, Status
from .serializers import CustomUserSerializer, StatusSerializer
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .permissions import IsOwnerOrReadOnly
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsOwnerOrReadOnly]

    @action(detail=False, methods=["post"])
    def signup(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"])
    def login(self, request):
        # 로그인 처리를 위한 코드 작성
        pass

    @action(detail=True, methods=["put"])
    def update_info(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["delete"])
    def withdraw(self, request, pk=None):
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


@receiver(post_save, sender=CustomUser)
def set_default_status(sender, instance, created, **kwargs):
    if created:
        default_status = Status.objects.get(name="Default")
        instance.status = default_status
        instance.save()
