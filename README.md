# ADK Bot Exemplos

A comprehensive collection of Google Agent Development Kit (ADK) examples demonstrating different architectural patterns and advanced features for building intelligent agents.

## 🎯 Overview

This project showcases **8 different agent implementation patterns** using Google ADK, featuring two business domains:

- **🌿 Natura**: Brazilian cosmetics company refund processing system
- **🍔 CRF (Comida Rápida Fantástica)**: Fast food ordering system with "Félix" character

## 🏗️ Agent Examples

### Basic Patterns (Examples 1-5)

#### 1. Single Agent (`src/1-llm-single-agent/`)
**Pattern**: Monolithic approach with one agent handling the entire workflow
- **Domain**: Natura refund system
- **Tools**: `get_purchase_history`, `check_refund_eligibility`, `process_refund`
- **Use Case**: Simple, straightforward interactions where one agent can handle all tasks
- **Model**: `gemini-2.5-flash-preview-05-20`

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
- **Domain**: Natura refund system
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

### Advanced Features (Examples 6-8)

#### 6. Live Agent (`src/6-llm-live/`)
**Pattern**: Real-time interactive conversational agent
- **Domain**: CRF fast food ordering system
- **Character**: Félix - enthusiastic Spanish-speaking assistant
- **Tools**: `finalize_order`, `get_menu_item_info`
- **Model**: `gemini-2.0-flash-live-preview-04-09`
- **Features**: Real-time conversation, personality-driven interactions

```python
root_agent = Agent(
    model=GEMINI_MODEL,
    name="FelixCRF",
    description="Félix, el Amigo del Sabor - Fast food ordering agent",
    instruction=felix_crf_agent['personality'],
    tools=[finalize_order, get_menu_item_info],
)
```

#### 7. Agent with Tracing (`src/7-agent-with-trace/`)
**Pattern**: Single agent with ADK execution tracing enabled
- **Domain**: Natura refund system
- **Features**: Execution monitoring and trace collection
- **Technology**: `AdkApp` with `enable_tracing=True`
- **Use Case**: Debugging, performance monitoring, execution analysis

```python
# Wrap agent with AdkApp to enable tracing
app = AdkApp(
    agent=root_agent,
    enable_tracing=True,
)
```

#### 8. Agent with Logging (`src/8-agent-with-log/`)
**Pattern**: Single agent with Google Cloud Logging integration
- **Domain**: Natura refund system
- **Features**: Structured logging, cloud integration, event tracking
- **Technology**: `google.cloud.logging` with custom resource labeling
- **Use Case**: Production monitoring, analytics, audit trails

```python
class NaturaAgentWithLogging:
    def set_up(self):
        self.logging_client = google.cloud.logging.Client(project="PROJECT_ID")
        # Configure structured logging with resource metadata
```

## 🛠️ Technical Stack

- **Framework**: Google Agent Development Kit (ADK)
- **Language**: Python 3.x
- **Models**: Gemini 2.5 Flash Preview, Gemini 2.0 Flash Live
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

#### Basic Examples (1-5)
```python
# Example 1: Single Agent
from src.1_llm_single_agent.agent import root_agent
response = root_agent.query("I need help with a refund")
```

#### Live Agent (Example 6)
```python
# Example 6: Live Agent
from src.6_llm_live.agent import root_agent
# Real-time conversation with Félix
response = root_agent.query("¡Hola! Quiero hacer un pedido")
```

#### Tracing Agent (Example 7)
```python
# Example 7: With Tracing
from src.7_agent_with_trace.agent import app
# Traces will appear in Google Cloud Console
response = app.query("Check my refund status")
```

#### Logging Agent (Example 8)
```python
# Example 8: With Logging
from src.8_agent_with_log.agent import natura_logging, root_agent
natura_logging.set_up()  # Configure cloud logging
response = natura_logging.query({"message": "Process my refund"})
```

## 📊 Business Domains

### Natura Refund System
- **Language**: Portuguese
- **Tools**: Purchase history, eligibility checking, refund processing
- **Business Logic**: Shipping method and reason-based eligibility
- **Examples**: 1, 2, 3, 4, 5, 7, 8

### CRF Fast Food Ordering
- **Language**: Spanish
- **Character**: Félix - enthusiastic food assistant
- **Tools**: Menu information, order finalization
- **API Integration**: External ordering system
- **Examples**: 6

## 📁 Project Structure

```
adk-bot-exemplos/
├── src/
│   ├── 1-llm-single-agent/          # Basic single agent
│   ├── 2-llm-multi-agent/           # Multi-agent coordinator
│   ├── 3-workflow-sequential-multi-agent/  # Sequential workflow
│   ├── 4-workflow-parallel-multi-agent/    # Parallel workflow
│   ├── 5-custom-agent-control-flow/        # Custom control flow
│   ├── 6-llm-live/                  # Live conversational agent
│   ├── 7-agent-with-trace/          # Tracing integration
│   ├── 8-agent-with-log/            # Logging integration
│   └── tools/                       # Shared tools and prompts
├── docs/                            # Detailed documentation
├── memory-bank/                     # Project context and patterns
└── README.md                        # This file
```

## 🔧 Configuration Notes

### Model Compatibility
- **Recommended**: `gemini-2.5-flash-preview-05-20` (stable, proven)
- **Live Agent**: `gemini-2.0-flash-live-preview-04-09` (real-time features)
- **Avoid**: `gemini-2.0-flash-live-001` (known WebSocket issues)

### Cloud Services Setup
- **Tracing**: Requires Vertex AI deployment for full functionality
- **Logging**: Needs proper IAM permissions (`roles/logging.logWriter`)
- **Authentication**: Service account or user credentials required

## 📚 Documentation

- [`docs/`](docs/) - Detailed documentation for each pattern
- [`memory-bank/`](memory-bank/) - Project context and architectural decisions
- [`docs/api/`](docs/api/) - API documentation for tools and prompts

## 🤝 Contributing

Each example is self-contained and can be extended independently. When adding new patterns:

1. Follow the established naming convention (`N-description/`)
2. Include proper logging and error handling
3. Update this README with the new example
4. Add documentation in the `docs/` directory

## 📄 License

See [LICENSE](LICENSE) file for details.

---

**Note**: This project demonstrates various ADK patterns for educational purposes. Adapt the examples to your specific use cases and production requirements.
