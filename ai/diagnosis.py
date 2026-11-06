import json


def diagnose_case(case):
    """
    Simple rule-based mock AI.

    Later this function can be replaced
    with a real LLM/API call.
    """

    concept = case["concept"]
    fault = case["expected_fault"]
    layer = case["osi_layer"]

    commands = {
        "VLAN": "show vlan brief",
        "Gateway": "show ip interface brief",
        "DHCP": "show ip dhcp binding",
        "DNS": "show ip interface brief",
        "Routing": "show ip route",
        "ACL": "show access-lists",
        "NAT": "show ip nat translations",
        "Wireless": "show vlan brief",
        "Interface": "show ip interface brief",
        "Switching": "show mac address-table"
    }

    next_command = commands.get(
        concept,
        "show running-config"
    )

    result = {
        "root_cause": fault,
        "confidence": "medium",
        "osi_layer": layer,
        "concept": concept,
        "evidence": [
            case["show_outputs"]
        ],
        "next_command": next_command,
        "fix_steps": [
            f"Verify the suspected problem: {fault}.",
            "Do not change configuration until a human reviewer approves the diagnosis.",
            "Apply the approved configuration change manually.",
            "Run the verification command."
        ],
        "verification_command": "ping <destination>",
        "human_review_required": True
    }

    return result


def diagnosis_as_json(case):
    result = diagnose_case(case)
    return json.dumps(result, indent=2)

