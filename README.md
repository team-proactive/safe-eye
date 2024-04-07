# Safe Eye - 스마트안전 경고 알람 서비스

Safe Eye는 CCTV 카메라와 AI 기술을 활용하여 공간 안전을 강화하고자 만든 프로젝트입니다. 컴퓨터 비전 및 인공지능 기술을 활용하여 CCTV 영상을 분석하고, 잠재적인 위험 상황을 신속하게 감지하여 대응할 수 있도록 안전 관리자를 지원합니다.

## 기능(되면 체크 표시)

1. **실시간 이상 행동 감지**

   - CCTV 영상에서 사람들의 행동을 실시간으로 분석하여 이상 행동을 감지합니다.
   - 폭력, 절도, 기물 파손 등 다양한 유형의 이상 행동을 인식할 수 있습니다.
   - 이상 행동 발생 시 즉각적인 알람을 발송하여 신속한 대응을 촉진합니다.

2. **상세 분석 화면**

   - 선택한 카메라 또는 영역의 고해상도 비디오 피드
   - 감지 이벤트 목록 및 상세 정보
   - 사용자 메모 및 설명 추가 기능
   - 비디오 클립, 스크린샷 및 이벤트 데이터 내보내기

3. **경고 및 알람 설정 화면**

   - 경고 및 알람 수준에 따른 특정 작업 설정
   - 생성형 AI 모델을 활용한 맥락 적합 경고 및 알람 메시지 자동 생성
   - 사용자 정의 가능한 알림 메시지 및 수신자 목록
   - 정기적인 테스트 및 훈련 예약 기능

4. **통계 및 보고 화면**

   - 기간 별 이벤트에 대한 상세 보고서 생성
   - 이벤트 데이터 필터링 및 정렬 옵션
   - 통계 데이터, 이벤트 로그 및 보고서 내보내기
   - 자동 보고서 생성 및 전달 예약 기능

5. **사용자 관리 및 설정 화면**
   - 사용자 프로필 정보 업데이트 및 알림 기본 설정
   - 시스템 상태 모니터링 및 진단 도구
   - 각 사용자의 스테이터스에 따라 알람을 분류

## 기술 스택(예상)

- 백엔드: Django, Pillow, DRF, 스웨거, NumPy
- 프론트엔드: Next.js
- 머신러닝: TensorFlow, PyTorch
- 컴퓨터 비전: OpenCV
- 데이터베이스: PostgreSQL
- 실시간 처리: Apache Kafka
- DevOps: Docker, Kubernetes

## 라이선스

SafeEye 프로젝트는 [MIT 라이선스](LICENSE)를 따릅니다.

## 시스템 요구사항

1. 환경 준비:

- 하드웨어 요구 사항: Ubuntu 18.04, 12th Gen Intel(R) Core(TM) i5 CPU, NVIDIA GeForce RTX 3070 GPU
- 소프트웨어 및 모듈 설치:
  Python 3.9과 CUDA 11.6 설치
  필요한 Python 모듈을 requirements.txt을 사용해 설치

2. 모델 정보:
   - LSTM과 MIL Ranking 모델 주로 이상 행동 인식에 사용
   - OpenPose와 UniPose 모델은 자세 추정에 사용

## 아키텍쳐 예시

![alt text](a-team.png)

## 설치 및 실행

1. 프로젝트 저장소 클론:

   ```
   git clone https://github.com/proactive/safe-eye.git
   cd Safe-eye
   ```

2. 필요한 종속성 설치:

   ```
   source ./venv/Scripts/activate
   pip install -r requirements.txt
   ```

   or

   ```
   ./commands.sh
   reinstall
   ```

3. 환경 변수 설정:

   ```
   cp .env.example .env
   # .env 파일을 편집하여 필요한 설정 값 입력
   ```

4. 데이터베이스 마이그레이션 실행:

   ```
   python manage.py migrate
   ```

   or

   ```
   ./commands.sh migrate
   ```

5. Django 서버 실행:

   ```
   python manage.py runserver
   ```

6. Next.js 프론트엔드 프로젝트 레포지토리:

   ```js
   // git clone
   git clone https://github.com/team-proactive/safe-eye-front.git
   cd safe-eye-front

   cp .env.local.example .env.local

   npm install
   npm run dev
   ```

## commands script file

1. `commands.sh` 파일을 실행하여 필요한 작업을 수행할 수 있습니다. 이 파일은 Git Bash에서 실행해야 합니다.

   - 세션 내에서 실행하고 가상환경을 종료하려면 `./commands.sh`를 입력합니다.
   - 세션이 종료되더라도 가상환경을 유지하려면 `. commands.sh`를 입력합니다.

2. 가상 환경을 생성하고 활성화하려면 `reinstall` 커맨드를 실행합니다. 추가로 설치할 패키지를 입력하라는 메시지가 표시되면 필요한 패키지를 입력하거나 엔터를 눌러 건너뛸 수 있습니다.

3. 데이터베이스 마이그레이션을 수행하려면 `migrate` 커맨드를 실행합니다.

4. 프로젝트를 실행하려면 `run` 커맨드를 실행합니다.

## 기타 커맨드

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
