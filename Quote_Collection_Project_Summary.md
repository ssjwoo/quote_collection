# Project: MOMENTARY (Quote Collection)

> **"오늘의 날씨와 기분에 건네는 한 문장, MOMENTARY"**
>
> **사용자의 취향(북마크)과 실시간 환경(날씨, 트렌드)을 분석하여 최적의 도서와 인용구를 큐레이션해주는 지능형 감성 AI 플랫폼**

---

## 1. 프로젝트 개요 (Overview)

단순한 명언 나열이 아닌, **사용자의 현재 상황(Context/Weather)**과 **관심사 히스토리(Bookmarks)**를 입체적으로 분석하여 가장 공감할 수 있는 문장을 추천합니다. **Google Search Grounding**을 통해 실존하는 도서 정보만을 엄선하며, **AI 심판관(LLM-as-a-Judge)** 시스템을 통해 추천 품질을 스스로 검증하고 지속적으로 고도화하는 Self-Improving 아키텍처를 지향합니다.

---

## 2. 기술 스택 (Tech Stack)

| Category | Technologies |
| :--- | :--- |
| **Frontend** | ![React](https://img.shields.io/badge/React-61DAFB?logo=react&logoColor=black) ![TailwindCSS](https://img.shields.io/badge/TailwindCSS-06B6D4?logo=tailwindcss&logoColor=white) ![Vite](https://img.shields.io/badge/Vite-646CFF?logo=vite&logoColor=white) |
| **Backend** | ![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white) ![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white) |
| **AI Engine** | ![Google Vertex AI](https://img.shields.io/badge/Google_Vertex_AI-4285F4?logo=googlecloud&logoColor=white) (Gemini 2.0 Flash) |
| **Database** | ![MySQL](https://img.shields.io/badge/MySQL-4479A1?logo=mysql&logoColor=white) ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?logo=sqlalchemy&logoColor=white) |
| **Infrastructure** | ![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?logo=googlecloud&logoColor=white) (Cloud Run, Firebase Hosting, Cloud Build) |

---

## 3. 핵심 아키텍처 및 상세 내용

### Seoul Context 기반 초개인화 추천
- **감성 컴퓨팅(Affective Computing)**: OpenWeatherMap API를 통해 서울의 실시간 날씨 정보를 수집하고, 이를 AI 프롬프트에 동적으로 주입하여 "비 오는 날 어울리는 에세이", "화창한 주말을 위한 여행기" 등 상황에 특화된 추천을 제공합니다.
- **취향 + 다양성 황금비**: 사용자가 지루함을 느끼지 않도록 '취향 기반(Stable, 70%)'과 '새로운 발견(Fresh, 30%)' 문구를 정교하게 혼합하는 **Mixture Ratio Strategy**를 적용했습니다.

### Grounding(그라운딩) 기반 신뢰성 확보
- **할루시네이션(Hallucination) 차단**: 생성형 AI의 고질적인 문제인 '없는 책 지어내기'를 방지하기 위해 **Google Search Grounding**과 **알라딘(Aladin) API**를 연동했습니다.
- **실시간 검증**: 추천된 도서 제목과 저자를 실시간으로 검색하여 표지 이미지, 출판 정보 등이 검증된 콘텐츠만 최종적으로 사용자에게 노출합니다.

### LLM-as-a-Judge (AI 자동 평가 시스템)
- **Self-Critique 파이프라인**: AI 모델이 생성한 추천 결과를 또 다른 AI(Judge)가 "사용자 맥락에 적합한가?"를 기준으로 5점 만점으로 채점합니다.
- **지표 시각화**: 평가 결과와 응답 속도(Latency)를 **Streamlit 대시보드**로 실시간 모니터링하여, 프롬프트 엔지니어링의 효과를 정량적으로 측정하고 개선합니다.

### 모바일 퍼스트(Mobile-First) UI/UX 최적화
- **반응형 디자인**: PC뿐만 아니라 모바일 환경에서도 완벽한 경험을 제공하기 위해 로고 정렬, 터치 영역, 폰트 가독성을 세밀하게 튜닝했습니다.
- **대량 데이터 최적화**: 마이페이지 북마크 목록에 **서버 사이드 페이징(Pagination)**을 도입하여 데이터가 쌓여도 쾌적한 로딩 속도를 유지합니다.

### Cloud Native 배포 및 보안
- **Full-Stack Serverless**: 백엔드는 **Cloud Run**, 프론트엔드는 **Firebase Hosting**을 활용하여 인프라 관리 부담을 없애고 비용 효율성을 극대화했습니다.
- **CORS & Security**: 엄격한 CORS 정책 적용 및 환경 변수 기반의 시크릿 관리로 운영 보안성을 확보했습니다.

---
