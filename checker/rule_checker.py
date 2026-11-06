import ipaddress
import re


def check_ip(ip):
    """Check whether an IP address is valid."""
    try:
        ipaddress.ip_address(ip)
        return {
            "status": "PASS",
            "message": f"{ip} is a valid IP address"
        }
    except ValueError:
        return {
            "status": "FAIL",
            "message": f"{ip} is not a valid IP address"
        }


def check_duplicate_ips(ip_addresses):
    """Find duplicate IP addresses."""
    seen = set()
    duplicates = []

    for ip in ip_addresses:
        if ip in seen and ip not in duplicates:
            duplicates.append(ip)

        seen.add(ip)

    if duplicates:
        return {
            "status": "FAIL",
            "message": f"Duplicate IP addresses: {duplicates}"
        }

    return {
        "status": "PASS",
        "message": "No duplicate IP addresses found"
    }


def check_gateway(ip, mask, gateway):
    """Check whether gateway belongs to the same subnet."""
    try:
        network = ipaddress.ip_network(
            f"{ip}/{mask}",
            strict=False
        )

        gateway_ip = ipaddress.ip_address(gateway)

        if gateway_ip in network:
            return {
                "status": "PASS",
                "message": f"Gateway {gateway} belongs to {network}"
            }

        return {
            "status": "FAIL",
            "message": f"Gateway {gateway} is outside {network}"
        }

    except ValueError as error:
        return {
            "status": "FAIL",
            "message": str(error)
        }


def check_interface_status(show_output):
    """Check for common interface-down conditions."""

    output = show_output.lower()

    if "administratively down" in output:
        return {
            "status": "FAIL",
            "message": "Interface is administratively down"
        }

    if re.search(r"\bdown\s+down\b", output):
        return {
            "status": "FAIL",
            "message": "Interface appears to be down/down"
        }

    return {
        "status": "PASS",
        "message": "No obvious interface-down condition found"
    }


def check_vlan(show_output, vlan_id):
    """Check whether a VLAN appears in show vlan brief output."""

    pattern = rf"^\s*{vlan_id}\s+"

    if re.search(pattern, show_output, re.MULTILINE):
        return {
            "status": "PASS",
            "message": f"VLAN {vlan_id} appears to exist"
        }

    return {
        "status": "FAIL",
        "message": f"VLAN {vlan_id} may be missing"
    }


def check_route(show_output, destination):
    """Basic route existence check."""

    destination = destination.strip()

    if destination in show_output:
        return {
            "status": "PASS",
            "message": f"Route to {destination} appears in output"
        }

    return {
        "status": "FAIL",
        "message": f"No obvious route to {destination} found"
    }


def run_all_checks():
    print("=" * 60)
    print("CISCO TROUBLESHOOTING RULE CHECKER")
    print("=" * 60)

    print("\n1. IP CHECK")
    print(check_ip("192.168.10.10"))

    print("\n2. DUPLICATE IP CHECK")
    print(
        check_duplicate_ips(
            [
                "192.168.10.10",
                "192.168.10.11",
                "192.168.10.10"
            ]
        )
    )

    print("\n3. GATEWAY CHECK")
    print(
        check_gateway(
            "192.168.10.10",
            "255.255.255.0",
            "192.168.20.1"
        )
    )

    print("\n4. INTERFACE CHECK")

    interface_output = """
    GigabitEthernet0/1 is administratively down,
    line protocol is down
    """

    print(check_interface_status(interface_output))

    print("\n5. VLAN CHECK")

    vlan_output = """
    VLAN Name                             Status
    ---- -------------------------------- ---------
    10   USERS                            active
    20   SERVERS                          active
    """

    print(check_vlan(vlan_output, 30))

    print("\n6. ROUTE CHECK")

    route_output = """
    C 192.168.10.0/24 is directly connected
    C 192.168.20.0/24 is directly connected
    """

    print(
        check_route(
            route_output,
            "192.168.20.0/24"
        )
    )


if __name__ == "__main__":
    run_all_checks()

