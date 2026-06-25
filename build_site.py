#!/usr/bin/env python3
"""
build_site.py — Build the Revelation's Architecture (revs2) website.

Scans D:/bible/bible-studies/revs2-* for all 40 studies,
copies files into docs/studies/, generates mkdocs.yml and index.md,
and copies shared assets from etc-website.
"""

import os
import re
import shutil
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent
STUDIES_SRC = Path("D:/bible/bible-studies")
ETC_WEBSITE = Path("D:/bible/etc-website")
DOCS = PROJECT_ROOT / "docs"
DOCS_STUDIES = DOCS / "studies"

# ── Study metadata ─────────────────────────────────────────────────
SHORT_TITLES = {
    "revs2-01": "Structural Markers",
    "revs2-02": "Structural Key & Frame",
    "revs2-03": "Throne Room Anchor",
    "revs2-04": "Babylon-Bride Mirror",
    "revs2-05": "Structural Threads",
    "revs2-06": "Seven Letters Architecture",
    "revs2-07": "Chiastic Letters",
    "revs2-08": "Overcomer Promises",
    "revs2-09": "Seals 1-6",
    "revs2-10": "Seventh Seal & Transition",
    "revs2-11": "Trumpets 1-4",
    "revs2-12": "Three Woes & Interlude",
    "revs2-13": "Bowls & Final Judgment",
    "revs2-14": "Seven Spirits & Thunders",
    "revs2-15": "Seven Heads & Beatitudes",
    "revs2-16": "Christ's Declarations & Hymns",
    "revs2-17": "Numbers 12 and 4",
    "revs2-18": "Time Periods & Millennium",
    "revs2-19": "Unholy Trinity & Parody",
    "revs2-20": "Telescoping & Recapitulation",
    "revs2-21": "Already/Not-Yet",
    "revs2-22": "Sanctuary-Temple Typology",
    "revs2-23": "Exodus & Daniel Typology",
    "revs2-24": "Ezekiel & Zechariah Typology",
    "revs2-25": "Genesis Bookend & Canon",
    "revs2-26": "Revelation Macro-Structure",
    "revs2-27": "Number System",
    "revs2-28": "OT Source Synthesis",
    "revs2-29": "Chronological Model Assessment",
    "revs2-30": "Grand Structural Synthesis",
    "revs2-31": "Seven Churches",
    "revs2-32": "Seals, Trumpets & Bowls",
    "revs2-33": "Beast of Revelation 13",
    "revs2-34": "Babylon",
    "revs2-35": "The Millennium",
    "revs2-36": "Mark of the Beast",
    "revs2-37": "Three Angels' Messages",
    "revs2-38": "New Creation",
    "revs2-39": "Grand Interpretive Synthesis",
    "revs2-40": "Earth Beast & False Prophet",
}

FULL_TITLES = {
    "revs2-01": "What structural markers does John embed in Revelation, and what do they reveal about the book's literary architecture?",
    "revs2-02": "What is the structural key and frame of Revelation? How do the prologue and epilogue define the book's architecture?",
    "revs2-03": "How does the throne room vision (Rev 4-5) anchor the structure of Revelation?",
    "revs2-04": "How do Babylon and the Bride function as structural mirrors in Revelation?",
    "revs2-05": "What structural threads run through the entire book of Revelation?",
    "revs2-06": "What is the literary architecture of the seven letters (Rev 2-3)?",
    "revs2-07": "How do the seven letters form a chiastic structure, and what identifications emerge?",
    "revs2-08": "What do the overcomer promises reveal about Revelation's structure?",
    "revs2-09": "What structural and interpretive patterns emerge from seals 1-6?",
    "revs2-10": "What is the significance of the seventh seal and the transition to the trumpets?",
    "revs2-11": "What structural patterns govern trumpets 1-4?",
    "revs2-12": "How do the three woes and interlude function structurally in Revelation?",
    "revs2-13": "How do the bowls relate to the seals and trumpets, and what is their role in the final judgment sequence?",
    "revs2-14": "What structural role do the seven spirits and seven thunders play in Revelation?",
    "revs2-15": "How do the seven heads and seven beatitudes function in Revelation's architecture?",
    "revs2-16": "What structural patterns emerge from Christ's self-declarations and the hymnic passages?",
    "revs2-17": "What structural significance do the numbers 12 and 4 carry in Revelation?",
    "revs2-18": "How do time periods and the millennium function structurally in Revelation?",
    "revs2-19": "How does the unholy trinity parody the divine order, and what structural patterns emerge?",
    "revs2-20": "What evidence supports telescoping and recapitulation as structural features of Revelation?",
    "revs2-21": "How does the already/not-yet tension function as a structural principle in Revelation?",
    "revs2-22": "How does sanctuary-temple typology shape the structure of Revelation?",
    "revs2-23": "How do Exodus and Daniel typology shape Revelation's structure?",
    "revs2-24": "How do Ezekiel and Zechariah typology shape Revelation's structure?",
    "revs2-25": "How does the Genesis bookend and canonical placement shape Revelation's structure?",
    "revs2-26": "What is the macro-structure of Revelation?",
    "revs2-27": "What number system governs Revelation's literary architecture?",
    "revs2-28": "How do OT source texts combine in Revelation's compositional method?",
    "revs2-29": "How do the major chronological models account for Revelation's structure?",
    "revs2-30": "What is the grand structural synthesis of Revelation?",
    "revs2-31": "How should the seven churches be understood — historically, universally, or prophetically?",
    "revs2-32": "How do the seals, trumpets, and bowls relate to each other structurally and interpretively?",
    "revs2-33": "What does the beast of Revelation 13 represent?",
    "revs2-34": "What and who is Babylon in Revelation?",
    "revs2-35": "What is the millennium of Revelation 20?",
    "revs2-36": "What is the mark of the beast?",
    "revs2-37": "What is the architecture and message of the three angels?",
    "revs2-38": "What are the structural foundations of the new creation vision?",
    "revs2-39": "What is the grand interpretive synthesis — the message of Revelation?",
    "revs2-40": "What does the earth beast / false prophet represent?",
}

# Cluster groupings
CLUSTERS = [
    {
        "name": "Module 1 -- Foundational Architecture",
        "desc": "The structural markers, key-and-frame, throne room anchor, Babylon-Bride mirror, and structural threads that define Revelation's literary architecture.",
        "studies": ["revs2-01", "revs2-02", "revs2-03", "revs2-04", "revs2-05"],
    },
    {
        "name": "Module 2 -- Seven Letters",
        "desc": "The literary architecture, chiastic structure, and overcomer promises of the seven letters.",
        "studies": ["revs2-06", "revs2-07", "revs2-08"],
    },
    {
        "name": "Module 3 -- Seal Sequence",
        "desc": "Structural and interpretive patterns in the seal judgments.",
        "studies": ["revs2-09", "revs2-10"],
    },
    {
        "name": "Module 4 -- Trumpet & Bowl Sequences",
        "desc": "Structural patterns in the trumpets, woes, interlude, and bowl judgments.",
        "studies": ["revs2-11", "revs2-12", "revs2-13"],
    },
    {
        "name": "Module 5 -- Symbolic Numbers",
        "desc": "The role of sevens, twelve, four, time periods, and the millennium in Revelation's architecture.",
        "studies": ["revs2-14", "revs2-15", "revs2-16", "revs2-17", "revs2-18"],
    },
    {
        "name": "Module 6 -- Interpretive Frameworks",
        "desc": "Unholy trinity parody, telescoping/recapitulation, already/not-yet tension, and sanctuary-temple typology.",
        "studies": ["revs2-19", "revs2-20", "revs2-21", "revs2-22"],
    },
    {
        "name": "Module 7 -- OT Typology & Canon",
        "desc": "How Exodus, Daniel, Ezekiel, Zechariah, and Genesis shape Revelation's structure.",
        "studies": ["revs2-23", "revs2-24", "revs2-25"],
    },
    {
        "name": "Module 8 -- Structural Synthesis",
        "desc": "Macro-structure, number system, OT source synthesis, chronological models, and grand structural synthesis.",
        "studies": ["revs2-26", "revs2-27", "revs2-28", "revs2-29", "revs2-30"],
    },
    {
        "name": "Part 2 -- Interpretive Application",
        "desc": "Applying the structural findings to key interpretive questions in Revelation.",
        "studies": ["revs2-31", "revs2-32", "revs2-33", "revs2-34", "revs2-35",
                    "revs2-36", "revs2-37", "revs2-38", "revs2-39", "revs2-40"],
    },
]

# Standard study files (in display order for nav)
STUDY_FILES = [
    ("CONCLUSION.md", None),           # Landing page (no label = index page)
    ("03-analysis.md", "Analysis"),
    ("02-verses.md", "Verses"),
    ("04-word-studies.md", "Word Studies"),
    ("01-topics.md", "Topics"),
    ("PROMPT.md", "Research Scope"),
]

# Raw data file display names
RAW_DATA_NAMES = {
    "concept-context": "Concept Context",
    "existing-studies": "Existing Studies",
    "greek-parsing": "Greek Parsing",
    "hebrew-parsing": "Hebrew Parsing",
    "naves-topics": "Nave's Topics",
    "parallels": "Cross-Testament Parallels",
    "strongs-lookups": "Strong's Lookups",
    "strongs": "Strong's Lookups",
    "web-research": "Web Research",
    "grammar-references": "Grammar References",
    "evidence-tally": "Evidence Tally",
    "study-db-queries": "Study DB Queries",
    "sanctuary-evidence": "Sanctuary Evidence",
    "per-study-breakdown": "Per-Study Breakdown",
    "historical-sources": "Historical Sources",
    "model-tally": "Model Tally",
}


def get_raw_data_name(filename: str) -> str:
    """Get a display name for a raw-data file."""
    stem = Path(filename).stem
    if stem in RAW_DATA_NAMES:
        return RAW_DATA_NAMES[stem]
    return stem.replace("-", " ").title()


def find_study_folders() -> list[tuple[str, Path]]:
    """Find all revs2-NN-* folders in the studies source directory."""
    folders = []
    found_keys = set()
    for d in sorted(STUDIES_SRC.iterdir()):
        if d.is_dir() and re.match(r"revs2-\d{2}-", d.name):
            num = d.name.split("-")[1]
            key = f"revs2-{num}"
            if key not in SHORT_TITLES:
                continue
            if key not in found_keys:
                folders.append((key, d))
                found_keys.add(key)
    return folders


def copy_study(key: str, src: Path, preserved_simples: dict):
    """Copy a study folder into docs/studies/."""
    dest = DOCS_STUDIES / src.name
    dest.mkdir(parents=True, exist_ok=True)

    # Copy standard files
    for fname, _ in STUDY_FILES:
        src_file = src / fname
        if src_file.exists():
            shutil.copy2(src_file, dest / fname)

    # Restore preserved conclusion-simple.md, or copy from source
    simple_path = dest / "conclusion-simple.md"
    if src.name in preserved_simples:
        simple_path.write_text(preserved_simples[src.name], encoding="utf-8")
    else:
        simple_src = src / "conclusion-simple.md"
        if simple_src.exists():
            shutil.copy2(simple_src, dest / "conclusion-simple.md")

    # Copy METADATA.yaml if present
    meta = src / "METADATA.yaml"
    if meta.exists():
        shutil.copy2(meta, dest / "METADATA.yaml")

    # Copy raw-data/ (both .md and .txt files)
    raw_src = src / "raw-data"
    if raw_src.exists() and raw_src.is_dir():
        raw_dest = dest / "raw-data"
        raw_dest.mkdir(parents=True, exist_ok=True)
        for f in raw_src.iterdir():
            if f.is_file():
                if f.suffix == ".txt":
                    dest_file = raw_dest / (f.stem + ".md")
                    content = f.read_text(encoding="utf-8", errors="replace")
                    dest_file.write_text(f"# {get_raw_data_name(f.name)}\n\n```\n{content}\n```\n", encoding="utf-8")
                else:
                    shutil.copy2(f, raw_dest / f.name)

    return dest


def build_nav_entry(key: str, slug: str) -> dict:
    """Build a nav entry for one study."""
    num = key.split("-")[1]
    short_title = SHORT_TITLES.get(key, slug)
    nav_title = f"{num} -- {short_title}"

    dest = DOCS_STUDIES / slug
    items = []

    # Landing page: conclusion-simple.md if it exists, else CONCLUSION.md
    simple = dest / "conclusion-simple.md"
    conclusion = dest / "CONCLUSION.md"
    if simple.exists():
        items.append(f"studies/{slug}/conclusion-simple.md")
        if conclusion.exists():
            items.append({"Conclusion": f"studies/{slug}/CONCLUSION.md"})
    elif conclusion.exists():
        items.append(f"studies/{slug}/CONCLUSION.md")

    # Other standard files
    for fname, label in STUDY_FILES:
        if label is None:
            continue
        fpath = dest / fname
        if fpath.exists():
            items.append({label: f"studies/{slug}/{fname}"})

    # Raw data files
    raw_dir = dest / "raw-data"
    if raw_dir.exists() and raw_dir.is_dir():
        raw_items = []
        for f in sorted(raw_dir.iterdir()):
            if f.is_file() and f.suffix == ".md":
                display = get_raw_data_name(f.name)
                raw_items.append({display: f"studies/{slug}/raw-data/{f.name}"})
        if raw_items:
            items.append({"Raw Data": raw_items})

    return {nav_title: items}


def generate_mkdocs_yml(study_folders: list[tuple[str, Path]]):
    """Generate mkdocs.yml."""
    slug_map = {key: src.name for key, src in study_folders}

    lines = []
    lines.append('site_name: "Revelation\'s Architecture"')
    lines.append('site_description: "A 40-study structural and interpretive analysis of Revelation. 1,368 catalogued items across structural elements and evidence."')
    lines.append("")
    lines.append("theme:")
    lines.append("  name: material")
    lines.append("  palette:")
    lines.append("    - scheme: default")
    lines.append("      primary: deep purple")
    lines.append("      accent: orange")
    lines.append("      toggle:")
    lines.append("        icon: material/brightness-7")
    lines.append("        name: Switch to dark mode")
    lines.append("    - scheme: slate")
    lines.append("      primary: deep purple")
    lines.append("      accent: orange")
    lines.append("      toggle:")
    lines.append("        icon: material/brightness-4")
    lines.append("        name: Switch to light mode")
    lines.append("  features:")
    lines.append("    - navigation.instant")
    lines.append("    - navigation.tracking")
    lines.append("    - navigation.tabs")
    lines.append("    - navigation.sections")
    lines.append("    - navigation.top")
    lines.append("    - navigation.indexes")
    lines.append("    - search.suggest")
    lines.append("    - search.highlight")
    lines.append("    - content.tabs.link")
    lines.append("    - toc.follow")
    lines.append("  font:")
    lines.append("    text: Roboto")
    lines.append("    code: Roboto Mono")
    lines.append("  custom_dir: overrides")
    lines.append("")
    lines.append("plugins:")
    lines.append("  - search")
    lines.append("")
    lines.append("markdown_extensions:")
    lines.append("  - abbr")
    lines.append("  - admonition")
    lines.append("  - attr_list")
    lines.append("  - def_list")
    lines.append("  - footnotes")
    lines.append("  - md_in_html")
    lines.append("  - tables")
    lines.append("  - toc:")
    lines.append("      permalink: true")
    lines.append("  - pymdownx.details")
    lines.append("  - pymdownx.superfences")
    lines.append("  - pymdownx.highlight:")
    lines.append("      anchor_linenums: true")
    lines.append("  - pymdownx.inlinehilite")
    lines.append("  - pymdownx.tabbed:")
    lines.append("      alternate_style: true")
    lines.append("  - pymdownx.tasklist:")
    lines.append("      custom_checkbox: true")
    lines.append("")
    lines.append("extra:")
    lines.append("  social:")
    lines.append("    - icon: fontawesome/solid/book-bible")
    lines.append("      link: /")
    lines.append("")
    lines.append("extra_javascript:")
    lines.append("  - javascripts/verse-popup.js")
    lines.append("  - javascripts/study-breadcrumbs.js")
    lines.append("  - javascripts/external-links.js")
    lines.append("")
    lines.append("extra_css:")
    lines.append("  - stylesheets/extra.css")
    lines.append("")
    lines.append("nav:")
    lines.append("  - Home: index.md")
    lines.append("  - Studies:")
    lines.append("")

    for cluster in CLUSTERS:
        lines.append(f"    # ── {cluster['name']} ──")
        lines.append(f'    - "{cluster["name"]}":')
        lines.append("")
        for key in cluster["studies"]:
            slug = slug_map.get(key)
            if not slug:
                continue
            nav_entry = build_nav_entry(key, slug)
            for title, items in nav_entry.items():
                lines.append(f'      - "{title}":')
                for item in items:
                    if isinstance(item, str):
                        lines.append(f"        - {item}")
                    elif isinstance(item, dict):
                        for label, val in item.items():
                            if isinstance(val, list):
                                lines.append(f"        - {label}:")
                                for sub in val:
                                    if isinstance(sub, dict):
                                        for slabel, spath in sub.items():
                                            lines.append(f'          - "{slabel}": {spath}')
                                    else:
                                        lines.append(f"          - {sub}")
                            else:
                                lines.append(f"        - {label}: {val}")
        lines.append("")

    lines.append("  - Methodology: methodology.md")
    lines.append('  - "Tools & Process": tools.md')

    yml_path = PROJECT_ROOT / "mkdocs.yml"
    yml_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  Generated {yml_path}")


def generate_index_md():
    """Generate docs/index.md."""
    content = []

    content.append("# Revelation's Architecture")
    content.append("")
    content.append("*A 40-study structural and interpretive analysis of Revelation. Part 1 (Studies 1-30) maps Revelation's literary architecture through structural markers, symbolic numbers, interpretive frameworks, and OT typology. Part 2 (Studies 31-40) applies those structural findings to key interpretive questions. 1,368 catalogued items across structural elements and evidence.*")
    content.append("")
    content.append("---")
    content.append("")
    content.append("## The Question")
    content.append("")
    content.append("What is the literary architecture of Revelation, and what does it reveal about the book's message? Revelation is the most structurally complex book in the Bible -- saturated with sevens, twelves, chiastic patterns, OT allusions, and interlocking symbolic systems. But does this complexity follow a coherent design, and can that design be mapped? This series traces every structural element through the entire book, building from individual markers to a grand synthesis.")
    content.append("")
    content.append("The investigation covers 30 structural studies (Part 1) that map the architecture, followed by 10 interpretive studies (Part 2) that apply those structural findings to disputed questions about beasts, Babylon, the millennium, and more.")
    content.append("")
    content.append("## The Approach")
    content.append("")
    content.append("Each study is a genuine investigation. The agents gathered ALL relevant evidence, presented what the biblical text teaches, and classified findings using a rigorous evidence hierarchy:")
    content.append("")
    content.append("- **Explicit (E):** What the text directly says -- a quote or close paraphrase")
    content.append("- **Necessary Implication (N):** What unavoidably follows from explicit statements")
    content.append("- **Inference (I):** What positions claim the text implies, requiring something beyond the text itself")
    content.append("")
    content.append("**Hierarchy:** E > N > I (inferences cannot override explicit statements)")
    content.append("")
    content.append("[**Read the Methodology**](methodology.md){ .md-button }")

    synth_simple = DOCS_STUDIES / "revs2-30-grand-structural-synthesis" / "conclusion-simple.md"
    if synth_simple.exists():
        content.append("[**Skip to the Grand Structural Synthesis**](studies/revs2-30-grand-structural-synthesis/conclusion-simple.md){ .md-button .md-button--primary }")
    else:
        content.append("[**Skip to the Grand Structural Synthesis**](studies/revs2-30-grand-structural-synthesis/CONCLUSION.md){ .md-button .md-button--primary }")

    synth2_simple = DOCS_STUDIES / "revs2-39-message-of-revelation-grand-synthesis" / "conclusion-simple.md"
    if synth2_simple.exists():
        content.append("[**Skip to the Grand Interpretive Synthesis**](studies/revs2-39-message-of-revelation-grand-synthesis/conclusion-simple.md){ .md-button .md-button--primary }")
    else:
        content.append("[**Skip to the Grand Interpretive Synthesis**](studies/revs2-39-message-of-revelation-grand-synthesis/CONCLUSION.md){ .md-button .md-button--primary }")

    content.append("")
    content.append("---")
    content.append("")
    content.append("## The 40 Studies")
    content.append("")

    for cluster in CLUSTERS:
        content.append(f"### {cluster['name']}")
        content.append("")
        content.append(cluster["desc"])
        content.append("")
        content.append("| # | Study | Question |")
        content.append("|---|-------|----------|")
        for key in cluster["studies"]:
            num = key.split("-")[1]
            short = SHORT_TITLES.get(key, key)
            full = FULL_TITLES.get(key, short)
            slug = None
            for d in sorted(STUDIES_SRC.iterdir()):
                if d.is_dir() and d.name.startswith(f"{key}-"):
                    slug = d.name
                    break
            if slug:
                simple_path = DOCS_STUDIES / slug / "conclusion-simple.md"
                if simple_path.exists():
                    link = f"studies/{slug}/conclusion-simple.md"
                else:
                    link = f"studies/{slug}/CONCLUSION.md"
                content.append(f"| {num} | [{short}]({link}) | {full} |")
            else:
                content.append(f"| {num} | {short} | {full} |")
        content.append("")

    content.append("---")
    content.append("")
    content.append("## What Each Study Contains")
    content.append("")
    content.append("Every study includes multiple layers of research, all accessible through the navigation:")
    content.append("")
    content.append("| File | Contents |")
    content.append("|------|----------|")
    content.append("| **Simple Conclusion** | A plain-language summary of the study's findings -- no technical jargon or evidence tables |")
    content.append("| **Conclusion** | The final evidence classification with Explicit/Necessary Implication/Inference tables, tally, and assessment |")
    content.append("| **Analysis** | Verse-by-verse analysis, identified patterns, connections between passages |")
    content.append("| **Verses** | Full KJV text for every passage examined, organized thematically |")
    content.append("| **Word Studies** | Hebrew and Greek word studies with Strong's numbers, semantic ranges, and parsing |")
    content.append("| **Topics** | Nave's Topical Bible entries and key research findings |")
    content.append("| **Research Scope** | The original research question and scope that guided the investigation |")
    content.append("| **Raw Data** | Nave's topic output, Strong's lookups, Greek/Hebrew parsing, cross-testament parallels |")
    content.append("")
    content.append("---")
    content.append("")
    content.append("## Source Restrictions")
    content.append("")
    content.append("This series uses **no denominational or extra-biblical sources** as authoritative evidence. Permitted sources are:")
    content.append("")
    content.append("- Scripture (KJV text with Hebrew/Greek analysis)")
    content.append("- Secular and church historians (for verifying prophetic claims against historical events)")
    content.append("- Scholarly commentators from all traditions")
    content.append("- Hebrew and Greek lexicons, grammars, and concordances")
    content.append("")
    content.append("The question is always: **What does the Bible say?**")
    content.append("")

    index_path = DOCS / "index.md"
    index_path.write_text("\n".join(content) + "\n", encoding="utf-8")
    print(f"  Generated {index_path}")


def generate_tools_md():
    """Generate docs/tools.md."""
    content = """# Research Tools & Process

*This page describes the automated research system and investigative methodology that produced the 40 studies in this series.*

---

## Investigative Stance

Each study is produced by an agent that functions as an **investigator, not an advocate.** This distinction governs every step of the process:

- **Gather evidence from all sides.** If a passage is cited by one tradition, examine it honestly. If another tradition reads it differently, examine that reading honestly.
- **Do not assume a conclusion before examining the evidence.** The conclusion emerges FROM the evidence, not the reverse.
- **State what the text says, not opinions about it.** The agent does not use editorial characterizations like "genuine tension," "strongest argument," or "non-intuitive reading." It states what each passage says and what each interpretive position infers from it.
- **Never use language like "irrefutable," "obviously," or "clearly proves."** Use "the text states," "this is consistent with."

---

## How the Studies Were Produced

Each study was generated by a multi-agent pipeline, a Claude Code skill that answers Bible questions through tool-driven research. The pipeline ensures that:

- **Scope comes from tools, not training knowledge.** The AI does not decide which verses are relevant based on what it was trained on. Instead, tools search topical dictionaries, concordances, and semantic indexes to discover what Scripture says about the topic.
- **Research and analysis are separated.** The agent that gathers data is not the same agent that draws conclusions. This prevents confirmation bias.
- **Every claim is traceable.** Raw tool output is preserved in each study's `raw-data/` folder, so every finding can be verified against its source.

### The Multi-Agent Pipeline

```
Phase 0: Web Research Agent
   | Searches for academic papers, scholarly commentary, linguistic research
   | Writes 00-web-research.md

Phase 1: References Agent
   | Gathers prior studies and external corpus leads
   | Writes 00-references.md

Phase 2: Scoping Agent
   | Discovers topics, verses, Strong's numbers, related studies
   | Writes PROMPT.md (the research brief)

Phase 3: Research Agent
   | Reads PROMPT.md
   | Retrieves all verse text, runs parallels, word studies, parsing
   | Writes 01-topics.md, 02-verses.md, 04-word-studies.md
   | Saves raw tool output to raw-data/

Phase 4: Analysis Agent
   | Reads clean research files
   | Applies the evidence classification methodology
   | Writes 03-analysis.md and CONCLUSION.md
```

**Why multiple agents instead of one?**

- The **web research agent** searches for scholarly context online before the local corpus search begins.
- The **references agent** finds prior studies and prevents duplicated work across the series.
- The **scoping agent** prevents training-knowledge bias. Scope comes from tool discovery, not from what the AI "knows" about theology.
- The **research agent** gets a fresh context window dedicated to data gathering. This maximizes the amount of data it can collect without running out of context.
- The **analysis agent** gets a fresh context window loaded with clean, organized research. This maximizes its capacity for synthesis and careful reasoning.

---

## The Study Files

Each study directory contains these files, produced by the pipeline:

| File | Produced By | Contents |
|------|-------------|----------|
| `00-web-research.md` | Web Research Agent | Academic papers, scholarly commentary, and linguistic research from online sources |
| `00-references.md` | References Agent | Prior studies and external corpus leads |
| `PROMPT.md` | Scoping Agent | The research brief: tool-discovered topics, verses, Strong's numbers, related studies, and focus areas |
| `01-topics.md` | Research Agent | Nave's Topical Bible entries with all verse references for each topic |
| `02-verses.md` | Research Agent | Full KJV text for every verse examined, organized thematically |
| `04-word-studies.md` | Research Agent | Strong's concordance data: Hebrew/Greek words, definitions, translation statistics, verse occurrences |
| `raw-data/` | Research Agent | Raw tool output archived by category (Strong's lookups, parsing, parallels, etc.) |
| `03-analysis.md` | Analysis Agent | Verse-by-verse analysis with full evidence classification applied |
| `CONCLUSION.md` | Analysis Agent | Evidence tables (E/N/I), tally, and final assessment |

---

## Data Sources

The tools draw from these primary data sources:

| Source | Description | Size |
|--------|-------------|------|
| **KJV Bible** | Complete King James Version text | 31,102 verses |
| **Nave's Topical Bible** | Orville J. Nave's topical dictionary | 5,319 topics |
| **Strong's Concordance** | James Strong's exhaustive concordance with Hebrew/Greek lexicon | Every word in the KJV mapped to original language |
| **BHSA** (Biblia Hebraica Stuttgartensia Amstelodamensis) | Hebrew Bible linguistic database via Text-Fabric | Full morphological parsing of every Hebrew word |
| **N1904** (Nestle 1904) | Greek New Testament linguistic database via Text-Fabric | Full morphological parsing of every Greek word |
| **Textus Receptus** | Byzantine Greek text tradition | For textual variant comparison |
| **LXX Mapping** | Septuagint translation correspondences | Hebrew-to-Greek word mappings |
| **Sentence embeddings** | Pre-computed semantic vectors | For semantic search across all sources |

---

## Evidence Classification Methodology

The core of the methodology is a three-tier evidence classification system that distinguishes between what Scripture directly states, what necessarily follows from it, and what positions claim it implies.

### The Three Tiers

**E -- Explicit.** "The Bible says X." You can point to a verse that says X. A close paraphrase of the actual words of a specific verse, with no concept, framework, or interpretation added beyond what the words themselves require.

**N -- Necessary Implication.** "The Bible implies X." You can point to verses that, when combined, force X with no alternative. Every reader from any theological position must agree this follows -- no additional reasoning is required.

**I -- Inference.** "A position claims the Bible teaches X." No verse explicitly states X, and no combination of verses necessarily implies X. Something must be added beyond what the text contains.

**Critical rule:** Inferences cannot block explicit statements or necessary implications. If E and N items establish X, the existence of passages that *could be inferred* to teach not-X does not prevent X from being established.

[**Read the Full Methodology**](methodology.md){ .md-button }
"""
    tools_path = DOCS / "tools.md"
    tools_path.write_text(content, encoding="utf-8")
    print(f"  Generated {tools_path}")


def copy_assets():
    """Copy shared assets from etc-website."""
    js_src = ETC_WEBSITE / "docs" / "javascripts"
    js_dest = DOCS / "javascripts"
    js_dest.mkdir(parents=True, exist_ok=True)
    for fname in ["verse-popup.js", "study-breadcrumbs.js", "external-links.js",
                   "verses.json", "strongs.json"]:
        src = js_src / fname
        if src.exists():
            shutil.copy2(src, js_dest / fname)
            print(f"  Copied {fname}")
        else:
            print(f"  WARNING: {src} not found")

    css_src = ETC_WEBSITE / "docs" / "stylesheets" / "extra.css"
    css_dest = DOCS / "stylesheets"
    css_dest.mkdir(parents=True, exist_ok=True)
    if css_src.exists():
        shutil.copy2(css_src, css_dest / "extra.css")
        print(f"  Copied extra.css")


def copy_methodology():
    """Copy revs2 series methodology."""
    src = STUDIES_SRC / "revs2-series-methodology.md"
    if not src.exists():
        src = STUDIES_SRC / "revs-series-methodology.md"
    dest = DOCS / "methodology.md"
    if src.exists():
        shutil.copy2(src, dest)
        print(f"  Copied methodology.md from {src.name}")
    else:
        print(f"  WARNING: No methodology file found")


def copy_overrides():
    """Copy overrides from hist-website."""
    src = Path("D:/bible/hist-website/overrides/main.html")
    dest = PROJECT_ROOT / "overrides"
    dest.mkdir(parents=True, exist_ok=True)
    if src.exists():
        shutil.copy2(src, dest / "main.html")
        print(f"  Copied overrides/main.html")
    else:
        print(f"  WARNING: {src} not found")


def generate_gitignore():
    """Generate .gitignore."""
    content = """site/
.venv/
__pycache__/
node_modules/
"""
    (PROJECT_ROOT / ".gitignore").write_text(content, encoding="utf-8")
    print(f"  Generated .gitignore")


def generate_readme(study_folders: list[tuple[str, Path]]):
    """Generate README.md."""
    lines = []
    lines.append("# Revelation's Architecture")
    lines.append("")
    lines.append("A 40-study structural and interpretive analysis of Revelation. 1,368 catalogued items across structural elements and evidence.")
    lines.append("")
    lines.append("## Studies")
    lines.append("")

    part1_label = "### Part 1: Structural Analysis (Studies 01-30)"
    part2_label = "### Part 2: Interpretive Application (Studies 31-40)"
    lines.append(part1_label)
    lines.append("")
    lines.append("| # | Study | Question |")
    lines.append("|---|-------|----------|")
    for key, src in study_folders:
        num = key.split("-")[1]
        if num == "31":
            lines.append("")
            lines.append(part2_label)
            lines.append("")
            lines.append("| # | Study | Question |")
            lines.append("|---|-------|----------|")
        short = SHORT_TITLES.get(key, key)
        full = FULL_TITLES.get(key, short)
        lines.append(f"| {num} | {short} | {full} |")
    lines.append("")
    lines.append("## Built With")
    lines.append("")
    lines.append("- [MkDocs](https://www.mkdocs.org/) with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)")
    lines.append("- Interactive Bible verse and Strong's number popups")
    lines.append("- Full KJV text and Strong's Concordance data")

    (PROJECT_ROOT / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  Generated README.md")


def main():
    print("=" * 60)
    print("Building Revelation's Architecture (revs2) website")
    print("=" * 60)

    # Preserve any existing conclusion-simple.md files before cleaning
    preserved_simples = {}
    if DOCS_STUDIES.exists():
        for d in DOCS_STUDIES.iterdir():
            if d.is_dir():
                simple = d / "conclusion-simple.md"
                if simple.exists():
                    preserved_simples[d.name] = simple.read_text(encoding="utf-8")
        shutil.rmtree(DOCS_STUDIES)
    DOCS_STUDIES.mkdir(parents=True)
    print(f"  Preserved {len(preserved_simples)} conclusion-simple.md files")

    # Find all study folders
    print("\n[1/8] Finding study folders...")
    study_folders = find_study_folders()
    print(f"  Found {len(study_folders)} studies")

    # Copy studies
    print("\n[2/8] Copying study files...")
    for key, src in study_folders:
        dest = copy_study(key, src, preserved_simples)
        print(f"  {key}: {src.name} -> {dest.relative_to(PROJECT_ROOT)}")

    # Copy methodology
    print("\n[3/8] Copying methodology...")
    copy_methodology()

    # Copy shared assets
    print("\n[4/8] Copying shared assets from etc-website...")
    copy_assets()

    # Copy overrides
    print("\n[5/8] Copying overrides...")
    copy_overrides()

    # Generate mkdocs.yml
    print("\n[6/8] Generating mkdocs.yml...")
    generate_mkdocs_yml(study_folders)

    # Generate index.md and tools.md
    print("\n[7/8] Generating index.md and tools.md...")
    generate_index_md()
    generate_tools_md()

    # Generate supporting files
    print("\n[8/8] Generating supporting files...")
    generate_gitignore()
    generate_readme(study_folders)

    print("\n" + "=" * 60)
    print("Build complete!")
    print(f"  Studies: {len(study_folders)}")
    print(f"  Output: {DOCS}")
    print("\nNext steps:")
    print("  1. Generate conclusion-simple.md for each study")
    print("  2. Re-run build_site.py to pick up the simple conclusions")
    print("  3. mkdocs serve")
    print("=" * 60)


if __name__ == "__main__":
    main()
