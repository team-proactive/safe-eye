import requests
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import MediaFile
from .serializers import MediaFileSerializer

import os
from django.conf import settings

class MediaFileViewSet(viewsets.ModelViewSet):
    queryset = MediaFile.objects.all()
    serializer_class = MediaFileSerializer

    @action(detail=True, methods=['post'])
    def predict(self, request, pk=None):
        media_file = self.get_object()

        # PySlowFast API URL을 환경 변수에서 가져옴
        api_url = settings.PYSLOWFAST_API_URL
        payload = {'video_url': media_file.video.url}
        response = requests.post(api_url, json=payload)

        if response.status_code == 200:
            # API 응답 처리 로직
            result = response.json()
            output_video = result.get('output_video')
            abnormal_images = result.get('abnormal_images', [])
            coordinates = result.get('coordinates', [])

            # 결과를 MediaFile에 저장
            media_file.result = {
                'output_video': output_video,
                'abnormal_images': abnormal_images,
                'coordinates': coordinates
            }
            media_file.save()

            return Response(media_file.result, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Failed to predict'}, status=response.status_code)

