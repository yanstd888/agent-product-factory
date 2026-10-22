from dataclasses import dataclass
import json


@dataclass(frozen=True)
class Finding:
    id: str
    status: str
    severity: str
    message: str
    path: str | None = None

    def to_dict(self) -> dict[str, str]:
        finding = {
            "id": self.id,
            "status": self.status,
            "severity": self.severity,
            "message": self.message,
        }
        if self.path is not None:
            finding["path"] = self.path
        return finding


@dataclass
class Report:
    product_path: str
    product_type: str
    findings: list[Finding]

    @property
    def exit_code(self) -> int:
        if not self.findings:
            return 1
        return 1 if any(
            finding.status == "fail" and finding.severity == "blocker"
            for finding in self.findings
        ) else 0

    def to_dict(self) -> dict[str, object]:
        passed = sum(finding.status == "pass" for finding in self.findings)
        blockers = sum(
            finding.status == "fail" and finding.severity == "blocker"
            for finding in self.findings
        )
        warnings = sum(
            finding.status == "fail" and finding.severity == "warning"
            for finding in self.findings
        )
        return {
            "schema_version": "1.0",
            "product_path": self.product_path,
            "product_type": self.product_type,
            "findings": [finding.to_dict() for finding in self.findings],
            "summary": {
                "passed": passed,
                "blockers": blockers,
                "warnings": warnings,
            },
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2, sort_keys=True) + "\n"

    def to_human(self) -> str:
        summary = self.to_dict()["summary"]
        state = "PASS" if self.exit_code == 0 else "BLOCKED"
        lines = [
            f"Product QA: {state}",
            f"Type: {self.product_type}",
            f"Path: {self.product_path}",
            "Passed: {passed} | Blockers: {blockers} | Warnings: {warnings}".format(
                **summary
            ),
        ]
        for finding in self.findings:
            if finding.status == "fail":
                location = f" ({finding.path})" if finding.path else ""
                lines.append(
                    f"[{finding.severity.upper()}] {finding.id}{location}: {finding.message}"
                )
        return "\n".join(lines)
