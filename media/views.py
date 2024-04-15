import requests
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import MediaFile
from .serializers import MediaFileSerializer

class MediaFileViewSet(viewsets.ModelViewSet):
    queryset = MediaFile.objects.all()
    serializer_class = MediaFileSerializer

    @action(detail=True, methods=['post'])
    def predict(self, request, pk=None):
        media_file = self.get_object()

        # PySlowFast 모델 API 호출
        api_url = 'https://your-pyslowfast-api.com/predict'
        payload = {'video_url': media_file.video_url}
        response = requests.post(api_url, json=payload)

        if response.status_code == 200:
            result = response.json()
            media_file.result = result
            media_file.save()
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Failed to predict'}, status=response.status_code)

