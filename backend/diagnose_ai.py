import os
import sys
import asyncio

# llm 폴더를 sys.path에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../llm")))

from ai_service import AIService
from dotenv import load_dotenv

load_dotenv()

async def diagnose():
    project_id = os.getenv("GOOGLE_PROJECT_ID")
    location = "us-central1"
    
    print(f"진단 시작: Project={project_id}, Region={location}")
    
    service = AIService(project_id=project_id, location=location)
    
    print("모델 프롬퍼티 접근 중...")
    model = service.model
    
    if model:
        print("성공: 모델이 정상적으로 초기화되었습니다.")
        print(f"모델 이름: {model._model_name if hasattr(model, '_model_name') else '알 수 없음'}")
        
        try:
            print("간단한 테스트 생성 중...")
            response = await model.generate_content_async("안녕?")
            print(f"생성 성공: {response.text[:20]}...")
        except Exception as e:
            print(f"생성 실패: {e}")
    else:
        print("실패: 모델 초기화에 실패했습니다 (model is None).")
        # ai_error.log 위치 확인
        if os.path.exists("ai_error.log"):
            print("ai_error.log를 찾았습니다. 내용을 출력합니다:")
            with open("ai_error.log", "r", encoding="utf-8") as f:
                print(f.read())
        else:
            print("ai_error.log가 생성되지 않았습니다. 권한이나 경로 문제일 수 있습니다.")

if __name__ == "__main__":
    asyncio.run(diagnose())
