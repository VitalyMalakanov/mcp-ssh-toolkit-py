# mcp-ssh-toolkit-py

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/yourusername/mcp-ssh-toolkit-py/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-ready-blue)](https://hub.docker.com/r/yourusername/mcp-ssh-toolkit-py)

A minimal Model Context Protocol (MCP) server for secure SSH automation, built with [python-sdk](https://github.com/modelcontextprotocol/python-sdk) and [paramiko](https://www.paramiko.org/).

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quickstart](#quickstart)
- [Usage](#usage)
- [Development](#development)
- [License](#license)

---

## Overview

**mcp-ssh-toolkit-py** exposes an SSH command execution tool via the Model Context Protocol (MCP).  
It allows LLMs and MCP-compatible clients (like Claude/Cline) to securely execute commands on remote servers via SSH.

---

## Features

- Exposes an SSH command execution tool via MCP
- Works with Claude/Cline and other MCP-compatible clients
- Runs in Docker for easy deployment and isolation
- Simple, extensible Python codebase

---

## Installation

Clone the repository and build the Docker image:

```bash
git clone https://github.com/yourusername/mcp-ssh-toolkit-py.git
cd mcp-ssh-toolkit-py
docker build -t mcp-ssh-toolkit-py .
```

---

## Quickstart

### Run with Docker

```bash
docker run --rm -i mcp-ssh-toolkit-py
```

### MCP Integration

Add to your MCP configuration (e.g., `cline_mcp_settings.json`):

```json
"mcp-ssh-toolkit-py": {
  "command": "docker",
  "args": ["run", "--rm", "-i", "mcp-ssh-toolkit-py"],
  "env": {}
}
```

---

## Usage

### Tool: `ssh_execute_command`

**Description:**  
Execute a command on a remote server via SSH.

**Input parameters:**
- `host` (string, required): SSH server address
- `username` (string, required): SSH username
- `password` (string, optional): SSH password
- `privateKey` (string, optional): Path to SSH private key (PEM)
- `command` (string, required): Command to execute
- `port` (integer, optional, default 22): SSH port
- `timeout` (integer, optional, default 20): Connection timeout (seconds)

**Output:**
- `stdout`: Command output
- `stderr`: Error output
- `exit_code`: Exit code

**Example call:**
```json
{
  "host": "example.com",
  "username": "user",
  "password": "secret",
  "command": "uname -a"
}
```

---

## Development

- Python 3.8+
- [python-sdk](https://github.com/modelcontextprotocol/python-sdk)
- [paramiko](https://www.paramiko.org/)

Install dependencies locally:
```bash
pip install -r requirements.txt
```

Run locally:
```bash
python main.py
```

---

## Example Code

```python
import paramiko
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mcp-ssh-toolkit-py")

@mcp.tool()
def ssh_execute_command(
    host: str,
    username: str,
    password: str = None,
    privateKey: str = None,
    command: str = "",
    port: int = 22,
    timeout: int = 20
) -> dict:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        if privateKey:
            pkey = paramiko.RSAKey.from_private_key_file(privateKey)
            ssh.connect(host, port=port, username=username, pkey=pkey, timeout=timeout)
        else:
            ssh.connect(host, port=port, username=username, password=password, timeout=timeout)
        stdin, stdout, stderr = ssh.exec_command(command, timeout=timeout)
        out = stdout.read().decode()
        err = stderr.read().decode()
        exit_code = stdout.channel.recv_exit_status()
        ssh.close()
        return {
            "stdout": out,
            "stderr": err,
            "exit_code": exit_code
        }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": str(e),
            "exit_code": -1
        }

if __name__ == "__main__":
    mcp.run()
```

---

## Security

- SSH credentials are never stored or logged.
- Always use strong passwords or SSH keys for authentication.
- Do not expose the MCP server to untrusted networks.
- Review [paramiko security best practices](https://www.paramiko.org/security.html).
- If you discover a security vulnerability, please report it via GitHub Issues or contact the maintainer privately.

---

## License

MIT License. See [LICENSE](LICENSE) for details.
