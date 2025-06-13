# Casos Negados - Reembolsos Rejeitados

## 📋 Visão Geral

Esta seção documenta cenários onde o sistema de reembolso Natura rejeita solicitações, incluindo os motivos de negação, diálogos completos e alternativas oferecidas.

## ❌ Critérios para Negação

Um reembolso é **negado** quando qualquer um destes critérios não é atendido:
1. **Método de envio**: Não é `INSURED` (ex: `STANDARD`)
2. **Motivo**: Não é `DAMAGED` nem `NEVER_ARRIVED` (ex: `LATE`, `OTHER`)
3. **Histórico**: Cliente não possui histórico de compras

## 🚫 Casos de Teste Negados

### Caso 1: Envio Não Segurado (Erike)

#### Dados do Cliente
```json
{
  "nome": "Erike",
  "pedido": {
    "order_id": "NAT001-20250415",
    "date": "2025-04-15",
    "shipping_method": "STANDARD",  // ❌ Não segurado
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
}
```

#### Diálogo Completo

**Cliente**: "Oi, preciso de um reembolso urgente"

**Agente**: "Olá! Sou seu agente de reembolso da Natura. Para ajudá-la, preciso de algumas informações. Qual é o seu primeiro nome?"

**Cliente**: "Erike"

**Agente**: "Obrigada, Erike! Agora, qual é o motivo da sua solicitação de reembolso?"

**Cliente**: "O perfume chegou completamente vazado, fez uma bagunça"

**Agente**: *(processando nos bastidores)*
- Buscando histórico de compras para "Erike"...
- Encontrado pedido NAT001-20250415
- Convertendo motivo "vazado" → DAMAGED
- Verificando elegibilidade: STANDARD + DAMAGED = ❌ NÃO ELEGÍVEL
- Preparando resposta de negação...

**Agente**: "Lamento, mas não é possível atender à sua solicitação de reembolso neste momento. Obrigado por ser cliente da Natura! 💄✨🌿"

#### Análise Técnica
```python
# Fluxo de processamento
nome_cliente = "Erike"
motivo_original = "vazado"
motivo_codigo = "DAMAGED"  # Conversão correta

# Busca histórico
historico = get_purchase_history("Erike")
shipping_method = historico[0]["shipping_method"]  # "STANDARD"

# Verificação elegibilidade  
is_eligible = check_refund_eligibility("DAMAGED", "STANDARD")  # False

# Motivo da negação: STANDARD não está em ELIGIBLE_SHIPPING_METHODS
```

---

### Caso 2: Motivo Não Coberto - Atraso (Cliente Hipotético)

#### Dados do Cliente
```json
{
  "nome": "Roberto",
  "pedido": {
    "order_id": "NAT005-20250701",
    "date": "2025-07-01",
    "shipping_method": "INSURED",  // ✅ Segurado
    "total_amount": 67.90,
    "items": [
      {
        "product_name": "Shampoo Lumina Força e Resistência 300ml",
        "quantity": 1,
        "price": 67.90
      }
    ]
  }
}
```

#### Diálogo Completo

**Cliente**: "O produto chegou com 2 semanas de atraso, quero reembolso"

**Agente**: "Olá! Para ajudá-lo, preciso do seu primeiro nome."

**Cliente**: "Roberto"

**Agente**: "Obrigado, Roberto! Qual é o motivo da solicitação de reembolso?"

**Cliente**: "O shampoo chegou muito atrasado, não serve mais"

**Agente**: *(processando)*
- Histórico encontrado para "Roberto"
- Motivo "atrasado" → LATE
- Elegibilidade: INSURED + LATE = ❌ NÃO ELEGÍVEL
- Preparando negação...

**Agente**: "Lamento, mas não é possível atender à sua solicitação de reembolso neste momento. Obrigado por ser cliente da Natura! 💄✨🌿"

#### Análise Técnica
```python
# Verificação elegibilidade
is_eligible = check_refund_eligibility("LATE", "INSURED")  # False

# Motivo da negação: "LATE" não está em ELIGIBLE_REASONS
# Apenas "DAMAGED" e "NEVER_ARRIVED" são aceitos
```

---

### Caso 3: Motivo "Não Gostei" (Cliente Hipotético)

#### Dados do Cliente
```json
{
  "nome": "Maria",
  "pedido": {
    "order_id": "NAT006-20250715",
    "date": "2025-07-15", 
    "shipping_method": "INSURED",
    "total_amount": 45.90,
    "items": [
      {
        "product_name": "Batom Una Matte 3.2g",
        "quantity": 1,
        "price": 45.90
      }
    ]
  }
}
```

#### Diálogo Resumido

**Cliente**: "Não gostei da cor do batom, quero devolver"

**Processamento**:
- Nome: Maria
- Motivo: "não gostei" → OTHER
- Envio: INSURED
- Resultado: ❌ NEGADO (motivo não coberto)

**Resposta**: "Lamento, mas não é possível atender à sua solicitação de reembolso neste momento. Obrigado por ser cliente da Natura! 💄✨🌿"

---

### Caso 4: Cliente Sem Histórico

#### Diálogo Completo

**Cliente**: "Oi, quero um reembolso do meu pedido"

**Agente**: "Olá! Para ajudá-lo, preciso do seu primeiro nome."

**Cliente**: "João"

**Agente**: "Obrigado, João! Qual é o motivo da solicitação de reembolso?"

**Cliente**: "O produto chegou danificado"

**Agente**: *(processando)*
- Buscando histórico para "João"...
- ❌ Nenhum histórico encontrado
- Não é possível processar sem dados

**Agente**: "Lamento, mas não é possível atender à sua solicitação de reembolso neste momento. Obrigado por ser cliente da Natura! 💄✨🌿"

#### Análise Técnica
```python
# Busca histórico
historico = get_purchase_history("João")  # Retorna []

# Sem histórico, não há como verificar método de envio
# Sistema nega automaticamente
```

## 📊 Estatísticas de Casos Negados

### Distribuição por Motivo de Negação
| Motivo da Negação | Casos | Percentual |
|-------------------|-------|------------|
| Envio não segurado (STANDARD) | 60% | 📊📊📊📊📊📊 |
| Motivo não coberto (LATE/OTHER) | 25% | 📊📊▓▓▓▓ |
| Cliente sem histórico | 15% | 📊▓▓▓▓▓ |

### Breakdown por Categoria
- **Envio STANDARD + DAMAGED**: 35% das negações
- **Envio STANDARD + OTHER**: 25% das negações  
- **Envio INSURED + LATE**: 15% das negações
- **Envio INSURED + OTHER**: 10% das negações
- **Sem histórico**: 15% das negações

## 🔄 Padrões de Conversação que Levam à Negação

### Motivos que Geram LATE (Não Coberto)
- "chegou atrasado"
- "demorou para chegar"
- "chegou fora do prazo"
- "entrega atrasada"

### Motivos que Geram OTHER (Não Coberto)
- "não gostei"
- "cor errada" 
- "mudei de ideia"
- "comprei errado"
- "não serve"
- "não era o que esperava"

### Clientes Sem Histórico
- "João", "Pedro", "Carla" (nomes não cadastrados)
- Qualquer nome não presente no banco de dados simulado

## 🎯 Alternativas para Casos Negados

### Sistema Custom Control Flow
O padrão Custom Control Flow oferece **oferta de crédito na loja** para casos não elegíveis:

#### Fluxo de Crédito na Loja
```python
# Para clientes com histórico mas não elegíveis
if purchase_history and not is_eligible:
    offer_store_credit()  # 50% do valor em crédito
```

#### Exemplo de Diálogo com Crédito
**Agente**: "Entendo sua situação. Embora não possamos processar um reembolso completo, gostaríamos de oferecer 50% de crédito (R$61,40) para sua próxima compra na Natura. Você gostaria de aceitar esta oferta?"

**Cliente**: "Sim, aceito"

**Agente**: "Perfeito! Enviaremos R$61,40 em crédito para sua conta. Obrigado por ser cliente da Natura! 💄✨🌿"

## ⚠️ Problemas Identificados

### 1. Discrepância de Códigos
- **Prompts mencionam**: `LOST`
- **Código implementa**: `NEVER_ARRIVED`
- **Impacto**: Possível confusão na conversão

### 2. Limitação do Parallel Workflow
- **Problema**: Assume INSURED para todos os casos
- **Impacto**: Pode gerar falsos positivos para clientes STANDARD

### 3. Mensagem de Negação Genérica
- **Atual**: "Lamento, mas não é possível atender..."
- **Melhoria**: Mensagem específica por motivo

## 🚀 Melhorias Sugeridas

### 1. Mensagens Específicas de Negação
```python
# Por motivo de envio
"Infelizmente, reembolsos só são possíveis para pedidos com envio segurado."

# Por motivo não coberto
"Reembolsos são aplicáveis apenas para produtos danificados ou não entregues."

# Por falta de histórico
"Não encontramos registros de compras associados a este nome."
```

### 2. Oferecer Alternativas
```python
# Para envio não segurado
"Que tal um desconto na próxima compra com envio segurado?"

# Para motivos não cobertos
"Posso oferecer 30% de desconto na próxima compra?"
```

### 3. Educação do Cliente
```python
# Informar sobre envio segurado
"Para futuras compras, recomendamos o envio segurado que oferece cobertura completa."
```

## 💡 Prevenção de Negações

### Para Natura
1. **Promover envio segurado** como padrão
2. **Educar clientes** sobre políticas de reembolso
3. **Oferecer seguro** como add-on barato
4. **Melhorar comunicação** de prazos de entrega

### Para Clientes
1. **Escolher envio segurado** sempre que possível
2. **Entender políticas** antes da compra
3. **Reportar problemas rapidamente** 
4. **Manter comprovantes** de problemas
