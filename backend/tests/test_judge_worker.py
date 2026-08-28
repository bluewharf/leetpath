import subprocess
import sys

from judge import worker


def test_process_output_is_capped_and_terminated():
    result = worker._run_process_limited(
        [sys.executable, "-c", "import sys; sys.stdout.write('x' * 100000)"],
        timeout=10,
        output_limit=1024,
    )
    assert result.returncode == worker.OUTPUT_LIMIT_RETURN_CODE
    assert len(result.stdout.encode("utf-8")) <= 1024


def test_runtime_container_uses_security_boundaries(tmp_path, monkeypatch):
    captured: list[str] = []

    def fake_run(args, timeout, *, container_name=None):
        captured.extend(args)
        return subprocess.CompletedProcess(args, 0, "ok\n", "")

    monkeypatch.setattr(worker, "_run_docker", fake_run)
    monkeypatch.setattr(worker, "_force_rm_container", lambda _name: None)
    job = worker.JobData(
        submission_id=1,
        language="python3",
        code="print('ok')",
        time_limit_ms=1000,
        memory_limit_mb=128,
        cases=(),
        io_mode="acm",
        problem_slug="two-sum",
        leetcode_spec=None,
    )
    case = worker.CaseData(ordinal=1, input_text="", expected_output="ok", is_sample=True)
    tests_dir = tmp_path / "tests"
    tests_dir.mkdir()
    (tests_dir / "001.in").write_text("", encoding="utf-8")

    status, _, _, _ = worker._run_case(job, tmp_path, case, "python-image", "python3 main.py")

    assert status == worker.STATUS_AC
    assert ["--user", "65534:65534"] == captured[captured.index("--user"):captured.index("--user") + 2]
    assert ["--cap-drop", "ALL"] == captured[captured.index("--cap-drop"):captured.index("--cap-drop") + 2]
    assert ["--security-opt", "no-new-privileges"] == captured[
        captured.index("--security-opt"):captured.index("--security-opt") + 2
    ]


def test_compile_container_has_matching_security_limits(tmp_path, monkeypatch):
    captured: list[str] = []

    def fake_run(args, timeout, *, container_name=None):
        captured.extend(args)
        return subprocess.CompletedProcess(args, 0, "", "")

    monkeypatch.setattr(worker, "_run_docker", fake_run)
    assert worker._compile_cpp(tmp_path) is None
    for expected in (
        "--read-only",
        "--pids-limit",
        "--cap-drop",
        "--security-opt",
        "--user",
        "--tmpfs",
    ):
        assert expected in captured


def test_prepare_workdir_wraps_leetcode_solution(tmp_path, monkeypatch):
    from judge.leetcode_catalog import spec_for

    monkeypatch.setattr(worker.tempfile, "gettempdir", lambda: str(tmp_path))
    job = worker.JobData(
        submission_id=42,
        language="python3",
        code="class Solution:\n    def twoSum(self, nums, target):\n        return [0, 1]\n",
        time_limit_ms=1000,
        memory_limit_mb=128,
        cases=(worker.CaseData(ordinal=1, input_text="2\n1 2\n3\n", expected_output="0 1\n", is_sample=True),),
        io_mode="leetcode",
        problem_slug="two-sum",
        leetcode_spec=spec_for("two-sum"),
    )
    root = worker._prepare_workdir(job)
    source = (root / "main.py").read_text(encoding="utf-8")
    assert "class Solution:" in source
    assert "def twoSum" in source
    assert "json.loads" in source
    assert "if __name__" in source


def test_output_limit_closes_streams_without_waiting_on_blocked_writer():
    import time

    started = time.monotonic()
    result = worker._run_process_limited(
        [
            sys.executable,
            "-c",
            "import sys, time\n"
            "sys.stdout.write('x' * 8_000_000)\n"
            "sys.stdout.flush()\n"
            "time.sleep(30)\n",
        ],
        timeout=10,
        output_limit=2048,
    )
    elapsed = time.monotonic() - started
    assert result.returncode == worker.OUTPUT_LIMIT_RETURN_CODE
    assert len(result.stdout.encode("utf-8")) <= 2048
    assert elapsed < 5


def test_infra_error_compile_output_is_sanitized(admin_client, tmp_path, monkeypatch):
    from app import db as dbmod
    from app.models import Problem, Submission, Testcase

    leaked = str(tmp_path / "secret" / "host-worker.py")
    created = admin_client.post(
        "/api/submissions",
        json={"problem_slug": "two-sum", "language": "python3", "code": "print(1)"},
    ).json()
    assert dbmod.SessionLocal is not None
    with dbmod.SessionLocal() as db:
        submission = db.get(Submission, created["id"])
        assert submission is not None
        submission.status = "judging"
        db.commit()

    def explode(_job):
        raise RuntimeError(
            f"Traceback (most recent call last):\n  File \"{leaked}\", line 1\nboom"
        )

    monkeypatch.setattr(worker, "evaluate", explode)
    worker.process_submission(dbmod.SessionLocal, Submission, Problem, Testcase, created["id"])

    with dbmod.SessionLocal() as db:
        submission = db.get(Submission, created["id"])
        assert submission is not None
        assert submission.status == "IE"
        output = submission.compile_output or ""
        assert output == worker.USER_IE_MESSAGE
        assert "Traceback" not in output
        assert leaked not in output
        assert str(tmp_path) not in output


def test_write_result_requires_judging_status(admin_client):
    from app import db as dbmod
    from app.models import Submission

    created = admin_client.post(
        "/api/submissions",
        json={"problem_slug": "two-sum", "language": "python3", "code": "print(1)"},
    ).json()
    sub_id = created["id"]
    assert dbmod.SessionLocal is not None

    with dbmod.SessionLocal() as db:
        assert worker._write_result(
            db, Submission, sub_id, worker.STATUS_AC, 12, [{"ordinal": 1, "status": "AC"}], None
        ) is False
        assert db.get(Submission, sub_id).status == "pending"

        db.get(Submission, sub_id).status = "judging"
        db.commit()

    with dbmod.SessionLocal() as db:
        assert worker._write_result(
            db,
            Submission,
            sub_id,
            worker.STATUS_WA,
            8,
            [{"ordinal": 1, "status": "WA"}],
            None,
        ) is True
        row = db.get(Submission, sub_id)
        assert row.status == "WA"
        assert row.runtime_ms == 8
        assert row.detail[0]["status"] == "WA"


def test_worker_recovers_orphaned_judging_submissions(admin_client):
    from app import db as dbmod
    from app.models import Submission

    created = admin_client.post(
        "/api/submissions",
        json={"problem_slug": "two-sum", "language": "python3", "code": "print(1)"},
    ).json()
    assert dbmod.SessionLocal is not None
    with dbmod.SessionLocal() as db:
        submission = db.get(Submission, created["id"])
        assert submission is not None
        submission.status = "judging"
        db.commit()

    with dbmod.SessionLocal() as db:
        assert worker.recover_orphaned_judging(db, Submission) == 1

    with dbmod.SessionLocal() as db:
        assert db.get(Submission, created["id"]).status == "pending"
