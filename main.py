"""
mcp-ssh-toolkit-py

A minimal MCP server for secure SSH automation using fast_mcp_server.
Exposes SSH tools via the Model Context Protocol (MCP).
Compatible with Claude/Cline and other MCP clients.

Author: Your Name
License: MIT
"""

import os
import paramiko
import asyncio
from mcp.server.fastmcp import FastMCP
from mcp.types import Tool

# Create the low-level MCP server
server = FastMCP("mcp-ssh-toolkit-py")


@server.tool()
async def ssh_execute_command(arguments: dict) -> dict:
    """
    Execute a command on a remote server via SSH.
    """
    arguments = arguments["arguments"]
    host = arguments.get("host")
    username = arguments.get("username")
    password = arguments.get("password")
    privateKey = arguments.get("privateKey")
    command = arguments.get("command")
    port = int(arguments.get("port", 22))
    timeout = int(arguments.get("timeout", 20))

    try:
        with paramiko.SSHClient() as ssh:
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
            if privateKey:
                ssh.connect(host, port=port, username=username, password=password, key_filename=privateKey, timeout=timeout)
            else:
                ssh.connect(host, port=port, username=username, password=password, timeout=timeout)
            stdin, stdout, stderr = ssh.exec_command(command, timeout=timeout)
            out = stdout.read().decode()
            err = stderr.read().decode()
            exit_code = stdout.channel.recv_exit_status()
            return {
                "content": [
                    {"type": "text", "text": f"stdout:\n{out}\nstderr:\n{err}\nexit_code: {exit_code}"}
                ],
                "isError": False
            }
    except Exception as e:
        return {
            "content": [
                {"type": "text", "text": f"SSH error: {str(e)}"}
            ],
            "isError": True
        }

@server.tool()
async def sftp_upload(arguments: dict) -> dict:
    """
    Upload a file to a remote server via SFTP.
    """
    arguments = arguments["arguments"]
    host = arguments.get("host")
    username = arguments.get("username")
    password = arguments.get("password")
    privateKey = arguments.get("privateKey")
    local_path = arguments.get("local_path")
    remote_path = arguments.get("remote_path")
    port = int(arguments.get("port", 22))
    timeout = int(arguments.get("timeout", 20))

    try:
        with paramiko.SSHClient() as ssh:
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
            if privateKey:
                ssh.connect(host, port=port, username=username, password=password, key_filename=privateKey, timeout=timeout)
            else:
                ssh.connect(host, port=port, username=username, password=password, timeout=timeout)
            with ssh.open_sftp() as sftp:
                sftp.put(local_path, remote_path)
            return {
                "content": [
                    {"type": "text", "text": f"SFTP upload success: {local_path} -> {remote_path}"}
                ],
                "isError": False
            }
    except Exception as e:
        return {
            "content": [
                {"type": "text", "text": f"SFTP upload error: {str(e)}"}
            ],
            "isError": True
        }

@server.tool()
async def sftp_download(arguments: dict) -> dict:
    """
    Download a file from a remote server via SFTP.
    """
    host = arguments.get("host")
    username = arguments.get("username")
    password = arguments.get("password")
    privateKey = arguments.get("privateKey")
    local_path = arguments.get("local_path")
    remote_path = arguments.get("remote_path")
    port = int(arguments.get("port", 22))
    timeout = int(arguments.get("timeout", 20))

    try:
        with paramiko.SSHClient() as ssh:
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
            if privateKey:
                ssh.connect(host, port=port, username=username, password=password, key_filename=privateKey, timeout=timeout)
            else:
                ssh.connect(host, port=port, username=username, password=password, timeout=timeout)
            with ssh.open_sftp() as sftp:
                sftp.get(remote_path, local_path)
            return {
                "content": [
                    {"type": "text", "text": f"SFTP download success: {remote_path} -> {local_path}"}
                ],
                "isError": False
            }
    except Exception as e:
        return {
            "content": [
                {"type": "text", "text": f"SFTP download error: {str(e)}"}
            ],
            "isError": True
        }

# --- Test wrappers ---

from typing import Any

async def test_ssh_execute_command(arguments: dict) -> Any:
    """Wrapper for testing ssh_execute_command"""
    return await ssh_execute_command(arguments)

async def test_sftp_upload(arguments: dict) -> Any:
    """Wrapper for testing sftp_upload"""
    return await sftp_upload(arguments)

async def test_sftp_download(arguments: dict) -> Any:
    """Wrapper for testing sftp_download"""
    return await sftp_download(arguments)

# --- End test wrappers ---

if __name__ == "__main__":
    asyncio.run(server.run())
