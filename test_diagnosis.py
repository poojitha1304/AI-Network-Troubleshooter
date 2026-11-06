import pandas as pd

from ai.diagnosis import diagnose_case


# Load cases
cases = pd.read_csv("data/cases.csv")


# Select Case 1
case = cases[
    cases["case_id"] == 1
].iloc[0]


# Run diagnosis
result = diagnose_case(case)


# Print result
print("=" * 60)
print("AI TROUBLESHOOTING TEST")
print("=" * 60)

print("\nCASE ID:")
print(case["case_id"])

print("\nSYMPTOM:")
print(case["symptom"])

print("\nTOPOLOGY:")
print(case["topology_note"])

print("\nSHOW OUTPUT:")
print(case["show_outputs"])

print("\nAI DIAGNOSIS:")
print(result)
