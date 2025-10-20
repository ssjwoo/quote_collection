# 백엔드 문서

uv 설치 추천

## 설정

의존 패키지들을 설치: 

```bash
uv pip install -r requirements.txt
```

## 데이터베이스 마이그레이션

Alembic을 사용하여 데이터 마이그레이션을 적용:

```bash
uv run alembic upgrade head
```

모델 변경 후 새로운 마이그레이션을 생성하려면:

```bash
uv run alembic revision --autogenerate -m "Your migration message"
```

## 서버 실행

FastAPI 서버를 시작:

```bash
uv run main.py
```


## 데이터베이스 데이터 시딩 및 초기화

개발 및 테스트를 위한 더미 데이터를 관리하려면 `seed_data.py` 스크립트를 사용하십시오.

*   **데이터베이스를 시딩하려면** (기존 데이터를 모두 지우고 더미 데이터로 채웁니다):

    ```bash
uv run python -m app.seed_data --seed
    ```

*   **데이터베이스를 초기화 하려면** (확인 메시지에 yes 입력):

    ```bash
uv run python -m app.seed_data --wipe
    ```

## 테스트 실행

Pytest 실행:

```bash
uv run pytest
```

특정 테스트를 실행하려면 (예: 단일 파일):

```bash
uv run pytest tests/test_your_module.py
```