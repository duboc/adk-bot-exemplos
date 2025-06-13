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
