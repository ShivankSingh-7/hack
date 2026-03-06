from agents.bug_detector import detect_bug_line
from agents.explanation_agent import explain_bug
from agents.code_analysis_agent import CodeAnalysisAgent

class OrchestratorAgent:
    def __init__(self):
        self.code_analyzer = CodeAnalysisAgent()

    def process_code_sample(self, code, context, explanation_hint):
        analysis_findings = self.code_analyzer.analyze_code(code)

        pattern_based_line = self.code_analyzer.get_bug_line_from_findings(
            code, analysis_findings
        )

        ai_detected_line = detect_bug_line(code, context, explanation_hint)

        if pattern_based_line > 1 and analysis_findings:
            bug_line = pattern_based_line
        else:
            bug_line = ai_detected_line

        if not self.code_analyzer.validate_result(bug_line, code):
            bug_line = 1

        explanation = explain_bug(code, context, bug_line)

        confidence_score = self._calculate_confidence(
            analysis_findings, pattern_based_line, ai_detected_line
        )

        result = {
            "bug_line": bug_line,
            "explanation": explanation,
            "confidence": confidence_score,
            "findings": analysis_findings
        }

        return result

    def _calculate_confidence(self, findings, pattern_line, ai_line):
        base_confidence = 0.5

        if findings:
            base_confidence += 0.3

        if pattern_line == ai_line:
            base_confidence += 0.2

        return min(base_confidence, 1.0)

    def batch_process(self, dataset):
        results = []

        for _, row in dataset.iterrows():
            code = row["Code"]
            context = row["Context"]
            id_value = row["ID"]
            explanation_hint = row["Explanation"]

            result = self.process_code_sample(code, context, explanation_hint)

            results.append({
                "id": id_value,
                "bug_line": result["bug_line"],
                "explanation": result["explanation"],
                "confidence": result["confidence"]
            })

            print(f"Processed ID {id_value}: Line {result['bug_line']} (Confidence: {result['confidence']:.2f})")

        return results
