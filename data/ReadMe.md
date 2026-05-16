# JSON Structure Guide

Complete documentation for all JSON files in the FAANG Frontend Lead Interview Prep system.

---

## Table of Contents

1. [prompts.json](#1-promptsjson) - Study content generation prompts
2. [test_prompts.json](#2-test_promptsjson) - Test question generation prompts
3. [evaluation_prompts.json](#3-evaluation_promptsjson) - Test evaluation prompts
4. [plan.json](#4-planjson) - Master study plan with topics
5. [schedule.json](#5-schedulejson) - Week-by-week study schedule
6. [Generated Files](#6-generated-files)
   - [Topic study content](#61-topic-study-content)
   - [Test questions](#62-test-questions)
   - [Test results](#63-test-results)

---

## 1. prompts.json

**Purpose**: Contains study content generation prompts for all 68 topics.

**Location**: `data/prompts.json`

**Size**: ~199 KB

### Structure

```json
{
  "topic-id-1": "Full study prompt text...",
  "topic-id-2": "Full study prompt text...",
  ...
  "topic-id-68": "Full study prompt text..."
}
```

### Example Entry

```json
{
  "event-loop-microtasks-macrotasks": "You are my FAANG Frontend Lead interview coach. I am preparing for interviews at Meta, Google, Amazon, Microsoft, or similar companies. I have 11 years of frontend experience.\n\nToday's topic: Event loop, call stack, microtasks vs macrotasks\n\nTeach me this topic as if you're preparing me for a FAANG interview...\n\n[Full prompt continues with sections for Core Concept, Interview Context, etc.]"
}
```

### Usage

```javascript
// Load prompts
const prompts = await fetch('data/prompts.json').then(r => r.json());

// Get prompt for a specific topic
const topicId = 'event-loop-microtasks-macrotasks';
const studyPrompt = prompts[topicId];

// Display with copy button in your app
displayPrompt(studyPrompt);
```

### Prompt Content Includes

Each prompt contains:
- Topic name and category
- Core concept deep dive
- Interview context (why it matters)
- Lead vs Senior answer examples
- Common mistakes to avoid
- Practice questions (5 questions)
- Mini-test format
- JSON output specification

---

## 2. test_prompts.json

**Purpose**: Contains test question generation prompts for all 68 topics.

**Location**: `data/test_prompts.json`

**Size**: ~315 KB

### Structure

```json
{
  "topic-id-1": "Full test generation prompt text...",
  "topic-id-2": "Full test generation prompt text...",
  ...
  "topic-id-68": "Full test generation prompt text..."
}
```

### Example Entry

```json
{
  "react-reconciliation": "You are my FAANG Frontend Lead interview test generator. I am preparing for interviews at Meta, Google, Amazon, Microsoft, or similar companies. I have 11 years of frontend experience.\n\nGenerate a comprehensive test for the topic: React reconciliation and virtual DOM diffing algorithm\n\n[Detailed specifications for test generation...]"
}
```

### Usage

```javascript
// Load test prompts
const testPrompts = await fetch('data/test_prompts.json').then(r => r.json());

// Get test generation prompt for a topic
const testPrompt = testPrompts['react-reconciliation'];

// User copies prompt, pastes into Claude
// Claude generates test JSON
// Save to data/tests/react-reconciliation-test.json
```

### Test Specifications in Prompt

Each prompt specifies:
- 10 questions total
- Mix: 4 multiple-choice, 3 short-answer, 3 code-scenario
- Difficulty: 3 easy, 4 medium, 3 hard
- FAANG Lead-level standards
- JSON output format for test

---

## 3. evaluation_prompts.json

**Purpose**: Contains test evaluation prompts that score answers and generate result JSON.

**Location**: `data/evaluation_prompts.json`

**Size**: ~452 KB

### Structure

```json
{
  "topic-id-1": "Full evaluation prompt text...",
  "topic-id-2": "Full evaluation prompt text...",
  ...
  "topic-id-68": "Full evaluation prompt text..."
}
```

### Example Entry

```json
{
  "core-web-vitals": "You are my FAANG Frontend Lead interview evaluator. I just completed a test on: Core Web Vitals: LCP, CLS, INP — definitions, thresholds, improvements\n\nYour task: Evaluate my answers strictly according to FAANG Lead-level standards and generate a detailed result report.\n\n[Evaluation criteria, scoring rubric, JSON format specification...]"
}
```

### Usage

```javascript
// Load evaluation prompts
const evalPrompts = await fetch('data/evaluation_prompts.json').then(r => r.json());

// Get evaluation prompt
const evalPrompt = evalPrompts['core-web-vitals'];

// User pastes:
// 1. Evaluation prompt
// 2. Test JSON (from data/tests/core-web-vitals-test.json)
// 3. Their answers
//
// Claude evaluates and generates result JSON
// Save to data/results/core-web-vitals-result-20260515.json
```

### Evaluation Output Specified

Each prompt specifies JSON result structure with:
- Score (0-100)
- Grade (A, B+, B, etc.)
- Readiness level
- Question-by-question feedback
- Strengths and weaknesses
- Recommendations

---

## 4. plan.json

**Purpose**: Master study plan containing all 68 topics with metadata.

**Location**: `data/plan.json`

**Size**: ~68 KB (when complete)

### Structure

```json
{
  "plan": {
    "title": "FAANG Frontend Lead Interview Prep",
    "targetDate": "2026-07-10",
    "startDate": "2026-05-15",
    "description": "Complete preparation system for Frontend Lead role...",
    "categories": [
      {
        "id": "category-1",
        "name": "JavaScript & Browser Internals",
        "description": "Deep dive into JS engine, event loop, and browser mechanics",
        "topics": [
          {
            "id": "event-loop-microtasks-macrotasks",
            "name": "Event loop, call stack, microtasks vs macrotasks",
            "category": "JavaScript & Browser Internals",
            "difficulty": "Medium",
            "estimatedHours": 3,
            "priority": "High",
            "status": "not-started",
            "score": 0,
            "passingScore": 70,
            "recommendedWeek": "Week 1-2",
            "tags": ["javascript", "async", "event-loop", "promises"]
          }
          // ... more topics
        ]
      }
      // ... more categories
    ]
  }
}
```

### Top-Level Fields

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Plan title |
| `targetDate` | string | Interview target date (YYYY-MM-DD) |
| `startDate` | string | Study start date (YYYY-MM-DD) |
| `description` | string | Plan description |
| `categories` | array | Array of category objects |

### Category Object

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique category identifier (e.g., "category-1") |
| `name` | string | Category display name |
| `description` | string | Category description |
| `topics` | array | Array of topic objects |

### Topic Object

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique topic identifier (kebab-case) |
| `name` | string | Topic display name |
| `category` | string | Parent category name |
| `difficulty` | string | "Easy", "Medium", or "Hard" |
| `estimatedHours` | number | Estimated study hours (2-4) |
| `priority` | string | "High", "Medium", or "Low" |
| `status` | string | "not-started", "in-progress", "completed" |
| `score` | number | Test score (0-100) |
| `passingScore` | number | Minimum passing score (typically 70) |
| `recommendedWeek` | string | Recommended study week (e.g., "Week 1-2") |
| `tags` | array | Array of tag strings |

### Usage

```javascript
// Load plan
const planData = await fetch('data/plan.json').then(r => r.json());

// Get all categories
const categories = planData.plan.categories;

// Get all topics in a category
const jsTopics = categories.find(c => c.id === 'category-1').topics;

// Filter high-priority topics
const highPriority = jsTopics.filter(t => t.priority === 'High');

// Update topic status
topic.status = 'in-progress';
topic.score = 85;

// Save back to plan.json
```

---

## 5. schedule.json

**Purpose**: Week-by-week study schedule from May 15 to July 10, 2026.

**Location**: `data/schedule.json`

**Size**: ~45 KB

### Structure

```json
{
  "schedule": {
    "startDate": "2026-05-15",
    "targetDate": "2026-07-10",
    "totalWeeks": 8,
    "totalDays": 57,
    "phases": [ /* ... */ ],
    "weeks": [ /* ... */ ],
    "milestones": [ /* ... */ ],
    "summary": { /* ... */ },
    "categoryBreakdown": { /* ... */ },
    "studyTips": [ /* ... */ ]
  }
}
```

### Top-Level Fields

| Field | Type | Description |
|-------|------|-------------|
| `startDate` | string | Schedule start date (YYYY-MM-DD) |
| `targetDate` | string | Interview target date (YYYY-MM-DD) |
| `totalWeeks` | number | Total weeks in schedule (8) |
| `totalDays` | number | Total days (57) |
| `phases` | array | Study phases with date ranges |
| `weeks` | array | Weekly schedule objects |
| `milestones` | array | Key milestone objects |
| `summary` | object | Overall summary statistics |
| `categoryBreakdown` | object | Topics per category |
| `studyTips` | array | Study tips and recommendations |

### Phase Object

```json
{
  "name": "Employed - Evening Study",
  "dateRange": "May 15 - June 19",
  "weeks": "Week 1-5",
  "dailyHours": "1-1.5 hours weekdays",
  "weeklyHours": "7.5 hours"
}
```

### Week Object

```json
{
  "weekNumber": 1,
  "dateRange": "May 15 - May 21",
  "phase": "Employed - Evening Study",
  "availableHours": 10.5,
  "focus": "High-priority React + Core Web Vitals + STAR method",
  "days": [
    {
      "date": "2026-05-15",
      "day": "Thursday",
      "availableHours": 1.5,
      "topics": [
        {
          "topicId": "react-reconciliation",
          "topicName": "React reconciliation and virtual DOM diffing algorithm",
          "category": "React & Frontend Frameworks (Deep)",
          "estimatedHours": 1.5,
          "activity": "Study (Part 1/3)"
        }
      ]
    }
    // ... more days
  ],
  "weeklyGoals": [
    "Complete React reconciliation topic",
    "Complete Core Web Vitals topic"
  ],
  "topicsCompleted": 2
}
```

### Day Object

| Field | Type | Description |
|-------|------|-------------|
| `date` | string | Date (YYYY-MM-DD) |
| `day` | string | Day of week |
| `availableHours` | number | Study hours available |
| `topics` | array | Topics scheduled for this day |
| `note` | string (optional) | Special notes (e.g., "Rest day") |

### Topic Activity Object

| Field | Type | Description |
|-------|------|-------------|
| `topicId` | string | Topic identifier |
| `topicName` | string | Topic display name |
| `category` | string | Category name |
| `estimatedHours` | number | Hours allocated for this session |
| `activity` | string | Activity description (e.g., "Study (Part 1/3)") |

### Milestone Object

```json
{
  "date": "2026-05-21",
  "milestone": "Complete Week 1: React reconciliation, Core Web Vitals, STAR method started"
}
```

### Summary Object

```json
{
  "totalTopics": 68,
  "coveredInSchedule": 68,
  "highPriorityFirst": true,
  "balancedCategories": true,
  "mockInterviews": 3,
  "expectedReadiness": "Interview Ready - 85%+ average score across all topics"
}
```

### Usage

```javascript
// Load schedule
const schedule = await fetch('data/schedule.json').then(r => r.json());

// Get current week
const today = new Date('2026-05-18');
const currentWeek = schedule.schedule.weeks.find(week => {
  const [start, end] = week.dateRange.split(' - ');
  // ... date comparison logic
});

// Get today's topics
const todayDate = '2026-05-18';
const todaySchedule = currentWeek.days.find(d => d.date === todayDate);
const todaysTopics = todaySchedule.topics;

// Display week overview
displayWeek(currentWeek);

// Show progress
const completedWeeks = schedule.schedule.weeks.filter(w => w.weekNumber < 3);
const progressPercent = (completedWeeks.length / 8) * 100;
```

---

## 6. Generated Files

These files are created by pasting prompts into Claude and saving the JSON responses.

### 6.1 Topic Study Content

**Location**: `data/topics/[topic-id].json`

**Example**: `data/topics/event-loop-microtasks-macrotasks.json`

**Generated by**: Pasting prompt from `prompts.json` into Claude

### Structure

```json
{
  "topic": {
    "id": "event-loop-microtasks-macrotasks",
    "name": "Event loop, call stack, microtasks vs macrotasks",
    "category": "JavaScript & Browser Internals",
    "difficulty": "Medium",
    "estimatedStudyTime": 3,

    "coreConcept": {
      "summary": "The event loop is JavaScript's concurrency model...",
      "keyPoints": [
        "JavaScript is single-threaded but can handle async operations",
        "Call stack executes synchronous code",
        "Microtasks have higher priority than macrotasks"
      ],
      "detailedExplanation": "Long-form explanation here..."
    },

    "interviewContext": {
      "whyItMatters": "This topic is critical because...",
      "frequencyInInterviews": "High - appears in 70% of frontend interviews",
      "commonQuestions": [
        "Explain the event loop",
        "What's the difference between microtasks and macrotasks?",
        "What's the output of this async code?"
      ]
    },

    "leadVsSeniorAnswer": {
      "seniorDevAnswer": "Demonstrates solid understanding...",
      "leadLevelAnswer": "Not only explains but discusses trade-offs...",
      "keyDifferences": [
        "Lead mentions performance implications",
        "Lead discusses architectural decisions"
      ]
    },

    "commonMistakes": [
      {
        "mistake": "Confusing microtask and macrotask execution order",
        "whyItsMistaken": "This shows lack of understanding of priority",
        "correctApproach": "Microtasks always execute before next macrotask"
      }
    ],

    "practiceQuestions": [
      {
        "id": 1,
        "question": "What's the output of this code?",
        "code": "console.log('1');\nsetTimeout(() => console.log('2'), 0);",
        "expectedAnswer": "1, 3, 2",
        "explanation": "Detailed explanation..."
      }
    ],

    "miniTest": {
      "questions": [
        {
          "id": 1,
          "question": "Which executes first: microtask or macrotask?",
          "options": ["A) Microtask", "B) Macrotask", "C) Same priority", "D) Depends"],
          "correctAnswer": "A",
          "explanation": "Microtasks always have higher priority"
        }
      ],
      "passingScore": 3,
      "totalQuestions": 5
    },

    "resources": [
      {
        "title": "MDN: Event Loop",
        "type": "documentation",
        "relevance": "High"
      }
    ],

    "relatedTopics": [
      "closures-scope-hoisting",
      "react-fiber-concurrent"
    ]
  }
}
```

### Key Sections

| Section | Description |
|---------|-------------|
| `coreConcept` | Core technical explanation |
| `interviewContext` | Why it matters in interviews |
| `leadVsSeniorAnswer` | How Lead answers differ from Senior |
| `commonMistakes` | Pitfalls to avoid |
| `practiceQuestions` | 5 practice questions with answers |
| `miniTest` | Quick 5-question test |
| `resources` | Additional learning resources |
| `relatedTopics` | Connected topics to study |

---

### 6.2 Test Questions

**Location**: `data/tests/[topic-id]-test.json`

**Example**: `data/tests/react-reconciliation-test.json`

**Generated by**: Pasting prompt from `test_prompts.json` into Claude

### Structure

```json
{
  "test": {
    "topicId": "react-reconciliation",
    "topicName": "React reconciliation and virtual DOM diffing algorithm",
    "category": "React & Frontend Frameworks (Deep)",
    "totalQuestions": 10,
    "totalPoints": 100,
    "passingScore": 70,
    "estimatedTime": 30,
    "difficulty": "FAANG Lead Level",
    "instructions": "Answer all questions to the best of your ability...",

    "questions": [
      {
        "id": 1,
        "type": "multiple-choice",
        "difficulty": "easy",
        "question": "What is the primary purpose of React's reconciliation?",
        "options": [
          "A) To update the virtual DOM",
          "B) To minimize DOM updates by comparing virtual DOM trees",
          "C) To create new components",
          "D) To handle state management"
        ],
        "correctAnswer": "B",
        "explanation": "Reconciliation is React's diffing algorithm...",
        "points": 10,
        "tags": ["react", "reconciliation", "vdom"]
      },

      {
        "id": 5,
        "type": "short-answer",
        "difficulty": "medium",
        "question": "Explain how React's keys help in the reconciliation process. What happens if you use array indices as keys?",
        "keyPoints": [
          "Keys help React identify which items changed",
          "Stable keys improve reconciliation performance",
          "Array indices as keys cause issues with reordering",
          "Can lead to incorrect state associations"
        ],
        "sampleAnswer": "Keys are used by React to identify elements...",
        "points": 10,
        "tags": ["react", "keys", "reconciliation"]
      },

      {
        "id": 8,
        "type": "code-scenario",
        "difficulty": "hard",
        "scenario": "You're in a technical interview. The interviewer shows you this component that's experiencing performance issues:",
        "question": "What's the problem with this approach? How would you fix it? What are the trade-offs?",
        "code": "function List({ items }) {\n  return items.map((item, i) => <Item key={i} data={item} />);\n}",
        "correctAnswer": "The problem is using array index as key. When items reorder, React can't properly track components...",
        "rubric": {
          "identified_issue": "3 points - Must identify index as key problem",
          "explained_why": "3 points - Must explain reconciliation issues",
          "proposed_fix": "3 points - Must provide working solution with stable keys",
          "discussed_tradeoffs": "1 point - Bonus for discussing performance vs convenience"
        },
        "points": 10,
        "tags": ["react", "performance", "keys", "reconciliation"]
      }
    ],

    "answerSubmissionFormat": {
      "instructions": "After completing the test, submit your answers in this format for evaluation",
      "format": {
        "candidateName": "Your Name",
        "testDate": "YYYY-MM-DD",
        "topicId": "react-reconciliation",
        "answers": [
          {"questionId": 1, "answer": "Your answer here"},
          {"questionId": 2, "answer": "Your answer here"}
        ]
      }
    }
  }
}
```

### Question Types

**Multiple Choice** (`type: "multiple-choice"`)
- 4 options (A, B, C, D)
- Single correct answer
- 10 points each
- 4 questions per test

**Short Answer** (`type: "short-answer"`)
- Open-ended question
- Key points to cover
- Sample answer provided
- 10 points each
- 3 questions per test

**Code Scenario** (`type: "code-scenario"`)
- Real-world scenario
- Code provided
- Must identify issue, explain why, propose fix
- Scoring rubric included
- 10 points each
- 3 questions per test

---

### 6.3 Test Results

**Location**: `data/results/[topic-id]-result-[date].json`

**Example**: `data/results/react-reconciliation-result-20260518.json`

**Generated by**: Pasting prompt from `evaluation_prompts.json` + test JSON + answers into Claude

### Structure

```json
{
  "result": {
    "topicId": "react-reconciliation",
    "topicName": "React reconciliation and virtual DOM diffing algorithm",
    "category": "React & Frontend Frameworks (Deep)",
    "testDate": "2026-05-18",
    "candidateName": "Your Name",

    "score": 85,
    "totalPoints": 100,
    "percentage": 85,
    "passed": true,
    "grade": "B+",
    "readinessLevel": "Interview Ready",
    "timeSpent": 28,

    "questionResults": [
      {
        "questionId": 1,
        "type": "multiple-choice",
        "question": "What is the primary purpose of React's reconciliation?",
        "yourAnswer": "B",
        "correctAnswer": "B",
        "isCorrect": true,
        "pointsEarned": 10,
        "pointsPossible": 10,
        "feedback": "Correct! You understand the purpose of reconciliation."
      },

      {
        "questionId": 5,
        "type": "short-answer",
        "question": "Explain how React's keys help...",
        "yourAnswer": "Keys help React identify which items changed. Using stable keys improves performance...",
        "keyPointsCovered": [
          {"point": "Keys help React identify which items changed", "covered": true},
          {"point": "Stable keys improve reconciliation performance", "covered": true},
          {"point": "Array indices as keys cause issues with reordering", "covered": false},
          {"point": "Can lead to incorrect state associations", "covered": true}
        ],
        "isCorrect": false,
        "pointsEarned": 7,
        "pointsPossible": 10,
        "feedback": "Good coverage of key points 1, 2, and 4. Missed point 3 about reordering issues..."
      },

      {
        "questionId": 8,
        "type": "code-scenario",
        "question": "What's the problem with this approach?",
        "yourAnswer": "The problem is using array index as key. This causes React to lose track...",
        "rubricScores": {
          "identified_issue": 3,
          "explained_why": 2,
          "proposed_fix": 3,
          "discussed_tradeoffs": 1
        },
        "isCorrect": false,
        "pointsEarned": 9,
        "pointsPossible": 10,
        "feedback": "Correctly identified the issue and provided a fix. Explanation of 'why' could be more detailed..."
      }
    ],

    "overallFeedback": {
      "strengths": [
        "Strong understanding of reconciliation basics",
        "Correctly identified the key as index anti-pattern",
        "Good grasp of performance implications"
      ],
      "weaknesses": [
        "Missed some details about reordering behavior",
        "Could be more specific about state association issues"
      ],
      "missedConcepts": [
        "How reordering affects reconciliation with index keys",
        "Edge cases in key usage"
      ],
      "recommendations": "You're interview-ready on this topic with minor gaps. Review the specific behavior when items reorder and practice explaining reconciliation edge cases."
    },

    "readinessAssessment": {
      "readinessLevel": "Interview Ready",
      "confidence": "High",
      "shouldRetake": false,
      "estimatedStudyHoursNeeded": 0.5,
      "nextSteps": [
        "Quick review of reordering behavior",
        "Practice whiteboard explanation of reconciliation",
        "Move to next topic: Fiber architecture"
      ]
    },

    "breakdown": {
      "multipleChoiceScore": 40,
      "shortAnswerScore": 22,
      "codeScenarioScore": 23,
      "totalScore": 85
    },

    "comparisonToStandard": {
      "juniorLevel": "Would score ~50-60%",
      "midLevel": "Would score ~65-75%",
      "seniorLevel": "Would score ~75-85%",
      "leadLevel": "Would score 85%+",
      "yourLevel": "Senior+ level, approaching Lead",
      "gapToLead": "To reach full Lead level: deeper understanding of edge cases and reordering mechanics"
    }
  }
}
```

### Result Fields

| Field | Type | Description |
|-------|------|-------------|
| `score` | number | Total points earned (0-100) |
| `totalPoints` | number | Maximum possible points (100) |
| `percentage` | number | Score as percentage (0-100) |
| `passed` | boolean | true if score >= 70 |
| `grade` | string | Letter grade (A, A-, B+, B, etc.) |
| `readinessLevel` | string | "Excellent", "Interview Ready", "Needs Review", "Not Ready" |
| `timeSpent` | number | Minutes spent on test |

### Question Result Object

For **multiple-choice**:
- `yourAnswer`: "A", "B", "C", or "D"
- `correctAnswer`: The right answer
- `isCorrect`: boolean
- `pointsEarned`: 10 or 0

For **short-answer**:
- `yourAnswer`: Full text answer
- `keyPointsCovered`: Array of key points with `covered: true/false`
- `pointsEarned`: 0-10 based on coverage

For **code-scenario**:
- `yourAnswer`: Full text answer
- `rubricScores`: Object with scores for each rubric item
- `pointsEarned`: Sum of rubric scores

### Readiness Levels

| Level | Score Range | Meaning |
|-------|-------------|---------|
| Excellent | 90-100% | Deep expertise, definitely ready |
| Interview Ready | 70-89% | Ready for interviews, minor gaps OK |
| Needs Review | 50-69% | Not ready, focused study needed |
| Not Ready | < 50% | Significant gaps, comprehensive review |

### Grading Scale

| Grade | Score Range |
|-------|-------------|
| A | 90-100% |
| A- | 85-89% |
| B+ | 80-84% |
| B | 75-79% |
| B- | 70-74% |
| C+ | 65-69% |
| C | 60-64% |
| F | < 60% |

---

## File Relationships

```
prompts.json
    ↓
    [User copies prompt, pastes into Claude]
    ↓
data/topics/[topic-id].json (Study content)
    ↓
    [User studies content]
    ↓
test_prompts.json
    ↓
    [User copies test prompt, pastes into Claude]
    ↓
data/tests/[topic-id]-test.json (Test questions)
    ↓
    [User answers questions]
    ↓
evaluation_prompts.json
    ↓
    [User pastes eval prompt + test + answers into Claude]
    ↓
data/results/[topic-id]-result-[date].json (Scored result)
    ↓
plan.json (Update topic.score and topic.status)
```

---

## Usage in Web App

### Loading Data

```javascript
// Load all data files
const [plan, prompts, testPrompts, evalPrompts, schedule] = await Promise.all([
  fetch('data/plan.json').then(r => r.json()),
  fetch('data/prompts.json').then(r => r.json()),
  fetch('data/test_prompts.json').then(r => r.json()),
  fetch('data/evaluation_prompts.json').then(r => r.json()),
  fetch('data/schedule.json').then(r => r.json())
]);
```

### Displaying Topic Detail

```javascript
function displayTopicDetail(topicId) {
  // Get topic metadata from plan
  const topic = findTopicById(topicId, plan);

  // Get study prompt
  const studyPrompt = prompts[topicId];

  // Get test prompt
  const testPrompt = testPrompts[topicId];

  // Get evaluation prompt
  const evalPrompt = evalPrompts[topicId];

  // Check if study content exists
  const studyContent = await loadStudyContent(topicId);

  // Check if test exists
  const test = await loadTest(topicId);

  // Check if results exist
  const results = await loadResults(topicId);

  // Display everything
  displayTopic(topic, studyPrompt, testPrompt, evalPrompt, studyContent, test, results);
}
```

### Updating Progress

```javascript
async function updateTopicProgress(topicId, score) {
  // Load plan
  const plan = await fetch('data/plan.json').then(r => r.json());

  // Find topic
  const topic = findTopicById(topicId, plan);

  // Update
  topic.score = score;
  topic.status = score >= 70 ? 'completed' : 'in-progress';

  // Save (requires backend or manual save)
  savePlan(plan);
}
```

---

## Summary

**Total JSON Files**:
- 3 prompt files (prompts, test_prompts, evaluation_prompts)
- 1 plan file
- 1 schedule file
- 68+ generated topic content files
- 68+ generated test files
- 68+ generated result files (one per test attempt)

**Total Size**: ~1 MB of prompt files + generated content

**All files use clean, predictable JSON structures** that are easy to parse and display in a web application.
