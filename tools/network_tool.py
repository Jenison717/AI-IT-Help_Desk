"""
Network Connectivity Diagnostic Tool for LangChain.
Safely tests internet reachability and DNS resolution without executing shell commands.
"""

import socket
from pydantic import BaseModel, Field
from langchain_core.tools import tool


class NetworkCheckInput(BaseModel):
    target_host: str = Field(
        default="8.8.8.8",
        description="Public IP or host to test TCP connection (defaults to Google DNS 8.8.8.8)"
    )


@tool("network_check", args_schema=NetworkCheckInput)
def check_network_connectivity(target_host: str = "8.8.8.8") -> str:
    """
    Checks if the local system currently has active internet connectivity.
    Performs a safe, non-invasive socket handshake to verify network access and DNS.
    """
    timeout_seconds = 3
    port = 53  # DNS standard port

    # 1. Test direct IP connectivity
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout_seconds)
        result = sock.connect_ex((target_host, port))
        sock.close()

        if result == 0:
            status_ip = "Online (Direct TCP connection successful)"
        else:
            status_ip = "Offline (Socket connection failed)"
    except Exception as e:
        status_ip = f"Connection error: {str(e)}"

    # 2. Test DNS hostname resolution
    dns_status = "Unknown"
    try:
        socket.gethostbyname("cloudflare.com")
        dns_status = "Functional (Domain names resolve properly)"
    except Exception:
        dns_status = "Failed (DNS resolution unavailable)"

    if "Online" in status_ip:
        return (
            f"Network Status: CONNECTED\n"
            f"- Gateway Reachability: {status_ip}\n"
            f"- DNS Resolution: {dns_status}\n"
            f"- Summary: System has an active internet connection."
        )
    else:
        return (
            f"Network Status: DISCONNECTED OR RESTRICTED\n"
            f"- Gateway Reachability: {status_ip}\n"
            f"- DNS Resolution: {dns_status}\n"
            f"- Summary: Unable to reach external network. Check Wi-Fi/Ethernet link."
        )
