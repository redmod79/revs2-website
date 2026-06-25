# Revelation Structure Series v2 — Investigative Methodology

*This file defines the methodology for ALL studies in the revs2-XX series. Every analysis agent MUST follow this methodology.*

## Series Overview

**Central Question:** What is the literary architecture and structural pattern system of the book of Revelation, and what does the structure reveal about the book's message?

**Method:** Each study uses `bible-study8` (five-agent pipeline: web research → references → scoping → word study generation → research → analysis with Python verification).

**Output:** 30+ studies in two parts. Part 1 (studies 01-30): structural analysis. Part 2 (studies 31+): interpretive application built on the structural findings.

**Predecessor:** This series is a condensed, upgraded version of the 47-study `revs` series. The original studies remain available as read-only reference. The structural DB is shared — revs2 extends the existing element catalog.

---

## Investigative Methodology (include verbatim in every Part 1 agent prompt)

```
INVESTIGATIVE METHODOLOGY:
- You are a structural analyst, not an advocate for any interpretive school.
- Your job is to catalog what the text contains and what patterns are observable.
- Gather structural observations from ALL angles. If a passage could support
  recapitulation, document the evidence. If it could support linear sequence,
  document that evidence too.
- Do NOT assume a structural model before examining the evidence.
- Do NOT state opinions. State what the text contains.
- Use "the text contains," "this is consistent with," "this pattern is
  validated/not validated by." Avoid "clearly proves," "obviously shows,"
  "the strongest evidence," or "must mean."
- The structural model should emerge FROM the cataloged evidence, not be
  imposed ON it.
```

## Canonical Cross-Reference Principle

When a Revelation passage is structurally ambiguous, the study MUST trace the allusion back to its OT/NT source and let the source's clearer statement govern.

**The principle:** Scripture interprets Scripture. Where Revelation alludes to a source, the source's plain statement interprets the echo.

**Examples:**
- Dan 7:17, 23 explicitly decodes beast = kingdom — resolves whether Rev 13's beast is an individual or a system
- Ezek 1:5-10 identifies the four living creatures and their faces — clarifies the throne room in Rev 4:6-8
- Zech 4:2, 10 explicitly decodes seven lamps = eyes of the LORD = "my Spirit" — resolves the identity of the seven Spirits in Rev 1:4 / 4:5 / 5:6
- Exod 25-40 provides the sanctuary blueprint — locates the altar of Rev 6:9 (outer court), the golden altar of Rev 8:3 (Holy Place), and the ark of Rev 11:19 (Most Holy Place)
- Lev 16:17 ("no man in the tabernacle") provides the explicit structural decoder for Rev 15:8
- Dan 7:9-10 (judgment seated, books opened, fire) provides the template for Rev 20:11-13

**Requirement:** Every AN-tier item must document the OT source in its own context before assessing the allusion. The source text is the interpretive key.

---

## Structural Evidence Classification System

Every structural observation falls into one of five tiers. Higher tiers are more objective; lower tiers involve more interpretation. Evidence flows upward: IC claims must be supported by SP patterns, which are built from VP/TM items.

### Tier 1: Textual Markers (TM)
Observable, verifiable structural devices in the Greek text. Both sides of any structural debate must accept these.

**What qualifies:** Word occurrences and counts, grammatical features, formulaic phrases and their distribution, structural reversals observable in the text, vocabulary presence/absence.

**Test:** Can this be verified by anyone with a Greek concordance? If yes → TM.

### Tier 2: Verbal Parallels (VP)
Shared vocabulary, phrases, or structural elements between two or more passages.

**Documentation requirement:** Each VP MUST list Passage A, Passage B, shared elements (exact words), and link count.

**Strength:** 5+ shared elements → Strong; 3-4 → Moderate; 2 → Minimal; 1 → Not VP.

### Tier 3: Structural Patterns (SP)
Claims about larger-scale patterns: chiasms, inclusios, progressions, telescoping, numerical architectures. MUST be built from multiple TM and/or VP items.

**Validation ratings:** Strong, Moderate, or Weak — based on the pattern validation criteria below.

### Tier 4: Allusion Networks (AN)
Claims that Revelation draws on specific OT source material.

**Allusion strength:** Explicit quotation → Strong allusion (3+ shared vocab + shared context) → Probable allusion (2 shared vocab + context) → Echo (1 shared element).

**OT source context check (REQUIRED):** Read the OT source in its own context before classifying.

### Tier 5: Interpretive Claims (IC)
What the structural observations mean. MUST cite supporting lower-tier items.

**Competing claims:** List both, list supporting evidence for each, assess which has stronger lower-tier support.

---

## Pattern Validation Criteria

### Chiasm Validation
**Strong:** 3+ matching pairs with 2+ verbal links each; thematically significant center; not forced; alternatives considered.
**Moderate:** Criteria 1-4 met; no strong alternative but one exists.
**Weak:** <3 pairs, or pairs rely on single links, or significant material ignored.

### Inclusio Validation
**Strong:** 3+ distinctive verbal elements shared between opening and closing.
**Moderate:** 2 distinctive verbal elements.
**Weak:** 1-2 elements or generic vocabulary.

### Progression Validation
**Strong:** Each step demonstrably intensifies; no unexplained reversals; escalation measurable.
**Moderate:** Direction clear but not all steps measurable.
**Weak:** Escalation subjective.

### Parallel Sequence Validation
**Strong:** >75% element-by-element correspondence; order matches; shared vocabulary documented; differences noted.
**Moderate:** 50-75% with order match.
**Weak:** <50% or order rearranged.

---

## Chronological Model Classification

- **Recapitulation** — evidence sequences cover overlapping time periods
- **Linear/Sequential** — evidence sequences follow chronologically
- **Telescoping** — evidence later sequences contained within earlier ones
- **Neutral** — observation does not favor any model

---

## Output Format

### CONCLUSION.md (Prose-driven — primary deliverable)

```markdown
# [Descriptive Title] (revs2-XX)

## Study Question
[Original question — copy verbatim]

## Summary Answer
[2-3 sentence direct answer]

## Key Verses
[6-12 most important verses with full KJV text]

## Analysis
[Prose sections organized by argument. Embed Greek terms, cite structural
evidence naturally. Use the canonical cross-reference principle — when
Revelation is ambiguous, cite the source passage that clarifies.]

## Word Studies
[Key Greek/Hebrew terms with Strong's numbers, occurrence counts, semantic ranges]

## Difficult Passages
[Passages where the structural evidence is ambiguous or competing readings exist]

## Conclusion
[Final synthesis. Cite structural element counts and validation ratings.
Present competing readings when they exist.]

---
*Study completed: [YYYY-MM-DD]*
```

### structural-catalog.md (Companion file — structural evidence tables)

```markdown
# Structural Catalog — revs2-XX

Elements tracked in D:/bible/bible-studies/revelation-structural.db (series='revs2').

## Textual Markers (TM)
[Also-cited prior items table + New items table]

## Verbal Parallels (VP)
[Table with Link Count and Strength]

## Structural Patterns (SP)
[Table with Validation and Chronological columns]

## OT Allusion Network (AN)
[Table with Allusion Strength]

## Interpretive Claims (IC)
[Table with Chronological model]

## Tally Summary
[Counts by tier + chronological model indicator grid]
```

---

## Structural Databases

### revelation-structural.db
**Script:** `python D:/bible/revs_structural_db.py`
**Usage:** Studies 01-30 register elements with `series='revs2'`. Use `also-in` for existing revs elements; `next-id` + `add` for new ones.

### revelation-study.db
**Script:** `python D:/bible/revs_study_db.py`
**Usage:** All studies ingested after completion.

### evidence.db (Part 2 only)
**Script:** `python D:/bible/evidence_db.py --series revs2`
**Usage:** Studies 31+ register E/N/I theological evidence.

---

## Cross-Study References

- Reference other revs2-XX studies by slug
- Reference original revs-XX studies as read-only background
- Reference 3am, etc, sanc, and other series when relevant
- Use the study DB to find prior analysis before beginning: `revs_study_db.py find-passage "Rev 8:1"`

---

## Conclusion Tone Rule (Part 1)

- Present structural findings as cataloged data
- State what validation criteria produced
- Do NOT editorialize about what results mean for interpretive schools
- Let the structural evidence and validation ratings speak for themselves
- Save interpretive conclusions for Part 2

---
*Created: 2026-06-11*
