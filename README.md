# AgentOps Lite

Lightweight agentic AI system demonstrating LLM tool-calling, enterprise workflow automation, and observable agent execution patterns.

## Overview

AgentOps Lite is a prototype AI agent designed to simulate enterprise customer support workflows. The system uses an LLM-powered decision engine to dynamically select and execute tools, enabling action-oriented responses rather than traditional chatbot-style interactions.

The project demonstrates core concepts behind modern agentic systems, including:

* LLM tool calling
* Multi-step reasoning loops
* Enterprise workflow automation
* Structured agent observability
* CRM-style support operations

## Architecture

```text
            ┌──────────────────────┐
            │   User Query         │
            └─────────┬────────────┘
                      │
                      ▼
        ┌───────────────────────────┐
        │   LLM Agent               │
        │  - Reasoning              │
        │  - Tool Selection         │
        └─────────┬─────────────────┘
                  │
                  ▼
     ┌──────────────────────────────┐
     │  Tool Execution Layer        │
     │  - Order Lookup              │
     │  - Refund Processing         │
     │  - Ticket Creation           │
     └─────────┬────────────────────┘
               │
               ▼
     ┌──────────────────────────────┐
     │  Observation & Trace Layer   │
     └─────────┬────────────────────┘
               │
               ▼
     ┌──────────────────────────────┐
     │  Final Response              │
     │  + Execution Trace           │
     └──────────────────────────────┘
```

## Features

### Agentic Decision Making

The agent evaluates user requests and determines which actions should be taken using available tools.

### Tool Calling

Supports dynamic execution of business functions such as:

* Order status retrieval
* Refund processing
* Support ticket creation

### Observability

Every execution generates a structured trace containing:

* Tool calls
* Arguments
* Results
* Final response

### Enterprise Workflow Simulation

Models common customer support workflows found in CRM and service operations environments.

## Example Agent Workflow

The repository includes a complete example execution trace:
examples/refund_workflow_trace.json

### Agent Actions

1. Retrieve order status
2. Verify eligibility
3. Process refund
4. Generate customer response

### Output

```json
{
  "tool": "issue_refund",
  "order_id": "1001",
  "refund_status": "approved"
}
```

## Project Structure

```text
agentops-lite/
├── README.md
├── requirements.txt
├── .env.example
├── src/
├── data/
├── examples/
└── diagrams/
```

## Tech Stack

* Python
* OpenAI API
* Function Calling
* JSON Tool Schemas

## Future Improvements

* Multi-agent workflows
* Human-in-the-loop escalation
* Vector database memory
* Web UI dashboard
* CRM integration layer

## Motivation

This project was built to explore how modern AI agents move beyond conversational interfaces and interact directly with business workflows through structured tool execution and reasoning loops.

### Note :
The demo uses the Gemini free tier, so API rate limits may apply during repeated testing.
