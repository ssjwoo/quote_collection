# MOMENTARY (Quote Collection)

**"오늘의 날씨와 기분에 건네는 한 문장, MOMENTARY"**

MOMENTARY는 단순한 명언집이 아닙니다. 사용자의 **현재 날씨, 시간, 기분** 그리고 **과거의 취향(북마크)**을 실시간으로 분석하여, 지금 이 순간 가장 필요한 책과 문장을 큐레이션해주는 지능형 감성 AI 플랫폼입니다.

---

## 주요 기능

### 1. Seoul Context 기반 초개인화 추천
- **감성 컴퓨팅**: OpenWeatherMap API를 통해 서울의 실시간 날씨와 시간대 정보를 수집합니다.
- **동적 프롬프트**: "비 오는 오후에 읽기 좋은 차분한 에세이", "화창한 주말을 위한 여행기" 등 상황에 맞는 추천을 제공합니다.
- **취향 + 다양성**: 사용자의 기존 취향을 반영함과 동시에(70%), 새로운 장르의 발견(30%)을 유도하는 혼합 추천 전략을 사용합니다.

### 2. Google Search Grounding 기반 신뢰성 확보
- **할루시네이션 방지**: 생성형 AI가 없는 책을 지어내는 문제를 방지하기 위해 Google Search Grounding 기술을 적용했습니다.
- **실시간 검증**: 추천된 도서와 저자가 실제 존재하는지 실시간으로 검색 및 검증하여 신뢰할 수 있는 정보만 제공합니다.

### 3. LLM-as-a-Judge (AI 자동 평가 시스템)
- **자율 품질 관리**: AI 모델이 생성한 추천 결과를 또 다른 AI(Judge)가 "사용자 맥락에 적합한가?"를 기준으로 채점(5점 만점)합니다.
- **성능 대시보드**: Streamlit 대시보드를 통해 추천 적합성 점수와 응답 속도를 실시간으로 모니터링하고 개선합니다.

### 4. 사용자 경험(UX) 고도화
- **모바일 퍼스트**: 모든 UI 컴포넌트는 모바일 환경에 최적화된 반응형 디자인으로 설계되었습니다.
- **대용량 데이터 처리**: 마이페이지의 북마크 및 업로드와 같은 대량 데이터 목록에 서버 사이드 페이징(Pagination)을 도입하여 빠른 로딩 속도를 보장합니다.

---

## 기술 스택

### Frontend
- **Framework**: React.js
- **Styling**: Tailwind CSS
- **Build Tool**: Vite
- **Deployment**: Firebase Hosting

### Backend
- **Framework**: FastAPI (Python Async)
- **Database**: MySQL (Google Cloud SQL)
- **AI Engine**: Google Vertex AI (Gemini 2.0 Flash)
- **Deployment**: Google Cloud Run

### AI & Data Pipeline
- **Orchestration**: Custom AI Service (Context Injection, Grounding)
- **Evaluation**: Streamlit (Dashboard), LLM-as-a-Judge Script

---

## 프로젝트 구조

```
quote_collection/
├── backend/            # FastAPI 백엔드
│   ├── app/            # 핵심 애플리케이션 로직
│   ├── llm/            # AI 서비스 및 프롬프트 관리
│   └── scripts/        # AI 평가 및 유틸리티 스크립트
└── frontend/           # React 프론트엔드
    └── src/            # 컴포넌트, 페이지, 훅
```

---

## 시작하기 (Getting Started)

### Backend

1.  **가상환경 설정 및 의존성 설치:**
    ```bash
    cd backend
    uv venv
    uv pip install -r requirements.txt
    ```

2.  **환경 변수 설정:**
    `.env` 파일을 생성하고 데이터베이스 접속 정보와 Google Cloud Project ID, API Key 등을 설정합니다.

3.  **서버 실행:**
    ```bash
    uvicorn app.main:app --reload
    ```

### Frontend

1.  **의존성 설치:**
    ```bash
    cd frontend
    npm install
    ```

2.  **개발 서버 실행:**
    ```bash
    npm run dev
    ```

### AI 평가 대시보드 실행

```bash
streamlit run backend/scripts/dashboard.py
```
