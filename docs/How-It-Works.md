# AutoResearch — Agentic System Overview

## What Is This?

AutoResearch is an **agentic pipeline** — a network of autonomous AI agents that each own a specific task, make decisions independently, and hand off results to the next agent. The system handles a full research cycle end-to-end, from raw topic to formatted PDF, with a human checkpoint before final output.

---

## The Agent Network

### 1. Planner Agent
Receives the research topic and decomposes it into **6–10 focused sub-questions**, covering definition, history, current state, challenges, future outlook, and controversies. Every downstream agent operates from these sub-questions.

### 2. Search Agent
Runs in **parallel** across all sub-questions. For each one, it generates targeted search queries, hits the Tavily API, retrieves relevant URLs, and filters out low-relevance results autonomously.

### 3. Scraper Agent
Visits each URL and extracts clean, readable text — stripping ads, nav, and boilerplate. Failed or timed-out URLs are logged and skipped. The agent never blocks the pipeline on a single bad source.

### 4. Extraction Agent
Reads each scraped page and pulls out facts relevant to the sub-question that sourced it. Each fact is assigned an initial credibility score for the next agent to evaluate.

### 5. Validation Agent
Cross-checks all extracted facts across every source. It scores each fact by source quality, recency, and corroboration. **Conflicting claims are flagged as contradictions.** This is the agent that separates the system from a basic summarizer — it does not blindly trust any single source.

### 6. Synthesis Agent
Reviews all validated facts and builds a **structured report outline** organised by theme. It calculates an overall confidence score. If confidence is too low or a major section lacks supporting facts, it signals the pipeline to loop back to the Planner — up to **two times** before forcing forward progress.

### 7. Report Agent
Activated only after human approval. Generates the final report in Markdown with **inline citations** on every factual claim, then converts it to a PDF with a table of contents, page numbers, source credibility scores, and a limitations section disclosing AI assistance.

---

## Human-in-the-Loop (HITL) Checkpoint

The pipeline **pauses** before report generation. This is not a formality.

The human reviewer sees:
- The report outline
- The overall confidence score
- All detected contradictions
- A sample of the strongest and weakest facts

**Three choices are available:**

| Action | What happens |
|--------|--------------|
| **Approve** | Pipeline continues to the Report Agent. The human takes responsibility for output quality. |
| **Reject** | Agents loop back and re-research with the rejection feedback in context. |
| **Edit** | Human reshapes the outline with specific instructions before report generation begins. |

---

## Agent Loop — Quality Control

After the Synthesis Agent scores the research:

- If quality is **below threshold** → loop back to Planner Agent (aware of what was missing)
- This loop can happen **at most twice**
- After two iterations, the pipeline always proceeds to HITL regardless of score

---

## Pipeline Flow

```
User submits topic
        ↓
Planner Agent      — breaks topic into sub-questions
        ↓
Search Agent       — finds relevant URLs (runs in parallel)
        ↓
Scraper Agent      — extracts clean text from each URL
        ↓
Extraction Agent   — pulls facts per page
        ↓
Validation Agent   — scores and cross-checks every fact
        ↓
Synthesis Agent    — builds outline, checks quality
        ↓  ↑ loops back if quality too low (max 2×)
HITL Checkpoint    — human reviews and approves / rejects / edits
        ↓  ↑ loops back if human rejects
Report Agent       — generates Markdown + PDF
        ↓
Report delivered
```

---

## Key Agentic Properties

- **Autonomy** — each agent acts independently within its scope, no manual hand-holding between steps
- **Parallelism** — the Search Agent fans out across all sub-questions simultaneously
- **Self-correction** — the Synthesis Agent can trigger re-runs when quality falls short
- **Graceful degradation** — failed sources are skipped; the pipeline never halts on partial failures
- **Human oversight** — the HITL checkpoint ensures a human is accountable for every output before it ships# How AutoResearch Works



---

## The Workflow

### 1. User Submits a Topic
The user sends a research topic through the API. The system creates a job, queues it in the background, and immediately returns a job ID. The user does not wait — they get notified when each stage completes.

### 2. Planner Agent
The pipeline starts here. The Planner reads the topic and breaks it down into 6 to 10 focused sub-questions. These sub-questions cover the topic from multiple angles — definition, history, current state, challenges, future outlook, and controversies. Every other agent works from these sub-questions.

### 3. Search Agent
For each sub-question, the Search Agent generates targeted search queries and retrieves relevant URLs from the web using the Tavily API. It runs in parallel for all sub-questions at the same time and filters out low-relevance results.

### 4. Scraper Agent
The Scraper visits each URL and extracts clean readable text — stripping ads, navigation, and boilerplate. If a URL fails or times out, it is logged and skipped. The pipeline never stops for a single failed source.

### 5. Extraction Agent
For each scraped page, the Extraction Agent reads the content and pulls out facts that are relevant to the sub-question that page was fetched for. Each fact starts with a neutral credibility score that the next agent will adjust.

### 6. Validation Agent
The Validation Agent cross-checks all extracted facts across every source. It scores each fact based on source quality, recency, and how many independent sources agree with it. If two facts make conflicting claims, both are flagged as contradictions. This is what separates the system from a basic summarizer — it does not blindly trust one source.

### 7. Synthesis Agent
The Synthesis Agent reviews all validated facts and builds a structured report outline organized by theme. It also calculates an overall confidence score for the research. If the confidence is too low or any major section lacks enough supporting facts, the pipeline loops back to the Planner Agent to research again. This can happen a maximum of two times total.

### 8. HITL Checkpoint — Human Review
The pipeline pauses here. Every run must pass through this step. The human is shown the report outline, the confidence score, detected contradictions, and a sample of the strongest and weakest facts. The human has three choices — approve the research and continue, reject it with feedback to trigger a re-run, or edit the outline with specific instructions before continuing.

### 9. Report Agent
Once the human approves, the Report Agent generates the final research report in Markdown with inline citations for every factual claim. The report is then converted into a professionally formatted PDF complete with a table of contents, page numbers, all sources listed with their credibility scores, and a limitations section disclosing AI assistance.

### 10. Report Delivered
The user receives a notification that the report is ready and can download the PDF through the API.

---

## What Happens If Quality Is Too Low

After the Synthesis Agent calculates the confidence score, if the research does not meet the quality threshold the pipeline automatically loops back to the Planner Agent. The Planner runs again with awareness of what was missing the first time. This loop can happen at most twice. After two iterations the pipeline always moves forward to the human review regardless of the score.

---

## What the Human Review Actually Controls

The HITL (Human-In-The-Loop) checkpoint is not a formality. The human sees exactly what the agents found — including contradictions and low-confidence facts. Approving means the human takes responsibility for the quality of the final report. Rejecting sends the agents back to research again. Editing lets the human reshape the report structure before it is written. This makes the output trustworthy rather than blindly automated.

---

## Summary

```
Topic submitted
      ↓
Planner  →  breaks topic into sub-questions
      ↓
Search   →  finds relevant URLs
      ↓
Scraper  →  extracts clean text from each URL
      ↓
Extract  →  pulls facts from each page
      ↓
Validate →  scores and cross-checks every fact
      ↓
Synthesize → builds outline, checks quality
      ↓        (loops back if quality too low, max 2x)
HITL     →  human reviews and approves
      ↓        (loops back if human rejects)
Report   →  generates markdown + PDF
      ↓
Done
```
📌 Have to add some new agentic concept in order to make the flow better
