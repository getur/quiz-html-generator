---
name: quiz-html-generator
description: >
  Trigger when the user asks to create, generate, or build an interactive quiz HTML
  file from structured data. Accepts input as JSON, Markdown, Excel/CSV, DOCX, or PDF
  and produces a standalone HTML file with flip-cards, progress bar, audio replay,
  character avatar, splash screen, and result screen — matching the Duolingo-style
  "Programa Geração BIZ" template. Use whenever the user provides a quiz data source
  (file path, pasted content, spreadsheet) and wants a ready-to-use interactive HTML output.
license: MIT
compatibility: opencode
metadata:
  source: custom
---

# Quiz HTML Generator

Generates a standalone, interactive HTML quiz file from structured data (JSON,
Markdown, Excel/CSV, DOCX, PDF). The output is a complete self-contained HTML file
with Duolingo-style design: splash screen, progress bar, character + speech bubble
with audio replay, flip-card grid, result screen, and popup instructions.

## CRITICAL: How to Generate the HTML

**DO NOT redesign or create a new HTML from scratch.** Follow these steps exactly:

1. Read `assets/template.html` using the Read tool.
2. **Copy the entire file content** — this is your starting point.
3. **Only modify** these specific parts:
   - `<title>` tag text
   - `.splash-title` heading text
   - `.splash-sub` subtitle paragraph text
   - `.splash-objectives` list items (`<li>`)
   - The `allQuestions` JavaScript array (replace entirely with parsed data)
4. **Do NOT change any CSS, HTML structure, class names, IDs, or JavaScript logic.**
   - Keep `--duo-*` CSS variables exactly as they are
   - Keep `.card-flippable`, `.card-inner`, `.card-front`, `.card-back` classes
   - Keep `#splash`, `#game`, `#result`, `#popup`, `#progress-fill`, `#question-text` IDs
   - Keep the Fredoka One + Nunito font imports
5. Save the result to the current working directory.

## Data Schema (allQuestions Array)

The template expects this exact JavaScript structure:

```javascript
const allQuestions = [
  {
    id: "q1",                    // unique string identifier per question
    question: "Pergunta aqui...",  // the question text shown in speech bubble
    audioquestao: "data:audio/mp3;base64,...",  // optional base64 audio for question
    cards: [
      {
        id: "c1",                 // unique string per card within question
        title: "Título da carta",  // card front title (bold, centered)
        explanation: "Explicação...", // shown on card back after flip
        image: "data:image/png;base64,...", // optional base64 image on card front
        audio_resposta: "data:audio/mp3;base64,...", // optional base64 audio for explanation
        explanationaudio: "data:audio/mp3;base64,..." // alias for audio_resposta
      }
    ],
    correctCardIds: ["c1"]        // array of card IDs that are correct
  }
]
```

## Input Format Handling

### JSON
If input has `isCorrect: true/false` per card, transform it:

```javascript
// Input:
{ "question": "...", "cards": [
  { "title": "A", "explanation": "..", "isCorrect": true },
  { "title": "B", "explanation": "..", "isCorrect": false }
]}

// Output allQuestions entry:
{
  id: "q1",
  question: "...",
  cards: [
    { id: "c1", title: "A", explanation: ".." },
    { id: "c2", title: "B", explanation: ".." }
  ],
  correctCardIds: ["c1"]  // only cards where isCorrect === true
}
```

Map alternate field names: `answerOptions` → `cards`, `correctId` → `correctCardIds`,
`text` → `title`, `description` → `explanation`.

### Markdown
Parse headings as questions, list items as cards:

```markdown
# Question text here
- **Card Title**: Explanation [correct]
- **Card Title B**: Explanation
```

`[correct]` or `[✓]` after a card marks it as correct. Omit all media fields.

### Excel/CSV
Columns: `question`,`card_title`,`card_explanation`,`is_correct` (yes/no/true/false/1/0).
Group rows by question text. Omit media columns if not present.

### DOCX/PDF
Extract text, parse as Markdown-like structure. If ambiguous, ask user.

## Media (Base64) Policy

- **Only include base64** if source already has `data:image/...` or `data:audio/...` URIs.
- If source has URLs (http/https to images/audio), strip them entirely.
- If no media in source, omit `image`, `audioquestao`, `audio_resposta` fields.
- The template handles missing media gracefully — `btn-replay` is hidden when no audio, card images are just absent.

## Title and Branding

- Quiz title = input filename without extension (e.g., `climate-change.json` → `Climate Change`).
- Set the title in these template locations:
  - `<title>` tag
  - `.splash-title` heading
  - `.splash-sub` subtitle
  - `.splash-objectives` list items (generic or derived from data)
- Keep `.topbar-brand` as-is ("📘 Quiz<span> Geração BIZ</span>").

## Output

- Save to **current working directory**.
- File name: `<input-filename-without-ext>.html`.
- Fully standalone: all CSS/JS inline, only external dep is Google Fonts `<link>`.

## Verification Checklist

After generating, verify the output contains ALL of these (search for them):
- `--duo-green` CSS variable
- `Fredoka+One` in font URL
- `class="card-flippable"`
- `class="card-front"` and `class="card-back"`
- `id="splash"` section with start button
- `id="progress-fill"` and `id="progress-text"`
- `class="avatar-wrap"` and `class="speech-bubble"`
- `id="result"` section with `id="percent"` and `id="score-detail"`
- `const allQuestions = [` with correct number of questions
- `<title>` matches filename

If any are missing, fix the output before saving.
