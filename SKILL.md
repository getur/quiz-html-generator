---
name: quiz-html-generator
description: >
  Trigger when the user asks to create, generate, or build an interactive quiz HTML
  file from structured data. Accepts input as JSON, Markdown, Excel/CSV, DOCX, or PDF
  and produces a standalone HTML file with 8 question types (MCQ, Multi-Select,
  True/False, Fill-in-the-Blank, Matching, Sequencing, Numeric, Flash Card),
  progress bar, lives system, XP/streak tracking, audio replay, splash screen,
  and result screen with confetti — matching the MAZA dark theme template.
  Use whenever the user provides a quiz data source (file path, pasted content,
  spreadsheet) and wants a ready-to-use interactive HTML output.
license: MIT
compatibility: opencode
metadata:
  source: custom
---

# Quiz HTML Generator

Generates a standalone, interactive HTML quiz file from structured data (JSON,
Markdown, Excel/CSV, DOCX, PDF). The output is a complete self-contained HTML file
with a dark MAZA-style design: splash screen, progress bar, 3 lives (hearts),
XP/streak system, 8 question types, audio replay, and result screen with confetti.

## Supported Question Types

The template supports **8 question types** via the `type` field:

| Type              | `type` value      | Description |
|-------------------|-------------------|-------------|
| MCQ               | `mcq`             | Single-choice, tap-to-select cards |
| Multi-Select      | `multi-select`    | Pick multiple correct answers (partial credit shown) |
| True/False        | `true-false`      | Two large buttons: Verdadeiro / Falso |
| Fill-in-the-Blank | `fill-blank`      | Type or drag tiles into blanks; near-miss detection via Levenshtein |
| Matching          | `matching`        | Pair left/right items by clicking each side |
| Sequencing        | `sequencing`      | Drag-and-drop reorder items |
| Numeric           | `numeric`         | Enter a number with tolerance and unit; near-miss feedback |
| Flash Card        | `flashcard`       | Flip cards to reveal answer, then select one |

## CRITICAL: How to Generate the HTML — Optimized Reading Strategy

**DO NOT read the entire template.html file.** It is ~2500 lines. Instead, read only what you need:

### Step 1: Parse input data → determine which question types are used
Read the input file, parse all questions, and extract the set of `type` values used (e.g. `mcq`, `matching`, `numeric`).

### Step 2: Read template skeleton (lines 1–60)
Read `assets/template.html` from line 1 to 60 to get `<head>`, CSS variables, body setup, and the screen structure (`.screen` classes, welcome/quiz/results/loading screens, progress bar, feedback banner, buttons, modals).

### Step 3: Read only the CSS for the question types you need
The template has CSS sections for each type. Read only the needed ranges:

| Type              | CSS lines |
|-------------------|-----------|
| MCQ               | 530–545   |
| Multi-Select      | 545–560   |
| True/False        | 560–575   |
| Fill-in-the-Blank | 575–620   |
| Matching          | 620–670   |
| Sequencing        | 670–710   |
| Numeric           | 710–740   |
| Flash Card        | 740–770   |
| Results & Confetti| 770–820   |
| Common/General    | 820–880   |

Read each range only if that type appears in your data. Always read Results & Confetti and Common/General sections.

### Step 4: Read only the JS functions for the question types you need
The template has render and submit functions for each type:

| Function(s)              | Lines       | Used by |
|--------------------------|-------------|---------|
| `renderMCQ`, `submitMCQ` | ~1420–1500  | mcq     |
| `renderFlashcard`, `submitFlashcard` | ~1500–1610  | flashcard |
| `renderMultiSelect`, `submitMultiSelect` | ~1610–1680  | multi-select |
| `renderTF`, `submitTF`   | ~1680–1760  | true-false |
| `renderFillBlank`, `submitFillBlank` | ~1760–1910  | fill-blank |
| `renderMatching`, `selectMatch`, `checkMatchingComplete` | ~1910–2050  | matching |
| `renderSequencing`, `submitSequencing` | ~2050–2170  | sequencing |
| `renderNumeric`, `submitNumeric` | ~2170–2250  | numeric |
| `handleAnswer`           | ~2260–2340  | always needed |
| `nextQuestion`           | ~2340–2370  | always needed |
| `showResults`            | ~2370–2400  | always needed |
| `launchConfetti`         | ~2400–2440  | always needed |

Read only the render/submit functions for the types in your data. Always read `handleAnswer`, `nextQuestion`, `showResults`, `launchConfetti`.

### Step 5: Assemble the final HTML
- Start with the skeleton (Step 2)
- Append the CSS sections for your types (Step 3)
- Append the common CSS (media queries, scrollbar, confetti canvas)
- Append the HTML body (the static screens, modals, buttons)
- Append the JS: global vars, helper functions, question data, and the specific render/submit functions for your types (Step 4)
- Replace placeholder data with your parsed quiz data

### Editing Guidelines
- **Do NOT change** CSS class names, HTML structure, IDs, or JS logic
- Keep `--clr-*` CSS variables exactly as they are
- Keep all Tabler Icons imports
- Only modify: `<title>`, `.welcome-title`, `.welcome-sub`, `const quizData = { ... }`
- Save to current working directory as `<input-filename-without-ext>.html`

## Data Schema (quizData Object)

The template expects this exact JavaScript structure:

```javascript
const quizData = {
  quiz_title: "Quiz Title",
  language: "pt-PT",
  total_questions: 10,
  questions: [
    // ... question objects (see below)
  ]
};
```

### Common fields (all question types):

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier (e.g. `"q1"`) |
| `type` | string | One of: `mcq`, `multi-select`, `true-false`, `fill-blank`, `matching`, `sequencing`, `numeric`, `flashcard` |
| `question` | string | The question text displayed in the question card |
| `audioquestao` | string | Optional base64 audio for question replay (omit if none) |
| `points` | number | XP earned when answered correctly (default 10) |
| `explanation` | string | Feedback text shown after answering |

**⚠️ CRITICAL: Do NOT add or modify `instructions` or `instructions_audio` fields.** These are pre-defined per question type in the template and must remain untouched. Omit them entirely from generated quiz data — the template handles default instructions via the Instructions button.

### MCQ (`type: "mcq"`) & Multi-Select (`type: "multi-select"`)

```javascript
{
  id: "q1",
  type: "mcq",           // or "multi-select"
  question: "Pergunta aqui...",
  audioquestao: "",       // optional base64 audio
  cards: [
    {
      id: "c1",
      title: "Título da carta",
      explanation: "Explicação...",
      image: ""           // optional base64 image
    }
  ],
  correctCardIds: ["c1"], // array of correct card IDs
  points: 10,
  explanation: "Texto de feedback..."
}
```

- For **MCQ**: user picks exactly one card. Only one `correctCardIds` entry should match.
- For **Multi-Select**: user picks multiple. Partial credit shown if some correct answers selected.
- `cards[].image`: optional `data:image/...` base64 URI (omit if none).
- `cards[].audio_resposta`: optional base64 audio for the card's explanation.
- `cards[].explanationaudio`: alias for `audio_resposta`.

### True/False (`type: "true-false"`)

```javascript
{
  id: "q2",
  type: "true-false",
  question: "A Terra é o terceiro planeta mais próximo do Sol.",
  audioquestao: "",
  cards: [],               // must be empty array
  correctAnswer: true,     // boolean: true or false
  explanation: "Verdadeiro! ...",
  points: 10
}
```

### Fill-in-the-Blank (`type: "fill-blank"`)

```javascript
{
  id: "q3",
  type: "fill-blank",
  question: "Completa a frase:",
  audioquestao: "",
  sentence: "O {0} é o maior oceano do mundo.",  // {0} = first blank, {1} = second, etc.
  blanks: [
    {
      id: "b1",
      answer: "Pacífico",                    // exact answer
      accept: ["Pacífico", "Oceano Pacífico"], // optional accepted variants
      hint: "Começa com P e termina com o"    // optional hint (not shown in UI)
    }
  ],
  tiles: ["Pacífico", "Atlântico", "Índico", "Ártico"], // draggable/clickable tile options
  explanation: "O Oceano Pacífico é o maior...",
  points: 12
}
```

- `sentence` uses `{0}`, `{1}`, etc. as placeholders mapped to `blanks` array by index.
- `tiles` is optional — if provided, users can drag/click tiles into blanks.
- Near-miss detection (Levenshtein distance ≤ 2) shows a "🤏 Quase!" warning.
- Omit `tiles` for pure text-input blanks.

### Matching (`type: "matching"`)

```javascript
{
  id: "q4",
  type: "matching",
  question: "Associa cada continente ao seu país:",
  audioquestao: "",
  left: [
    { id: "l1", text: "Europa" },
    { id: "l2", text: "África" }
  ],
  right: [
    { id: "r1", text: "França", matchId: "l1" },  // matchId links to left item's id
    { id: "r2", text: "Quénia", matchId: "l2" }
  ],
  explanation: "...",
  points: 15
}
```

- User clicks a left item, then a right item to create a pair.
- All pairs must be matched before evaluation.
- `right[].matchId` must match a `left[].id` value.

### Sequencing (`type: "sequencing"`)

```javascript
{
  id: "q5",
  type: "sequencing",
  question: "Ordena os planetas do mais próximo ao mais distante do Sol:",
  audioquestao: "",
  items: [
    { id: "s1", text: "Mercúrio", correctPosition: 0 },
    { id: "s2", text: "Vénus",   correctPosition: 1 },
    { id: "s3", text: "Terra",   correctPosition: 2 }
  ],
  explanation: "...",
  points: 15
}
```

- `items` are shuffled randomly on render.
- User drag-and-drop reorders items.
- `correctPosition` is 0-based index of the correct position.

### Numeric (`type: "numeric"`)

```javascript
{
  id: "q6",
  type: "numeric",
  question: "Qual é a velocidade da luz no vácuo?",
  audioquestao: "",
  answer: 299792458,
  tolerance: 1000,          // ± acceptable deviation
  unit: "m/s",              // optional unit label
  hint: "Aproximadamente 300 milhões de metros por segundo.",  // optional hint
  explanation: "A velocidade da luz...",
  points: 12
}
```

- User types a numeric value.
- `tolerance` defines acceptable range (`|user - answer| ≤ tolerance`).
- Near-miss = within 3× tolerance (shows a hint with the exact answer).
- `unit` is displayed next to the input field.

### Flash Card (`type: "flashcard"`)

```javascript
{
  id: "q7",
  type: "flashcard",
  question: "Qual destes é um método contraceptivo de barreira?",
  audioquestao: "",
  cards: [
    {
      id: "c1",
      front: "Preservativo",
      back: "O preservativo (masculino ou feminino) é um método de barreira...",
      image: ""            // optional base64 image
    }
  ],
  correctCardIds: ["c1"],
  points: 10
}
```

- Cards start showing the `front` text.
- User taps/toggles a card to flip it and see the `back`.
- User clicks "Selecionar" on the card they believe is correct.
- Then clicks "Verificar" to submit.

## Input Format Handling

### JSON
If input has `isCorrect: true/false` per card, transform it:

```javascript
// Input:
{ "question": "...", "cards": [
  { "title": "A", "explanation": "..", "isCorrect": true },
  { "title": "B", "explanation": "..", "isCorrect": false }
]}

// Output for MCQ (type: "mcq"):
{
  id: "q1",
  type: "mcq",
  question: "...",
  cards: [
    { id: "c1", title: "A", explanation: ".." },
    { id: "c2", title: "B", explanation: ".." }
  ],
  correctCardIds: ["c1"]
}
```

Map alternate field names:
- `answerOptions` → `cards`
- `correctId` / `correctAnswerId` → `correctCardIds`
- `text` → `title`
- `description` → `explanation`
- `imageUrl` / `image` → `image`
- `questionAudio` / `audio` → `audioquestao`
- `answerAudio` / `explanationAudio` → `audio_resposta`

### Inferred question types
If input does not specify a `type` field, **infer it from structure**:

| Input structure | Inferred type |
|----------------|---------------|
| `correctCardIds` array with single ID | `mcq` |
| `correctCardIds` array with multiple IDs | `multi-select` |
| `correctAnswer` boolean field | `true-false` |
| `sentence` field | `fill-blank` |
| `left` and `right` arrays | `matching` |
| `items` array with `correctPosition` | `sequencing` |
| `answer` number field | `numeric` |
| `cards` with `front`/`back` fields | `flashcard` |

### Markdown
Parse headings as questions. Use sub-syntax per type:

```markdown
# MCQ question
- **Card Title**: Explanation [correct]
- **Card Title B**: Explanation

## True/False question
- Correct: true / false
- Explanation: ...

## Fill in the blank: The {0} is the largest ocean
- [Pacífico] [Atlântico] [Índico] [Ártico]
- Answer: Pacífico
- Accept: Pacífico, Oceano Pacífico

## Matching question
- Left: Europa → Right: França (l1)
- Left: África → Right: Quénia (l2)

## Sequencing question
- Mercúrio (0), Vénus (1), Terra (2)

## Numeric question
- Answer: 299792458
- Tolerance: 1000
- Unit: m/s
```

`[correct]` or `[✓]` after a card marks it as correct. Omit all media fields.

### Excel/CSV
Common columns: `question`, `card_title`, `card_explanation`, `is_correct` (yes/no/true/false/1/0).
Group rows by question text.

For type-specific CSV formats:
- **fill-blank**: columns `question`, `sentence`, `blanks_json` (JSON string), `tiles_json` (comma-separated), `explanation`
- **matching**: columns `question`, `left_text`, `right_text`, `match_id`, `explanation`
- **sequencing**: columns `question`, `item_text`, `correct_position`, `explanation`
- **numeric**: columns `question`, `answer` (number), `tolerance`, `unit`, `hint`, `explanation`
- **true-false**: columns `question`, `correct_answer` (TRUE/FALSE), `explanation`

If a question type cannot be determined from the data, default to **MCQ**.

### DOCX/PDF
Extract text, parse as Markdown-like structure. If ambiguous, ask user.

## Media (Base64) Policy

- **Only include base64** if source already has `data:image/...` or `data:audio/...` URIs.
- If source has URLs (http/https to images/audio), strip them entirely.
- If no media in source, omit `image`, `audioquestao`, `audio_resposta` fields.
- The template handles missing media gracefully — audio buttons are hidden when no audio, images are just absent.

## Title and Branding

- Quiz title = input filename without extension (e.g., `climate-change.json` → `Climate Change`).
- Set the title in these template locations:
  - `<title>` tag
  - `quizData.quiz_title`
  - `.welcome-title` heading (keep the `<span>` around the second word for color)
  - `.welcome-sub` subtitle paragraph
- Keep the welcome logo gradient as-is (blue → emerald).

## Output

- Save to **current working directory**.
- File name: `<input-filename-without-ext>.html`.
- Fully standalone: all CSS/JS inline, only external deps are Google Fonts `<link>` and Tabler Icons `<link>`.

## Quality Standards Reference

Before generating the quiz, read `references/Quality Standards - Quiz Source.md` and apply these mandatory rules:

### Spelling & Language (Section 4)
- Use **pre-1990 Mozambican Portuguese** spelling (e.g. "correcto", "acção", "óptimo", "adopção")
- No Brazilian Portuguese, no post-1990 European Portuguese
- Consistent terminology, tone and register across all questions and feedback

### Answer Options (Section 6)
- **At least 4 answer options** per MCQ/multi-select question to reduce guessing
- True/False questions are exempt (they only have 2 options)

### Assessment Levels (Section 4)
- Questions must span **Recall, Understanding, and Application** levels
- Do NOT use only basic recall questions

### Answer Verdict & Explanations (Section 4)
- Each answer must show **correct/incorrect** immediately, both as **written text and spoken narration**
- Provide a written + spoken explanation after each question (not just correct/incorrect)

### Audio Requirements (Section 5)
- All audio must be **pre-recorded**, embedded as base64 — **do NOT use Web Speech API or device-generated speech**
- Instruction screens must include both written text and audio narration with a play button

### Offline & Deliverable (Section 5)
- Quiz must work fully offline — all assets embedded as base64
- Single self-contained HTML file with descriptive name (not `index.html`)

### Navigation & Accessibility (Section 5)
- Clear Next/Back buttons and instructions on every screen
- Large clickable areas and buttons. High contrast text.
- Alt text on all images and icons

### Curriculum Alignment (Section 4)
- Each question should link to a specific learning outcome
- Questions must not contradict each other
- No time-based penalties — learners answer at their own pace

## Verification Checklist

After generating, verify the output contains ALL of these (search for them):
- `--clr-midnight` CSS variable
- `Inter` in font URL
- `@tabler/icons-webfont` in stylesheet link
- `class="screen"` with `#screen-welcome`, `#screen-quiz`, `#screen-results`, `#screen-loading`
- `class="question-card"` with `#question-text`
- `class="feedback-banner"` with `#feedback-banner`
- `class="btn-primary btn-next"` with `#btn-next`
- `const quizData = {` with correct number of questions in `quizData.total_questions` and `quizData.questions.length`
- `<title>` matches filename
- At least one question object with a valid `type` field from the 8 supported types
- Each question has all required fields for its type (see schemas above)
- Correct fields present for each type:
  - **mcq/multi-select**: `cards[]`, `correctCardIds[]`
  - **true-false**: `correctAnswer` (boolean)
  - **fill-blank**: `sentence`, `blanks[]`, optionally `tiles[]`
  - **matching**: `left[]`, `right[]` with `matchId`
  - **sequencing**: `items[]` with `correctPosition`
  - **numeric**: `answer` (number), `tolerance`, optionally `unit`, `hint`
  - **flashcard**: `cards[]` with `front`/`back`, `correctCardIds[]`

If any are missing, fix the output before saving.
