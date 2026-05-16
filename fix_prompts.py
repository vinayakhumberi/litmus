import json
import os

FILE_PATH = '/Users/carollucas/Desktop/Summit/data/deep-dive.json'

MARKDOWN_INSTRUCTION_TEMPLATE = """

---
OUTPUT INSTRUCTIONS:
Format your ENTIRE response as a high-fidelity Markdown (.md) document. 
This is a Staff-level technical deep dive for a FAANG Frontend Lead candidate.

Structure:
# [Topic Name]

## 🎯 Executive Summary
(A concise, high-impact summary of the topic and why it's a "must-know" for Leads.)

## 🧠 Core Technical Deep Dive
(Extensive explanation. Go deep into the JavaScript engine, browser runtime, memory management, or specific framework internals. Do not explain basics.)

## 📊 Visual Architecture & Logic
(Provide at least TWO Mermaid.js diagrams:
1. A flow diagram (graph TD) explaining the logic/execution process.
2. A sequence or architectural diagram explaining the interaction between components.)

## 🏢 Interview Context & FAANG Signals
(Where this appears in the interview loop and the specific "Lead signals" interviewers are looking for.)

## ⚔️ Lead Level vs Senior Level
(Contrast a Senior dev response with a Staff/Lead response. Focus on trade-offs, scalability, and system-wide impact.)

## ⚠️ Common Pitfalls & Anti-Patterns
(Use this specific format for each item:)
> ### ✕ [Anti-Pattern Name]
> **Why it's wrong:** ...
> **✓ Correct Lead Approach:** ...

## 🛠️ Practice Scenarios (5-10 Scenarios)
(Provide 5 to 10 realistic, complex interview scenarios. Each should include a problem statement and a hidden "Staff-Level Solution" block.)

Use professional technical language. Use ```javascript or ```typescript for all code blocks. Return ONLY the markdown content. No conversational preamble.
"""

def fix_prompts():
    if not os.path.exists(FILE_PATH):
        print(f"Error: {FILE_PATH} not found.")
        return

    with open(FILE_PATH, 'r') as f:
        data = json.load(f)

    # Markers that indicate the start of instruction blocks we want to remove
    STRIP_MARKERS = [
        "Generate the complete study content",
        "Format your ENTIRE output",
        "Return ONLY valid JSON",
        "OUTPUT INSTRUCTIONS:",
        "\n\n{", # Start of a JSON block
        "---"
    ]

    updated_count = 0
    for topic_id, prompt in data.items():
        # Find the earliest occurrence of any strip marker
        cut_index = len(prompt)
        for marker in STRIP_MARKERS:
            idx = prompt.find(marker)
            if idx != -1 and idx < cut_index:
                cut_index = idx

        # Truncate the prompt to remove old instructions
        clean_prompt = prompt[:cut_index].strip()
        
        # Extract topic name
        topic_name = topic_id.replace('-', ' ').title()
        
        # Create and append the new instruction
        instruction = MARKDOWN_INSTRUCTION_TEMPLATE.replace('[Topic Name]', topic_name)
        data[topic_id] = clean_prompt + instruction
        updated_count += 1

    with open(FILE_PATH, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"Successfully cleaned and updated {updated_count} prompts in {FILE_PATH}.")

if __name__ == "__main__":
    fix_prompts()
