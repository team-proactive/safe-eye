# tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from .models import Tag, Status

class TagTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.content_type = ContentType.objects.get_for_model(User)
        self.tag = Tag.objects.create(
            tag_type='test',
            tag_content='test',
            tag_id=1,
            content_type=self.content_type,
            object_id=self.user.id
        )

    def test_tag_list(self):
        response = self.client.get(reverse('tag_list'))
        self.assertEqual(response.status_code, 200)

    def test_tag_detail(self):
        response = self.client.get(reverse('tag_detail', args=[self.tag.id]))
        self.assertEqual(response.status_code, 200)

class StatusTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.content_type = ContentType.objects.get_for_model(User)
        self.status = Status.objects.create(
            available=True,
            content_type=self.content_type,
            object_id=self.user.id
        )

    def test_status_list(self):
        response = self.client.get(reverse('status_list'))
        self.assertEqual(response.status_code, 200)

    def test_status_detail(self):
        response = self.client.get(reverse('status_detail', args=[self.status.id]))
        self.assertEqual(response.status_code, 200)