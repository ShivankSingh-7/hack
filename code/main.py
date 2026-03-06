from services.dataset_loader import load_dataset
from agents.bug_detector import detect_bug_line
from agents.explanation_agent import explain_bug
import csv


df = load_dataset()

results = []

for _, row in df.iterrows():

    code = row["Code"]
    context = row["Context"]
    id_value = row["ID"]

    bug_line = detect_bug_line(code)

    explanation = explain_bug(code, context)

    results.append([id_value, bug_line, explanation])


with open("output.csv", "w", newline="") as f:

    writer = csv.writer(f)
    writer.writerow(["ID", "Bug Line", "Explanation"])
    writer.writerows(results)