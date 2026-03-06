# Agentic AI Bug Hunter

A modular AI system that detects bugs in C++ code snippets using an agent-based architecture and Hugging Face API.

## Architecture

The system uses a multi-agent architecture with the following components:

### 1. Orchestrator Agent
- Coordinates all sub-agents
- Manages the workflow pipeline
- Combines results from multiple agents
- Calculates confidence scores

### 2. Bug Detector Agent
- Uses pattern matching and AI inference
- Detects the exact line number where bugs occur
- Leverages Mistral-7B-Instruct for intelligent detection
- Fallback to pattern-based detection

### 3. Explanation Agent
- Generates concise bug explanations
- Uses context-aware prompting
- Provides technical insights about the bug
- Temperature-controlled for consistent outputs

### 4. Code Analysis Agent
- Pattern-based static analysis
- Detects common bug patterns:
  - Lifecycle order issues
  - API misuse
  - Parameter mismatches
  - Type errors
  - Range overflows
- Severity classification

## Features

- Multi-agent collaboration
- AI-powered bug detection using Hugging Face
- Pattern-based static analysis
- Confidence scoring
- Batch processing
- Error handling and validation
- CSV output generation

## Usage

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the bug hunter:
```bash
python code/main.py
```

Output will be saved to `output.csv` with columns:
- ID: Sample identifier
- Bug Line: Line number where the bug occurs
- Explanation: Technical explanation of the bug

## Dataset

The system expects a CSV file named `samples.csv` with columns:
- ID: Unique identifier
- Code: C++ code snippet
- Context: Context about the code
- Explanation: Bug explanation hint
- Correct Code: Fixed version

## Agent Workflow

```
Input Code Sample
      |
      v
Orchestrator Agent
      |
      +---> Code Analysis Agent (Pattern Matching)
      |
      +---> Bug Detector Agent (AI + Patterns)
      |
      +---> Explanation Agent (AI-Generated)
      |
      v
Result Validation
      |
      v
Confidence Scoring
      |
      v
Output CSV
```

## Technology Stack

- Python 3.x
- Pandas for data processing
- Hugging Face Inference API
- Mistral-7B-Instruct model
- Regular expressions for pattern matching

## Hackathon Project

This project was built for a hackathon to demonstrate modular AI agent architecture for automated code analysis and bug detection.
