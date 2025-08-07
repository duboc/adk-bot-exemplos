# ADK Bot Exemplos

A comprehensive collection of Google Agent Development Kit (ADK) examples demonstrating different architectural patterns and advanced features for building intelligent agents.

## 🎯 Overview

This project showcases **16 different agent implementation patterns** using Google ADK, featuring two business domains:

- **🌿 Natura**: Brazilian cosmetics company refund processing system
- **🍔 CRF (Comida Rápida Fantástica)**: Fast food ordering system with "Félix" character

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

## 🛠️ Technical Stack

- **Framework**: Google Agent Development Kit (ADK)
- **Language**: Python 3.x
- **Models**: Gemini 2.5 Flash, Gemini 2.5 Pro
- **Cloud Services**: Google Cloud Logging, Cloud Trace, Vertex AI
- **Tools**: Custom business logic functions for each domain

## 🚀 Quick Start

### Prerequisites
```bash
pip install -r src/requirements.txt
```

### Environment Setup
1. Configure Google Cloud credentials
2. Set up `.env` file with required API keys
3. Enable required Google Cloud APIs:
   - Vertex AI API
   - Cloud Trace API (for Example 7)
   - Cloud Logging API (for Example 8)

### Running Examples

To run any example, you can execute the `main()` function in the respective `agent.py` file.

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
│   └── tools/
├── README.md
└── LICENSE
```

## 🤝 Contributing

Each example is self-contained and can be extended independently. When adding new patterns:

1. Follow the established naming convention (`N-description/`)
2. Include proper logging and error handling
3. Update this README with the new example

## 📄 License

See [LICENSE](LICENSE) file for details.

---

**Note**: This project demonstrates various ADK patterns for educational purposes. Adapt the examples to your specific use cases and production requirements.