import asyncio
import sys
import os
import json
import time
import statistics
from datetime import datetime

# Add paths
base_dir = os.path.dirname(os.path.abspath(__file__)) # backend/scripts
backend_dir = os.path.abspath(os.path.join(base_dir, "..")) # backend
project_dir = os.path.abspath(os.path.join(backend_dir, "..")) # quote_collection
llm_dir = os.path.join(project_dir, "llm")

sys.path.append(backend_dir)
sys.path.append(llm_dir)

from ai_service import AIService
from app.core.config import settings

SCENARIOS = [
    {
        "id": "persona_a",
        "description": "Exhausted office worker, raining evening",
        "context": "Tired, stressed, rainy weather, seeking comfort and calmness. Likes essays."
    },
    {
        "id": "persona_b",
        "description": "Passionate dreamer, sunny morning",
        "context": "Energetic, looking for strong motivation and courage for life, sunny weather. Likes biography and self-growth."
    },
    {
        "id": "persona_c",
        "description": "Philosophical student, midnight",
        "context": "Deep thinking, existentialism, midnight solitude. Likes Nietzsche and Kafka."
    },
    {
        "id": "persona_d",
        "description": "Happy traveler, weekend",
        "context": "Excited, planning a trip, sunny weekend. Likes travelogues and light fiction."
    }
]

async def run_evaluation():
    print("Initializing AIService for Evaluation...")
    ai = AIService(
        project_id=settings.google_project_id,
        location="us-central1",
        aladin_api_key=settings.aladin_api_key
    )
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "summary": {},
        "details": []
    }
    
    all_scores = []
    all_latencies = []
    
    print(f"Starting evaluation on {len(SCENARIOS)} scenarios...")
    
    for scenario in SCENARIOS:
        print(f"\n--- Testing Scenario: {scenario['id']} ---")
        print(f"Context: {scenario['context']}")
        
        start_time = time.time()
        recommendations = await ai.get_recommendations("book", limit=3, user_context=scenario['context'])
        latency = (time.time() - start_time) * 1000 # ms
        
        all_latencies.append(latency)
        
        scenario_scores = []
        evaluations = []
        
        for rec in recommendations:
            # Judge the recommendation
            judge_result = await ai.evaluate_relevance(scenario['context'], rec)
            score = judge_result.get("score", 0)
            reason = judge_result.get("reason", "No reason provided")
            
            scenario_scores.append(score)
            evaluations.append({
                "quote": rec.get("content"),
                "source": rec.get("source_title"),
                "author": rec.get("author"),
                "score": score,
                "reason": reason
            })
            print(f"   -> Score: {score}/5 | Source: {rec.get('source_title')}")

        results["details"].append({
            "scenario_id": scenario['id'],
            "description": scenario['description'],
            "latency_ms": round(latency, 2),
            "avg_score": statistics.mean(scenario_scores) if scenario_scores else 0,
            "recommendations": evaluations
        })
        all_scores.extend(scenario_scores)

    # Calculate Summary
    results["summary"] = {
        "total_scenarios": len(SCENARIOS),
        "average_latency_ms": round(statistics.mean(all_latencies), 2) if all_latencies else 0,
        "average_relevance_score": round(statistics.mean(all_scores), 2) if all_scores else 0,
        "score_distribution": {i: all_scores.count(i) for i in range(1, 6)}
    }
    
    # Save to file
    output_path = os.path.join(os.path.dirname(__file__), "../evaluation_results.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
        
    print(f"\nEvaluation Complete! Results saved to {output_path}")
    print(f"Global Average Score: {results['summary']['average_relevance_score']}/5.0")
    print(f"Global Average Latency: {results['summary']['average_latency_ms']}ms")

if __name__ == "__main__":
    # Fix import path for running script directly
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    asyncio.run(run_evaluation())
