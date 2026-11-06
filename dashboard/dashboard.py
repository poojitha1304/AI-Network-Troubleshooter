import os
from pathlib import Path

import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).resolve().parents[1]


def resolve_project_path(*parts):
    return str(BASE_DIR.joinpath(*parts))


RESULT_FILE = resolve_project_path("results", "responsible_ai_log.csv")
CASE_FILE = resolve_project_path("data", "cases.csv")


def load_review_results():
    if not os.path.exists(RESULT_FILE):
        return pd.DataFrame()

    results = pd.read_csv(RESULT_FILE)
    if results.empty:
        return pd.DataFrame()

    required_columns = {"case_id", "human_decision"}
    if not required_columns.issubset(results.columns):
        return pd.DataFrame(columns=["case_id", "human_decision"])

    return results


def main():
    st.set_page_config(
        page_title="Troubleshooting Dashboard",
        page_icon="📊",
        layout="wide",
    )

    st.title("📊 AI Troubleshooting Dashboard")

    cases = pd.read_csv(CASE_FILE)
    results = load_review_results()

    if results.empty:
        st.warning("No human review data available yet. Run the app and save a review to populate this dashboard.")
        return

    total_reviews = len(results)
    accepted = len(results[results["human_decision"] == "Accepted"])
    edited = len(results[results["human_decision"] == "Edited"])
    rejected = len(results[results["human_decision"] == "Rejected"])
    agreement = (accepted / total_reviews * 100) if total_reviews > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Reviews", total_reviews)
    col2.metric("Accepted", accepted)
    col3.metric("Edited", edited)
    col4.metric("Rejected", rejected)
    st.metric("AI Agreement Rate", f"{agreement:.1f}%")

    st.header("Human Review Outcomes")
    st.bar_chart(results["human_decision"].value_counts())

    merged = results.merge(
        cases[["case_id", "concept", "severity", "osi_layer"]],
        on="case_id",
        how="left",
    )

    st.header("Issues by Concept")
    st.bar_chart(merged["concept"].value_counts())

    st.header("Cases by Severity")
    st.bar_chart(merged["severity"].value_counts())

    st.header("Human Corrections")
    corrections = merged[merged["human_decision"].isin(["Edited", "Rejected"])]
    st.dataframe(corrections, use_container_width=True)


if __name__ == "__main__":
    main()

