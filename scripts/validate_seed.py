#!/usr/bin/env python3
"""校验题库种子：对每题用 reference.py 跑全部用例，规范化比对 .out；
若存在 solution.md，则检查结构并用其中的 Python3 模板代码跑全部用例。

用法: python scripts/validate_seed.py [slug ...]   （无参数则校验全部）
退出码非零表示存在失败项。
"""
import re
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROBLEMS = ROOT / "backend" / "app" / "seed" / "problems"

DIFFICULTIES = {"easy", "medium", "hard"}
SOURCES = {"hot100", "mianjing"}

PY_BLOCK = re.compile(r"###\s*Python3.*?```python\s*\n(.*?)```", re.S)
CPP_BLOCK = re.compile(r"###\s*C\+\+.*?```cpp\s*\n(.*?)```", re.S)
SAMPLE_BLOCK = re.compile(
    r"###\s*样例\s*\d+\s*\n输入：\s*\n```(?:text)?\n(.*?)```\s*\n输出：\s*\n```(?:text)?\n(.*?)```",
    re.S,
)


def extract_solution(md: str) -> tuple[str | None, str | None]:
    py = PY_BLOCK.search(md)
    cpp = CPP_BLOCK.search(md)
    return (py.group(1) if py else None, cpp.group(1) if cpp else None)


def norm(s: str) -> str:
    lines = [ln.rstrip() for ln in s.replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def check(slug: str) -> list[str]:
    d = PROBLEMS / slug
    errs: list[str] = []
    if not d.is_dir():
        return [f"{slug}: 目录不存在"]
    for name in ("meta.toml", "statement.md", "reference.py"):
        if not (d / name).exists():
            errs.append(f"{slug}: 缺少 {name}")
    if errs:
        return errs
    try:
        meta = tomllib.loads((d / "meta.toml").read_text(encoding="utf-8"))
    except Exception as e:
        return [f"{slug}: meta.toml 解析失败: {e}"]
    if meta.get("slug") != slug:
        errs.append(f"{slug}: meta.slug 与目录名不一致")
    if not meta.get("title"):
        errs.append(f"{slug}: meta 缺 title")
    if meta.get("difficulty") not in DIFFICULTIES:
        errs.append(f"{slug}: difficulty 非法: {meta.get('difficulty')}")
    if meta.get("source") not in SOURCES:
        errs.append(f"{slug}: source 非法: {meta.get('source')}")
    if "leetcode_id" in meta:
        lc = meta.get("leetcode_id")
        if not isinstance(lc, int) or isinstance(lc, bool) or lc < 1:
            errs.append(f"{slug}: leetcode_id 必须是正整数")
    samples = meta.get("samples")
    if not isinstance(samples, list) or not samples:
        errs.append(f"{slug}: samples 必须是非空列表")
        samples = []
    limit_s = meta.get("time_limit_ms", 5000) / 1000 * 2

    tests = sorted((d / "tests").glob("*.in")) if (d / "tests").is_dir() else []
    if not tests:
        errs.append(f"{slug}: tests/ 没有用例")
    ordinals = [int(p.stem) for p in tests if p.stem.isdigit()]
    if sorted(samples) and (not all(isinstance(o, int) for o in ordinals)
                            or max(samples) > len(tests)):
        errs.append(f"{slug}: samples={samples} 超出用例数量 {len(tests)}")
    if len(set(samples)) != len(samples):
        errs.append(f"{slug}: samples 有重复编号: {samples}")

    seen_in: dict[str, str] = {}
    for inp in tests:
        key = norm(inp.read_text(encoding="utf-8"))
        prev = seen_in.get(key)
        if prev is not None:
            errs.append(f"{slug}: {inp.name} 与 {prev} 输入重复")
        else:
            seen_in[key] = inp.name

    stmt_path = d / "statement.md"
    if stmt_path.exists() and samples:
        blocks = SAMPLE_BLOCK.findall(stmt_path.read_text(encoding="utf-8"))
        if len(blocks) != len(samples):
            errs.append(
                f"{slug}: 题面样例 {len(blocks)} 组，meta.samples 有 {len(samples)} 组"
            )
        else:
            by_ord = {int(p.stem): p for p in tests if p.stem.isdigit()}
            for i, sidx in enumerate(samples):
                t = by_ord.get(int(sidx))
                if t is None:
                    continue
                stmt_in, stmt_out = blocks[i]
                test_in = t.read_text(encoding="utf-8")
                test_out = t.with_suffix(".out").read_text(encoding="utf-8")
                if norm(stmt_in) != norm(test_in):
                    errs.append(f"{slug}: 题面样例 {i + 1} 输入与 tests/{t.name} 不一致")
                if norm(stmt_out) != norm(test_out):
                    errs.append(f"{slug}: 题面样例 {i + 1} 输出与 tests/{t.stem}.out 不一致")

    def run_case(program: Path, inp: Path, label: str) -> None:
        outp = inp.with_suffix(".out")
        if not outp.exists():
            errs.append(f"{slug}/{inp.name}: 缺少 {outp.name}")
            return
        if inp.stat().st_size > 64 * 1024 or outp.stat().st_size > 64 * 1024:
            errs.append(f"{slug}/{inp.name}: 用例文件超过 64KB")
        try:
            r = subprocess.run(
                [sys.executable, str(program)],
                input=inp.read_text(encoding="utf-8"),
                capture_output=True, text=True, timeout=limit_s,
            )
        except subprocess.TimeoutExpired:
            errs.append(f"{slug}/{inp.name}: {label}超时(>{limit_s:.0f}s)")
            return
        if r.returncode != 0:
            errs.append(f"{slug}/{inp.name}: {label}运行错误: {r.stderr[:300]}")
            return
        if norm(r.stdout) != norm(outp.read_text(encoding="utf-8")):
            errs.append(f"{slug}/{inp.name}: {label}输出与 {outp.name} 不匹配")

    for inp in tests:
        run_case(d / "reference.py", inp, "参考解")

    # solution.md：结构 + Python3 模板代码逐用例实测
    sol_path = d / "solution.md"
    if not sol_path.exists():
        errs.append(f"{slug}: 缺少 solution.md")
        return errs
    sol_md = sol_path.read_text(encoding="utf-8")
    for section in ("## 思路", "## 复杂度", "## 模板代码"):
        if section not in sol_md:
            errs.append(f"{slug}: solution.md 缺少「{section}」小节")
    py_code, cpp_code = extract_solution(sol_md)
    if not py_code or not py_code.strip():
        errs.append(f"{slug}: solution.md 缺少 Python3 代码块")
    if not cpp_code or not cpp_code.strip():
        errs.append(f"{slug}: solution.md 缺少 C++ 代码块")
    if py_code and py_code.strip():
        with tempfile.NamedTemporaryFile(
            "w", suffix=".py", delete=False, encoding="utf-8"
        ) as f:
            f.write(py_code)
            tmp = Path(f.name)
        try:
            for inp in tests:
                run_case(tmp, inp, "题解模板")
        finally:
            tmp.unlink(missing_ok=True)
    return errs


def main() -> None:
    slugs = sys.argv[1:] or sorted(p.name for p in PROBLEMS.iterdir() if p.is_dir())
    all_errs: list[str] = []
    for s in slugs:
        errs = check(s)
        all_errs += errs
        print(("FAIL " if errs else "OK   ") + s)
        for e in errs:
            print("      " + e)
    print(f"\n{len(slugs)} 题, {len(all_errs)} 个问题")
    sys.exit(1 if all_errs else 0)


if __name__ == "__main__":
    main()
