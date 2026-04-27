# Voice Note Script — Daily Reflection Tree
### DeepThought Fellowship Assignment Submission

**Duration:** ~4–5 minutes  
**Tone:** Conversational, honest, reflective — not scripted-sounding  
**Instructions:** Record this as a voice note. Pause naturally between sections. You don't have to follow it word-for-word — speak in your own voice. The points in brackets are reminders of what to cover.

---

## Opening (15 seconds)

> "Hi, this is my voice note submission for the Daily Reflection Tree assignment for the DeepThought fellowship. I'll walk through how I approached the problem, how I thought about AI hallucination, and a few places where I pushed back on what the AI gave me."

---

## Part 1: How I Approached the Problem (60–75 seconds)

> "The first thing I did was read the assignment twice — not skim it, actually read it. What struck me was the line: *'The questions are the product.'* That reoriented everything. This wasn't really a coding problem. It was a question-design problem, and the code was just the delivery mechanism.

> So before I touched a JSON file or wrote any code, I spent time understanding the three psychological frameworks — Rotter's locus of control, Organ's organizational citizenship behavior, and Maslow's self-transcendence. I wanted to know the *original* ideas, not just blog summaries, because I knew those would show in the quality of the questions.

> Then I drew the tree on paper first — literally sketched out who enters what kind of day, what question they'd face, how that answer would shape the next one. Walking through it as if I was a tired employee at 7pm. Would I actually stop to think at this question? Or would I just click through?

> The structure I landed on uses two kinds of routing — answer-based for the opening branch, and signal-accumulation for the reflection selection — because no single question should define your axis. The pattern across two answers is more honest than one snap response."

---

## Part 2: How I Controlled AI Hallucination (60 seconds)

> "The assignment has a really elegant built-in hallucination guardrail: the product is deterministic. The LLM is only involved in *building* the tree — designing questions, testing options, iterating on language — not in running it. So at runtime, there's literally nothing to hallucinate. The employee always gets the same path for the same answers.

> But within the design process, I was deliberate about not letting the AI write the questions wholesale. I used AI to test my questions — asking it to roleplay as a frustrated employee, or a self-aware one, and see if the options felt authentic. I also used it to push back: *'Would a real person distinguish between option B and C here?'* or *'Does this reflection feel preachy?'*

> Where I was most careful: the reflection nodes. LLMs default to motivational-poster language. I kept asking: *'Does this sound like a wise colleague, or a self-help chatbot?'* And I revised until the reflections felt quiet and honest rather than energetic and performed."

---

## Part 3: Where I Disagreed with the AI (45–60 seconds)

> "A few specific places where I pushed back.

> First — the summary. The AI initially wanted a score: 'You scored 4/6 on agency.' I rejected that immediately. Scoring reflection is the fastest way to make it feel like a performance review instead of a genuine moment of self-awareness. The assignment guidelines said no moralizing, and a score is the most moralistic thing you can do. I replaced it with a pattern label and a tailored paragraph.

> Second — the Axis 2 reflection for the entitlement path. The AI's first draft was basically: *'You focused on what you deserved. Next time, try giving more.'* That's a lecture, not a reflection. I rewrote it to ask a question instead — *'If you picture those interactions from the other side, what would they have seen? Not for guilt — just to see the full picture.'* That reframe came from me, not the AI.

> Third — the number of options per question. The AI kept wanting to give five options. I trimmed most questions to four because five options on a tired evening invites decision fatigue and clicking randomly."

---

## Part 4: My Negative Prompting Strategy (30–40 seconds)

> "Negative prompting was mostly about tone. I used phrases like:

> *'Don't sound like a self-help book. Don't use the word journey. Don't use motivational language. Don't grade or score the user. Don't suggest the employee is broken and needs fixing.'*

> And structurally: *'Don't add free-text input fields. Don't suggest anything that requires an API call at runtime. Don't add more than four options — if you have five, combine two.'*

> The constraint I kept returning to was the assignment's own language: *'a wise colleague — not a therapist, not a manager, not a motivational poster.'* I used that as a litmus test every time I evaluated generated text."

---

## Part 5: How I Aligned with the Assignment Guidelines (30–40 seconds)

> "The three things the assignment was really testing, as I read it, were: structural thinking, psychological grounding, and AI fluency without AI dependency.

> For structure — every path is traceable in the JSON without running any code. The tree has 26 nodes, all references validated programmatically.

> For psychological grounding — I tied each question directly back to a source. The options on A1_Q_HIGH, for example, are directly informed by Dweck's distinction between attributing success to effort versus luck.

> For the AI fluency piece — I built the agent in Python that actually loads the JSON and walks the tree. But I also built a web UI, which felt important because the target users are employees on a workday evening. A CLI is not the experience; a browser is.

> I think the most honest version of this submission is: I used AI heavily as a design partner, and kept authorship of every decision. The questions are mine. The tree structure is mine. The tone is mine."

---

## Closing (10 seconds)

> "That's my submission. Happy to answer questions. Looking forward to hearing from you."

---
