# ADK Bot Exemplos

A comprehensive collection of Google Agent Development Kit (ADK) examples demonstrating different architectural patterns and advanced features for building intelligent agents.

## 🎯 Overview

This project showcases **19 different agent implementation patterns** using Google ADK, featuring three business domains:

- **🌿 Natura**: Brazilian cosmetics company refund processing system
- **🍔 CRF (Comida Rápida Fantástica)**: Fast food ordering system with "Félix" character
- **💄 Essencia**: Brazilian cosmetics company for state management and memory examples

## 🏗️ Agent Examples

### Basic Patterns (Examples 1-5)

#### 1. Single Agent (`src/1-llm-single-agent/`)
**Pattern**: Monolithic approach with one agent handling the entire workflow
- **Domain**: Natura refund system
- **Tools**: `get_purchase_history`, `check_refund_eligibility`, `process_refund`
- **Use Case**: Simple, straightforward interactions where one agent can handle all tasks
- **Model**: `gemini-2.5-flash`

```python
root_agent = Agent(
    model=GEMINI_MODEL,
    name="RefundSingleAgent",
    description="Customer refund single-agent for Natura company",
    instruction=top_level_prompt,
    tools=[get_purchase_history, check_refund_eligibility, process_refund],
)
```

#### 2. Multi LLM Agent (`src/2-llm-multi-agent/`)
**Pattern**: Coordinator/Dispatcher pattern with multiple specialized agents
- **Domain**: Natura refund system
- **Architecture**: Multiple agents with different specializations
- **Use Case**: Complex workflows requiring different expertise areas

#### 3. Sequential Workflow (`src/3-workflow-sequential-multi-agent/`)
**Pattern**: Linear pipeline where agents execute in sequence
- **Domain**: Code generation pipeline (Write, Review, Refactor)
- **Architecture**: Step-by-step processing with defined order
- **Use Case**: Workflows with clear dependencies and sequential steps

#### 4. Parallel Workflow (`src/4-workflow-parallel-multi-agent/`)
**Pattern**: Concurrent processing with multiple agents working simultaneously
- **Domain**: Natura refund system
- **Architecture**: Parallel execution for independent tasks
- **Use Case**: Tasks that can be processed concurrently for better performance

#### 5. Custom Control Flow (`src/5-custom-agent-control-flow/`)
**Pattern**: Custom orchestration logic with conditional branching
- **Domain**: Natura refund system
- **Architecture**: Dynamic workflow control based on conditions
- **Use Case**: Complex business logic requiring custom decision trees

### Advanced Features & Callbacks (Examples 6-16)

#### 6. Live Agent (`src/6-llm-live/`)
**Pattern**: Real-time interactive conversational agent
- **Domain**: CRF fast food ordering system
- **Character**: Félix - enthusiastic Spanish-speaking assistant
- **Tools**: `finalize_order`, `get_menu_item_info`
- **Model**: `gemini-2.0-flash-live-preview-04-09`
- **Features**: Real-time conversation, personality-driven interactions

#### 7. Agent with Tracing (`src/7-agent-with-trace/`)
**Pattern**: Single agent with ADK execution tracing enabled
- **Domain**: Natura refund system
- **Features**: Execution monitoring and trace collection
- **Technology**: `AdkApp` with `enable_tracing=True`
- **Use Case**: Debugging, performance monitoring, execution analysis

#### 8. Agent with Logging (`src/8-agent-with-log/`)
**Pattern**: Single agent with Google Cloud Logging integration
- **Domain**: Natura refund system
- **Features**: Structured logging, cloud integration, event tracking
- **Technology**: `google.cloud.logging`
- **Use Case**: Production monitoring, analytics, audit trails

#### 9. Agent with URL Context (`src/9-agent-url-context/`)
**Pattern**: Agent that can analyze content from a URL.
- **Domain**: Web content analysis
- **Tools**: `analyze_url_content`
- **Use Case**: Summarizing articles, extracting information from websites.

#### 10. Agent with Before Agent Callback (`src/10-agent-before-callback/`)
**Pattern**: Demonstrates the `before_agent_callback` to control agent execution.
- **Theme**: Magic 8-Ball with mood control.
- **Feature**: The callback can skip the agent's execution based on session state.

#### 11. Agent with After Agent Callback (`src/11-agent-after-callback/`)
**Pattern**: Demonstrates the `after_agent_callback` to review and improve agent responses.
- **Theme**: Restaurant reviewer with an LLM auditor.
- **Feature**: A callback uses an LLM auditor for quality control of the agent's output.

#### 12. Agent with Before Model Callback (`src/12-before-model-callback/`)
**Pattern**: Demonstrates the `before_model_callback` to implement content filtering.
- **Theme**: Content filter with guardrails.
- **Feature**: The callback filters inappropriate content before it reaches the LLM.

#### 13. Agent with After Model Callback (`src/13-after-model-callback/`)
**Pattern**: Demonstrates the `after_model_callback` for post-processing LLM responses.
- **Theme**: Translation service with quality improvement.
- **Feature**: The callback uses an LLM auditor to improve translation quality.

#### 14. Agent with Before Tool Callback (`src/14-before-tool-callback/`)
**Pattern**: Demonstrates the `before_tool_callback` for permission checks.
- **Theme**: Weather service with permission checks and rate limiting.
- **Feature**: The callback implements permission checks before tool execution.

#### 15. Agent with After Tool Callback (`src/15-after-tool-callback/`)
**Pattern**: Demonstrates the `after_tool_callback` for validating and enhancing tool results.
- **Theme**: Calculator service with result validation.
- **Feature**: The callback validates and enhances calculation results.

#### 16. Agent with Image Handling (`src/16-image-handling/`)
**Pattern**: Agent specialized in comprehensive image analysis.
- **Features**: Can save, list, show and analyze images using Gemini.
- **Use Case**: Image description, object recognition, etc.

### State Management & Memory (Examples 18-19)

#### 18. Session State Management (`src/18-session-state-example/`)
**Pattern**: Stateful conversational agent with session state tracking
- **Domain**: Essencia customer service
- **Features**: Session, user, app, and temporary state scopes
- **Tools**: `save_user_preference`, `get_product_recommendation`, `track_interaction`
- **Key Concept**: Using `tool_context` parameter for state access
- **State Injection**: `{key}` syntax in agent instructions
- **Use Case**: Personalized customer interactions with preference tracking

```python
def save_user_preference(
    preference_key: str,
    preference_value: str,
    tool_context: ToolContext  # Auto-injected by ADK
) -> str:
    tool_context.state[f"user:{preference_key}"] = preference_value
    return "Saved!"
```

**Run**: `adk web src/18-session-state-example/agent.py`

#### 19. Memory Management (`src/19-memory-example/`)
**Pattern**: Agent with long-term memory across conversations
- **Domain**: Essencia customer service
- **Features**: InMemoryMemoryService, load_memory tool
- **Tools**: `load_memory` (built-in ADK tool)
- **Key Concept**: Memory vs. State - long-term knowledge vs. temporary scratchpad
- **Use Case**: Agents that remember customer interactions across sessions

```python
agent = LlmAgent(
    model="gemini-2.5-flash",
    tools=[load_memory],  # Built-in ADK tool
    instruction="Use load_memory to recall past conversations..."
)

# Store session in memory
await memory_service.add_session_to_memory(session)
```

**Run**: `adk web src/19-memory-example/agent.py`

## 🛠️ Technical Stack

- **Framework**: Google Agent Development Kit (ADK)
- **Language**: Python 3.x
- **Models**: Gemini 2.5 Flash, Gemini 2.5 Pro, Gemini 2.0 Flash Live
- **Cloud Services**: Google Cloud Logging, Cloud Trace, Vertex AI
- **State Management**: ADK Session State, Memory Services
- **Tools**: Custom business logic functions for each domain

## 🚀 Quick Start

### Prerequisites
```bash
pip install -r src/requirements.txt
```

### Environment Setup

1. **Configure Google Cloud credentials**
   ```bash
   gcloud auth application-default login
   ```

2. **Set up `.env` file**
   ```bash
   # Copy the template
   cp .env.local .env

   # Edit .env and add your Agent Engine resource ID
   # MEMORY_SERVICE_URI=agentengine://YOUR_RESOURCE_ID
   ```

3. **Enable required Google Cloud APIs**:
   - Vertex AI API
   - Agent Engine API (for Example 19 - Memory)
   - Cloud Trace API (for Example 7)
   - Cloud Logging API (for Example 8)

### Running Examples

#### Using ADK Web Interface (Basic)
```bash
# Run examples without memory service
adk web src/{example-name}/agent.py

# Examples:
adk web src/1-llm-single-agent/agent.py
adk web src/18-session-state-example/agent.py
```

#### Using ADK Web Interface with Memory Service (Example 19)
```bash
# Load environment variables and run with memory service
source .env
adk web src/19-memory-example/agent.py --memory_service_uri="$MEMORY_SERVICE_URI"

# Or directly:
adk web src/19-memory-example/agent.py --memory_service_uri="agentengine://YOUR_RESOURCE_ID"
```

#### Programmatic Execution
You can also execute the `main()` function in the respective `agent.py` file, or run demo scripts where available.

## 📁 Project Structure

```
adk-bot-exemplos/
├── src/
│   ├── 1-llm-single-agent/
│   ├── 2-llm-multi-agent/
│   ├── 3-workflow-sequential-multi-agent/
│   ├── 4-workflow-parallel-multi-agent/
│   ├── 5-custom-agent-control-flow/
│   ├── 6-llm-live/
│   ├── 7-agent-with-trace/
│   ├── 8-agent-with-log/
│   ├── 9-agent-url-context/
│   ├── 10-agent-before-callback/
│   ├── 11-agent-after-callback/
│   ├── 12-before-model-callback/
│   ├── 13-after-model-callback/
│   ├── 14-before-tool-callback/
│   ├── 15-after-tool-callback/
│   ├── 16-image-handling/
│   ├── 18-session-state-example/
│   ├── 19-memory-example/
│   └── tools/
├── README.md
└── LICENSE
```

## 🎓 Learning Path

### For Beginners
1. Start with **Example 1** (Single Agent) - Understand basic agent structure
2. Move to **Example 18** (Session State) - Learn stateful conversations
3. Try **Example 19** (Memory) - Understand long-term memory

### For Intermediate Users
4. Explore **Example 3** (Sequential) and **Example 4** (Parallel) - Multi-agent patterns
5. Study **Examples 10-15** (Callbacks) - Advanced control flow
6. Experiment with **Example 6** (Live Agent) - Real-time interactions

### For Advanced Users
7. Implement **Example 7** (Tracing) and **Example 8** (Logging) - Production monitoring
8. Build custom patterns combining multiple examples

## 🤝 Contributing

Each example is self-contained and can be extended independently. When adding new patterns:

1. Follow the established naming convention (`N-description/`)
2. Include proper logging and error handling
3. Add comprehensive README.md to the example directory
4. Update this main README with the new example

## 📄 License

See [LICENSE](LICENSE) file for details.

---

**Note**: This project demonstrates various ADK patterns for educational purposes. Adapt the examples to your specific use cases and production requirements.
