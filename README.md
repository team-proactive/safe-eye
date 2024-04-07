# Safe Eye README

Safe Eye는 실시간 군중 밀집도 모니터링과 화재 감지 기능을 통합한 스마트 안전 경고 알람 서비스입니다.

공공 안전, 이벤트 관리, 시설 관리 등 다양한 분야에서 안전 관리자가 군중 밀집과 화재 위험을 효율적으로 모니터링하고 대응할 수 있도록 도와줍니다. AI 기술과 직관적인 사용자 인터페이스를 통해 안전 관리 프로세스를 간소화하고 최적화하며, 잠재적인 위험 상황에 신속하게 대처.

## 주요 기능(종료일까지 가능한 것을 제작하고, 체크표시를 합니다.)

1. **실시간 모니터링 화면**

   - 다중 CCTV 카메라 피드를 실시간으로 표시
   - 군중 밀도 히트맵 오버레이와 화재 감지 상태 표시
   - 실시간 군중 수 및 밀도 백분율 표시
   - 사용자 정의 가능한 카메라 뷰 및 레이아웃
   - 이벤트 및 시간대 북마크 및 태그 기능

2. **상세 분석 화면**

   - 선택한 카메라 또는 영역의 고해상도 비디오 피드
   - 시간에 따른 군중 밀도 변화를 보여주는 타임라인 그래프
   - 화재 감지 이벤트 목록 및 상세 정보
   - 모니터링 영역의 상세 지도 또는 평면도
   - 사용자 메모 및 설명 추가 기능
   - 비디오 클립, 스크린샷 및 이벤트 데이터 내보내기

3. **경고 및 알람 설정 화면**

   - 맞춤형 군중 밀도 경고 및 화재 감지 알람 임계값 설정
   - 경고 및 알람 수준에 따른 특정 작업 설정
   - 생성형 AI 모델을 활용한 맥락 적합 경고 및 알람 메시지 자동 생성
   - 사용자 정의 가능한 알림 메시지 및 수신자 목록
   - 정기적인 테스트 및 훈련 예약 기능

4. **통계 및 보고 화면**

   - 군중 밀도 추세, 피크 시간 및 평균 밀도에 대한 대화형 그래프와 차트
   - 군중 밀도 및 화재 사고 지역 히트맵 오버레이
   - 화재 이벤트에 대한 상세 보고서 생성
   - 이벤트 데이터 필터링 및 정렬 옵션
   - 통계 데이터, 이벤트 로그 및 보고서 내보내기
   - 자동 보고서 생성 및 전달 예약 기능

5. **사용자 관리 및 설정 화면**
   - 다양한 액세스 수준 및 권한을 가진 사용자 계정 관리
   - 사용자 프로필 정보 업데이트 및 알림 기본 설정
   - 글로벌 시스템 설정 구성
   - AI 모델 관리 및 업데이트
   - 시스템 상태 모니터링 및 진단 도구
   - 사용자 인터페이스 테마 및 개인화 옵션

## 기술 스택

- Django
- Pillow: Python Imaging Library로, 이미지 처리 기능을 제공합니다.
- djangorestframework: Django 기반의 RESTful API를 구축하기 위한 프레임워크입니다.
- drf-yasg: Django REST Framework용 Swagger 생성기입니다. API 문서 자동화를 지원합니다.
- psycopg2-binary: PostgreSQL 데이터베이스와 연동하기 위한 어댑터입니다.
- django-cors-headers: 프론트엔드와의 연결을 위한 라이브러리
- django-environ: env 설정

현재 없는 것, JWT 관련 패키지.
accounts 앱을 담당하실 분이 관련 패키지를 설치한 후, 로그인 기능을 만들고 test id, test password, 프론트에 전달할 토큰 관련 설정을 여기에 적어주시면 됩니다.

```bash
   pip freeze > requirements.txt
```

## 아키텍쳐 예시

![e03cb933-eb4b-499c-88c1-d45d6ed31793](https://github.com/team-proactive/safe-eye/assets/89088205/c135a321-97a8-4ad3-b941-22a97f723345)

- 94-01 프론트 Next.js로 변경
- jenkins는 사용하지 않는게 좋겠다고 하셨음
- graphQL도 사용하지 않는게 좋겠다고 하셨음

## Django 공식 문서!

Django에 대한 자세한 내용은 공식 문서를 참고하세요: [https://docs.djangoproject.com/](https://docs.djangoproject.com/)

## GraphQL 공식 문서

GraphQL에 대한 자세한 내용은 공식 문서를 참고하세요: [https://graphql.org/learn/](https://graphql.org/learn/)

## DB - PostgreSQL 설치하기

프로젝트의 요구 조건인 `PostgreSQL`을 씁니다.

`PostgreSQL 16`을 씁니다. [소개 링크](https://postgresql.kr/news/pg16_release.html)

홈페이지 [여기](https://www.postgresql.org/)
다운로드는 [여기](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)

웹에 올려지는, 배포용 db는 공용이고, 로컬에서는 각자 로컬 db로 작업하겠습니다.

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

다운받은 것 중에 `터미널`을 사용하거나 `ADMIN`을 사용해서 서버와 DB를 만듭니다. 윈도우인 경우 `path 환경변수 설정`을 해주세요.
아름은 원하는거로 지어주시고 `database password`는 나중에 변경할 수 있긴 하지만 서버 설치 시에 정하는 것이므로 잊어버리지 않게 해주세요.

로컬호스트와 5432 부분은 그대로 둡니다.
여기 튜토리얼이 있습니다.

[커맨드라인](https://devpro.kr/posts/PSQL-%EC%82%AC%EC%9A%A9%EB%B2%95-%EC%A0%95%EB%A6%AC/)
[admin으로](https://blog.eunsukim.me/posts/usage-and-istallation-of-postgresql-and-pgadmin4)

## DRF 사용

이 프로젝트에서는 Django REST Framework(DRF)를 사용하여 RESTful API를 구축합니다.

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

## 폴더 구조

## ERD

## API 명세

## Notice 앱

`notice` 앱은 이 프로젝트의 예시 앱입니다. 이 앱은 공지사항 기능을 제공하며, 모델과 뷰, 시리얼라이저 등이 구현되어 있습니다.

이 앱의 모델과 API 엔드포인트를 참고하여 다른 앱을 개발할 수 있습니다.
