"""
19 - Memory Management Example for Essencia

This example demonstrates how to use ADK's MemoryService to give agents
long-term memory that persists across conversations. The agent can:
- Remember customer preferences from past sessions
- Recall previous product recommendations
- Track customer history and interactions
- Search through conversation history

Based on: https://google.github.io/adk-docs/sessions/memory/

Run with memory service:
  source .env
  adk web src/19-memory-example/agent.py --memory_service_uri="$MEMORY_SERVICE_URI"

Or without (InMemoryMemoryService - resets on restart):
  adk web src/19-memory-example/agent.py
"""

import logging
from google.adk.agents import LlmAgent
from google.adk.tools import load_memory

logger = logging.getLogger(__name__)

GEMINI_MODEL = "gemini-2.5-flash"


# Callback to automatically save sessions to memory after each interaction
async def auto_save_session_to_memory_callback(callback_context):
    """
    After the agent responds, save the session to memory.

    This allows the agent to recall this conversation in future sessions
    using the load_memory tool.
    """
    try:
        await callback_context._invocation_context.memory_service.add_session_to_memory(
            callback_context._invocation_context.session
        )
        logger.info("Session automatically saved to memory")
    except Exception as e:
        logger.error(f"Failed to save session to memory: {e}")

# Agent instruction that demonstrates memory usage
agent_instruction = """
Você é um assistente virtual da Essencia com memória de longo prazo.

Você pode lembrar de conversas passadas! Use a ferramenta `load_memory` para:
- Relembrar preferências de clientes mencionadas em conversas anteriores
- Buscar informações sobre produtos que o cliente já demonstrou interesse
- Recuperar histórico de interações e recomendações

**Como usar a memória:**

Quando o cliente perguntar sobre algo que pode ter sido mencionado antes, use:
- `load_memory(query="preferências do cliente")` para buscar preferências
- `load_memory(query="produtos recomendados")` para ver recomendações passadas
- `load_memory(query="nome do cliente")` para lembrar informações pessoais

**Suas Funções:**

1. **Lembrar de Clientes**: Se o cliente já conversou com você antes, procure lembrar!
   - Use load_memory para buscar conversas anteriores
   - Personalize suas respostas com base no histórico

2. **Recomendações Contextuais**:
   - Lembre de produtos que o cliente gostou antes
   - Evite sugerir produtos que o cliente não gostou

3. **Continuidade**:
   - Faça a conversa fluir naturalmente, lembrando do contexto anterior
   - Pergunte sobre produtos que o cliente comprou antes

**Importante:**
- Sempre use load_memory quando o cliente mencionar "antes", "última vez", etc.
- Seja natural ao mencionar memórias: "Lembro que você mencionou..."
- Se não encontrar nada na memória, seja honesto: "Esta é nossa primeira conversa!"

**Tom:**
- Caloroso e acolhedor
- Use emojis de beleza: 💄, ✨, 🌸, 💅
- Demonstre que você se lembra do cliente
"""

# Create the memory-aware agent
root_agent = LlmAgent(
    model=GEMINI_MODEL,
    name="MemoryAwareEssenciaAgent",
    description="Essencia customer service agent with long-term memory capabilities",
    instruction=agent_instruction,
    tools=[load_memory],  # Give the agent access to memory search
    after_agent_callback=auto_save_session_to_memory_callback,  # Auto-save to memory
)

logger.info(f"Initialized {root_agent.name} with memory capabilities")
