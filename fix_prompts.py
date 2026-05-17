import json
import os

# Target the evaluation prompts specifically
EVAL_FILE_PATH = '/Users/carollucas/Desktop/Summit/data/evaluation.json'

TEST_JSON_TEMPLATE = """

Format your ENTIRE response as structured JSON matching this EXACT schema. Return ONLY valid JSON. No preamble.

{
  "test": {
    "topicId": "[topic-id]",
    "topicName": "[Topic Name]",
    "category": "[Category]",
    "totalQuestions": 10,
    "totalPoints": 100,
    "passingScore": 70,
    "questions": [
      {
        "id": 1,
        "type": "multiple-choice",
        "difficulty": "easy | medium | hard",
        "question": "...",
        "options": ["A) Option text", "B) Option text", "C) Option text", "D) Option text"],
        "correctAnswer": "A",
        "explanation": "Detailed lead-level explanation...",
        "points": 10
      },
      {
        "id": 5,
        "type": "short-answer",
        "difficulty": "medium",
        "question": "...",
        "sampleAnswer": "Comprehensive lead-level model answer...",
        "explanation": "Key points that must be covered for full credit.",
        "points": 10
      },
      {
        "id": 8,
        "type": "code-scenario",
        "difficulty": "hard",
        "scenario": "Architectural problem statement...",
        "code": "// JavaScript/TypeScript snippet for context",
        "correctAnswer": "Complete solution including fix and trade-off analysis.",
        "explanation": "Scoring rubric and technical rationale.",
        "points": 10
      }
    ]
  }
}
"""

def fix_evaluation_prompts():
    if not os.path.exists(EVAL_FILE_PATH):
        print(f"Error: {EVAL_FILE_PATH} not found.")
        return

    with open(EVAL_FILE_PATH, 'r') as f:
        data = json.load(f)

    updated_count = 0
    for topic_id, prompt in data.items():
        # Clean up legacy instructions or formatting requirements
        if 'Generate the test in this' in prompt:
            prompt = prompt.split('Generate the test in this')[0]
        if 'IMPORTANT GUIDELINES:' in prompt:
            prompt = prompt.split('IMPORTANT GUIDELINES:')[0]
        if 'Format your ENTIRE output' in prompt:
            prompt = prompt.split('Format your ENTIRE output')[0]
        
        # Clean topic name
        topic_name = topic_id.replace('-', ' ').title()
        
        # Create the new instruction block
        instruction = TEST_JSON_TEMPLATE.replace('[topic-id]', topic_id).replace('[Topic Name]', topic_name)
        
        data[topic_id] = prompt.strip() + instruction
        updated_count += 1

    with open(EVAL_FILE_PATH, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"Successfully updated {updated_count} evaluation prompts in {EVAL_FILE_PATH}.")

if __name__ == "__main__":
    fix_evaluation_prompts()
