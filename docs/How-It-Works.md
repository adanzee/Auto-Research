# How AutoResearch Works

## The Big Picture

A user submits a research topic. The system spins up a pipeline of AI agents that search the web, read sources, extract facts, validate them, and produce a structured PDF report. Before the final report is generated, a human must review and approve the research — this is the trust layer.

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

The HITL checkpoint is not a formality. The human sees exactly what the agents found — including contradictions and low-confidence facts. Approving means the human takes responsibility for the quality of the final report. Rejecting sends the agents back to research again. Editing lets the human reshape the report structure before it is written. This makes the output trustworthy rather than blindly automated.

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