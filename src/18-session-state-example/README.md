# Session State Management Example

This example demonstrates how to use **session state** in Google's Agent Development Kit (ADK) to build stateful, context-aware conversational agents.

## 📚 What You'll Learn

Based on the [official ADK session state documentation](https://google.github.io/adk-docs/sessions/state/), this example shows:

1. **Session State Basics**: Using `session.state` as a scratchpad for dynamic data
2. **State Scopes**: Different prefixes for session, user, app, and temporary state
3. **State Injection**: Using `{key}` templating in agent instructions
4. **Tool Integration**: Using the `tool_context` parameter to access state
5. **State Persistence**: How state is tracked and updated across interactions

## 🏗️ Project Structure

```
18-session-state-example/
├── agent.py              # Agent with state-aware instructions
├── tools/
│   ├── __init__.py
│   └── state_tools.py    # Tools using tool_context parameter
├── quick_test.py         # Test to verify tool_context injection
└── README.md             # This file
```

---

## 🚀 Running the Example

### Method 1: ADK Web Interface (Recommended)

```bash
# From the project root
adk web src/18-session-state-example/agent.py
```

This starts the ADK web interface at http://localhost:8000 where you can interact with the agent.

### Method 2: Run the Test

Verify that the `tool_context` injection is working:

```bash
cd src/18-session-state-example
python quick_test.py
```

---

## 🎯 Key Concepts

### State Scopes

State keys use prefixes to define their scope and persistence:

| Prefix | Scope | Persistence | Use Case |
|--------|-------|-------------|----------|
| *(none)* | Current session | With persistent services | Conversation-specific data |
| `user:` | All sessions for a user | With persistent services | User preferences, profile |
| `app:` | All users and sessions | With persistent services | Global settings, shared data |
| `temp:` | Current invocation only | **Never persisted** | Intermediate calculations |

### State Injection in Instructions

Use `{key}` syntax to inject state values directly into agent instructions:

```python
agent_instruction = """
Hello {user:name}!
Your skin type is: {user:skin_type}
Preferences: {user:favorite_category?}
"""
```

- `{key}` - Required key (errors if missing)
- `{key?}` - Optional key (empty string if missing)

### The `tool_context` Pattern

**Important Discovery**: ADK automatically injects `ToolContext` when you name a parameter exactly `tool_context`:

```python
def save_preference(preference_key: str, preference_value: str, tool_context: ToolContext) -> str:
    """
    The tool_context parameter is automatically injected by ADK.
    It's NOT sent to the LLM for function calling.
    """
    # Read state
    user_name = tool_context.state.get("user:name", "Guest")

    # Write state
    tool_context.state[f"user:{preference_key}"] = preference_value
    tool_context.state["temp:processing"] = True

    return "Saved!"
```

**How it works:**
- When `FunctionTool` sees a parameter named `tool_context`, it automatically injects it
- The parameter is **filtered out** from the function declaration sent to the LLM
- This allows tools to access state without confusing the LLM's function calling

---

## 💡 Example Interactions

Try these in the ADK web interface:

### Interaction 1: Save User Preferences
```
👤 You: "Olá! Meu nome é Maria e meu tipo de pele é seca."
🤖 Agent: Calls save_user_preference("name", "Maria")
         Calls save_user_preference("skin_type", "seca")
         State: user:name = "Maria", user:skin_type = "seca"
```

### Interaction 2: Personalized Recommendations
```
👤 You: "Me recomenda produtos para hidratação"
🤖 Agent: Calls get_product_recommendation("hidratante")
         Reads user:skin_type from state → returns products for dry skin
         State: last_recommendation_category = "hidratante"
```

### Interaction 3: Track Engagement
```
👤 You: "Gostei! Quero comprar o creme."
🤖 Agent: Calls track_interaction("purchase", "...")
         Updates all state scopes:
         - session: current_interaction_type = "purchase"
         - user: total_interactions += 1
         - app: total_customer_interactions += 1
         - temp: processing_timestamp (discarded after response)
```

### Interaction 4: New Session (Test Persistence)
```
Refresh the page (new session) and type:
👤 You: "Olá!"
🤖 Agent: Greets "Olá, Maria!"
         user: state persists! ✅
         session: state is fresh (new conversation) ✅
```

---

## 📝 Code Examples

### 1. State-Aware Agent ([agent.py](agent.py))

```python
agent_instruction = """
Você é um assistente da Essencia.

🌟 INFORMAÇÕES DO CLIENTE (do estado da sessão):
- Nome: {user:name?}
- Tipo de pele: {user:skin_type?}

Quando o cliente mencionar preferências:
- Use save_user_preference(preference_key, preference_value)

Para fazer recomendações:
- Use get_product_recommendation(category)
"""

root_agent = LlmAgent(
    model="gemini-2.5-flash",
    instruction=agent_instruction,
    tools=[save_user_preference, get_product_recommendation, track_interaction],
    output_key="last_response",  # Auto-saves response to state
)
```

### 2. State-Aware Tool ([tools/state_tools.py](tools/state_tools.py))

```python
def save_user_preference(
    preference_key: str,
    preference_value: str,
    tool_context: ToolContext  # ← Automatically injected!
) -> str:
    """Save user preference to state."""

    # Use user: prefix for user-scoped state
    tool_context.state[f"user:{preference_key}"] = preference_value

    # Update interaction count
    count = tool_context.state.get("user:interaction_count", 0)
    tool_context.state["user:interaction_count"] = count + 1

    return f"✅ Preferência '{preference_key}' salva!"
```

---

## 🎨 Common State Patterns

### Pattern 1: User Profile Management
```python
def save_profile(name: str, email: str, tool_context: ToolContext):
    tool_context.state["user:name"] = name
    tool_context.state["user:email"] = email
    return "Profile saved!"
```

### Pattern 2: Shopping Cart
```python
def add_to_cart(product_id: str, quantity: int, tool_context: ToolContext):
    cart = tool_context.state.get("shopping_cart", [])
    cart.append({"product_id": product_id, "quantity": quantity})
    tool_context.state["shopping_cart"] = cart
    return f"Added! Total items: {len(cart)}"
```

### Pattern 3: Conversation Context
```python
def track_topic(topic: str, step: int, tool_context: ToolContext):
    tool_context.state["current_topic"] = topic
    tool_context.state["conversation_step"] = step
```

### Pattern 4: Global Configuration
```python
def set_config(tool_context: ToolContext):
    tool_context.state["app:api_version"] = "v2"
    tool_context.state["app:discount_code"] = "SAVE2025"
```

### Pattern 5: Temporary Processing
```python
def process_data(data: dict, tool_context: ToolContext):
    # Temp state - discarded after invocation
    tool_context.state["temp:raw_input"] = data
    tool_context.state["temp:timestamp"] = datetime.now().isoformat()

    # Session state - persists
    result = calculate(data)
    tool_context.state["last_result"] = result
    return result
```

---

## ⚠️ Best Practices

### ✅ DO:
- Use the exact parameter name `tool_context` to get automatic injection
- Use descriptive key names with appropriate prefixes
- Store only serializable data (strings, numbers, booleans, simple lists/dicts)
- Use `temp:` for data that shouldn't persist
- Use `.get()` or `{key?}` to handle missing keys gracefully

### ❌ DON'T:
- Don't use `context` or `ctx` - must be exactly `tool_context`
- Don't store complex objects or class instances
- Don't directly modify `session.state` on retrieved sessions (bypasses tracking)
- Don't use deep nesting excessively

### State Persistence

This example uses `InMemorySessionService`:
- ✅ State persists **within the same process**
- ❌ State is **lost on restart**

For production, use:
- `DatabaseSessionService`: Persists to database
- `VertexAiSessionService`: Persists to Google Cloud

---

## 🧪 Testing

Run the test to verify `tool_context` injection:

```bash
python quick_test.py
```

**Expected output:**
```
✅ FunctionTool correctly hides tool_context from LLM
✅ tool_context is injected when calling tools
✅ save_user_preference saves to user: state
✅ get_product_recommendation reads from state
✅ track_interaction uses all 4 state scopes
🎉 ALL TESTS PASSED!
```

---

## 🔍 State Scope Decision Tree

```
Need to store data?
│
├─ Should it persist after invocation?
│  ├─ No → Use temp: prefix
│  └─ Yes ↓
│
├─ Should it persist across sessions?
│  ├─ No → Use no prefix (session-scoped)
│  └─ Yes ↓
│
├─ Is it user-specific?
│  ├─ Yes → Use user: prefix
│  └─ No ↓
│
└─ Is it shared across all users?
   ├─ Yes → Use app: prefix
   └─ Reconsider if state is the right solution
```

---

## 🔗 Related Examples

- **[1-llm-single-agent](../1-llm-single-agent)**: Basic agent without state
- **[3-workflow-sequential-multi-agent](../3-workflow-sequential-multi-agent)**: Sequential agents with state
- **[4-workflow-parallel-multi-agent](../4-workflow-parallel-multi-agent)**: Parallel agents with state

---

## 📖 Further Reading

- [ADK Session State Documentation](https://google.github.io/adk-docs/sessions/state/)
- [ADK Session Documentation](https://google.github.io/adk-docs/sessions/session/)
- [ADK Context Documentation](https://google.github.io/adk-docs/sessions/context/)
- [ADK Quickstart](https://google.github.io/adk-docs/get-started/quickstart/)

---

## 💡 Next Steps

Try extending this example:

1. Add more user preferences (language, budget range, allergies)
2. Implement a full shopping cart with checkout
3. Track conversation sentiment over time
4. Add app-level analytics (most popular products, peak hours)
5. Use a persistent `SessionService` for production
6. Add user authentication state
7. Implement multi-step workflows with state tracking

---

## 🎉 Summary

This example demonstrates:

- ✅ **State injection** in instructions using `{key}` and `{key?}`
- ✅ **The `tool_context` pattern** for accessing state in tools
- ✅ **All 4 state scopes**: session, user, app, and temp
- ✅ **State persistence** across interactions and sessions
- ✅ **output_key** for automatic response storage

**Key Takeaway**: The `tool_context` parameter name is the magic that enables state management in ADK tools! 🪄
