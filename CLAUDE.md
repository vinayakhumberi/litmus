# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A static, no-build personal study tracker for FAANG Frontend Lead interview prep. Plain HTML/CSS/JS pages that fetch JSON/Markdown files from `data/` at runtime — there is no framework, bundler, package.json, or test runner. Everything is Tailwind via CDN (`<script src="https://cdn.tailwindcss.com">`) plus a few CDN libraries (marked, Prism, Mermaid).

Deployed as-is to GitHub Pages: https://vinayakhumberi.github.io/litmus/

## Commands

There is no build/lint/test tooling. To develop locally, serve the repo root over HTTP (the pages use `fetch()` against relative paths, which fails under `file://`):

```bash
python3 -m http.server 3002
```

Then open `http://localhost:3002/index.html`. Changes to HTML/JS/JSON/MD are picked up on browser refresh — watch for the browser caching `fetch()`ed JSON/MD responses; hard refresh (Cmd+Shift+R) if edits to `data/*.json` or `data/topics/*.md` don't show up.

## Page architecture

Five top-level HTML pages, each self-contained (no shared JS module/bundle):

- **`index.html`** — the tracker dashboard. Loads `data/plan.json` (topic metadata: status/score/priority) and `data/scedule.json` (calendar), cross-references them client-side in `buildTopicList()` to compute each topic's `actualWeek`, and renders a filterable/sortable table. Topics not present in any scheduled week get `actualWeek: 'deferred'` and show up under the "Deferred" filter chip.
- **`topic-detail.html`** — fetches `data/topics/{id}.md`, renders it with `marked.js`, syntax-highlights code blocks with Prism, and renders ```mermaid fenced blocks via `mermaid.render()`.
- **`test-portal.html`** — fetches a topic's test JSON and lets the user take it locally (client-side scoring/UI only).
- **`resources.html`** — lists files under `resources/`. On GitHub Pages it lists via the GitHub Contents API; locally it parses the directory-index HTML page from the dev server (so local file listing only works when serving via something that emits an `Index of /resources/` page, e.g. `python -m http.server`).
- **`resources/*.html`** — standalone reference pages, not part of the theming/routing system.

## Theming: two unrelated systems, don't mix them up

- `index.html` does **not** use Tailwind dark mode at all. It's plain CSS custom properties on `:root`, overridden by a `body.light-theme` class. Its own toggle button flips this class and writes `localStorage.theme`.
- `topic-detail.html`, `test-portal.html`, and `resources.html` use **Tailwind's `dark:` variant** and require both of these on every page, or dark styling silently falls back to the OS `prefers-color-scheme` media query instead of the site's own toggle (this exact bug was found and fixed on `resources.html` and `test-portal.html`):
  ```html
  <script>
    tailwind.config = { darkMode: 'class' }
  </script>
  ```
  and in the init script:
  ```js
  const isLight = localStorage.getItem('theme') === 'light';
  if (isLight) { document.body.classList.add('light-theme'); } else { document.documentElement.classList.add('dark'); }
  ```
  Any new Tailwind-based page must copy both pieces verbatim from `topic-detail.html`.

## Mermaid diagrams in topic content

Diagrams are read both in-app and via Safari Reader Mode, which strips the page's own CSS (including the `.mermaid-target` overrides in `topic-detail.html`) but keeps whatever the Mermaid SVG bakes in itself. Because of this:
- Never use near-black or near-white `classDef` fills — they disappear against Reader Mode's inverted background. Use mid-tone fills (Tailwind ~600/700-ish lightness) with pastel strokes and off-white (not pure `#fff`) text.
- Give every diagram its own `%%{init: {"theme": "base", "themeVariables": {...}}}%%` directive setting `lineColor`, `edgeLabelBackground`, and `textColor` explicitly — edges/arrowheads/edge-labels aren't covered by `classDef` and otherwise fall back to the page's global `mermaid.initialize({theme:'neutral'})`, which is invisible in some combinations.

## Data layer (`data/`)

`data/ReadMe.md` documents an **aspirational/older** schema (`prompts.json`, `test_prompts.json`, `evaluation_prompts.json`, `schedule.json`). The actual files on disk have different names and one has a different purpose than its name suggests:

| Actual file | Role | Notes |
|---|---|---|
| `data/plan.json` | Master list of 68 topics (id, category, difficulty, priority, status, score, tags) | Source of truth for topic metadata |
| `data/scedule.json` | Week/day calendar assigning topics to study sessions | **Typo is intentional** — `index.html` fetches this exact filename (`data/scedule.json`, not `schedule.json`). Don't "fix" the typo without updating the fetch call. |
| `data/deep-dive.json` | Per-topic **study-content generation prompt**, keyed by topic id, plain string values | Matches `ReadMe.md`'s description of `prompts.json` |
| `data/evaluation.json` | Per-topic **test-question generation prompt**, keyed by topic id, plain string values | Despite the filename, this is test-generation, not scoring/evaluation, prompts — matches `ReadMe.md`'s `test_prompts.json`. There is currently no separate evaluation/scoring-prompt file in the repo. |
| `data/topics/{id}.md` | Rendered study content, Markdown (not JSON as `ReadMe.md` describes) | Only a handful of the 68 planned topics exist as files so far; `topic-detail.html` shows "Topic Not Found" for the rest |
| `data/tests/{id}.json` | Test question set, shape `{ "test": {...} } ` | `test-portal.html` also falls back to legacy `{id}-test.json` |
| `data/results/{id}.json` | Scored test result, shape `{ "result": {...} }` | `test-portal.html` also falls back to legacy `{id}-result.json`; finishing a test in the UI offers a `{id}.json` download meant to be saved here manually |

The content pipeline is manual/human-in-the-loop, not automated: a prompt from `deep-dive.json`/`evaluation.json` is copy-pasted into a Claude chat, and the response is hand-saved into `data/topics/`, `data/tests/`, or `data/results/`. There is no script wiring these steps together.

`fix_prompts.py` at the repo root is a one-off cleanup script for `data/evaluation.json`, left over from before the repo was renamed/moved — it has a hardcoded absolute path to a different local directory (`/Users/carollucas/Desktop/Summit/data/evaluation.json`) and needs that path updated before it would run against this repo.
