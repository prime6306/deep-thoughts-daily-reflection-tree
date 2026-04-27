# Write-Up: Daily Reflection Tree — Design Rationale

**Author:** DeepThought Fellowship Candidate  
**Assignment:** The Daily Reflection Tree (Part A)

---

## Why These Specific Questions

The hardest part of this assignment was not the tree structure — it was writing questions that a tired employee at 7pm would actually stop to think about, rather than click through to escape.

My first drafts were clinical: "Rate your locus of control today on a scale of 1–4." These failed immediately. Rotter's original insight is that locus of control is often *invisible to the person holding it* — someone with an external locus doesn't think "I have an external locus"; they think "things keep happening to me." So the questions had to surface the behavior, not label the concept.

**For Axis 1 (Locus),** the opening question "How would you describe today in one word?" serves two purposes. First, it warms the employee up with a low-stakes choice. Second, the answer acts as an anchor — subsequent questions can reference it ("You said 'Frustrating'..."), which personalizes the conversation and forces the employee to reckon with their own framing. The follow-up questions then ask about *what they did* when things went well or poorly, not how they felt — because behavior is more traceable than emotion.

**For Axis 2 (Orientation),** the challenge was making entitlement visible without making the employee feel accused. Campbell et al. note that psychological entitlement is ego-syntonic — it feels justified from the inside. So rather than asking "Were you entitled today?", the questions ask about what was *on your mind* in interactions and what was *underneath* acts of helping. The option "I wondered if it would be noticed or remembered" is the key — most employees have had this thought and will recognize it honestly.

**For Axis 3 (Radius),** Maslow's self-transcendence paper (1969) argues that the healthiest humans move from "what do I need?" to "what does the world need from me?" The progression in A3_OPEN's options — from "Mine" to "My team" to "A specific colleague" to "Customers" — mirrors this spectrum. The follow-up questions then test whether the awareness was cognitive only or actually changed behavior, which is Batson's distinction between perspective-taking as a thought experiment versus as a driver of action.

---

## Branching Design and Trade-offs

### The Two-Layer Routing Model

The tree uses two kinds of branching:

1. **Answer-based routing** (node A1_D0): The opening question routes directly to different Axis 1 follow-ups based on whether the day was described positively or negatively. This felt honest — a productive day and a frustrating day call for different first questions. Asking someone who had a "Productive" day "When things got hard, what did you do?" is a non-sequitur.

2. **Signal-accumulation routing** (nodes A1_D1, A2_D1, A3_D1): Each question node emits signals that are tallied across the axis. The decision node routes based on which pole has the higher total, not a single answer. This models the psychological reality that locus of control is not a single choice — it's a pattern. An employee might answer one question internally and another externally; the tree synthesizes across them.

### Trade-off: Depth vs. Branching

I chose to give each axis two questions per path (opening + axis-specific question + shared follow-up) rather than deeply branching within an axis. The alternative — branching at every question — would produce 4–8 paths per axis and require 50+ nodes to cover well. More importantly, deeper branching would risk making some paths feel much shorter than others, creating an inconsistent experience. The current design gives every employee roughly the same number of questions regardless of their path.

### Trade-off: The Shared A1_Q2 and A2_Q2

Both Axis 1 and Axis 2 converge their two branches to a shared final question before the decision node. This was deliberate. Having already answered the branch-specific question, the employee arrives at A1_Q2 with some self-awareness built up. The shared question ("When you replay today, which feels most honest?") then tests whether they can hold that awareness under a more direct prompt. The branching happens after, not before.

---

## Psychological Sources and How They Shaped Decisions

| Source | Key Insight Used | Where It Appears |
|--------|-----------------|------------------|
| Rotter (1954), Locus of Control | Behavior under adversity reveals locus more than self-report | A1_Q_LOW options: "waiting for situation to change" vs "looking for what I could control" |
| Dweck (2006), Growth Mindset | Fixed-mindset thinkers attribute success to talent/luck, not effort | A1_Q_HIGH option: "Things happened to fall into place — I got fortunate" as the external signal |
| Organ (1988), OCB | Discretionary citizenship is defined by *not* expecting reward | A2_Q2 option: "They needed it, so I helped — simple as that" as the cleanest contribution signal |
| Campbell et al. (2004), Entitlement | Entitlement is ego-syntonic; must be surfaced indirectly | A2_OPEN: asking what was *on your mind* rather than labeling the person |
| Maslow (1969), Self-Transcendence | The spectrum runs from self-referential to world-referential | A3_OPEN options ordered from narrowest (Mine) to widest (Customers) radius |
| Batson (2011), Perspective-Taking | The value is in action, not just empathy as thought | A3_Q_ALTO: "Did that awareness *change what you did*?" |

---

## What I Would Improve with More Time

**1. Cross-axis interpolation.** The current tree treats each axis as independent. But someone who showed strong internal locus (Axis 1) yet scores highly entitlement (Axis 2) is a particularly interesting pattern — they believe in their own agency but orient it toward receiving rather than giving. A richer tree would exploit these cross-axis tensions, surfacing them in the reflection text. The JSON structure supports this (signals are accumulated per axis throughout), but the reflection nodes don't yet use cross-axis conditions.

**2. Richer summary variations.** There are currently 8 summary reflection keys (2³ combinations). With cross-axis conditions, you could have weighted summaries that call out specific patterns — e.g., "high agency + entitlement" versus "low agency + contribution" tell very different stories about a person's growth trajectory.

**3. Temporal continuity.** The most powerful version of this tool would track an employee across multiple sessions and show them their pattern over time: "This is the third day this week you described as 'Frustrating'." The tree structure already supports this — every answer is stored by node ID — but it would require a persistence layer outside the tree itself.

**4. Tone calibration for different use cases.** The current tone is calibrated for a knowledge-worker in a collaborative team setting. A different deployment context (e.g., a sales team, a healthcare worker, a student) would need different examples baked into the options. The tree structure and axis design would remain the same; only the option text would need to change.

---

*Total nodes: 26 | Question nodes: 11 | Decision nodes: 4 | Reflection nodes: 6 | Bridge nodes: 2 | Summary: 1 | End: 1*
