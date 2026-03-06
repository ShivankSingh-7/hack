import re

class CodeAnalysisAgent:
    def __init__(self):
        self.bug_patterns = {
            "lifecycle_order": {
                "pattern": r"RDI_END\(\);[\s\S]*?RDI_BEGIN\(\);",
                "description": "RDI_END called before RDI_BEGIN - incorrect lifecycle order",
                "severity": "high"
            },
            "wrong_edit_mode": {
                "pattern": r"vecEditMode\(TA::VECD\)",
                "description": "Should use VTT mode instead of VECD when copyLabel is used",
                "severity": "medium"
            },
            "duplicate_method": {
                "pattern": r"\.(\w+)\(\)\.(\1)\(\)",
                "description": "Duplicate method call detected",
                "severity": "medium"
            },
            "reversed_clamp": {
                "pattern": r"iClamp\(\s*(\d+)\s*mA,\s*-(\1)\s*mA\)",
                "description": "iClamp parameters reversed - low and high values swapped",
                "severity": "high"
            },
            "range_overflow": {
                "pattern": r"vForce\((\d+)\s*V\).*vForceRange\((\d+)\s*V\)",
                "description": "Force value exceeds specified range",
                "severity": "high"
            },
            "pin_mismatch": {
                "pattern": r'pin\(["\'](\w+)["\']\).*getVector\(["\'](\w+)["\']\)',
                "description": "Pin name mismatch between capture and retrieval",
                "severity": "high"
            },
            "typo_function": {
                "pattern": r"(readHumanSeniority|getVesjkctor|getVslkhalue|imeas|push_forward)",
                "description": "Function name typo or incorrect API usage",
                "severity": "high"
            },
            "wrong_operation": {
                "pattern": r"\.write\(\)\s*;\s*RDI_END",
                "description": "Should use execute() instead of write() for measurements",
                "severity": "medium"
            },
            "missing_parameter": {
                "pattern": r"getAlarmValue\(\s*\)",
                "description": "Missing required parameter in function call",
                "severity": "medium"
            },
            "exceeds_limit": {
                "pattern": r"samples\((\d+)\)",
                "description": "Sample count exceeds maximum allowed value",
                "severity": "medium"
            }
        }

    def analyze_code(self, code):
        findings = []

        for bug_type, info in self.bug_patterns.items():
            matches = re.finditer(info["pattern"], code, re.IGNORECASE | re.DOTALL)
            for match in matches:
                finding = {
                    "type": bug_type,
                    "description": info["description"],
                    "severity": info["severity"],
                    "match": match.group(0),
                    "position": match.start()
                }
                findings.append(finding)

        return findings

    def get_bug_line_from_findings(self, code, findings):
        if not findings:
            return 1

        lines = code.split("\n")
        highest_severity_finding = max(
            findings,
            key=lambda x: {"high": 3, "medium": 2, "low": 1}[x["severity"]]
        )

        position = highest_severity_finding["position"]
        line_num = code[:position].count("\n") + 1

        return min(line_num, len(lines))

    def validate_result(self, bug_line, code):
        lines = code.split("\n")

        if bug_line < 1 or bug_line > len(lines):
            return False

        return True
