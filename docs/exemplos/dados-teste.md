# Dados de Teste - Base de Dados Simulada

## 📋 Visão Geral

Esta seção documenta todos os dados de teste disponíveis no sistema, incluindo clientes cadastrados, histórico de compras e cenários para validação dos diferentes padrões de agentes.

## 👥 Clientes Cadastrados

### Cliente 1: Erike (Envio STANDARD)
```json
{
  "nome": "Erike",
  "histórico": [
    {
      "order_id": "NAT001-20250415",
      "date": "2025-04-15",
      "shipping_method": "STANDARD",
      "total_amount": 122.80,
      "items": [
        {
          "product_name": "Perfume Kaiak Feminino 100ml",
          "quantity": 1,
          "price": 89.90
        },
        {
          "product_name": "Creme Hidratante Tododia Algodão 400ml",
          "quantity": 1,
          "price": 32.90
        }
      ]
    }
  ],
  "perfil": "Cliente não elegível para reembolso",
  "casos_teste": ["Produto danificado + STANDARD = Negado"]
}
```

### Cliente 2: Massini (Envio INSURED)
```json
{
  "nome": "Massini", 
  "histórico": [
    {
      "order_id": "NAT002-20250610",
      "date": "2025-06-03",
      "shipping_method": "INSURED",
      "total_amount": 74.80,
      "items": [
        {
          "product_name": "Desodorante Natura Homem Humor 75ml",
          "quantity": 1,
          "price": 45.90
        },
        {
          "product_name": "Shampoo Plant Cachos Intensos 300ml",
          "quantity": 1,
          "price": 28.90
        }
      ]
    }
  ],
  "perfil": "Cliente elegível para reembolso",
  "casos_teste": ["Produto danificado + INSURED = Aprovado"]
}
```

## 🛍️ Análise de Produtos

### Produtos por Categoria
| Categoria | Produto | Preço | Frequência |
|-----------|---------|-------|------------|
| **Perfumes** | Kaiak Feminino 100ml | R$ 89,90 | 40% |
| **Cuidados Pessoais** | Desodorante Humor 75ml | R$ 45,90 | 25% |
| **Cabelos** | Shampoo Plant 300ml | R$ 28,90 | 20% |
| **Corpo** | Creme Tododia 400ml | R$ 32,90 | 15% |

### Faixas de Preço
- **Produtos Premium** (R$ 80+): Perfumes
- **Produtos Médios** (R$ 30-80): Desodorantes, Cremes
- **Produtos Básicos** (R$ 10-30): Shampoos, Condicionadores

## 🧪 Cenários de Teste Completos

### Matriz de Teste: Envio × Motivo

| Cliente | Envio | Motivo | Código | Elegível? | Resultado |
|---------|--------|--------|---------|-----------|-----------|
| Erike | STANDARD | "vazado" | DAMAGED | ❌ | Negado |
| Erike | STANDARD | "não gostei" | OTHER | ❌ | Negado |
| Erike | STANDARD | "atrasado" | LATE | ❌ | Negado |
| Erike | STANDARD | "não chegou" | NEVER_ARRIVED | ❌ | Negado |
| Massini | INSURED | "danificado" | DAMAGED | ✅ | Aprovado |
| Massini | INSURED | "não chegou" | NEVER_ARRIVED | ✅ | Aprovado |
| Massini | INSURED | "atrasado" | LATE | ❌ | Negado |
| Massini | INSURED | "não gostei" | OTHER | ❌ | Negado |

### Scripts de Teste por Padrão

#### Single Agent
```python
# Teste básico de aprovação
test_case_1 = {
    "input": "Olá, sou Massini e meu produto chegou danificado",
    "expected_steps": [
        "coleta_nome: Massini",
        "coleta_motivo: danificado", 
        "busca_historico: encontrado",
        "verifica_elegibilidade: true",
        "processa_reembolso: REF-NAT002-20250610-7480"
    ],
    "expected_output": "✅ Reembolso REF-NAT002-20250610-7480 realizado com sucesso!"
}

# Teste básico de negação
test_case_2 = {
    "input": "Sou Erike, produto vazou",
    "expected_steps": [
        "coleta_nome: Erike",
        "coleta_motivo: vazou",
        "busca_historico: encontrado", 
        "verifica_elegibilidade: false",
        "nega_reembolso"
    ],
    "expected_output": "Lamento, mas não é possível atender à sua solicitação"
}
```

#### Multi-Agent
```python
# Teste de coordenação entre agentes
test_multiagent = {
    "input": "Massini - produto danificado",
    "expected_coordination": [
        "coordinator -> purchase_agent",
        "coordinator -> eligibility_agent", 
        "coordinator -> process_agent",
        "coordinator -> final_response"
    ],
    "agent_outputs": {
        "purchase_agent": {"purchase_history": [...]},
        "eligibility_agent": {"is_refund_eligible": "true"},
        "process_agent": {"refund_confirmation": "..."}
    }
}
```

#### Sequential Workflow
```python
# Teste de sequência obrigatória
test_sequential = {
    "input": "Massini - danificado",
    "expected_sequence": [
        "step_1: PurchaseVerifierAgent",
        "step_2: RefundEligibilityAgent", 
        "step_3: RefundProcessorAgent"
    ],
    "timing": "~9 segundos (3s por etapa)"
}
```

#### Parallel Workflow
```python
# Teste de execução paralela
test_parallel = {
    "input": "Massini - danificado",
    "expected_parallel": [
        "parallel_block: [PurchaseVerifier, EligibilityAgent]",
        "sequential_step: RefundProcessor"
    ],
    "timing": "~6 segundos (3s paralelo + 3s sequencial)",
    "performance_gain": "33% melhoria vs sequential"
}
```

#### Custom Control Flow
```python
# Teste de fluxos condicionais
test_custom_approved = {
    "input": "Massini - danificado",
    "expected_flow": "full_refund_path",
    "custom_logic": "if eligible and history: process_full_refund()"
}

test_custom_credit = {
    "input": "Erike - não gostei", 
    "expected_flow": "store_credit_path",
    "custom_logic": "if not eligible and history: offer_store_credit()"
}

test_custom_no_history = {
    "input": "João - danificado",
    "expected_flow": "no_history_path", 
    "custom_logic": "if not history: handle_no_history()"
}
```

## 🔧 Ferramentas de Teste

### Validação de Ferramentas

#### get_purchase_history
```python
# Casos de teste
test_cases = [
    {"input": "Massini", "expected": [pedido_nat002], "status": "success"},
    {"input": "Erike", "expected": [pedido_nat001], "status": "success"},
    {"input": "João", "expected": [], "status": "not_found"},
    {"input": "  massini  ", "expected": [pedido_nat002], "status": "normalized"},
    {"input": "ERIKE", "expected": [pedido_nat001], "status": "normalized"}
]
```

#### check_refund_eligibility  
```python
# Matriz de elegibilidade completa
test_matrix = [
    {"reason": "DAMAGED", "shipping": "INSURED", "expected": True},
    {"reason": "NEVER_ARRIVED", "shipping": "INSURED", "expected": True},
    {"reason": "LATE", "shipping": "INSURED", "expected": False},
    {"reason": "OTHER", "shipping": "INSURED", "expected": False},
    {"reason": "DAMAGED", "shipping": "STANDARD", "expected": False},
    {"reason": "NEVER_ARRIVED", "shipping": "STANDARD", "expected": False},
    {"reason": "LATE", "shipping": "STANDARD", "expected": False},
    {"reason": "OTHER", "shipping": "STANDARD", "expected": False}
]
```

#### process_refund
```python
# Testes de processamento
test_cases = [
    {
        "amount": 74.80, 
        "order_id": "NAT002-20250610",
        "expected_id": "REF-NAT002-20250610-7480",
        "expected_message": "✅ Reembolso REF-NAT002-20250610-7480 realizado com sucesso!"
    },
    {
        "amount": 122.80,
        "order_id": "NAT001-20250415", 
        "expected_id": "REF-NAT001-20250415-12280",
        "expected_message": "✅ Reembolso REF-NAT001-20250415-12280 realizado com sucesso!"
    }
]
```

## 📊 Dados Estatísticos para Análise

### Volume de Dados
- **Total de clientes**: 2 (base mínima para teste)
- **Total de pedidos**: 2
- **Valor total em pedidos**: R$ 197,60
- **Ticket médio**: R$ 98,80

### Distribuição de Elegibilidade
- **Clientes elegíveis**: 50% (Massini)
- **Clientes não elegíveis**: 50% (Erike)
- **Taxa de aprovação real**: 100% (quando elegível)

### Performance Esperada por Padrão
| Padrão | Tempo (s) | Complexidade | Casos de Uso |
|--------|-----------|--------------|--------------|
| Single | 3-5 | Baixa | Testes básicos |
| Multi | 5-8 | Média | Testes modulares |
| Sequential | 6-10 | Média | Testes estruturados |
| Parallel | 4-6 | Alta | Testes de performance |
| Custom | 6-12 | Muito Alta | Testes complexos |

## 🎯 Cenários de Edge Cases

### Casos Limite para Teste
```python
edge_cases = [
    # Nomes com espaços e case sensitivity
    {"input": "  massini  ", "expected": "normalized_to_Massini"},
    {"input": "ERIKE", "expected": "normalized_to_Erike"},
    
    # Motivos ambíguos
    {"input": "produto estragado", "expected_code": "DAMAGED"},
    {"input": "nunca recebi", "expected_code": "NEVER_ARRIVED"},
    {"input": "demorou muito", "expected_code": "LATE"},
    
    # Valores monetários
    {"amount": 0.01, "expected_id": "REF-TEST-1"},
    {"amount": 999.99, "expected_id": "REF-TEST-99999"},
    
    # IDs de pedido especiais
    {"order_id": "NAT-123-ABC", "expected": "REF-NAT-123-ABC-{amount}"},
    {"order_id": "", "expected": "REF--{amount}"}
]
```

## 🚀 Expansão de Dados de Teste

### Clientes Adicionais Sugeridos
```python
# Para testes mais abrangentes
additional_test_data = {
    "Ana": {
        "shipping_method": "INSURED",
        "order_value": 156.90,
        "use_case": "Produto nunca chegou"
    },
    "Carlos": {
        "shipping_method": "INSURED", 
        "order_value": 89.90,
        "use_case": "Embalagem violada"
    },
    "Roberto": {
        "shipping_method": "INSURED",
        "order_value": 67.90, 
        "use_case": "Produto atrasado (negação)"
    },
    "Maria": {
        "shipping_method": "INSURED",
        "order_value": 45.90,
        "use_case": "Não gostei (negação)"
    }
}
```

### Produtos Adicionais
```python
# Expansão do catálogo para testes
extended_catalog = [
    {"name": "Perfume Essencial Feminino 100ml", "price": 129.90, "category": "fragrance"},
    {"name": "Batom Una Cor Intensa", "price": 27.00, "category": "makeup"},
    {"name": "Creme Facial Chronos 40ml", "price": 89.90, "category": "skincare"},
    {"name": "Shampoo Lumina 300ml", "price": 67.90, "category": "haircare"}
]
```

## 📝 Como Usar os Dados de Teste

### 1. Desenvolvimento
```python
# Importar dados
from tools.tools import get_purchase_history

# Teste rápido
history = get_purchase_history("Massini")
assert len(history) == 1
assert history[0]["shipping_method"] == "INSURED"
```

### 2. Debug
```python
# Verificar elegibilidade
from tools.tools import check_refund_eligibility

is_eligible = check_refund_eligibility("DAMAGED", "INSURED")
print(f"Elegível: {is_eligible}")  # True
```

### 3. Validação End-to-End
```python
# Teste completo de agente
input_text = "Sou Massini, produto chegou danificado"
result = root_agent.process(input_text)
assert "REF-NAT002-20250610-7480" in result
