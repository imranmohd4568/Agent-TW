# Agent-TW

```mermaid
graph TD
    A[Start] -->|Feedback Collected| B[Extract Key Points]
    B --> C{Check for LLM Processing}
    C -->|Yes| D[Analyze Sentiment & Urgency]
    C -->|No| E[Store Raw Feedback in DB]

    D -->|Negative & Urgent| F[Escalate to Human Support]
    D -->|Neutral| G[Store in DB for Trends & Reports]
    D -->|Positive| H[Thank User & Store in DB]

    F --> I[Notify Support Team]
    I --> J[Human Responds & Closes Issue]
    H --> L[End Process]

    E --> M[Generate Insights Later]
    M --> K
