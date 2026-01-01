# 🛠️ 배포 트러블슈팅 및 장애 복구 보고서 (Cloud Run & Firebase)

본 문서는 Google Cloud Run(Back-end)과 Firebase Hosting(Front-end) 배포 과정에서 발생했던 치명적인 오류들과 이를 해결하기 위해 적용한 기술적 조치 사항들을 기록합니다.

---

## 1. 백엔드 배포 및 런타임 오류 (Cloud Run)

### 🚨 이슈 A: AI 추천 시스템 404 및 500 에러 발생
- **현상**: 배포 직후 AI 추천 요청 시 특정 경로를 찾지 못하거나 서버 내부 오류가 발생함.
- **원인**: 
    - `VertexAIClient` 초기화 시 구글 서치 그라운딩을 위한 `tools` 매개변수가 누락됨.
    - 코드 내에서 `url_quote`라는 존재하지 않는 함수를 호출하여 `NameError` 발생.
- **해결**:
    - `llm/vertex_client.py` 수정: `GenerativeModel` 생성 시 `Tool.from_google_search_retrieval`을 명시적으로 주입.
    - `llm/ai_service.py` 수정: `url_quote`를 표준 라이브러리인 `urllib.parse.quote`로 교체.

### 🚨 이슈 B: 라이브러리 버전 불일치 및 임포트 오류
- **현상**: Cloud Run 환경에서 `google-cloud-aiplatform` 관련 모듈을 불러오지 못해 서버가 크래시됨.
- **원인**: 로컬 환경과 배포 환경의 라이브러리 버전(1.38 vs 1.74) 차이로 인해 최신 접지(Grounding) 기능을 지원하지 못함.
- **해결**:
    - `requirements.txt` 업데이트: `google-cloud-aiplatform` 버전을 최신으로 고정.
    - 비동기 로딩 로직 도입: `_ensure_vertex_libs` 함수를 통해 라이브러리를 동적으로 안전하게 로드하도록 설계 변경.

### 🚨 이슈 C: 데이터베이스 커넥션 및 스키마 불일치
- **현상**: 특정 API 응답 시 `updated_at` 필드가 없다는 에러와 함께 500 오류 발생.
- **원인**: DB 모델(`Quote`)과 Pydantic 스키마(`QuoteRead`) 간의 필드 정의가 일치하지 않음.
- **해결**: 스키마 파일에서 누락되거나 불필요한 필드를 정리하여 정합성을 확보함.

---

## 2. 프론트엔드 및 통신 이슈 (Firebase & CORS)

### 🚨 이슈 D: CORS(Cross-Origin Resource Sharing) 정책 위반
- **현상**: 로컬 접속과 배포된 Firebase URL 접속 시 API 요청이 차단됨.
- **원인**: 백엔드 `main.py`의 CORS 허용 목록에 Firebase 호스팅 도메인이 누락되거나 세미콜론(;) 구분자 처리가 미흡했음.
- **해결**:
    - 백엔드 CORS 설정을 업데이트하여 로컬호스트 및 `de-caf.web.app` 도메인을 명시적으로 허용.
    - Cloud Build 설정(`cloudbuild.yaml`)에 환경 변수로 정확한 Origin 값 주입.

### 🚨 이슈 E: 't.map is not a function' 렌더링 오류
- **현상**: 배포된 사이트에서 데이터 로딩 후 화면이 하얗게 변하며 에러 발생.
- **원인**: AI 추천 결과가 비어있거나 예상치 못한 JSON 구조로 반환될 때 프론트엔드 배열 처리 로직이 충돌함.
- **해결**:
    - 백엔드: API 반환 시 항상 리스트 형태를 보장하도록 예외 처리.
    - 프론트엔드: `Array.isArray()` 체크 및 옵셔널 체이닝(`?.`)을 적용하여 렌더링 안정성 확보.

---

## 3. 인프라 및 환경 설정

### 🚨 이슈 F: 인코딩 오류 (UnicodeDecodeError)
- **현상**: 윈도우 환경에서 서버 기동 시 `.env` 파일을 읽지 못하는 현상.
- **원인**: 시스템 기본 인코딩(cp949)과 파일 인코딩(UTF-8) 충돌.
- **해결**: 환경 변수 로드 로직에 명시적 인코딩 옵션을 적용하거나 시스템 환경 변수를 재설정하여 해결.

---

## 💡 교훈 및 개선 방향
1. **환경 격차 최소화**: `Dockerfile`과 `requirements.txt`를 통해 배포 환경을 로컬과 최대한 동기화해야 함.
2. **방어적 프로그래밍**: 외부 API(AI, Aladin 등) 호출 시 반드시 폴백(Fallback) 로직을 갖춰야 함.
3. **로깅의 중요성**: Cloud Run 로그 탐색기를 통해 `stderr`와 `stdout`을 실시간 모니터링하는 것이 문제 해결의 열쇠였음.

모든 설명은 한국어로 제공됩니다.
