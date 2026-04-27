# Daily Reflection Tree — DeepThought Fellowship Assignment

A deterministic end-of-day reflection tool built as a structured decision tree. No LLMs at runtime. Same answers always produce the same conversation.

---

## Repository Structure

```
/tree/
  reflection-tree.json      ← Part A: the full 26-node tree (readable as data)
  tree-diagram.md           ← Part A: Mermaid flowchart + path table

/agent/
  agent.py                  ← Part B: Python CLI walker (no dependencies)

/transcripts/
  persona-1-transcript.md   ← Victor / Contribution / Altrocentric path
  persona-2-transcript.md   ← Victim / Entitlement / Self-Centric path

index.html                  ← Part B (bonus): browser-based web UI
write-up.md                 ← Part A: design rationale (2 pages)
voice_note_script.md        ← Script for the required voice note submission
requirements.txt            ← No dependencies (Python stdlib only)
README.md                   ← This file
```

---

## Reading the Tree (Part A)

Open `tree/reflection-tree.json`. Every possible conversation path can be traced by following the `next` fields and `routes` arrays without running any code.

**Node types:**

| Type | User sees? | Behavior |
|------|-----------|----------|
| `start` | Yes | Auto-advances after greeting |
| `question` | Yes | Employee picks one of 3–4 fixed options |
| `decision` | No | Routes based on prior answer or accumulated signals |
| `reflection` | Yes | Employee reads insight, presses Continue |
| `bridge` | Yes | Axis transition text, auto-advances |
| `summary` | Yes | Synthesized end-of-session reflection |
| `end` | Yes | Closes session |

**Signal accumulation:** Each option on a question node has an optional `signal` field (e.g., `"axis1:internal"`). The agent tallies these per axis. Decision nodes route based on whichever pole has accumulated more signals.

**Interpolation:** Text fields like `"You said \"{A1_OPEN}\""` are filled at runtime by looking up the stored answer for that node ID. No LLM is involved — it's a dictionary lookup.

**8 unique paths:** The tree has 3 binary axes, producing 8 distinct conversation outcomes, each with a unique `summary_reflection` in the top-level `summary_reflections` map.

---

## Running the Agent (Part B)

**Requirements:** Python 3.8+, no external libraries.

```bash
# From the repository root:
python agent/agent.py

# Or specify a custom tree path:
python agent/agent.py tree/reflection-tree.json
```

The agent:
1. Loads the tree from the JSON file (not hardcoded in source)
2. Renders each node to the terminal
3. Waits for numbered input at `question` nodes
4. Auto-advances at `start`, `bridge`, and `decision` nodes
5. Accumulates signals from each answer
6. Interpolates earlier answers into reflection text
7. Produces a personalized summary based on the path taken

---

## Running the Web UI (Bonus)

Open `index.html` in a browser — but since it fetches `tree/reflection-tree.json`, you need a local server:

```bash
# From the repository root:
python -m http.server 8000
# Then open: http://localhost:8000
```

Features: animated card transitions, axis progress bar, per-axis score visualization in the summary, mobile-responsive, no dependencies.

---

## The Three Axes

| Axis | Spectrum | Psychology |
|------|----------|------------|
| **Locus** | Victim ↔ Victor | Rotter (1954) Locus of Control + Dweck (2006) Growth Mindset |
| **Orientation** | Entitlement ↔ Contribution | Campbell et al. (2004) + Organ (1988) OCB |
| **Radius** | Self-Centric ↔ Altrocentric | Maslow (1969) Self-Transcendence + Batson (2011) Perspective-Taking |

---

## Key Design Decisions

- **No free text.** Every question has fixed options. This forces the designer to encode the spectrum — which is where the real work is.
- **Two-layer routing.** Simple answer-based routing for the opening question; signal-accumulation routing for reflection selection. This prevents a single outlier answer from driving the entire conversation.
- **No moralizing.** Both ends of every spectrum receive a non-judgmental reflection. The "external/entitlement/self" path does not shame — it opens a door.
- **Axes are connected.** Bridge nodes explicitly link the insight from one axis to the question of the next, making this feel like a conversation, not three separate quizzes.
