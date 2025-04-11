"""
Unit tests for mcp-ssh-toolkit-py using pytest, pytest-asyncio, and unittest.mock.
"""

import pytest
import pytest_asyncio
from unittest.mock import patch, MagicMock
import main

@pytest.mark.asyncio
async def test_ssh_execute_command_success():
    with patch("paramiko.SSHClient") as MockSSHClient:
        mock_ssh = MockSSHClient.return_value.__enter__.return_value
        mock_stdout = MagicMock()
        mock_stdout.read.return_value = b"test output"
        mock_stdout.channel.recv_exit_status.return_value = 0
        mock_stderr = MagicMock()
        mock_stderr.read.return_value = b""
        mock_ssh.exec_command.return_value = (None, mock_stdout, mock_stderr)
        result = await main.test_ssh_execute_command({
            "host": "localhost",
            "username": "user",
            "password": "pass",
            "command": "echo test"
        })
        assert not result["isError"]
        assert "stdout:" in result["content"][0]["text"]
        assert "stderr:" in result["content"][0]["text"]
        assert "exit_code: 0" in result["content"][0]["text"]

@pytest.mark.asyncio
async def test_ssh_execute_command_error():
    with patch("paramiko.SSHClient") as MockSSHClient:
        mock_ssh = MockSSHClient.return_value.__enter__.return_value
        mock_ssh.connect.side_effect = Exception("Connection failed")
        result = await main.test_ssh_execute_command({
            "host": "localhost",
            "username": "user",
            "password": "pass",
            "command": "echo test"
        })
        assert result["isError"]
        assert "SSH error: Connection failed" in result["content"][0]["text"]

@pytest.mark.asyncio
async def test_sftp_upload_success():
    with patch("paramiko.SSHClient") as MockSSHClient:
        mock_ssh = MockSSHClient.return_value.__enter__.return_value
        mock_sftp = MagicMock()
        mock_ssh.open_sftp.return_value.__enter__.return_value = mock_sftp
        result = await main.test_sftp_upload({
            "host": "localhost",
            "username": "user",
            "password": "pass",
            "local_path": "local.txt",
            "remote_path": "remote.txt"
        })
        assert not result["isError"]
        assert "SFTP upload success" in result["content"][0]["text"]
        mock_sftp.put.assert_called_once_with("local.txt", "remote.txt")

@pytest.mark.asyncio
async def test_sftp_upload_error():
    with patch("paramiko.SSHClient") as MockSSHClient:
        mock_ssh = MockSSHClient.return_value.__enter__.return_value
        mock_ssh.connect.side_effect = Exception("Upload failed")
        result = await main.test_sftp_upload({
            "host": "localhost",
            "username": "user",
            "password": "pass",
            "local_path": "local.txt",
            "remote_path": "remote.txt"
        })
        assert result["isError"]
        assert "SFTP upload error: Upload failed" in result["content"][0]["text"]

@pytest.mark.asyncio
async def test_sftp_download_success():
    with patch("paramiko.SSHClient") as MockSSHClient:
        mock_ssh = MockSSHClient.return_value.__enter__.return_value
        mock_sftp = MagicMock()
        mock_ssh.open_sftp.return_value.__enter__.return_value = mock_sftp
        result = await main.test_sftp_download({
            "host": "localhost",
            "username": "user",
            "password": "pass",
            "local_path": "local.txt",
            "remote_path": "remote.txt"
        })
        assert not result["isError"]
        assert "SFTP download success" in result["content"][0]["text"]
        mock_sftp.get.assert_called_once_with("remote.txt", "local.txt")

@pytest.mark.asyncio
async def test_sftp_download_error():
    with patch("paramiko.SSHClient") as MockSSHClient:
        mock_ssh = MockSSHClient.return_value.__enter__.return_value
        mock_ssh.connect.side_effect = Exception("Download failed")
        result = await main.test_sftp_download({
            "host": "localhost",
            "username": "user",
            "password": "pass",
            "local_path": "local.txt",
            "remote_path": "remote.txt"
        })
        assert result["isError"]
        assert "SFTP download error: Download failed" in result["content"][0]["text"]
