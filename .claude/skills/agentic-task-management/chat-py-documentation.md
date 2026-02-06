# 10-Message Stateless History Fetcher Documentation

## Overview
The `chat.py` file implements a conversation system with a stateless history fetcher that retrieves the last 10 messages from a conversation. This enables the AI to maintain context during conversations without storing long-term state in memory.

## Key Components

### History Retrieval Logic
```python
stmt = (
    select(Message)
    .where(Message.conversation_id == conversation.id)
    .order_by(Message.created_at.desc())
    .limit(10)
)

history = list(reversed(session.exec(stmt).all()))
```

### How It Works
1. When a user sends a message, the system identifies the conversation using `conversation_id`
2. It queries the database for the 10 most recent messages in that conversation
3. The messages are retrieved in descending chronological order (most recent first)
4. The list is reversed to restore chronological order (oldest to newest)
5. These messages are formatted as role-content pairs and sent to the AI model

### Stateless Nature
- The system does not maintain in-memory conversation state
- Each request independently fetches the last 10 messages from the database
- This approach ensures scalability and reliability across server restarts
- Limits conversation context to the last 10 messages to maintain performance

### Integration with AI Model
- The retrieved history is prepended to the current request before sending to the AI
- The system includes a system prompt that guides the AI's behavior
- Tool calls are preserved in the history to maintain context of previous actions

## Benefits
- Scalable: No memory overhead for maintaining conversation state
- Reliable: Survives server restarts and crashes
- Performant: Limited history prevents oversized requests to the AI
- Consistent: Same history is available regardless of which server instance handles the request