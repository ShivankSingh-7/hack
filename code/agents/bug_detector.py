def detect_bug_line(code):

    lines = code.split("\n")

    for i, line in enumerate(lines, start=1):

        if "RDI_BEGIN" in line or "RDI_begin" in line:
            return i

        if "vecEditMode" in line:
            return i

    return 1