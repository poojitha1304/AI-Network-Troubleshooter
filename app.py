import os
from pathlib import Path

import pandas as pd
import streamlit as st

from ai.diagnosis import diagnose_case


BASE_DIR = Path(__file__).resolve().parent


def resolve_project_path(*parts):
    return str(BASE_DIR.joinpath(*parts))


CASE_FILE = resolve_project_path("data", "cases.csv")
RESULT_FILE = resolve_project_path("results", "responsible_ai_log.csv")


@st.cache_data
def load_cases():
    return pd.read_csv(CASE_FILE)


def save_review(case_id, diagnosis, decision, reviewer, comment, corrected):
    new_record = pd.DataFrame([
        {
            "case_id": case_id,
            "ai_diagnosis": diagnosis["root_cause"],
            "human_decision": decision,
            "corrected_diagnosis": corrected,
            "reviewer": reviewer,
            "reason": comment,
        }
    ])

    os.makedirs(Path(RESULT_FILE).parent, exist_ok=True)

    if os.path.exists(RESULT_FILE):
        old = pd.read_csv(RESULT_FILE)
        if "human_decision" not in old.columns:
            old = pd.DataFrame(columns=[
                "case_id",
                "ai_diagnosis",
                "human_decision",
                "corrected_diagnosis",
                "reviewer",
                "reason",
            ])
        combined = pd.concat([old, new_record], ignore_index=True)
    else:
        combined = new_record

    combined.to_csv(RESULT_FILE, index=False)
    return RESULT_FILE


def main():
    # --------------------------------------------------
    # Load cases
    # --------------------------------------------------
    cases = load_cases()

    # --------------------------------------------------
    # Page configuration
    # --------------------------------------------------
    st.set_page_config(
        page_title="AI Network Troubleshooter",
        page_icon="🌐",
        layout="wide",
    )

    st.title("🌐 AI Network Troubleshooting Assistant")
    st.write(
        """
        AI-assisted troubleshooting for Cisco Packet Tracer labs.

        **Safety rule:** AI recommendations must be reviewed by
        a human before a configuration fix is accepted.
        """
    )

    case_id = st.selectbox("Select a troubleshooting case", cases["case_id"].tolist())
    case = cases[cases["case_id"] == case_id].iloc[0]

    st.header("1. Case Information")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Symptom")
        st.write(case["symptom"])
        st.subheader("Topology")
        st.write(case["topology_note"])

    with col2:
        st.subheader("Concept")
        st.write(case["concept"])
        st.subheader("Severity")
        st.write(case["severity"])
        st.subheader("Expected fault")
        st.write(case["expected_fault"])

    st.header("2. Show-Command Evidence")
    st.code(case["show_outputs"], language="text")

    st.header("3. AI Diagnosis")
    if st.button("Run AI Diagnosis"):
        diagnosis = diagnose_case(case)
        st.session_state["diagnosis"] = diagnosis

    if "diagnosis" in st.session_state:
        diagnosis = st.session_state["diagnosis"]

        st.subheader("Root Cause")
        st.info(diagnosis["root_cause"])

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Confidence", diagnosis["confidence"])
        with col2:
            st.metric("OSI Layer", diagnosis["osi_layer"])
        with col3:
            st.metric("Concept", diagnosis["concept"])

        st.subheader("Evidence")
        for evidence in diagnosis["evidence"]:
            st.write("•", evidence)

        st.subheader("Next Command")
        st.code(diagnosis["next_command"])

        st.subheader("Suggested Fix")
        for step in diagnosis["fix_steps"]:
            st.write("•", step)

        st.subheader("Verification")
        st.code(diagnosis["verification_command"])

        st.warning("⚠️ Human review is required before accepting this diagnosis.")

        st.header("4. Human Review")
        decision = st.radio("Reviewer decision", ["Accepted", "Edited", "Rejected"])
        reviewer = st.text_input("Reviewer name")
        comment = st.text_area("Reviewer comments")
        corrected = st.text_area("Corrected diagnosis (if needed)")

        if st.button("Save Review"):
            save_review(case_id, diagnosis, decision, reviewer, comment, corrected)
            st.success("Human review saved successfully.")


if __name__ == "__main__":
    main()

