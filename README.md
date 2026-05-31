# Agentops-lite
Lightweight agentic AI system demonstrating LLM tool-calling, enterprise workflow automation, and observable agent execution patterns.

## Topics 
- ai-agents
- llm
- agentic-ai
- python
- openai
- tool-calling
- prompt-engineering
- generative-ai

## Website 

## Architecture
            ┌──────────────────────┐
            │   User Query         │
            └─────────┬────────────┘
                      │
                      ▼
        ┌───────────────────────────┐
        │   LLM Agent (GPT-4.1)     │
        │  - Reasoning              │
        │  - Tool Selection         │
        └─────────┬─────────────────┘
                  │ tool call
                  ▼
     ┌──────────────────────────────┐
     │  Tool Execution Layer        │
     │  - get_order_status          │
     │  - issue_refund              │
     │  - create_ticket             │
     └─────────┬────────────────────┘
               │ result
               ▼
     ┌──────────────────────────────┐
     │  Observation Loop            │
     │  (LLM re-evaluates state)    │
     └─────────┬────────────────────┘
               │
               ▼
     ┌──────────────────────────────┐
     │  Final Response + Trace      │
     │  - Output                    │
     │  - Tool History              │
     └──────────────────────────────┘
