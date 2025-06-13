# API Reference - Tools

## 📋 Visão Geral

O sistema de reembolso Natura utiliza três ferramentas principais que implementam a lógica de negócio essencial. Cada ferramenta é uma função Python que pode ser chamada pelos agentes para executar operações específicas.

## 🔧 Configuração e Constantes

### Constantes de Elegibilidade

```python
# Métodos de envio elegíveis para reembolso
ELIGIBLE_SHIPPING_METHODS = ["INSURED"]

# Motivos elegíveis para reembolso
ELIGIBLE_REASONS = ["DAMAGED", "NEVER_ARRIVED"]
```

### Configuração de Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
```

## 🛠️ Ferramentas Disponíveis

### 1. get_purchase_history

**Função**: Recupera o histórico de compras de um cliente específico.

#### Assinatura
```python
def get_purchase_history(purchaser: str) -> List[Dict[str, Any]]
```

#### Parâmetros
- **purchaser** (`str`): Nome do cliente para busca no histórico

#### Retorno
- **`List[Dict[str, Any]]`**: Lista de registros de compras ou lista vazia se não encontrado

#### Estrutura do Retorno
```python
[
    {
        "order_id": "NAT001-20250415",        # ID único do pedido
        "date": "2025-04-15",                 # Data da compra
        "items": [                            # Lista de produtos
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
        ],
        "shipping_method": "STANDARD",        # Método de envio (STANDARD/INSURED)
        "total_amount": 122.80               # Valor total do pedido
    }
]
```

#### Dados de Exemplo
```python
history_data = {
    "Erike": [
        {
            "order_id": "NAT001-20250415",
            "date": "2025-04-15", 
            "items": [
                {"product_name": "Perfume Kaiak Feminino 100ml", "quantity": 1, "price": 89.90},
                {"product_name": "Creme Hidratante Tododia Algodão 400ml", "quantity": 1, "price": 32.90}
            ],
            "shipping_method": "STANDARD",
            "total_amount": 122.80
        }
    ],
    "Massini": [
        {
            "order_id": "NAT002-20250610",
            "date": "2025-06-03",
            "items": [
                {"product_name": "Desodorante Natura Homem Humor 75ml", "quantity": 1, "price": 45.90},
                {"product_name": "Shampoo Plant Cachos Intensos 300ml", "quantity": 1, "price": 28.90}
            ],
            "shipping_method": "INSURED", 
            "total_amount": 74.80
        }
    ]
}
```

#### Comportamento
1. **Normalização**: Nome do cliente é normalizado com `strip().title()`
2. **Busca**: Procura exata no dicionário de dados
3. **Logging**: Registra tentativas de busca e resultados
4. **Retorno vazio**: Lista vazia `[]` se cliente não encontrado

#### Exemplo de Uso
```python
# Busca bem-sucedida
history = get_purchase_history("Massini")
# Retorna: [{"order_id": "NAT002-20250610", ...}]

# Cliente não encontrado
history = get_purchase_history("João")  
# Retorna: []
```

---

### 2. check_refund_eligibility

**Função**: Verifica se uma solicitação de reembolso é elegível baseada no motivo e método de envio.

#### Assinatura
```python
def check_refund_eligibility(reason: str, shipping_method: str) -> bool
```

#### Parâmetros
- **reason** (`str`): Motivo do reembolso (código padronizado)
- **shipping_method** (`str`): Método de envio usado no pedido

#### Retorno
- **`bool`**: `True` se elegível, `False` caso contrário

#### Lógica de Elegibilidade
```python
# Critérios obrigatórios (ambos devem ser atendidos)
is_eligible = (
    shipping_method.upper() in ELIGIBLE_SHIPPING_METHODS and
    reason.upper() in ELIGIBLE_REASONS
)
```

#### Combinações de Elegibilidade

| Método de Envio | Motivo | Elegível? | Observação |
|----------------|--------|-----------|------------|
| `INSURED` | `DAMAGED` | ✅ | Produto danificado com seguro |
| `INSURED` | `NEVER_ARRIVED` | ✅ | Produto perdido com seguro |
| `INSURED` | `LATE` | ❌ | Atraso não é coberto |
| `INSURED` | `OTHER` | ❌ | Outros motivos não cobertos |
| `STANDARD` | `DAMAGED` | ❌ | Sem seguro de envio |
| `STANDARD` | `NEVER_ARRIVED` | ❌ | Sem seguro de envio |
| `STANDARD` | `LATE` | ❌ | Sem seguro + motivo não coberto |
| `STANDARD` | `OTHER` | ❌ | Sem seguro + motivo não coberto |

#### Exemplo de Uso
```python
# Caso elegível
is_eligible = check_refund_eligibility("DAMAGED", "INSURED")
# Retorna: True

# Caso não elegível
is_eligible = check_refund_eligibility("DAMAGED", "STANDARD") 
# Retorna: False

# Case insensitive
is_eligible = check_refund_eligibility("damaged", "insured")
# Retorna: True
```

---

### 3. process_refund

**Função**: Processa um reembolso aprovado, gerando ID único e mensagem de confirmação.

#### Assinatura
```python
def process_refund(amount: float, order_id: str) -> str
```

#### Parâmetros
- **amount** (`float`): Valor do reembolso em reais
- **order_id** (`str`): ID do pedido original

#### Retorno
- **`str`**: Mensagem de confirmação formatada para o cliente

#### Lógica de Processamento
1. **Geração de ID**: `REF-{order_id}-{amount*100}`
2. **Logging**: Registro detalhado da operação
3. **Simulação**: Em ambiente real, integraria com processadores de pagamento

#### Formato da Mensagem
```python
f"✅ Reembolso {refund_id} realizado com sucesso! Creditaremos R${amount:.2f} em sua conta em até 2 dias úteis."
```

#### Exemplo de Uso
```python
# Processar reembolso
confirmation = process_refund(74.80, "NAT002-20250610")

# Resultado:
"✅ Reembolso REF-NAT002-20250610-7480 realizado com sucesso! Creditaremos R$74.80 em sua conta em até 2 dias úteis."
```

#### Geração de IDs
| Valor | Order ID | Refund ID Gerado |
|-------|----------|------------------|
| R$ 74.80 | NAT002-20250610 | REF-NAT002-20250610-7480 |
| R$ 122.80 | NAT001-20250415 | REF-NAT001-20250415-12280 |
| R$ 45.90 | NAT003-20250701 | REF-NAT003-20250701-4590 |

## 🔍 Tratamento de Erros e Edge Cases

### get_purchase_history
```python
# Entrada vazia ou None
get_purchase_history("")      # Busca por ""
get_purchase_history(None)    # TypeError (esperado)

# Normalização de entrada
get_purchase_history("  erike  ")  # Torna-se "Erike"
get_purchase_history("MASSINI")     # Torna-se "Massini"
```

### check_refund_eligibility
```python
# Normalização automática
check_refund_eligibility("damaged", "insured")     # True
check_refund_eligibility("DAMAGED", "INSURED")     # True
check_refund_eligibility("  damaged  ", "insured") # True

# Valores inválidos
check_refund_eligibility("UNKNOWN", "INSURED")     # False
check_refund_eligibility("DAMAGED", "UNKNOWN")     # False
```

### process_refund
```python
# Valores decimais
process_refund(74.80, "NAT002")    # REF-NAT002-7480
process_refund(100.00, "NAT001")   # REF-NAT001-10000
process_refund(0.50, "NAT003")     # REF-NAT003-50

# Order IDs especiais
process_refund(50.0, "ORDER-123-ABC")  # REF-ORDER-123-ABC-5000
```

## 📊 Logs e Monitoramento

### Estrutura dos Logs
```python
# get_purchase_history
"Recuperando histórico de compras para: {purchaser}"
"Encontradas {count} compra(s) para {purchaser}"
"Nenhum histórico de compras encontrado para: {purchaser}"

# check_refund_eligibility  
"Verificando elegibilidade para reembolso - Motivo: {reason}, Envio: {shipping_method}"
"Resultado da elegibilidade para reembolso: {is_eligible}"

# process_refund
"Processando reembolso - Pedido: {order_id}, Valor: R${amount:.2f}"
"Reembolso processado com sucesso - ID do Reembolso: {refund_id}"
```

### Exemplo de Log Completo
```
2025-06-13 11:49:00 - tools - INFO - Recuperando histórico de compras para: Massini
2025-06-13 11:49:00 - tools - INFO - Encontradas 1 compra(s) para Massini
2025-06-13 11:49:01 - tools - INFO - Verificando elegibilidade para reembolso - Motivo: DAMAGED, Envio: INSURED
2025-06-13 11:49:01 - tools - INFO - Resultado da elegibilidade para reembolso: True
2025-06-13 11:49:02 - tools - INFO - Processando reembolso - Pedido: NAT002-20250610, Valor: R$74.80
2025-06-13 11:49:02 - tools - INFO - Reembolso processado com sucesso - ID do Reembolso: REF-NAT002-20250610-7480
```

## 🚀 Extensões e Melhorias

### Potenciais Melhorias
1. **Persistência real**: Integração com banco de dados
2. **Validação avançada**: CPF, e-mail, telefone
3. **Cache**: Para consultas frequentes de histórico
4. **Rate limiting**: Para evitar abuso
5. **Auditoria**: Logs detalhados para compliance
6. **Integração externa**: APIs de pagamento reais
7. **Notificações**: E-mail/SMS de confirmação

### Extensão para Produção
```python
# Exemplo de extensão com banco de dados
async def get_purchase_history_db(purchaser: str) -> List[Dict[str, Any]]:
    async with database.connection() as conn:
        query = "SELECT * FROM orders WHERE customer_name = ?"
        results = await conn.fetch_all(query, (purchaser,))
        return [dict(row) for row in results]
