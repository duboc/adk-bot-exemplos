# Sistema de Reembolso Natura - Documentação

## Visão Geral

Este projeto demonstra diferentes padrões arquiteturais de agentes usando o Google Agent Development Kit (ADK) para processar solicitações de reembolso da Natura, empresa brasileira de cosméticos e produtos de beleza.

## 🏗️ Arquitetura do Sistema

O sistema implementa 5 padrões diferentes de agentes:

1. **Single Agent** - Um único agente que gerencia todo o fluxo
2. **Multi LLM Agent** - Múltiplos agentes coordenados (padrão Coordinator/Dispatcher)
3. **Sequential Workflow** - Agentes executados em sequência fixa
4. **Parallel Workflow** - Agentes executados em paralelo dentro de um fluxo sequencial
5. **Custom Control Flow** - Lógica de orquestração personalizada

## 🎯 Funcionalidades

- **Coleta de informações**: Nome do cliente e motivo do reembolso
- **Verificação de histórico**: Busca pedidos anteriores do cliente
- **Análise de elegibilidade**: Verifica se o reembolso é válido baseado em políticas
- **Processamento**: Executa o reembolso ou oferece alternativas
- **Atendimento em português**: Totalmente localizado para o mercado brasileiro

## 📋 Critérios de Elegibilidade

### Métodos de Envio Elegíveis
- ✅ `INSURED` - Envio segurado

### Motivos Elegíveis
- ✅ `DAMAGED` - Produto danificado, vazado ou embalagem violada
- ✅ `NEVER_ARRIVED` - Produto nunca chegou ou se perdeu no transporte
- ❌ `LATE` - Produto chegou atrasado (não elegível)
- ❌ `OTHER` - Outros motivos (não elegível)

## 🚀 Como Executar

### Pré-requisitos
```bash
pip install -r src/requirements.txt
```

### Execução dos Diferentes Agentes

#### 1. Single Agent
```python
from src.single_agent.agent import root_agent
# Execute o agente único
```

#### 2. Multi LLM Agent
```python
from src.multi_agent.agent import root_agent
# Execute o sistema multi-agente
```

#### 3. Sequential Workflow
```python
from src.sequential_workflow.agent import root_agent
# Execute o fluxo sequencial
```

#### 4. Parallel Workflow
```python
from src.parallel_workflow.agent import root_agent
# Execute o fluxo paralelo
```

#### 5. Custom Control Flow
```python
from src.custom_control_flow.agent import root_agent
# Execute o fluxo customizado
```

## 📚 Documentação Detalhada

- [🔄 Fluxo de Decisão](fluxo-decisao.md) - Diagrama completo do processo
- [🤖 Tipos de Agentes](agentes/) - Documentação de cada padrão arquitetural
- [⚙️ API Reference](api/) - Documentação das ferramentas e prompts
- [📖 Exemplos](exemplos/) - Casos de uso e dados de teste

## 🧪 Dados de Teste

O sistema inclui dois clientes de exemplo:

### Erike (Envio STANDARD - Não elegível)
- **Pedido**: NAT001-20250415
- **Produtos**: Perfume Kaiak Feminino, Creme Tododia
- **Total**: R$ 122,80
- **Envio**: STANDARD (não segurado)

### Massini (Envio INSURED - Elegível)
- **Pedido**: NAT002-20250610
- **Produtos**: Desodorante Natura Humor, Shampoo Plant
- **Total**: R$ 74,80
- **Envio**: INSURED (segurado)

## 🎨 Identidade Visual

O sistema utiliza emojis relacionados à beleza e cuidados pessoais da Natura:
- 💄 Maquiagem
- ✨ Brilho/Beleza
- 🌿 Natureza/Sustentabilidade

## 🔧 Tecnologias Utilizadas

- **Google Agent Development Kit (ADK)**
- **Gemini 2.5 Flash Preview**
- **Python 3.x**
- **Logging integrado**
- **Padrões de arquitetura de agentes**

## 📞 Suporte

Para dúvidas sobre implementação ou uso do sistema, consulte a documentação específica de cada componente nas seções correspondentes.

---

# Complete ADK Callback Examples Collection

This collection provides comprehensive examples for all 6 types of callbacks available in Google Agent Development Kit (ADK). Each example demonstrates practical use cases with fun, memorable themes and includes LLM-powered quality control.

## 🎯 Complete Callback Coverage

### **Agent Lifecycle Callbacks**

#### 10. Before Agent Callback - Magic 8-Ball with Mood Control 🔮
- **Theme**: Mystical fortune teller with mood-based behavior
- **Character**: Madame Mystique
- **Demonstrates**: Session state control, conditional agent execution
- **Key Feature**: Agent can be completely bypassed based on mood
- **Use Cases**: Maintenance mode, user permissions, A/B testing

#### 11. After Agent Callback - Restaurant Reviewer with Quality Control 🍽️
- **Theme**: Professional restaurant critic with quality assurance
- **Character**: Chef Gordon Critique
- **Demonstrates**: Response auditing and improvement via LLM
- **Key Feature**: Automatic quality enhancement of reviews
- **Use Cases**: Content moderation, response improvement, brand consistency

### **LLM Interaction Callbacks**

#### 12. Before Model Callback - Content Filter with Guardrails 🛡️
- **Theme**: Educational assistant with safety controls
- **Character**: Professor Sage
- **Demonstrates**: Content filtering, request modification, safety guardrails
- **Key Feature**: Blocks inappropriate content before reaching LLM
- **Use Cases**: Content safety, request enhancement, compliance

#### 13. After Model Callback - Translation Service with Post-Processing 🌍
- **Theme**: Multilingual expert with cultural awareness
- **Character**: Professor Polyglot
- **Demonstrates**: Response post-processing and cultural enhancement
- **Key Feature**: Adds cultural context and alternative translations
- **Use Cases**: Response formatting, cultural adaptation, quality improvement

### **Tool Execution Callbacks**

#### 14. Before Tool Callback - Weather Service with Permission Checks 🌤️
- **Theme**: Meteorologist with role-based access control
- **Character**: Dr. Stormy Forecast
- **Demonstrates**: Permission checks, rate limiting, argument modification
- **Key Feature**: Role-based tool access and usage controls
- **Use Cases**: Authorization, rate limiting, argument validation

#### 15. After Tool Callback - Calculator Service with Result Validation 🧮
- **Theme**: Mathematician with result enhancement
- **Character**: Professor Calculate
- **Demonstrates**: Result validation, enhancement, and error handling
- **Key Feature**: Adds mathematical context and alternative representations
- **Use Cases**: Result validation, data enrichment, error enhancement

## 🏗️ Shared Infrastructure

### **LLM Auditor Framework** (`src/shared/auditor.py`)
- Reusable quality control system
- JSON-based audit responses
- Configurable criteria for different domains
- Error handling and fallbacks
- Pre-defined configurations for common use cases

### **Audit Configurations**
- **Restaurant Reviews**: Professional tone, balanced perspective
- **Content Filter**: Safety, appropriateness, inclusivity
- **Translation Quality**: Accuracy, cultural appropriateness
- **Weather Service**: Accuracy, safety warnings
- **Calculation Accuracy**: Mathematical correctness, explanations

## 🎭 Character Personalities

Each example features a unique, memorable character:

| Example | Character | Personality | Emojis |
|---------|-----------|-------------|---------|
| Before Agent | Madame Mystique | Mystical fortune teller | 🔮✨🌟🎭🌙 |
| After Agent | Chef Gordon Critique | Professional food critic | 🍽️🍕🍝🍣🥘 |
| Before Model | Professor Sage | Educational librarian | 📚📖🎓🔍💡 |
| After Model | Professor Polyglot | Multilingual expert | 🌍📚🗣️💬🔤 |
| Before Tool | Dr. Stormy Forecast | Safety-conscious meteorologist | 🌤️⛅🌧️❄️⚡ |
| After Tool | Professor Calculate | Methodical mathematician | 🧮📊📈🔢➕ |

## 🚀 Getting Started with Callbacks

### **Prerequisites**
```bash
pip install google-adk
export GOOGLE_API_KEY="your-api-key-here"
```

### **Running Callback Examples**

Each example can be run in multiple ways:

#### **Option 1: Test Scripts**
```bash
cd src/[example-folder]/
python test_demo.py
```

#### **Option 2: Direct Import**
```python
from src.[example-folder] import main
await main()
```

#### **Option 3: Agent Import**
```python
from src.[example-folder] import root_agent
# Use agent in your own code
```

## 📋 Callback Example Structure

Each callback example follows a consistent structure:

```
src/[XX-callback-type]/
├── agent.py           # Main implementation
├── __init__.py        # Module exports
├── test_demo.py       # Interactive demo (some examples)
└── README.md          # Detailed documentation (some examples)
```

### **Common Components**
- **Custom Tools**: Domain-specific functionality
- **Character Prompt**: Engaging personality definition
- **Callback Function**: Core callback implementation
- **Demo Scenarios**: Multiple test cases
- **Session State**: Configuration via state management

## 🎯 Key Learning Objectives

### **Technical Skills**
1. **Callback Implementation**: How to create and use each callback type
2. **Session Management**: Control behavior via session state
3. **LLM Integration**: Use secondary LLMs for quality control
4. **Error Handling**: Graceful failure and recovery patterns
5. **Tool Development**: Create domain-specific tools

### **Practical Applications**
1. **Quality Assurance**: Automated response improvement
2. **Safety Controls**: Content filtering and guardrails
3. **Access Control**: Permission-based functionality
4. **User Experience**: Enhanced responses and error messages
5. **Business Logic**: Custom rules and validations

## 🔧 Customization Guide

### **Adapting for Your Domain**

1. **Choose Callback Type**: Select based on when you need intervention
2. **Define Character**: Create engaging personality for your domain
3. **Create Tools**: Build domain-specific functionality
4. **Configure Auditor**: Set quality criteria for your use case
5. **Test Scenarios**: Create comprehensive test cases

### **Session State Patterns**

Common session state configurations:
```python
# Feature toggles
{"feature_enabled": True/False}

# User permissions
{"user_role": "basic"/"premium"/"admin"}

# Behavior modification
{"enhancement_level": "minimal"/"standard"/"detailed"}

# Safety controls
{"safety_mode": "strict"/"moderate"/"permissive"}
```

## 📚 Additional Documentation Links

- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [Callback API Reference](https://google.github.io/adk-docs/agents/callbacks/)
- [Agent Development Guide](https://google.github.io/adk-docs/agents/)
- [Tool Development](https://google.github.io/adk-docs/tools/)

## 🎉 Next Steps

1. **Explore Examples**: Run each callback type to understand the patterns
2. **Modify Characters**: Adapt personalities for your domain
3. **Create Custom Tools**: Build functionality specific to your needs
4. **Implement Auditors**: Add quality control for your use cases
5. **Build Production Systems**: Scale patterns for real applications

This collection provides a complete foundation for understanding and implementing all ADK callback types with practical, engaging examples! 🌟
