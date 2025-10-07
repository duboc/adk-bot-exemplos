# Memory Management Example

This example demonstrates how to use ADK's **MemoryService** to give agents long-term memory that persists across conversations.

## 📚 What You'll Learn

Based on the [official ADK memory documentation](https://google.github.io/adk-docs/sessions/memory/), this example shows:

1. **Memory Basics**: Understanding long-term knowledge vs. session state
2. **load_memory Tool**: Using the built-in tool to search past conversations
3. **Auto-Save Pattern**: Using `after_agent_callback` to automatically save sessions
4. **Memory Services**: InMemoryMemoryService vs. VertexAiMemoryBankService

## 🏗️ Project Structure

```
19-memory-example/
├── agent.py              # Memory-aware agent with load_memory tool + auto-save callback
├── tools/
│   └── __init__.py
└── README.md             # This file
```

---

## 🚀 Running the Example

### Method 1: With InMemoryMemoryService (Quick Testing)

For local testing without any setup:

```bash
# From the project root
adk web src/19-memory-example/agent.py
```

**Test the memory:**

1. **First conversation** - Share information:
   ```
   👤 "Olá! Meu nome é Maria e tenho pele seca."
   👤 "Eu adoro produtos com lavanda!"
   ```

2. **Refresh the page** (starts a new session, but memory persists in the process)

3. **Second conversation** - Test recall:
   ```
   👤 "Olá! Você se lembra de mim?"
   👤 "Qual é o meu tipo de pele?"
   ```

The agent uses `load_memory` to recall information from the first conversation! 🎉

**Note**: Memory persists while the server is running. When you stop `adk web`, memory is lost.

---

### Method 2: With VertexAiMemoryBankService (Production - Persistent)

For persistent memory using Google Agent Engine:

#### Prerequisites:
1. Google Cloud Project with Vertex AI enabled
2. Agent Engine instance created
3. Environment variables configured

#### Setup:

```bash
# 1. Configure environment
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_LOCATION="us-central1"

# 2. Set up .env file
cp .env.local .env
# Edit .env and set: MEMORY_SERVICE_URI=agentengine://YOUR_RESOURCE_ID

# 3. Run with persistent memory
source .env
adk web src/19-memory-example/agent.py --memory_service_uri="$MEMORY_SERVICE_URI"
```

**Benefits:**
- ✅ Memory persists across server restarts
- ✅ Semantic search (better than keyword matching)
- ✅ Managed by Google Cloud
- ✅ Production-ready

---

## 🎯 Key Concepts

### Memory vs. State

| Feature | Session State | Memory (MemoryService) |
|---------|--------------|------------------------|
| **Scope** | Current conversation | Across all conversations |
| **Purpose** | Temporary scratchpad | Long-term knowledge store |
| **Access** | Direct via `state` | Search via `load_memory` tool |
| **Lifecycle** | Lives with session | Persists indefinitely |
| **Example** | Shopping cart items | Customer preferences from last month |

### The `load_memory` Tool

ADK provides a built-in tool for searching memory:

```python
from google.adk.tools import load_memory

# Give it to your agent
agent = LlmAgent(
    tools=[load_memory],
    instruction="Use load_memory to recall past conversations..."
)
```

**How it works:**
- Agent calls `load_memory(query="customer preferences")`
- MemoryService searches past sessions
- Returns relevant conversation snippets
- Agent uses results to personalize responses

### Auto-Save Pattern

The example uses `after_agent_callback` to automatically save sessions to memory:

```python
async def auto_save_session_to_memory_callback(callback_context):
    await callback_context._invocation_context.memory_service.add_session_to_memory(
        callback_context._invocation_context.session
    )

agent = LlmAgent(
    tools=[load_memory],
    after_agent_callback=auto_save_session_to_memory_callback
)
```

This ensures every conversation is automatically stored for future retrieval!

---

## 💡 Example Interactions

### Interaction 1: Building Memory
```
👤 You: "Olá! Meu nome é Ana e tenho 28 anos."
🤖 Agent: "Olá Ana! 🌸 Bem-vinda à Essencia! Como posso ajudá-la?"

👤 You: "Tenho pele oleosa e gosto de produtos naturais."
🤖 Agent: "Perfeito! Vou anotar suas preferências... ✨"
```

Session is automatically saved to memory via `after_agent_callback`.

### Interaction 2: Recalling Memory (New Session)
```
👤 You: "Olá! Você se lembra de mim?"
🤖 Agent: [Uses load_memory tool]
         "Claro que sim, Ana! 💄 Você tem pele oleosa e gosta de produtos naturais..."

👤 You: "Me recomenda um produto para controle de oleosidade"
🤖 Agent: "Para sua pele oleosa, recomendo..."
```

---

## 📝 Code Example

Here's the complete agent implementation:

```python
from google.adk.agents import LlmAgent
from google.adk.tools import load_memory

# Callback to auto-save sessions
async def auto_save_session_to_memory_callback(callback_context):
    await callback_context._invocation_context.memory_service.add_session_to_memory(
        callback_context._invocation_context.session
    )

# Memory-aware agent
root_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="MemoryAwareEssenciaAgent",
    description="Essencia customer service agent with long-term memory",
    instruction="""
    Você é um assistente da Essencia com memória de longo prazo.

    Use a ferramenta 'load_memory' para:
    - Relembrar preferências de clientes
    - Buscar conversas anteriores
    - Personalizar recomendações

    Seja caloroso e demonstre que você se lembra do cliente! 💄✨
    """,
    tools=[load_memory],
    after_agent_callback=auto_save_session_to_memory_callback
)
```

---

## 🔍 InMemoryMemoryService vs VertexAiMemoryBankService

| Feature | InMemoryMemoryService | VertexAiMemoryBankService |
|---------|----------------------|---------------------------|
| **Persistence** | None (lost on restart) | Yes (managed by Vertex AI) |
| **Setup** | None | Requires Agent Engine |
| **Search** | Basic keyword matching | Semantic search |
| **Use Case** | Prototyping, testing | Production deployments |
| **Cost** | Free | Google Cloud pricing |

---

## ⚠️ Best Practices

### ✅ DO:
- Use `load_memory` when users mention past interactions
- Let `after_agent_callback` handle memory saves automatically
- Use descriptive queries: `"customer skin type"` not just `"skin"`
- Test memory with page refreshes (new sessions)

### ❌ DON'T:
- Don't manually call `add_session_to_memory` in tools (use callback)
- Don't assume memory persists without Agent Engine
- Don't query memory on every turn (let agent decide when needed)

---

## 🔗 Related Examples

- **[Example 18 - Session State](../18-session-state-example)**: Short-term state management
- **[Example 1 - Single Agent](../1-llm-single-agent)**: Basic agent without memory
- **[Example 11 - After Agent Callback](../11-agent-after-callback)**: Callback patterns

---

## 📖 Further Reading

- [ADK Memory Documentation](https://google.github.io/adk-docs/sessions/memory/)
- [ADK Session State Documentation](https://google.github.io/adk-docs/sessions/state/)
- [Agent Engine Documentation](https://cloud.google.com/vertex-ai/docs/agent-builder)

---

## 💡 Next Steps

Try extending this example:

1. **Combine with State**: Use both session state (Example 18) and memory together
2. **Add More Tools**: Give the agent tools to save specific information types
3. **Implement Forgetting**: Add logic to clear old or irrelevant memories
4. **User Profiles**: Build comprehensive user profiles across sessions
5. **Deploy to Production**: Use VertexAiMemoryBankService for real applications

---

## 🎉 Summary

This example demonstrates:

- ✅ **load_memory tool** for searching past conversations
- ✅ **after_agent_callback** for automatic memory saves
- ✅ **Memory persistence** across sessions and restarts (with Agent Engine)
- ✅ **InMemoryMemoryService** for quick testing
- ✅ **VertexAiMemoryBankService** for production use

**Key Takeaway**: Memory enables agents to build context over time, creating more personalized and intelligent interactions! 🧠✨
