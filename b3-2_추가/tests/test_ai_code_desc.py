"""과제 기능 요구사항의 회귀 테스트.

실행: python3 -B -m unittest discover -s tests -v
anthropic 패키지가 없으면 SDK 예외 변환 테스트만 건너뛴다. 실제 API는 호출하지 않는다.
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ai_code_desc import ai_client, cli, generator  # noqa: E402
from ai_code_desc.convention import CONVENTION_FILENAME, Convention, load_convention  # noqa: E402
from ai_code_desc.git_context import GitError, collect_git_context, parse_status_files  # noqa: E402
from ai_code_desc.safe_mode import SafeModePolicy, apply_safe_mode, mask_sensitive_text  # noqa: E402

try:
    import anthropic
    try:
        import httpx2 as httpx  # anthropic 2.x
    except ImportError:  # pragma: no cover
        import httpx  # anthropic 1.x 이하
except ImportError:  # pragma: no cover
    anthropic = None

GOOD = """TITLE: feat: 로그인 입력 검증 추가
BODY:
## Summary
- 빈 사용자 입력을 거부합니다.
## What Changed
- app.py의 login()에 검증을 추가했습니다.
## Why It Was Needed
- 빈 입력이 로그인에 성공하던 문제를 막습니다.
## How to Verify
- login("")이 ValueError를 내는지 확인합니다.
"""


def git(cwd, *args):
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True)


class RepoTestCase(unittest.TestCase):
    """임시 Git 저장소를 만드는 공통 설정."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = self.tmp.name
        git(self.repo, "init", "-q")
        git(self.repo, "config", "user.email", "test@example.com")
        git(self.repo, "config", "user.name", "tester")
        Path(self.repo, "app.py").write_text("def login(u):\n    return True\n", encoding="utf-8")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-qm", "init")

    def tearDown(self):
        self.tmp.cleanup()

    def run_cli(self, *args, env=None):
        full_env = {k: v for k, v in os.environ.items() if k not in ("AI_API_KEY", "ANTHROPIC_API_KEY")}
        full_env.update(env or {})
        return subprocess.run([sys.executable, "-B", str(ROOT / "main.py"), *args], cwd=self.repo,
                              capture_output=True, text=True, env=full_env, stdin=subprocess.DEVNULL)


class GitContextTests(RepoTestCase):
    def test_no_changes(self):
        self.assertFalse(collect_git_context(self.repo).has_changes)

    def test_unstaged_staged_untracked_all_collected(self):
        Path(self.repo, "app.py").write_text("def login(u):\n    return bool(u)\n", encoding="utf-8")
        Path(self.repo, "staged.py").write_text("A = 1\n", encoding="utf-8")
        git(self.repo, "add", "staged.py")
        Path(self.repo, "새파일.py").write_text("B = 2\n", encoding="utf-8")
        ctx = collect_git_context(self.repo)
        self.assertEqual(sorted(ctx.files), ["app.py", "staged.py", "새파일.py"])
        for text in ("return bool(u)", "+A = 1", "+B = 2"):
            self.assertIn(text, ctx.diff_text)

    def test_must_run_at_repo_root(self):
        sub = Path(self.repo, "sub")
        sub.mkdir()
        with self.assertRaisesRegex(GitError, "프로젝트 루트"):
            collect_git_context(str(sub))

    def test_not_a_repo(self):
        with tempfile.TemporaryDirectory() as d, self.assertRaisesRegex(GitError, "git 저장소가 아닙니다"):
            collect_git_context(d)

    def test_parse_rename(self):
        self.assertEqual(parse_status_files("R  old.py -> new.py\n M a.py"), ["new.py", "a.py"])


class SafeModeTests(unittest.TestCase):
    def test_masks_keys_email_phone_and_assignments(self):
        text = ('key = "sk-ant-abcdefghijklmnopqrstuvwxyz"\nAKIAABCDEFGHIJKLMNOP\n'
                "password: hunter2\nmail dev@example.com 010-1234-5678\n")
        masked, hits = mask_sensitive_text(text, SafeModePolicy())
        for secret in ("sk-ant-abc", "AKIAABCD", "hunter2", "dev@example.com", "010-1234-5678"):
            self.assertNotIn(secret, masked)
        self.assertIn("anthropic_key", hits)
        self.assertIn("email", hits)

    def test_custom_pattern(self):
        masked, hits = mask_sensitive_text("emp_id=EMP-0042", SafeModePolicy(extra_patterns=[r"EMP-\d{4}"]))
        self.assertNotIn("EMP-0042", masked)
        self.assertEqual(hits["custom_1"], 1)

    def test_limits_files_and_lines(self):
        diff = "".join(f"diff --git a/f{i} b/f{i}\n+line\n+line\n" for i in range(15))
        result = apply_safe_mode(diff, SafeModePolicy(max_files=10, max_lines=200))
        self.assertEqual((result.total_files, result.sent_files), (15, 10))
        self.assertNotIn("f10", result.text.split("...")[0])
        result = apply_safe_mode(diff, SafeModePolicy(max_files=100, max_lines=5))
        self.assertEqual(result.sent_lines, 5)
        self.assertIn("45줄 중 5줄만 전송", result.text)


class FormatTests(unittest.TestCase):
    conv = Convention()

    def test_valid_response(self):
        desc = generator.normalize(generator.parse_title_body(GOOD))
        self.assertEqual(desc.title, "feat: 로그인 입력 검증 추가")
        self.assertTrue(generator.validate(desc, self.conv).ok)

    def test_normalize_header_and_bullet_variants(self):
        raw = GOOD.replace("## Summary", "### Summary:").replace("- 빈 사용자", "* 빈 사용자")
        raw = "```\n" + raw.replace("## How to Verify", "**How to Verify**") + "```"
        self.assertTrue(generator.validate(generator.normalize(generator.parse_title_body(raw)), self.conv).ok)

    def test_detects_errors_and_warnings(self):
        desc = generator.Description("x" * 80, "## Summary\n본문만 있음\n")
        report = generator.validate(desc, self.conv)
        self.assertTrue(any("72자" in e for e in report.errors))
        self.assertTrue(any("What Changed" in e for e in report.errors))
        self.assertTrue(any("불릿" in e for e in report.errors))
        warn = generator.validate(generator.Description("feat: " + "가" * 50, GOOD.split("BODY:\n")[1]), self.conv)
        self.assertTrue(warn.ok)
        self.assertTrue(any("권장 50자" in w for w in warn.warnings))

    def test_nested_bullets_not_counted_toward_limit(self):
        body = GOOD.split("BODY:\n")[1].replace(
            "- app.py의 login()에 검증을 추가했습니다.",
            "- a\n  - a1\n  - a2\n- b\n- c")
        report = generator.validate(generator.Description("feat: x", body), self.conv)
        self.assertFalse(any("What Changed" in w for w in report.warnings))

    def test_repair_fixes_all_required_rules(self):
        desc = generator.repair(generator.Description("t" * 100, "## Summary\n문장\n"), self.conv)
        self.assertLessEqual(len(desc.title), 72)
        self.assertTrue(generator.validate(desc, self.conv).ok)
        self.assertIn("- 문장", desc.body)

    def test_prompt_contains_inputs_and_template(self):
        prompt = generator.build_user_prompt(" M app.py", ["app.py"], "+diffline", "의도문장", self.conv)
        for text in ("의도문장", "app.py", "+diffline", "TITLE:", *generator.REQUIRED_SECTIONS):
            self.assertIn(text, prompt)


class ConventionTests(RepoTestCase):
    def test_default_when_missing(self):
        self.assertEqual(load_convention(self.repo).source, "내장 기본값")

    def test_loads_repo_file_and_applies_rules(self):
        data = {"name": "팀", "title_prefixes": ["Add", "Fix"], "rules": ["과제 코드 포함"],
                "safe_mode": {"max_files": 3, "max_lines": 50}}
        Path(self.repo, CONVENTION_FILENAME).write_text(json.dumps(data), encoding="utf-8")
        conv = load_convention(self.repo)
        self.assertEqual((conv.safe_mode.max_files, conv.safe_mode.max_lines), (3, 50))
        self.assertIn("과제 코드 포함", conv.prompt_rules())
        report = generator.validate(generator.Description("feat: x", GOOD.split("BODY:\n")[1]), conv)
        self.assertTrue(any("접두어" in w for w in report.warnings))

    def test_invalid_convention_file(self):
        Path(self.repo, "bad.json").write_text("{", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "JSON"):
            load_convention(self.repo, str(Path(self.repo, "bad.json")))


class CliTests(RepoTestCase):
    def change(self):
        Path(self.repo, "app.py").write_text(
            'def login(u):\n    return bool(u)\nTOKEN = "ghp_abcdefghijklmnopqrstuvwxyz"\n', encoding="utf-8")

    def test_no_changes_message(self):
        out = self.run_cli("describe", "--mock")
        self.assertEqual(out.returncode, 0)
        self.assertIn("변경 사항이 없습니다", out.stdout)

    def test_mock_end_to_end_uses_intent(self):
        self.change()
        out = self.run_cli("describe", "--mock", "--intent", "로그인 검증 추가")
        self.assertEqual(out.returncode, 0, out.stderr)
        for text in ("1개 파일 변경 감지", "--- Description Title ---", "feat: 로그인 검증 추가",
                     "## How to Verify", "[OK]", "AI API 호출 횟수: 0회"):
            self.assertIn(text, out.stdout)

    def test_missing_api_key(self):
        self.change()
        out = self.run_cli("describe", "--no-input")
        self.assertEqual(out.returncode, 1)
        self.assertIn("AI_API_KEY 환경변수가 설정되지 않았습니다", out.stderr)

    def test_dry_run_safe_mode_masks_prompt(self):
        self.change()
        off = self.run_cli("describe", "--dry-run", "--no-input")
        on = self.run_cli("describe", "--dry-run", "--no-input", "--safe-mode")
        self.assertIn("ghp_abcdefghij", off.stdout)
        self.assertNotIn("ghp_abcdefghij", on.stdout)
        self.assertIn("[MASKED_GITHUB_TOKEN]", on.stdout)

    def test_options_parse(self):
        args = cli.build_parser().parse_args(
            ["describe", "--model", "m", "--max-tokens", "100", "--effort", "high", "--temperature", "0.2"])
        self.assertEqual((args.model, args.max_tokens, args.effort, args.temperature), ("m", 100, "high", 0.2))

    def test_regenerates_once_then_succeeds(self):
        self.change()
        bad = "TITLE: feat: x\nBODY:\n## Summary\n- a\n"
        args = cli.build_parser().parse_args(["describe", "--intent", "x"])
        cwd = os.getcwd()
        os.chdir(self.repo)
        try:
            with patch.object(ai_client, "ensure_ready"), \
                 patch.object(ai_client, "call_model", side_effect=[bad, GOOD]) as call:
                self.assertEqual(cli.describe_command(args), 0)
            self.assertEqual(call.call_count, 2)
            self.assertIn("이전 응답의 형식 오류", call.call_args_list[1].args[1])
        finally:
            os.chdir(cwd)

    def test_repairs_after_two_bad_responses(self):
        self.change()
        bad = "TITLE: feat: x\nBODY:\n## Summary\n- a\n"
        args = cli.build_parser().parse_args(["describe", "--intent", "x"])
        cwd = os.getcwd()
        os.chdir(self.repo)
        try:
            with patch.object(ai_client, "ensure_ready"), \
                 patch.object(ai_client, "call_model", side_effect=[bad, bad]) as call:
                self.assertEqual(cli.describe_command(args), 0)
            self.assertEqual(call.call_count, 2)
        finally:
            os.chdir(cwd)


@unittest.skipIf(anthropic is None, "anthropic 패키지 미설치")
class ApiErrorTests(unittest.TestCase):
    """SDK 예외가 원인을 담은 AIError로 바뀌는지 확인한다(네트워크 미사용)."""

    def raise_with(self, exc):
        settings = ai_client.ModelSettings()
        with patch.dict(os.environ, {"AI_API_KEY": "test"}), \
             patch("anthropic.resources.beta.messages.messages.Messages.create", side_effect=exc):
            with self.assertRaises(ai_client.AIError) as ctx:
                ai_client.call_model("s", "u", settings)
        return str(ctx.exception)

    def status_error(self, cls, code, message):
        req = httpx.Request("POST", "https://api.anthropic.com/v1/messages")
        resp = httpx.Response(code, request=req)
        return cls(message, response=resp, body={"error": {"message": message}})

    def test_auth_error(self):
        msg = self.raise_with(self.status_error(anthropic.AuthenticationError, 401, "invalid x-api-key"))
        self.assertIn("인증 실패(401)", msg)
        self.assertIn("invalid x-api-key", msg)

    def test_rate_limit(self):
        self.assertIn("429", self.raise_with(self.status_error(anthropic.RateLimitError, 429, "slow down")))

    def test_network_error(self):
        req = httpx.Request("POST", "https://api.anthropic.com/v1/messages")
        self.assertIn("네트워크 오류", self.raise_with(anthropic.APIConnectionError(request=req)))


if __name__ == "__main__":
    unittest.main()
