from graphene.test import Client
from django.test import TestCase
from notice.models import Notice
from notice.schema import Query
from graphene import Schema


class NoticeGraphQLTestCase(TestCase):
    """
    Notice GraphQL API에 대한 테스트 케이스
    """

    def setUp(self):
        """
        두 개의 Notice 인스턴스를 사용하여 테스트 케이스를 설정
        """
        print("테스트 케이스 설정 중...")
        Notice.objects.create(title="Test title 1", content="Test content 1")
        Notice.objects.create(title="Test title 2", content="Test content 2")
        self.client = Client(Schema(query=Query))

    def test_list_notices(self):
        """
        Notice GraphQL API의 `notices` 쿼리를 테스트
        """
        print("`notices` 쿼리 테스트 중...")
        response = self.client.execute("{ notices { title content } }")
        print("응답 받음. 응답 검증 중...")
        self.assertEqual(len(response["data"]["notices"]), 2)
        self.assertEqual(response["data"]["notices"][0]["title"], "Test title 1")
        self.assertEqual(response["data"]["notices"][0]["content"], "Test content 1")
        self.assertEqual(response["data"]["notices"][1]["title"], "Test title 2")
        self.assertEqual(response["data"]["notices"][1]["content"], "Test content 2")
        print("모든 검증 통과.")
