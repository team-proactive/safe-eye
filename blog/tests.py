from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Post, Category, Tag, Comment

User = get_user_model()

class PostTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name='Test Category')
        self.tag1 = Tag.objects.create(name='Test Tag 1')
        self.tag2 = Tag.objects.create(name='Test Tag 2')

    def test_create_post(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Test Post',
            'content': 'This is a test post.',
            'category_id': self.category.id,
            'tag_ids': [self.tag1.id, self.tag2.id],
        }
        response = self.client.post('/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.category, self.category)
        self.assertIn(self.tag1, post.tags.all())
        self.assertIn(self.tag2, post.tags.all())

    def test_list_posts(self):
        Post.objects.create(title='Test Post 1', content='Content 1', author=self.user, category=self.category)
        Post.objects.create(title='Test Post 2', content='Content 2', author=self.user, category=self.category)
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_post(self):
        post = Post.objects.create(title='Test Post', content='Content', author=self.user, category=self.category)
        response = self.client.get(f'/posts/{post.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Post')

    def test_update_post(self):
        post = Post.objects.create(title='Test Post', content='Content', author=self.user, category=self.category)
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Updated Test Post',
            'content': 'Updated Content',
            'category_id': self.category.id,
            'tag_ids': [self.tag1.id],
        }
        response = self.client.put(f'/posts/{post.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertEqual(post.title, 'Updated Test Post')
        self.assertEqual(post.content, 'Updated Content')
        self.assertEqual(post.category, self.category)
        self.assertIn(self.tag1, post.tags.all())
        self.assertNotIn(self.tag2, post.tags.all())

    def test_delete_post(self):
        post = Post.objects.create(title='Test Post', content='Content', author=self.user, category=self.category)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/posts/{post.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)

class CommentTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.post = Post.objects.create(title='Test Post', content='Content', author=self.user)

    def test_create_comment(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'post': self.post.id,
            'content': 'Test Comment',
        }
        response = self.client.post(f'/posts/{self.post.id}/comments/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.first()
        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.content, 'Test Comment')

    def test_list_comments(self):
        Comment.objects.create(post=self.post, author=self.user, content='Comment 1')
        Comment.objects.create(post=self.post, author=self.user, content='Comment 2')
        response = self.client.get(f'/posts/{self.post.id}/comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_update_comment(self):
        comment = Comment.objects.create(post=self.post, author=self.user, content='Comment')
        self.client.force_authenticate(user=self.user)
        data = {
            'content': 'Updated Comment',
        }
        response = self.client.put(f'/posts/{self.post.id}/comments/{comment.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        comment.refresh_from_db()
        self.assertEqual(comment.content, 'Updated Comment')

    def test_delete_comment(self):
        comment = Comment.objects.create(post=self.post, author=self.user, content='Comment')
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/posts/{self.post.id}/comments/{comment.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)