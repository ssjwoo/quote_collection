# Quote Collection

## 📚 프로젝트 소개

**Quote Collection**은 책, 영화, 드라마, 실존 인물 등 다양한 출처의 인용구를 수집하고 공유할 수 있는 웹 플랫폼입니다. 마음에 드는 문장을 기록하고, 다른 사람들과 감동을 나눠보세요.

---

## 🛠️ 기술 스택

### Frontend

- **Framework/Library:** React.js
- **Styling:** Tailwind CSS
- **Build Tool:** Vite

### Backend

- **Framework:** FastAPI
- **Language:** Python
- **Database:** MySQL

---

## 📂 프로젝트 구조

```
quote_collection/
├── backend/         # FastAPI 백엔드 서버
│   ├── app/
│   └── tests/
└── frontend/        # React 프론트엔드 애플리케이션
    └── src/
```

---

## 🚀 시작하기

### Backend

1.  **가상환경 설정 및 의존성 설치:**
    ```bash
    # backend 디렉토리로 이동
    cd backend

    # uv 사용 시
    uv venv
    uv pip install -r requirements.txt
    ```

2.  **데이터베이스 설정:**
    `.env.example` 파일을 복사하여 `.env` 파일을 만들고, 본인의 데이터베이스 정보를 입력하세요.

3.  **서버 실행:**
    ```bash
    uvicorn app.main:app --reload
    ```

### Frontend

1.  **의존성 설치:**
    ```bash
    # frontend 디렉토리로 이동
    cd frontend
    npm install
    ```

2.  **개발 서버 실행:**
    ```bash
    npm run dev
    ```

---

## ✨ 주요 기능 (예정)

- [ ] 사용자 회원가입 및 로그인
- [ ] 인용구 작성, 수정, 삭제
- [ ] 출처별 (책, 영화, 드라마 등) 인용구 필터링
- [ ] 사용자별 '좋아요' 기능
- [ ] 다른 사용자의 컬렉션 구독
