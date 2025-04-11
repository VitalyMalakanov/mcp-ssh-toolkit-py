# mcp-ssh-toolkit-py

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/VitalyMalakanov/mcp-ssh-toolkit-py/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-ready-blue)](https://hub.docker.com/r/vitalymalakanov/mcp-ssh-toolkit-py)
[![Author](https://img.shields.io/badge/author-Vitaly_Malakanov_&_AI_Cline-blue)](https://github.com/VitalyMalakanov)

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

## Overview 🚀

**mcp-ssh-toolkit-py** is a powerful MCP server for secure SSH command execution via Model Context Protocol.

🔹 **Key Features**:
- Execute arbitrary commands on remote servers via SSH
- Upload/download files via SFTP
- Integration with Claude/Cline and other MCP clients
- Supports password and SSH key authentication
- Configurable connection parameters (timeouts, ports)

🔹 **Use Cases**:
- DevOps automation via LLMs
- Server management through chat interface
- Secure remote script execution
- SSH integration in MCP ecosystem

Example usage:
```python
# Through MCP client
response = mcp.tool("ssh_execute_command", {
    "host": "example.com",
    "username": "user",
    "command": "docker ps"
})
```

---

## Features ✨

### Core Functionality
- 🛡️ Secure SSH command execution via MCP
- 📁 SFTP operations (file upload/download)
- 🔑 Multiple authentication methods:
  - Username/password
  - SSH keys (RSA)
  - SSH agent

### Integration
- 🤖 Full compatibility with Claude/Cline
- 🐳 Ready-to-use Docker image
- 📦 Pip package installation

### Security
- 🔒 Encrypted connections
- ⏱ Configurable timeouts
- 🚫 No credential storage

---

## Installation 📦

### Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/VitalyMalakanov/mcp-ssh-toolkit-py.git
cd mcp-ssh-toolkit-py
```

2. Build the Docker image:
```bash
docker build -t mcp-ssh-toolkit-py .
```

3. (Optional) Push to your Docker registry:
```bash
docker tag mcp-ssh-toolkit-py yourusername/mcp-ssh-toolkit-py
docker push yourusername/mcp-ssh-toolkit-py
```

### Pip Installation

Install directly from GitHub:
```bash
pip install git+https://github.com/VitalyMalakanov/mcp-ssh-toolkit-py.git
```

Run the server after installation:
```bash
python -m mcp_ssh_toolkit
```

### Development Setup

For development, install with:
```bash
git clone https://github.com/VitalyMalakanov/mcp-ssh-toolkit-py.git
cd mcp-ssh-toolkit-py
pip install -e .
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


## Security

- SSH credentials are never stored or logged.
- Always use strong passwords or SSH keys for authentication.
- Do not expose the MCP server to untrusted networks.
- Review [paramiko security best practices](https://www.paramiko.org/security.html).
- If you discover a security vulnerability, please report it via GitHub Issues or contact the maintainer privately.

---

## License

MIT License. See [LICENSE](LICENSE) for details.
