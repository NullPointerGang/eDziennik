from ipaddress import ip_address, ip_network


def ip_in_same_subnet(ip1: str, ip2: str, mask: str = "255.255.255.0") -> bool:
    try:
        return ip_address(ip1) in ip_network(f"{ip2}/{mask}", strict=False)
    except ValueError:
        return False