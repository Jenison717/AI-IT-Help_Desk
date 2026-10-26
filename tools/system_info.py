"""
Safe System Information Diagnostic Tool for LangChain.
Retrieves non-sensitive hardware and environment details to assist with IT diagnosis.
"""

import platform
import sys
from pydantic import BaseModel, Field
from langchain_core.tools import tool

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


class SystemInfoInput(BaseModel):
    query_scope: str = Field(
        default="general",
        description="The scope of system information, e.g. 'general', 'hardware', or 'os'"
    )


@tool("system_info", args_schema=SystemInfoInput)
def get_system_information(query_scope: str = "general") -> str:
    """
    Returns safe, non-sensitive system information including OS name, release version,
    machine architecture, Python runtime version, CPU count, and memory metrics.
    Does NOT read sensitive files, credentials, or personal directories.
    """
    os_name = platform.system()
    os_release = platform.release()
    os_version = platform.version()
    architecture = platform.machine()
    python_ver = sys.version.split()[0]

    cpu_info = "N/A"
    ram_info = "N/A"

    if PSUTIL_AVAILABLE:
        try:
            logical_cpus = psutil.cpu_count(logical=True)
            physical_cpus = psutil.cpu_count(logical=False)
            cpu_info = f"{physical_cpus} physical cores, {logical_cpus} logical threads"

            mem = psutil.virtual_memory()
            total_gb = round(mem.total / (1024 ** 3), 2)
            avail_gb = round(mem.available / (1024 ** 3), 2)
            ram_info = f"Total: {total_gb} GB, Available: {avail_gb} GB ({mem.percent}% used)"
        except Exception:
            cpu_info = "Protected or restricted environment"

    return (
        f"System Diagnostic Specifications:\n"
        f"- Operating System: {os_name} {os_release} ({architecture})\n"
        f"- OS Build: {os_version}\n"
        f"- Python Runtime: v{python_ver}\n"
        f"- Processor Cores: {cpu_info}\n"
        f"- Memory (RAM): {ram_info}\n"
        f"- Status: Diagnostic metrics retrieved safely."
    )
