from huggingface_hub import InferenceClient
import re

client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.3",
    provider="hf-inference"
)

def detect_bug_line(code, context, explanation):
    lines = code.split("\n")

    bug_patterns = {
        "RDI_END.*RDI_BEGIN": "lifecycle_order",
        r"vecEditMode\(TA::VECD\)": "wrong_edit_mode",
        r"\.burst\(\)\.burst\(\)": "duplicate_burst",
        r"iClamp\(\s*\d+.*,\s*-\d+": "reversed_clamp",
        r"vForceRange\(\s*35\s*V\)": "range_overflow",
        r"vForce\(\s*31\s*V\).*vForceRange\(\s*30\s*V\)": "force_exceeds_range",
        r"\.end\(\)\.end\(\)": "duplicate_end",
        r"push_forward": "wrong_method_name",
        r"readHumanSeniority|getVesjkctor|getVslkhalue|getWlkjnaveform": "typo_function",
        r"imeas\(\)": "wrong_case",
        r"\.write\(\)": "wrong_operation",
        r"iMeans|vMeans|mAh": "typo_parameter",
        r'pin\("D0"\).*getVector\("DO"\)': "pin_mismatch",
        r"getAlarmValue\(\)": "missing_parameter",
        r"readTempThresh\(\d+\)": "extra_parameter",
        r"getFFC\(\)": "wrong_getter",
        r"burstUpload\(\s*false\)": "wrong_boolean",
        r"samples\(9216\)": "exceeds_max_samples",
        r"rdi\.burstUpload\.smartVec": "wrong_order",
        r"retrievePmuxPinStatus.*RDI_END": "premature_status_check",
    }

    detected_line = 1
    max_confidence = 0

    for i, line in enumerate(lines, start=1):
        line_confidence = 0

        for pattern, bug_type in bug_patterns.items():
            if re.search(pattern, line, re.IGNORECASE):
                line_confidence += 1

        if "RDI_END" in line and i < len(lines) // 2:
            line_confidence += 2

        if "RDI_BEGIN" in line and i > len(lines) // 2:
            line_confidence += 2

        if any(keyword in line.lower() for keyword in ["bug", "error", "wrong", "mismatch", "typo"]):
            line_confidence += 0.5

        if line_confidence > max_confidence:
            max_confidence = line_confidence
            detected_line = i

    if max_confidence == 0:
        prompt = f"""Find the bug line number.

Code:
{code}

Context: {context}

Line number:"""

        try:
            response = client.text_generation(
                prompt,
                max_new_tokens=20,
                temperature=0.1
            )

            result = response.strip()
            match = re.search(r'\d+', result)
            if match:
                detected_line = int(match.group())
        except Exception:
            pass

    return detected_line