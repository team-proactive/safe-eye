import graphene
from notice.schema import Query as NoticeQuery


class Query(NoticeQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)