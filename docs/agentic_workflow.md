# AutoResearch

An intelligent, agentic AI research system that performs deep web research and produces high-quality, trustworthy PDF reports with mandatory Human-in-the-Loop (HITL) approval.

## Overview

AutoResearch is a **goal-driven, multi-agent system** built with LangGraph. Unlike traditional linear pipelines, this is a truly **agentic workflow** where specialized agents collaborate, reason, reflect, self-correct, and dynamically adapt their strategy under the coordination of a Supervisor Agent.

The system accepts a research topic, conducts thorough investigation, validates facts, resolves contradictions, and delivers a professionally formatted PDF report — only after human review and approval.

---

## Core Architecture (Agentic Design)

### Key Principles
- **Agentic Philosophy**: Agents are goal-oriented, reflective, and proactive. They can request help, critique their own work, and adapt plans.
- **Centralized Coordination**: A Supervisor Agent orchestrates all agents and maintains strategic oversight.
- **Shared State**: All agents read from and write to a single `ResearchState` object.
- **Mandatory HITL**: Human approval is required before generating the final report.
- **Self-Improving Loops**: Agents can intelligently loop back to improve quality (max 2 iterations).

### Agents

| Agent              | Role | Key Behaviors |
|--------------------|------|---------------|
| **Supervisor Agent** | Orchestrator & Decision Maker | Assigns tasks, evaluates progress, routes work, manages loops, surfaces uncertainty, coordinates parallel execution |
| **Planner Agent** | Topic Decomposition | Breaks topic into 6–10 high-quality sub-questions, self-reflects on coverage and overlap, refines plan |
| **Researcher Agent** | Deep Web Research | Tool-using agent that generates queries (Tavily), selects & scrapes URLs, reflects on source quality, requests more resources if needed |
| **Extractor Agent** | Fact Extraction | Converts clean text into structured facts, filters noise, flags uncertain extractions |
| **Validator Agent** | Fact Validation & Cross-Checking | Applies credibility rubric, detects contradictions, scores facts, requests additional sources for weak claims |
| **Synthesizer Agent** | Knowledge Synthesis | Builds logical report outline, calculates overall confidence, identifies gaps, recommends next actions |
| **Reporter Agent** | Final Report Generation | Creates well-cited Markdown report and converts it to professional PDF (only after HITL approval) |
| **Human (HITL)** | Quality Gate & Strategic Agent | Reviews outline, confidence, contradictions, and sample facts. Can approve, reject with feedback, or edit |

---

## Agentic Workflow

```mermaid
flowchart TD
    A[User Submits Topic] --> B[Supervisor Agent Starts Job]
    B --> C[Planner Agent]
    C --> D[Supervisor Evaluates]
    D --> E[Researcher Agents Parallel]
    E --> F[Extractor Agents]
    F --> G[Validator Agent]
    G --> H[Synthesizer Agent]
    H --> I[Supervisor Decision Point]
    I -->|Quality Low + Iterations < 2| C
    I -->|Ready or Max Iterations| J[HITL Checkpoint]
    J -->|Reject + Feedback| C
    J -->|Edit / Approve| K[Reporter Agent]
    K --> L[PDF Report Delivered]