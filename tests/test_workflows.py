from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class WorkflowTests(unittest.TestCase):
    def test_cn_security_master_probe_uses_private_source_and_aggregate_output(self) -> None:
        text = (
            ROOT / ".github" / "workflows" / "cn-security-master-admission-probe.yml"
        ).read_text(encoding="utf-8")

        self.assertIn("name: CN Security Master Admission Probe", text)
        self.assertIn("schedule:", text)
        self.assertIn("cron: '47 11 * * 1-5'", text)
        self.assertIn("repository: peilinok/py-trading-data", text)
        self.assertIn("token: ${{ secrets.PY_TRADING_DATA_REPO_TOKEN }}", text)
        self.assertIn("python tools/cn_security_master_probe.py", text)
        self.assertIn("$RUNNER_TEMP/cn-security-master", text)
        self.assertIn("cn-security-master-coverage.json", text)
        self.assertIn("retry_probe:", text)
        self.assertIn("needs.probe.outputs.retry_needed == 'true'", text)
        self.assertIn("source_commit:", text)
        self.assertIn("ref: ${{ needs.probe.outputs.source_commit }}", text)
        self.assertIn("retention-days: 21", text)
        self.assertNotIn("pull_request:", text)
        self.assertNotIn("git push", text)


if __name__ == "__main__":
    unittest.main()
