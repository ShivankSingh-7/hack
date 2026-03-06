from services.dataset_loader import load_dataset
from agents.orchestrator_agent import OrchestratorAgent
import csv

def main():
    print("=" * 60)
    print("Agentic AI Bug Hunter - Hackathon Project")
    print("=" * 60)

    print("\n[1/3] Loading dataset...")
    df = load_dataset()
    print(f"Loaded {len(df)} code samples")

    print("\n[2/3] Initializing agent system...")
    orchestrator = OrchestratorAgent()
    print("Agent system ready: Orchestrator, Bug Detector, Explanation Agent, Code Analyzer")

    print("\n[3/3] Processing code samples...")
    results = orchestrator.batch_process(df)

    print("\n" + "=" * 60)
    print("Generating output.csv...")

    with open("output.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Bug Line", "Explanation"])

        for result in results:
            writer.writerow([
                result["id"],
                result["bug_line"],
                result["explanation"]
            ])

    print(f"Successfully processed {len(results)} samples")
    print("Output saved to: output.csv")
    print("=" * 60)

    avg_confidence = sum(r["confidence"] for r in results) / len(results)
    print(f"\nAverage Confidence Score: {avg_confidence:.2%}")
    print("Agentic AI Bug Hunter completed successfully!")

if __name__ == "__main__":
    main()