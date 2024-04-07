from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Tag, Status

User = get_user_model()


class TagTests(APITestCase):
    def setUp(self):
        print("태그 테스트 케이스 설정 중...")
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.client.force_authenticate(user=self.user)
        self.content_type = ContentType.objects.get_for_model(Tag)
        self.tag = Tag.objects.create(
            tag_type='test_type',
            tag_content='test_content',
            tag_id=1,
            content_type=self.content_type,
            object_id=1
        )
        print("태그 테스트 케이스 설정 완료.")

    def tearDown(self):
        print("태그 테스트 케이스 정리 중...")
        self.user.delete()
        self.tag.delete()
        print("태그 테스트 케이스 정리 완료.")

    def test_get_tags(self):
        print("태그 조회 테스트 중...")
        url = reverse('tag-list-create')
        print("GET 요청 전송 중...")
        response = self.client.get(url)
        print("응답 받음. 응답 검증 중...")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("태그 조회 테스트 통과.")

    def test_create_tag(self):
        print("태그 생성 테스트 중...")
        url = reverse('tag-list-create')
        data = {
            'tag_type': 'new_type',
            'tag_content': 'new_content',
            'tag_id': 2,
            'content_type': self.content_type.id,
            'object_id': 2
        }
        print("POST 요청 전송 중...")
        response = self.client.post(url, data, format='json')
        print("응답 받음. 응답 검증 중...")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tag.objects.count(), 2)
        print("태그 생성 테스트 통과.")

    def test_retrieve_tag(self):
        print("태그 조회 테스트 중...")
        url = reverse('tag-retrieve-update-destroy', kwargs={'pk': self.tag.id})
        print("GET 요청 전송 중...")
        response = self.client.get(url)
        print("응답 받음. 응답 검증 중...")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("태그 조회 테스트 통과.")

    def test_update_tag(self):
        print("태그 수정 테스트 중...")
        url = reverse('tag-retrieve-update-destroy', kwargs={'pk': self.tag.id})
        data = {
            'tag_type': 'updated_type',
            'tag_content': 'updated_content',
            'tag_id': 1,
            'content_type': self.content_type.id,
            'object_id': 1
        }
        print("PUT 요청 전송 중...")
        response = self.client.put(url, data, format='json')
        print("응답 받음. 응답 검증 중...")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tag.refresh_from_db()
        self.assertEqual(self.tag.tag_type, 'updated_type')
        print("태그 수정 테스트 통과.")

    def test_delete_tag(self):
        print("태그 삭제 테스트 중...")
        url = reverse('tag-retrieve-update-destroy', kwargs={'pk': self.tag.id})
        print("DELETE 요청 전송 중...")
        response = self.client.delete(url)
        print("응답 받음. 응답 검증 중...")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tag.objects.count(), 0)
        print("태그 삭제 테스트 통과.")


class StatusTests(APITestCase):
    def setUp(self):
        print("상태 테스트 케이스 설정 중...")
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.client.force_authenticate(user=self.user)
        self.content_type = ContentType.objects.get_for_model(Status)
        self.status = Status.objects.create(
            available=True,
            content_type=self.content_type,
            object_id=1
        )
        print("상태 테스트 케이스 설정 완료.")

    def tearDown(self):
        print("상태 테스트 케이스 정리 중...")
        self.user.delete()
        self.status.delete()
        print("상태 테스트 케이스 정리 완료.")

    def test_get_statuses(self):
        print("상태 조회 테스트 중...")
        url = reverse('status-list-create')
        print("GET 요청 전송 중...")
        response = self.client.get(url)
        print("응답 받음. 응답 검증 중...")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("상태 조회 테스트 통과.")

    def test_create_status(self):
        print("상태 생성 테스트 중...")
        url = reverse('status-list-create')
        data = {
            'available': False,
            'content_type': self.content_type.id,
            'object_id': 2
        }
        print("POST 요청 전송 중...")
        response = self.client.post(url, data, format='json')
        print("응답 받음. 응답 검증 중...")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Status.objects.count(), 2)
        print("상태 생성 테스트 통과.")

    def test_retrieve_status(self):
        print("상태 조회 테스트 중...")
        url = reverse('status-retrieve-update-destroy', kwargs={'pk': self.status.id})
        print("GET 요청 전송 중...")
        response = self.client.get(url)
        print("응답 받음. 응답 검증 중...")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("상태 조회 테스트 통과.")

    def test_update_status(self):
        print("상태 수정 테스트 중...")
        url = reverse('status-retrieve-update-destroy', kwargs={'pk': self.status.id})
        data = {
            'available': False,
            'content_type': self.content_type.id,
            'object_id': 1
        }
        print("PUT 요청 전송 중...")
        response = self.client.put(url, data, format='json')
        print("응답 받음. 응답 검증 중...")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.status.refresh_from_db()
        self.assertFalse(self.status.available)
        print("상태 수정 테스트 통과.")

    def test_delete_status(self):
        print("상태 삭제 테스트 중...")
        url = reverse('status-retrieve-update-destroy', kwargs={'pk': self.status.id})
        print("DELETE 요청 전송 중...")
        response = self.client.delete(url)
        print("응답 받음. 응답 검증 중...")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Status.objects.count(), 0)
        print("상태 삭제 테스트 통과.")