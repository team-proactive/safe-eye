from django.test import TestCase
from .models import MediaFile
from .serializers import MediaFileSerializer
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import MediaFile
from .serializers import MediaFileSerializer
import os
import shutil
import tempfile

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

class MediaFileViewSetTestCase(APITestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.video_file = os.path.join(self.temp_dir, 'test_video.mp4')
        with open(self.video_file, 'wb') as f:
            f.write(b'dummy video data')

        self.media_file = MediaFile.objects.create(file=self.video_file)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_predict_success(self):
        url = reverse('media-file-predict', args=[self.media_file.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('result', response.data)

    def test_predict_invalid_file(self):
        invalid_file = MediaFile.objects.create(file='invalid_file.txt')
        url = reverse('media-file-predict', args=[invalid_file.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_predict_response_format(self):
        url = reverse('media-file-predict', args=[self.media_file.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id', response.data)
        self.assertIn('file', response.data)
        self.assertIn('result', response.data)
        self.assertIsInstance(response.data['result'], dict)
        self.assertIn('class_names', response.data['result'])
        self.assertIn('probabilities', response.data['result'])
    