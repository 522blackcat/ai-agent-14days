#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""统计每日 progress.md 的勾选情况并更新 README。"""

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"


def main():
    content = README.read_text(encoding="utf-8")

    completed_days = 0
    completed_tasks = 0
    total_tasks = 0

    for day in range(1, 15):
        name = f"day{day:02d}"

        progress_file = (
            ROOT / "days" / name / "progress.md"
        )

        progress = progress_file.read_text(
            encoding="utf-8"
        )

        done = len(
            re.findall(
                r"^- \[[xX]\]",
                progress,
                flags=re.MULTILINE,
            )
        )

        pending = len(
            re.findall(
                r"^- \[ \]",
                progress,
                flags=re.MULTILINE,
            )
        )

        total = done + pending
        completed_tasks += done
        total_tasks += total

        if total and done == total:
            status = "✅ 已完成"
            completed_days += 1
        elif done:
            status = "🟡 进行中"
        else:
            status = "⬜ 未开始"

        pattern = (
            rf"(\| {day:02d} \| "
            rf"\[[^\n]+\]\(days/{name}/{name}\.md\)"
            rf" \| )[^|]+(\|)"
        )

        content = re.sub(
            pattern,
            lambda match: (
                match.group(1)
                + status
                + " "
                + match.group(2)
            ),
            content,
        )

    percentage = completed_days / 14 * 100

    summary = (
        "<!-- PROGRESS_START -->\n"
        f"**完成天数：{completed_days}/14**  \n"
        f"**完成率：{percentage:.1f}%**  \n"
        f"**完成任务：{completed_tasks}/{total_tasks}**\n"
        "<!-- PROGRESS_END -->"
    )

    content = re.sub(
        r"<!-- PROGRESS_START -->.*?<!-- PROGRESS_END -->",
        lambda _: summary,
        content,
        flags=re.DOTALL,
    )

    README.write_text(
        content,
        encoding="utf-8",
    )

    print(
        f"完成 {completed_days}/14 天；"
        f"任务 {completed_tasks}/{total_tasks}"
    )


if __name__ == "__main__":
    main()
