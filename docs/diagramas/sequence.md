# Sequence Diagrams - Diagramas de Sequência

## 📋 Visão Geral

Esta seção apresenta os diagramas de sequência detalhados do sistema de reembolso Natura, mostrando as interações entre componentes, timing de execução e fluxos de dados para cada padrão de agente.

## 🔵 Single Agent - Sequence Diagram

### Fluxo Completo - Caso de Sucesso (Massini)

```mermaid
sequenceDiagram
    participant C as 👤 Cliente
    participant SA as 🔵 Single Agent
    participant GPH as 📋 get_purchase_history
    participant CRE as ✅ check_refund_eligibility
    participant PR as 💳 process_refund
    participant DB as 📊 Database
    participant PAY as 💰 Payment Gateway
    
    Note over C,PAY: Caso de Sucesso - Cliente Elegível (Massini)
    
    C->>SA: "Oi, preciso de um reembolso"
    SA->>C: "Qual é o seu primeiro nome?"
    C->>SA: "Massini"
    SA->>C: "Qual o motivo do reembolso?"
    C->>SA: "O produto chegou vazado"
    
    Note over SA: Processamento interno - "DE UMA VEZ"
    
    SA->>GPH: get_purchase_history("Massini")
    GPH->>DB: Query customer data
    DB-->>GPH: Customer records
    GPH-->>SA: [order_id: "NAT002-20250610", shipping: "INSURED", amount: 74.80]
    
    SA->>CRE: check_refund_eligibility("DAMAGED", "INSURED")
    CRE->>CRE: Validate business rules
    CRE-->>SA: True (eligible)
    
    SA->>PR: process_refund(74.80, "NAT002-20250610")
    PR->>PAY: Process refund transaction
    PAY-->>PR: Transaction successful
    PR-->>SA: "✅ Reembolso REF-NAT002-20250610-7480 realizado com sucesso!"
    
    SA->>C: "✅ Reembolso REF-NAT002-20250610-7480 realizado com sucesso!<br/>Creditaremos R$74.80 em sua conta em até 2 dias úteis.<br/>Obrigado por ser cliente da Natura! 💄✨🌿"
    
    Note over C,PAY: Tempo total: ~3-5 segundos
```

### Fluxo de Negação - Caso de Falha (Erike)

```mermaid
sequenceDiagram
    participant C as 👤 Cliente
    participant SA as 🔵 Single Agent
    participant GPH as 📋 get_purchase_history
    participant CRE as ✅ check_refund_eligibility
    participant DB as 📊 Database
    
    Note over C,DB: Caso de Negação - Cliente Não Elegível (Erike)
    
    C->>SA: "Preciso de reembolso urgente"
    SA->>C: "Qual é o seu primeiro nome?"
    C->>SA: "Erike"
    SA->>C: "Qual o motivo do reembolso?"
    C->>SA: "O perfume chegou completamente vazado"
    
    Note over SA: Processamento interno
    
    SA->>GPH: get_purchase_history("Erike")
    GPH->>DB: Query customer data
    DB-->>GPH: Customer records
    GPH-->>SA: [order_id: "NAT001-20250415", shipping: "STANDARD", amount: 122.80]
    
    SA->>CRE: check_refund_eligibility("DAMAGED", "STANDARD")
    CRE->>CRE: Validate business rules
    CRE-->>SA: False (not eligible - shipping not insured)
    
    SA->>C: "Lamento, mas não é possível atender à sua solicitação de reembolso neste momento.<br/>Obrigado por ser cliente da Natura! 💄✨🌿"
    
    Note over C,DB: Tempo total: ~3-4 segundos (sem processamento de pagamento)
```

## 🟠 Multi-Agent - Sequence Diagram

### Coordinator/Dispatcher Pattern

```mermaid
sequenceDiagram
    participant C as 👤 Cliente
    participant RA as 🟠 Root Agent (Coordinator)
    participant PHA as 📋 Purchase History Agent
    participant EA as ✅ Eligibility Agent
    participant PRA as 💳 Process Refund Agent
    participant DB as 📊 Database
    participant PAY as 💰 Payment Gateway
    
    Note over C,PAY: Multi-Agent Coordination Pattern
    
    C->>RA: "Sou Massini, produto chegou danificado"
    RA->>C: Collect missing info if needed
    
    Note over RA: Coordenador decide sequência de sub-agentes
    
    RA->>PHA: Delegate: get purchase history for "Massini"
    PHA->>DB: Query customer data
    DB-->>PHA: Customer records
    PHA-->>RA: Session state: purchase_history = [...]
    
    RA->>EA: Delegate: check eligibility with purchase data
    EA->>EA: Extract shipping method from purchase_history
    EA->>EA: Convert "danificado" → "DAMAGED"
    EA->>EA: check_refund_eligibility("DAMAGED", "INSURED")
    EA-->>RA: Session state: is_refund_eligible = "true"
    
    RA->>PRA: Delegate: process refund with eligibility status
    PRA->>PRA: Check eligibility status from session
    PRA->>PAY: Process refund transaction
    PAY-->>PRA: Transaction successful
    PRA-->>RA: Final response message
    
    RA->>C: "✅ Reembolso processado com sucesso!<br/>Obrigado por ser cliente da Natura! 💄✨🌿"
    
    Note over C,PAY: Tempo total: ~5-8 segundos (overhead de coordenação)
```

### Sub-Agent Communication Detail

```mermaid
sequenceDiagram
    participant RA as 🟠 Root Agent
    participant PHA as 📋 Purchase Agent
    participant EA as ✅ Eligibility Agent
    participant PRA as 💳 Process Agent
    participant SS as 📝 Session State
    
    Note over RA,SS: Comunicação entre Sub-Agentes via Session State
    
    RA->>PHA: Execute with context
    PHA->>SS: Write: purchase_history = [{order_id: "...", shipping: "INSURED", ...}]
    PHA-->>RA: Task completed
    
    RA->>EA: Execute with context + purchase_history
    EA->>SS: Read: purchase_history
    EA->>EA: Extract shipping_method = "INSURED"
    EA->>EA: Convert reason → "DAMAGED"
    EA->>EA: Validate: INSURED + DAMAGED = eligible
    EA->>SS: Write: is_refund_eligible = "true"
    EA-->>RA: Task completed
    
    RA->>PRA: Execute with context + all previous data
    PRA->>SS: Read: is_refund_eligible
    PRA->>PRA: if eligible: process_refund()
    PRA->>SS: Write: refund_confirmation_message
    PRA-->>RA: Final response ready
    
    RA->>SS: Read: final response
    
    Note over RA,SS: Estado da sessão mantém contexto entre agentes
```

## 🟡 Sequential Workflow - Sequence Diagram

### Fixed Sequential Execution

```mermaid
sequenceDiagram
    participant C as 👤 Cliente
    participant SW as 🟡 Sequential Workflow
    participant PVA as 1️⃣ Purchase Verifier Agent
    participant REA as 2️⃣ Refund Eligibility Agent
    participant RPA as 3️⃣ Refund Processor Agent
    participant DB as 📊 Database
    participant PAY as 💰 Payment Gateway
    
    Note over C,PAY: Sequential Workflow - Execução Obrigatória em Ordem
    
    C->>SW: "Massini - produto danificado"
    
    Note over SW: Etapa 1: Purchase Verification (obrigatória)
    SW->>PVA: Execute step 1
    PVA->>DB: get_purchase_history("Massini")
    DB-->>PVA: Customer data
    PVA-->>SW: purchase_history = [...], step 1 complete ✅
    
    Note over SW: Etapa 2: Eligibility Check (depende da etapa 1)
    SW->>REA: Execute step 2 with previous results
    REA->>REA: Extract shipping from step 1 data
    REA->>REA: check_refund_eligibility("DAMAGED", "INSURED")
    REA-->>SW: is_refund_eligible = "true", step 2 complete ✅
    
    Note over SW: Etapa 3: Refund Processing (depende das etapas 1+2)
    SW->>RPA: Execute step 3 with all previous results
    RPA->>RPA: Check eligibility from step 2
    RPA->>PAY: process_refund(74.80, "NAT002-20250610")
    PAY-->>RPA: Transaction successful
    RPA-->>SW: refund_confirmation_message, step 3 complete ✅
    
    SW->>C: "✅ Reembolso processado! Obrigado pela Natura! 💄✨🌿"
    
    Note over C,PAY: Tempo total: ~6-10 segundos (soma de todas as etapas)
```

### Error Handling in Sequential Flow

```mermaid
sequenceDiagram
    participant C as 👤 Cliente
    participant SW as 🟡 Sequential Workflow
    participant PVA as 1️⃣ Purchase Verifier
    participant REA as 2️⃣ Eligibility Agent
    participant RPA as 3️⃣ Processor Agent
    participant DB as 📊 Database
    
    Note over C,DB: Tratamento de Erro no Fluxo Sequencial
    
    C->>SW: "João - produto danificado"
    
    Note over SW: Etapa 1: Verifica compras
    SW->>PVA: Execute step 1
    PVA->>DB: get_purchase_history("João")
    DB-->>PVA: [] (empty - no history found)
    PVA-->>SW: purchase_history = [], step 1 complete ✅
    
    Note over SW: Etapa 2: Continua mesmo com histórico vazio
    SW->>REA: Execute step 2 (will fail due to empty history)
    REA->>REA: Cannot extract shipping method from empty history
    REA-->>SW: is_refund_eligible = "false", step 2 complete ✅
    
    Note over SW: Etapa 3: Processa negação
    SW->>RPA: Execute step 3 (will deny)
    RPA->>RPA: Check eligibility = "false"
    RPA->>RPA: Generate denial message
    RPA-->>SW: denial_message, step 3 complete ✅
    
    SW->>C: "Lamento, mas não é possível atender à sua solicitação.<br/>Obrigado pela Natura! 💄✨🌿"
    
    Note over C,DB: Fluxo sempre completa todas as 3 etapas, mesmo com falhas
```

## 🟢 Parallel Workflow - Sequence Diagram

### Parallel Execution Block

```mermaid
sequenceDiagram
    participant C as 👤 Cliente
    participant SW as 🟢 Sequential Wrapper
    participant PA as 🟢 Parallel Agent
    participant PVA as 📋 Purchase Verifier
    participant REA as ✅ Eligibility Agent (Parallel)
    participant RPA as 💳 Refund Processor
    participant DB as 📊 Database
    participant PAY as 💰 Payment Gateway
    
    Note over C,PAY: Parallel Workflow - Otimização de Performance
    
    C->>SW: "Massini - produto danificado"
    
    Note over SW: Etapa 1: Bloco Paralelo (PurchaseVerifier + EligibilityAgent)
    SW->>PA: Execute parallel block
    
    par Execução Paralela
        PA->>PVA: Execute purchase verification
        PVA->>DB: get_purchase_history("Massini")
        DB-->>PVA: Customer data
        PVA-->>PA: purchase_history = [...]
    and
        PA->>REA: Execute eligibility check (parallel version)
        Note over REA: Assumes INSURED shipping method
        REA->>REA: check_refund_eligibility("DAMAGED", "INSURED")
        REA-->>PA: is_refund_eligible = "true"
    end
    
    PA-->>SW: Both parallel tasks complete ✅
    
    Note over SW: Etapa 2: Sequential Processing (usa resultados paralelos)
    SW->>RPA: Execute final processing
    RPA->>RPA: Check eligibility from parallel results
    RPA->>PAY: process_refund(74.80, "NAT002-20250610")
    PAY-->>RPA: Transaction successful
    RPA-->>SW: refund_confirmation_message
    
    SW->>C: "✅ Reembolso processado! Obrigado pela Natura! 💄✨🌿"
    
    Note over C,PAY: Tempo total: ~4-6 segundos (33% melhoria vs sequential)
```

### Performance Comparison

```mermaid
sequenceDiagram
    participant Sequential as 🟡 Sequential (9s)
    participant Parallel as 🟢 Parallel (6s)
    participant Timeline as ⏱️ Timeline
    
    Note over Sequential,Timeline: Comparação de Performance
    
    Sequential->>Timeline: 0s: Start
    Sequential->>Timeline: 3s: Step 1 Complete
    Sequential->>Timeline: 6s: Step 2 Complete
    Sequential->>Timeline: 9s: Step 3 Complete
    
    Parallel->>Timeline: 0s: Start
    
    Note over Parallel: Steps 1&2 execute in parallel
    Parallel->>Timeline: 3s: Parallel Block Complete
    Parallel->>Timeline: 6s: Step 3 Complete
    
    Note over Sequential,Timeline: Parallel Workflow: 33% faster execution
```

## 🟣 Custom Control Flow - Sequence Diagram

### Full Refund Path (Eligible Customer)

```mermaid
sequenceDiagram
    participant C as 👤 Cliente
    participant CRA as 🟣 Custom Refund Agent
    participant PA as 🟢 Parallel Block
    participant PVA as 📋 Purchase Agent
    participant REA as ✅ Eligibility Agent
    participant PFR as 💰 Process Full Refund
    participant DB as 📊 Database
    participant PAY as 💰 Payment Gateway
    
    Note over C,PAY: Custom Control Flow - Full Refund Path
    
    C->>CRA: "Massini - produto danificado"
    
    Note over CRA: 1. Execute parallel checks
    CRA->>PA: Run parallel verification
    
    par Parallel Execution
        PA->>PVA: get_purchase_history("Massini")
        PVA->>DB: Query customer
        DB-->>PVA: Customer data
        PVA-->>PA: purchase_history = [...]
    and
        PA->>REA: check_eligibility (assumes INSURED)
        REA->>REA: validate business rules
        REA-->>PA: is_refund_eligible = "true"
    end
    
    PA-->>CRA: Parallel results complete
    
    Note over CRA: 2. Custom decision logic
    CRA->>CRA: if (eligible && purchase_history): full_refund_path()
    
    Note over CRA: 3. Execute full refund
    CRA->>PFR: Process full refund
    PFR->>PAY: process_refund(74.80, "NAT002-20250610")
    PAY-->>PFR: Transaction successful
    PFR-->>CRA: Refund confirmation
    
    CRA->>C: "✅ Reembolso processado! Obrigado pela Natura! 💄✨🌿"
    
    Note over C,PAY: Tempo total: ~6-8 segundos
```

### Store Credit Path (Non-Eligible Customer)

```mermaid
sequenceDiagram
    participant C as 👤 Cliente
    participant CRA as 🟣 Custom Refund Agent
    participant PA as 🟢 Parallel Block
    participant OSC as 🎫 Offer Store Credit
    participant PSCR as 🤝 Process Credit Response
    participant DB as 📊 Database
    
    Note over C,DB: Custom Control Flow - Store Credit Path
    
    C->>CRA: "Erike - não gostei do produto"
    
    Note over CRA: 1. Execute parallel checks
    CRA->>PA: Run parallel verification
    PA-->>CRA: purchase_history = [...], is_refund_eligible = "false"
    
    Note over CRA: 2. Custom decision logic
    CRA->>CRA: if (not eligible && purchase_history): store_credit_path()
    
    Note over CRA: 3. Offer store credit alternative
    CRA->>OSC: Offer 50% store credit
    OSC-->>CRA: Credit offer message
    CRA->>C: "Embora não possamos processar reembolso,<br/>oferecemos 50% de crédito (R$61.40).<br/>Você aceita?"
    
    C->>CRA: "Sim, aceito"
    
    Note over CRA: 4. Process credit acceptance
    CRA->>PSCR: Process customer response
    PSCR->>PSCR: Generate credit confirmation
    PSCR-->>CRA: Credit confirmation message
    
    CRA->>C: "Perfeito! Enviaremos R$61.40 em crédito.<br/>Obrigado pela Natura! 💄✨🌿"
    
    Note over C,DB: Tempo total: ~8-10 segundos (inclui interação adicional)
```

### No History Path (Error Handling)

```mermaid
sequenceDiagram
    participant C as 👤 Cliente
    participant CRA as 🟣 Custom Refund Agent
    participant PA as 🟢 Parallel Block
    participant FRA as 📝 Final Response Agent
    participant DB as 📊 Database
    
    Note over C,DB: Custom Control Flow - No History Path
    
    C->>CRA: "João - produto danificado"
    
    Note over CRA: 1. Execute parallel checks
    CRA->>PA: Run parallel verification
    PA->>DB: Query customer data
    DB-->>PA: [] (empty result)
    PA-->>CRA: purchase_history = [], is_refund_eligible = N/A
    
    Note over CRA: 2. Custom decision logic
    CRA->>CRA: if (not purchase_history): handle_no_history()
    
    Note over CRA: 3. Generate error message
    CRA->>CRA: Create error message for no history
    CRA->>FRA: Output specific error message
    FRA-->>CRA: Formatted error response
    
    CRA->>C: "Não encontramos histórico de compras associado à sua conta.<br/>Verifique seus dados e tente novamente.<br/>Obrigado pela Natura! 💄✨🌿"
    
    Note over C,DB: Tempo total: ~4-6 segundos (path mais curto)
```

## ⚡ Performance Analysis

### Response Time Comparison

```mermaid
sequenceDiagram
    participant Metric as 📊 Performance Metrics
    participant Single as 🔵 Single (3-5s)
    participant Multi as 🟠 Multi (5-8s)
    participant Sequential as 🟡 Sequential (6-10s)
    participant Parallel as 🟢 Parallel (4-6s)
    participant Custom as 🟣 Custom (6-12s)
    
    Note over Metric,Custom: Comparison of Response Times
    
    Metric->>Single: Fastest for simple cases
    Metric->>Multi: Overhead of coordination
    Metric->>Sequential: Sum of all steps
    Metric->>Parallel: Optimized execution
    Metric->>Custom: Variable by path
    
    Note over Single: ✅ Best for MVP/prototypes
    Note over Multi: ✅ Best for modularity
    Note over Sequential: ✅ Best for reliability
    Note over Parallel: ✅ Best for performance
    Note over Custom: ✅ Best for complex logic
```

### Error Handling Patterns

```mermaid
sequenceDiagram
    participant Error as ❌ Error Scenarios
    participant Patterns as 🔧 Handling Patterns
    participant Recovery as 🔄 Recovery Actions
    
    Note over Error,Recovery: Error Handling Across Patterns
    
    Error->>Patterns: No customer history found
    Patterns->>Recovery: Graceful degradation + clear message
    
    Error->>Patterns: External service timeout
    Patterns->>Recovery: Retry logic + fallback response
    
    Error->>Patterns: Invalid input data
    Patterns->>Recovery: Input validation + user guidance
    
    Error->>Patterns: Business rule violation
    Patterns->>Recovery: Alternative offerings (store credit)
    
    Error->>Patterns: System overload
    Patterns->>Recovery: Queue management + estimated wait time
    
    Note over Error,Recovery: Consistent error handling maintains user experience
```

Esta documentação de sequência fornece uma visão detalhada das interações entre componentes, permitindo entender o timing, dependencies e fluxo de dados em cada padrão arquitetural do sistema de reembolso Natura.
