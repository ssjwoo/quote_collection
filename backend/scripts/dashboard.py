import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px

# Streamlit Config
st.set_page_config(
    page_title="AI Recommendation Quality Dashboard",
    layout="wide"
)

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_PATH = os.path.join(BASE_DIR, "../evaluation_results.json")

def load_data():
    if not os.path.exists(RESULTS_PATH):
        return None
    with open(RESULTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# Main UI
st.title("AI Recommendation Quality Dashboard (LLM-as-a-Judge)")

data = load_data()

if not data:
    st.warning("No evaluation results found. Please run `python scripts/evaluate_ai_quality.py` first.")
    if st.button("Run Evaluation Now"):
        with st.spinner("Running evaluation... This may take a minute."):
            os.system(f"python {os.path.join(BASE_DIR, 'evaluate_ai_quality.py')}")
            st.rerun()
else:
    # Summary Metrics
    summary = data.get("summary", {})
    timestamp = data.get("timestamp", "")
    st.caption(f"Last Updated: {timestamp}")

    c1, c2, c3 = st.columns(3)
    c1.metric("Average Relevance Score", f"{summary.get('average_relevance_score', 0)} / 5.0")
    c2.metric("Average Latency", f"{summary.get('average_latency_ms', 0)} ms")
    c3.metric("Total Scenarios Tested", summary.get("total_scenarios", 0))

    st.divider()

    # Score Distribution Chart
    st.subheader("Score Distribution")
    dist = summary.get("score_distribution", {})
    df_dist = pd.DataFrame(list(dist.items()), columns=["Score", "Count"])
    fig = px.bar(df_dist, x="Score", y="Count", text="Count", title="Relevance Score Distribution", color="Score")
    st.plotly_chart(fig, use_container_width=True)

    # Detailed Analysis
    st.subheader("Detailed Scenario Analysis")
    
    details = data.get("details", [])
    
    # Flat data for table
    table_data = []
    for d in details:
        scenario = d.get("scenario_id")
        desc = d.get("description")
        for rec in d.get("recommendations", []):
            table_data.append({
                "Scenario": scenario,
                "Description": desc,
                "Quote": rec.get("quote"),
                "Source": f"{rec.get('source')} ({rec.get('author')})",
                "Score": rec.get("score"),
                "Reason": rec.get("reason"),
                "Latency (ms)": d.get("latency_ms")
            })
    
    df_details = pd.DataFrame(table_data)
    
    # Filter by score
    score_filter = st.multiselect("Filter by Score", options=[1, 2, 3, 4, 5], default=[1, 2, 3, 4, 5])
    if score_filter:
        df_details = df_details[df_details["Score"].isin(score_filter)]

    # Display Table with formatting
    def highlight_score(val):
        color = 'red' if val < 3 else 'orange' if val < 4 else 'green'
        return f'color: {color}; font-weight: bold'

    st.dataframe(
        df_details,
        column_config={
            "Score": st.column_config.NumberColumn("Score", format="%d"),
        },
        use_container_width=True,
        hide_index=True
    )
    
    # Latency Chart
    st.subheader("Latency per Scenario")
    df_latency = pd.DataFrame(details)
    fig_lat = px.line(df_latency, x="scenario_id", y="latency_ms", markers=True, title="Response Time per Scenario")
    st.plotly_chart(fig_lat, use_container_width=True)
