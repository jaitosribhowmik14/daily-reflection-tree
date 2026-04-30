# DeepThought Daily Reflection Tree Agent

## DT Fellowship Assignment — Deterministic Reflection System

---

# Overview

This project is a deterministic end-of-day reflection agent designed for the DeepThought Fellowship Assignment.

It operationalizes three psychological axes into a structured decision tree:

## Axis 1 — Locus
**Victim ↔ Victor**  
Do I perceive today as something that happened to me, or something I navigated?

## Axis 2 — Orientation
**Entitlement ↔ Contribution**  
Was I focused more on what I deserved, or what I gave?

## Axis 3 — Radius
**Self-Centrism ↔ Altrocentrism**  
Was my frame limited to myself, or did it include others?

---

# Core Philosophy

This project was designed according to DeepThought’s emphasis on:

### Determinism over generative AI
- No LLM at runtime
- Fixed-option branching
- Same answers → same path
- Auditable logic

### AI as a design collaborator, not product
AI was used during:
- Psychological research
- Question drafting
- Branch testing
- Persona simulation

AI was NOT used at runtime.

---

# Folder Structure

```txt
Deterministic Reflection Agent/
 ┣ agent/
 ┃ ┗ app.py
 ┣ tree/
 ┃ ┗ reflection-tree.json
 ┣ templates/
 ┃ ┗ index.html
 ┣ static/
 ┃ ┗ style.css
 ┣ transcripts/
 ┃ ┣ persona-victim.md
 ┃ ┗ persona-victor.md
 ┗ README.md