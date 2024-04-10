from django.test import TestCase
from .models import MediaFile
from .serializers import MediaFileSerializer
from rest_framework.test import APIClient
from rest_framework import status

class MediaFileTestCase(TestCase):
    def setUp(self):
        # 테스트에 필요한 초기 설정 및 데이터 생성
        self.media_file = MediaFile.objects.create(file='path/to/file.jpg')
        self.client = APIClient()

    def test_media_file_model(self):
        # MediaFile 모델 테스트
        self.assertEqual(self.media_file.file.name, 'path/to/file.jpg')

    

    def test_media_file_list_view(self):
        # MediaFileViewSet의 list 액션 테스트
        response = self.client.get('/media/files/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_media_file_serializer(self):
        serializer = MediaFileSerializer(self.media_file)
        expected_data = {
            'id': self.media_file.id,
            'file': self.media_file.file.url,
            'created_at': serializer.data['created_at'],
            'description': serializer.data['description'],
            'file_size': serializer.data['file_size'],
            'file_type': serializer.data['file_type'],
        }
        self.assertEqual(serializer.data, expected_data)
    
    def test_media_file_predict_view(self):
        # MediaFileViewSet의 predict 액션 테스트
        response = self.client.post(f'/media/files/{self.media_file.id}/predict/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('result', response.data)
        self.assertEqual(response.data['result'], 'prediction')
    