"""Tests for service_health.py — asyncio health-check CLI tool."""

from __future__ import annotations

import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock, mock_open, patch

import service_health


class TestServiceHealthSkeleton(unittest.TestCase):
    """Basic import and version check."""

    def test_import_and_version(self) -> None:
        assert service_health.__version__ == "0.1.0"


class TestHelpers(unittest.TestCase):
    """Pure synchronous helpers."""

    @patch("os.kill")
    def test_is_pid_alive_true(self, mock_kill: MagicMock) -> None:
        mock_kill.return_value = None
        assert service_health.is_pid_alive(1234) is True

    @patch("os.kill", side_effect=ProcessLookupError)
    def test_is_pid_alive_false(self, mock_kill: MagicMock) -> None:
        assert service_health.is_pid_alive(1234) is False

    @patch("os.kill", side_effect=PermissionError)
    def test_is_pid_alive_permission(self, mock_kill: MagicMock) -> None:
        assert service_health.is_pid_alive(1234) is True

    def test_read_pid_file_success(self) -> None:
        m = mock_open(read_data="5678\n")
        with patch("os.path.exists", return_value=True), patch("builtins.open", m):
            assert service_health.read_pid_file("/tmp/test.pid") == 5678

    def test_read_pid_file_missing(self) -> None:
        with patch("os.path.exists", return_value=False):
            with self.assertRaises(FileNotFoundError):
                service_health.read_pid_file("/tmp/missing.pid")


class TestCoreRunner(unittest.IsolatedAsyncioTestCase):
    """async main() with mocked checks."""

    @staticmethod
    async def _dummy_ok() -> tuple[bool, str]:
        return True, "Mock OK"

    @staticmethod
    async def _dummy_fail() -> tuple[bool, str]:
        return False, "FAIL detail"

    @patch("sys.exit")
    @patch("builtins.print")
    async def test_main_all_healthy(
        self, mock_print: MagicMock, mock_exit: MagicMock
    ) -> None:
        checks: dict = {"Dummy Svc": self._dummy_ok}
        with patch.dict(service_health.CHECKS, checks, clear=True):
            await service_health.main()
            mock_exit.assert_called_once_with(0)
            printed = "".join(str(c[0][0]) for c in mock_print.call_args_list)
            assert "Dummy Svc" in printed
            assert "OK" in printed

    @patch("sys.exit")
    @patch("builtins.print")
    async def test_main_one_failed(
        self, mock_print: MagicMock, mock_exit: MagicMock
    ) -> None:
        checks: dict = {"Healthy": self._dummy_ok, "Unhealthy": self._dummy_fail}
        with patch.dict(service_health.CHECKS, checks, clear=True):
            await service_health.main()
            mock_exit.assert_called_once_with(1)
            printed = "".join(str(c[0][0]) for c in mock_print.call_args_list)
            assert "FAIL" in printed


class TestRunCheckWithTimeout(unittest.IsolatedAsyncioTestCase):
    """Timeout and error handling."""

    async def test_success(self) -> None:
        async def _ok() -> tuple[bool, str]:
            return True, "good"

        ok_flag, detail = await service_health.run_check_with_timeout("test", _ok)
        assert ok_flag is True
        assert detail == "good"

    async def test_timeout(self) -> None:
        async def _slow() -> tuple[bool, str]:
            await asyncio.sleep(5)
            return True, "never"

        ok_flag, detail = await service_health.run_check_with_timeout("test", _slow)
        assert ok_flag is False
        assert "Timeout" in detail

    async def test_exception(self) -> None:
        async def _err() -> tuple[bool, str]:
            raise RuntimeError("boom")

        ok_flag, detail = await service_health.run_check_with_timeout("test", _err)
        assert ok_flag is False
        assert "Error:" in detail


class TestCheckIiiEngine(unittest.IsolatedAsyncioTestCase):
    """iii --version check."""

    @patch("asyncio.create_subprocess_exec")
    async def test_success(self, mock_exec: MagicMock) -> None:
        proc = MagicMock()
        proc.communicate = AsyncMock(return_value=(b"iii version 0.11.2\n", b""))
        proc.returncode = 0
        mock_exec.return_value = proc
        ok_flag, detail = await service_health.check_iii_engine()
        assert ok_flag is True
        assert "0.11.2" in detail

    @patch("asyncio.create_subprocess_exec")
    async def test_wrong_version(self, mock_exec: MagicMock) -> None:
        proc = MagicMock()
        proc.communicate = AsyncMock(return_value=(b"iii version 0.10.0\n", b""))
        proc.returncode = 0
        mock_exec.return_value = proc
        ok_flag, detail = await service_health.check_iii_engine()
        assert ok_flag is False
        assert "Incorrect version" in detail


class TestCheckAgentMemory(unittest.IsolatedAsyncioTestCase):
    """agentmemory TCP probe + status."""

    @patch("service_health.probe_tcp", return_value=True)
    @patch("asyncio.create_subprocess_exec")
    async def test_success(
        self, mock_exec: MagicMock, mock_probe: MagicMock
    ) -> None:
        proc = MagicMock()
        proc.communicate = AsyncMock(return_value=(b"running\n", b""))
        proc.returncode = 0
        mock_exec.return_value = proc
        ok_flag, detail = await service_health.check_agentmemory()
        assert ok_flag is True
        assert "Port 3111 open" in detail

    @patch("service_health.probe_tcp", return_value=False)
    async def test_tcp_fail(self, mock_probe: MagicMock) -> None:
        ok_flag, detail = await service_health.check_agentmemory()
        assert ok_flag is False
        assert "TCP probe failed" in detail


class TestCheckViewerProxy(unittest.IsolatedAsyncioTestCase):
    """viewer-proxy PID + TCP check."""

    @patch("service_health.probe_tcp", return_value=True)
    @patch("service_health.is_pid_alive", return_value=True)
    @patch("service_health.read_pid_file", return_value=1234)
    async def test_success(
        self, mock_read: MagicMock, mock_alive: MagicMock, mock_tcp: MagicMock
    ) -> None:
        ok_flag, detail = await service_health.check_viewer_proxy()
        assert ok_flag is True
        assert "PID 1234 active" in detail


class TestCheckHermesGateway(unittest.IsolatedAsyncioTestCase):
    """Gateway JSON parsing + Telegram state."""

    @patch("asyncio.create_subprocess_exec")
    @patch("service_health.is_pid_alive", return_value=True)
    @patch("os.path.exists", return_value=True)
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data='{"pid":9999,"platforms":{"telegram":{"state":"connected"}}}',
    )
    async def test_success(
        self,
        mock_file: MagicMock,
        mock_exists: MagicMock,
        mock_alive: MagicMock,
        mock_exec: MagicMock,
    ) -> None:
        proc = MagicMock()
        proc.communicate = AsyncMock(return_value=(b"gateway active\n", b""))
        proc.returncode = 0
        mock_exec.return_value = proc
        ok_flag, detail = await service_health.check_hermes_gateway()
        assert ok_flag is True
        assert "Telegram connected" in detail

    @patch("os.path.exists", return_value=True)
    @patch("service_health.is_pid_alive", return_value=True)
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data='{"pid":9999,"platforms":{"telegram":{"state":"disconnected"}}}',
    )
    async def test_telegram_disconnected(
        self, mock_file: MagicMock, mock_alive: MagicMock, mock_exists: MagicMock
    ) -> None:
        ok_flag, detail = await service_health.check_hermes_gateway()
        assert ok_flag is False
        assert "disconnected" in detail


class TestIntegration(unittest.IsolatedAsyncioTestCase):
    """All 7 checks registered."""

    def test_all_checks_registered(self) -> None:
        expected = {
            "iii engine",
            "agentmemory",
            "viewer-proxy",
            "hermes dashboard",
            "dashboard-proxy",
            "fcc-server",
            "hermes gateway",
        }
        assert set(service_health.CHECKS.keys()) == expected


if __name__ == "__main__":
    unittest.main()
