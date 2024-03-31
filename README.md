제안해주신 내용을 반영하여 README.md 파일을 업데이트했습니다:

# Django 프로젝트 README

이 프로젝트는 Django를 사용하여 개발된 웹 애플리케이션입니다. Django는 Python 기반의 웹 프레임워크로, 빠른 개발과 깨끗한 디자인을 지향합니다. 다음과 같은 패키지들이 설치되어 있습니다:

- Django
- Pillow: Python Imaging Library로, 이미지 처리 기능을 제공합니다.
- djangorestframework: Django 기반의 RESTful API를 구축하기 위한 프레임워크입니다.
- drf-yasg: Django REST Framework용 Swagger 생성기입니다. API 문서 자동화를 지원합니다.
- graphene-django: Django에서 GraphQL을 사용하기 위한 라이브러리입니다.
- psycopg2-binary: PostgreSQL 데이터베이스와 연동하기 위한 어댑터입니다.

현재 없는 것, JWT 관련 패키지.
accounts 앱을 담당하실 분이 관련 패키지를 설치한 후, 로그인 기능을 만들고 test id, test password, 프론트에 전달할 토큰 관련 설정을 여기에 적어주시면 됩니다.

```bash
   pip freeze > requirements.txt
```

# Django 프로젝트 README

아직 이름 못지음, 월요일 회의 때 짓겠습니다.

## Django 공식 문서

Django에 대한 자세한 내용은 공식 문서를 참고하세요: [https://docs.djangoproject.com/](https://docs.djangoproject.com/)

## GraphQL 공식 문서

GraphQL에 대한 자세한 내용은 공식 문서를 참고하세요: [https://graphql.org/learn/](https://graphql.org/learn/)

## DB - PostgreSQL 설치하기

프로젝트의 요구 조건인 `PostgreSQL`을 씁니다.

`PostgreSQL 16`을 씁니다. [소개 링크](https://postgresql.kr/news/pg16_release.html)

홈페이지 [여기](https://www.postgresql.org/)
다운로드는 [여기](https://www.enterprisedb.com/download-postgresql-binaries)

웹에 올려지는 db는 공통이고, 로컬에서는 각자 로컬 db로 작업하겠습니다.

1. `.env.example` 파일을 복사해서 `.env`를 만드세요.

```
DEBUG=True
SECRET_KEY=your_secret_key
ALLOWED_HOSTS="*", "localhost"

DATABASE_NAME=postgres
DATABASE_USER=postgres
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

다운받은 것 중에 `터미널`을 사용하거나 `GUI`용을 사용해서 서버와 DB를 만듭니다. 윈도우인 경우 `path 환경변수 설정`을 해주세요.
아름은 원하는거로 지어주시고 `database password`는 나중에 변경할 수 있긴 하지만 서버 설치 시에 정하는 것이므로 잊어버리지 않게 해주세요.

로컬호스트와 5432 부분은 그대로 둡니다.
여기 튜토리얼이 있습니다.

[커맨드라인](https://devpro.kr/posts/PSQL-%EC%82%AC%EC%9A%A9%EB%B2%95-%EC%A0%95%EB%A6%AC/)
[admin으로](https://blog.eunsukim.me/posts/usage-and-istallation-of-postgresql-and-pgadmin4)

## DRF와 GraphQL 조합하기

이 프로젝트에서는 Django REST Framework(DRF)를 사용하여 RESTful API를 구축합니다. 또한, GraphQL을 함께 사용하여 클라이언트의 요구에 맞게 유연하고 효율적인 데이터 쿼리를 제공할 수 있습니다.

### DRF 사용 예시

DRF를 사용하여 `Notice` 모델에 대한 API 엔드포인트를 구현하는 예시입니다:

```python
# views.py
from rest_framework import viewsets
from .models import Notice
from .serializers import NoticeSerializer

class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
```

```python
# serializers.py
from rest_framework import serializers
from .models import Notice

class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ("title", "content", "created_at", "updated_at")
```

위의 코드는 `NoticeViewSet`과 `NoticeSerializer`를 정의하여 `Notice` 모델에 대한 CRUD 작업을 수행할 수 있는 API 엔드포인트를 제공합니다.

### GraphQL 사용 예시

GraphQL을 사용하여 `Notice` 모델에 대한 쿼리를 구현하는 예시입니다:

```python
# schema.py
import graphene
from graphene_django import DjangoObjectType
from .models import Notice

class NoticeType(DjangoObjectType):
    class Meta:
        model = Notice
        fields = ("id", "title", "content", "created_at", "updated_at")

class Query(graphene.ObjectType):
    notices = graphene.List(NoticeType)

    def resolve_notices(self, info):
        return Notice.objects.all()
```

위의 코드는 `NoticeType`을 정의하여 `Notice` 모델의 필드를 지정하고, `Query` 클래스에서 `notices` 쿼리를 정의하여 모든 `Notice` 객체를 반환합니다.

### DRF와 GraphQL 조합 예시

DRF와 GraphQL을 함께 사용하여 `Notice` 모델에 대한 API를 구현하는 예시입니다:

```python
# schema.py
import graphene
from graphene_django import DjangoObjectType
from .models import Notice
from .serializers import NoticeSerializer

class NoticeType(DjangoObjectType):
    class Meta:
        model = Notice
        fields = ("id", "title", "content", "created_at", "updated_at")
        serializer_class = NoticeSerializer

class Query(graphene.ObjectType):
    notices = graphene.List(NoticeType)

    def resolve_notices(self, info):
        queryset = Notice.objects.all()
        return queryset
```

위의 코드에서는 `NoticeType`에 `serializer_class`를 지정하여 DRF 시리얼라이저를 사용하도록 설정합니다. 이렇게 하면 GraphQL 타입이 DRF 시리얼라이저를 사용하여 데이터를 직렬화하고 검증할 수 있습니다.

### 선택적으로 사용하기

프로젝트의 요구 사항에 따라 DRF만 사용하거나 DRF와 GraphQL을 함께 사용할 수 있습니다. AI의 도움을 받아보면 좋습니다.

- DRF만 사용하는 경우: RESTful API를 구축하고 싶거나, 간단한 CRUD 작업과 인증/권한 부여 등의 기능이 필요한 경우에 적합합니다.
- DRF와 GraphQL을 함께 사용하는 경우: RESTful API와 함께 복잡한 쿼리나 관련된 데이터를 효율적으로 가져오고 싶은 경우에 적합합니다. GraphQL을 사용하면 클라이언트가 필요한 데이터를 유연하게 요청할 수 있습니다.

## GraphQL 설정

1. 각 앱의 `schema.py` 파일에 GraphQL 타입과 쿼리를 정의합니다.

   ```python
   import graphene
   from graphene_django import DjangoObjectType
   from .models import Notice

   class NoticeType(DjangoObjectType):
       class Meta:
           model = Notice
           fields = ("id", "title", "content", "created_at", "updated_at")

   class Query(graphene.ObjectType):
       notices = graphene.List(NoticeType)

       def resolve_notices(self, info):
           return Notice.objects.all()
   ```

2. 프로젝트 레벨의 `schema.py` 파일에서 각 앱의 쿼리가 병합되어 있습니다.

   ```python
   import graphene
   from notice.schema import Query as NoticeQuery

   class Query(NoticeQuery, graphene.ObjectType):
       pass

   schema = graphene.Schema(query=Query)
   ```

위의 예시 코드는 `notice` 앱의 `schema.py` 파일에서 `Notice` 모델에 대한 GraphQL 타입과 쿼리를 정의하는 방법을 보여줍니다. `NoticeType`은 `Notice` 모델의 필드를 지정하고, `Query` 클래스에서는 `notices` 쿼리를 정의하여 모든 `Notice` 객체를 반환합니다.

프로젝트 레벨의 `schema.py` 파일에서는 각 앱의 쿼리를 병합하여 최종 스키마를 생성합니다.

## 설치 및 실행

1. 프로젝트를 클론한 후, 터미널에서 프로젝트 디렉토리로 이동합니다.

2. `commands.sh` 파일을 실행하여 필요한 작업을 수행할 수 있습니다. 이 파일은 Git Bash에서 실행해야 합니다.

   - 세션 내에서 실행하고 가상환경을 종료하려면 `./commands.sh`를 입력합니다.
   - 세션이 종료되더라도 가상환경을 유지하려면 `. commands.sh`를 입력합니다.

3. 가상 환경을 생성하고 활성화하려면 `install` 커맨드를 실행합니다. 추가로 설치할 패키지를 입력하라는 메시지가 표시되면 필요한 패키지를 입력하거나 엔터를 눌러 건너뛸 수 있습니다.

4. 데이터베이스 마이그레이션을 수행하려면 `migrate` 커맨드를 실행합니다.

5. 프로젝트를 실행하려면 `run` 커맨드를 실행합니다.

## 커맨드 설명

- `install`: 초기 설치를 수행합니다. 가상 환경을 생성하고 Django 프로젝트와 앱을 생성합니다.
- `activate`: 가상 환경을 활성화합니다.
- `migrate`: 데이터베이스 마이그레이션을 수행합니다.
- `run`: Django 개발 서버를 실행합니다.
- `create`: static, media, templates 디렉토리를 생성합니다.
- `static`: static 파일을 수집합니다.
- `reinstall`: 가상 환경을 재설치하고 `requirements.txt`에 명시된 패키지를 설치합니다.
- `remove`: 가상 환경을 제거합니다.
- `add_admin`: 관리자 계정을 생성합니다.
- `mock_data`: 애플리케이션의 초기 데이터를 로드합니다.

## Mock Data

`mock_data` 커맨드를 사용하여 애플리케이션의 초기 데이터를 로드할 수 있습니다. 이 데이터는 각 앱의 `fixtures/initial_data.json` 파일에 정의되어 있습니다.

모델을 변경한 후에는 안전하게 데이터베이스를 삭제하고, AI를 활용하여 해당 모델에 대한 `initial_data.json` 파일을 생성합니다. 그런 다음 `mock_data` 명령어를 사용하여 초기 데이터를 로드합니다.

## GraphQL

이 프로젝트는 GraphQL을 사용하여 API를 제공합니다. GraphQL은 클라이언트가 필요한 데이터를 정확하게 요청할 수 있는 쿼리 언어입니다. GraphQL 스키마는 `schema.py` 파일에 정의되어 있으며, 쿼리와 뮤테이션을 포함합니다.

GraphQL 엔드포인트에 접근하려면 `/graphql` URL을 사용하면 됩니다.

## Notice 앱

`notice` 앱은 이 프로젝트의 예시 앱입니다. 이 앱은 공지사항 기능을 제공하며, 모델과 뷰, 시리얼라이저 등이 구현되어 있습니다.

이 앱의 모델과 API 엔드포인트를 참고하여 다른 앱을 개발할 수 있습니다.
