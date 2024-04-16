"""
이 모듈은 GraphQL 스키마를 정의합니다.

Notice 앱의 GraphQL 쿼리를 포함하고 있습니다.
"""

import graphene
from notice.schema import Query as NoticeQuery


class Query(NoticeQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
