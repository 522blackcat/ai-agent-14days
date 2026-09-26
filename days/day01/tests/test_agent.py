"""Day 01 工具执行测试：不依赖模型网络请求。"""

import importlib.util
from pathlib import Path


AGENT_FILE = (
    Path(__file__).resolve().parents[1]
    / "src"
    / "agent.py"
)

spec = importlib.util.spec_from_file_location(
    "day01_agent",
    AGENT_FILE,
)

agent = importlib.util.module_from_spec(spec)
spec.loader.exec_module(agent)


def test_add_numbers():
    result = agent.execute_tool(
        "add_numbers",
        '{"a": 12, "b": 30}',
    )

    assert result == {
        "ok": True,
        "data": {"result": 42.0},
    }


def test_reject_unknown_tool():
    result = agent.execute_tool(
        "delete_database",
        "{}",
    )

    assert result["error"] == "tool_not_allowed"


def test_reject_extra_fields():
    result = agent.execute_tool(
        "add_numbers",
        '{"a": 1, "b": 2, "admin": true}',
    )

    assert result["error"] == "invalid_arguments"


def test_reject_invalid_json():
    result = agent.execute_tool(
        "add_numbers",
        "{invalid-json}",
    )

    assert result["error"] == "invalid_arguments"
