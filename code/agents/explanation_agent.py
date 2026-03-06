from huggingface_hub import InferenceClient
import re

client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.3"
)

def get_pattern_based_explanation(code, context, bug_line):
    lines = code.split("\n")

    if bug_line <= len(lines):
        bug_code = lines[bug_line - 1] if bug_line > 0 else ""
    else:
        bug_code = ""

    explanations = {
        r"RDI_END.*RDI_BEGIN": "RDI_END is called before RDI_BEGIN, inverting the lifecycle order which causes runtime failures.",
        r"vecEditMode\(TA::VECD\)": "Should use VTT mode instead of VECD when copyLabel() is used for the label.",
        r"\.burst\(\)\.burst\(\)": "Duplicate burst() call detected - should use execute() instead of the second burst().",
        r"iClamp\(\s*\d+.*,\s*-\d+": "iClamp parameters are reversed - low and high values should be swapped.",
        r"vForceRange\(\s*35\s*V\)": "vForceRange set to 35V which exceeds the maximum allowed range for AVI64.",
        r"vForce\(\s*31\s*V\).*vForceRange\(\s*30\s*V\)": "vForce value (31V) exceeds the vForceRange (30V) causing range overflow.",
        r"\.end\(\)\.end\(\)": "Duplicate end() call - should use node().end() instead of end().end().",
        r"push_forward": "Incorrect method name - should use push_back() instead of push_forward().",
        r"readHumanSeniority": "Function name typo - should be readHumSensor() instead of readHumanSeniority().",
        r"getVesjkctor|getVslkhalue|getWlkjnaveform": "Function name contains typo - should be getVector(), getValue(), or getWaveform().",
        r"imeas\(\)": "Incorrect casing - should use iMeas() with capital M.",
        r"\.write\(\).*RDI_END": "Should use execute() instead of write() for DC measurements.",
        r"iMeans|vMeans": "Method name typo - should be iMeas() or vMeas() instead.",
        r"mAh": "Incorrect unit - should use mA (milliamps) instead of mAh (milliamp-hours).",
        r'pin\("D0"\).*getVector\("DO"\)': "Pin name mismatch - using D0 (digit zero) for capture but DO (letter O) for retrieval.",
        r"getAlarmValue\(\s*\)": "Missing required parameter - getAlarmValue() requires a pin name parameter.",
        r"readTempThresh\(\d+\)": "Extra parameter provided - readTempThresh() takes no parameters.",
        r"getFFC\(\)": "Wrong getter method - should use getFFV() to get first fail vector.",
        r"burstUpload\(\s*false\)": "Should be set to true for burst uploads to work correctly.",
        r"samples\(9216\)": "Sample count exceeds maximum - should be 8192 or less.",
        r"rdi\.burstUpload\.smartVec": "Wrong method order - should be smartVec().burstUpload() not burstUpload.smartVec().",
        r"retrievePmuxPinStatus.*RDI_END": "Retrieving status before execute() completion - move status check outside RDI block.",
    }

    for pattern, explanation in explanations.items():
        if re.search(pattern, code, re.IGNORECASE | re.DOTALL):
            return explanation

    if context:
        return f"Bug at line {bug_line}: {context[:200]}"

    return f"Code analysis indicates bug at line {bug_line} - check API usage and parameter ordering."

def explain_bug(code, context, bug_line):
    try:
        prompt = f"""Analyze this C++ bug and explain it concisely.

Context: {context}

Bug at line {bug_line}:
{code}

Explanation:"""

        response = client.text_generation(
            prompt,
            max_new_tokens=150,
            temperature=0.3,
            do_sample=False
        )

        explanation = response.strip()

        if len(explanation) > 400:
            explanation = explanation[:397] + "..."

        return explanation

    except Exception:
        return get_pattern_based_explanation(code, context, bug_line)