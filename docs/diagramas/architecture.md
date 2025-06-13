# Architecture Diagrams - Sistema de Reembolso Natura

## 📋 Visão Geral

Esta seção apresenta os diagramas de arquitetura do sistema de reembolso Natura, mostrando desde a visão high-level até os detalhes de implementação dos diferentes padrões de agentes.

## 🏗️ Arquitetura Geral do Sistema

### Sistema Completo - Visão High-Level

```mermaid
graph TB
    subgraph "Cliente Final"
        C[👤 Cliente Natura<br/>Solicita Reembolso]
    end
    
    subgraph "Interface Layer"
        WEB[🌐 Interface Web]
        API[🔌 API Gateway]
        CHAT[💬 Chat Interface]
    end
    
    subgraph "Agent Development Kit (ADK)"
        GEMINI[🤖 Gemini 2.5 Flash Preview]
        
        subgraph "Agent Patterns"
            direction LR
            SA[🔵 Single Agent]
            MA[🟠 Multi Agent]
            SEQ[🟡 Sequential]
            PAR[🟢 Parallel]
            CUSTOM[🟣 Custom Flow]
        end
        
        subgraph "Core Components"
            TOOLS[🔧 Tools Layer<br/>get_purchase_history<br/>check_refund_eligibility<br/>process_refund]
            PROMPTS[💭 Prompts Engine<br/>Specialized Instructions]
            SESSION[📝 Session Management<br/>State & Context]
        end
    end
    
    subgraph "Data Layer"
        DB[(📊 Customer Database<br/>Purchase History)]
        LOGS[(📋 Audit Logs<br/>Compliance)]
        CACHE[(⚡ Cache Layer<br/>Performance)]
    end
    
    subgraph "External Services"
        PAYMENT[💳 Payment Processor<br/>Refund Processing]
        NOTIFY[📧 Notification Service<br/>Email/SMS]
        ANALYTICS[📈 Analytics Platform<br/>Insights]
    end
    
    %% Connections
    C --> WEB & CHAT
    WEB & CHAT --> API
    API --> GEMINI
    GEMINI --> SA & MA & SEQ & PAR & CUSTOM
    SA & MA & SEQ & PAR & CUSTOM --> TOOLS
    SA & MA & SEQ & PAR & CUSTOM --> PROMPTS
    SA & MA & SEQ & PAR & CUSTOM --> SESSION
    
    TOOLS --> DB & CACHE
    TOOLS --> PAYMENT
    SESSION --> LOGS
    PAYMENT --> NOTIFY
    LOGS --> ANALYTICS
    
    %% Styling
    classDef clientStyle fill:#e8f5e8,stroke:#2e7d2e,stroke-width:3px
    classDef agentStyle fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef dataStyle fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef externalStyle fill:#fce4ec,stroke:#c2185b,stroke-width:2px
    
    class C clientStyle
    class SA,MA,SEQ,PAR,CUSTOM agentStyle
    class DB,LOGS,CACHE dataStyle
    class PAYMENT,NOTIFY,ANALYTICS externalStyle
```

## 🔄 Comparação de Padrões Arquiteturais

### Os 5 Padrões Lado a Lado

```mermaid
graph TB
    subgraph "1. Single Agent"
        SA_INPUT[📥 Input] --> SA_AGENT[🔵 RefundSingleAgent]
        SA_AGENT --> SA_TOOLS[🔧 All Tools]
        SA_TOOLS --> SA_OUTPUT[📤 Output]
        
        SA_METRICS[⏱️ 3-5s<br/>🔧 Simple<br/>📊 Low Scale]
    end
    
    subgraph "2. Multi Agent"
        MA_INPUT[📥 Input] --> MA_COORD[🟠 Coordinator]
        MA_COORD --> MA_SUB1[📋 Purchase Agent]
        MA_COORD --> MA_SUB2[✅ Eligibility Agent]
        MA_COORD --> MA_SUB3[💳 Process Agent]
        MA_SUB1 & MA_SUB2 & MA_SUB3 --> MA_OUTPUT[📤 Output]
        
        MA_METRICS[⏱️ 5-8s<br/>🔧 Modular<br/>📊 Med Scale]
    end
    
    subgraph "3. Sequential Workflow"
        SEQ_INPUT[📥 Input] --> SEQ_STEP1[1️⃣ Purchase Verifier]
        SEQ_STEP1 --> SEQ_STEP2[2️⃣ Eligibility Check]
        SEQ_STEP2 --> SEQ_STEP3[3️⃣ Refund Processor]
        SEQ_STEP3 --> SEQ_OUTPUT[📤 Output]
        
        SEQ_METRICS[⏱️ 6-10s<br/>🔧 Structured<br/>📊 Reliable]
    end
    
    subgraph "4. Parallel Workflow"
        PAR_INPUT[📥 Input] --> PAR_PARALLEL[🟢 Parallel Block]
        PAR_PARALLEL --> PAR_P1[📋 Purchase] & PAR_P2[✅ Eligibility]
        PAR_P1 & PAR_P2 --> PAR_SEQ[💳 Sequential Process]
        PAR_SEQ --> PAR_OUTPUT[📤 Output]
        
        PAR_METRICS[⏱️ 4-6s<br/>🔧 Optimized<br/>📊 High Perf]
    end
    
    subgraph "5. Custom Control Flow"
        CUSTOM_INPUT[📥 Input] --> CUSTOM_PARALLEL[🟣 Parallel Checks]
        CUSTOM_PARALLEL --> CUSTOM_DECISION{🤔 Custom Logic}
        CUSTOM_DECISION -->|Eligible| CUSTOM_REFUND[💰 Full Refund]
        CUSTOM_DECISION -->|Not Eligible| CUSTOM_CREDIT[🎫 Store Credit]
        CUSTOM_DECISION -->|No History| CUSTOM_ERROR[❌ Error Message]
        CUSTOM_REFUND & CUSTOM_CREDIT & CUSTOM_ERROR --> CUSTOM_OUTPUT[📤 Output]
        
        CUSTOM_METRICS[⏱️ 6-12s<br/>🔧 Complex<br/>📊 Flexible]
    end
    
    %% Styling for clarity
    classDef singleStyle fill:#e3f2fd,stroke:#1976d2
    classDef multiStyle fill:#fff3e0,stroke:#f57c00
    classDef seqStyle fill:#f3e5f5,stroke:#7b1fa2
    classDef parStyle fill:#e8f5e8,stroke:#388e3c
    classDef customStyle fill:#fce4ec,stroke:#c2185b
    
    class SA_INPUT,SA_AGENT,SA_TOOLS,SA_OUTPUT,SA_METRICS singleStyle
    class MA_INPUT,MA_COORD,MA_SUB1,MA_SUB2,MA_SUB3,MA_OUTPUT,MA_METRICS multiStyle
    class SEQ_INPUT,SEQ_STEP1,SEQ_STEP2,SEQ_STEP3,SEQ_OUTPUT,SEQ_METRICS seqStyle
    class PAR_INPUT,PAR_PARALLEL,PAR_P1,PAR_P2,PAR_SEQ,PAR_OUTPUT,PAR_METRICS parStyle
    class CUSTOM_INPUT,CUSTOM_PARALLEL,CUSTOM_DECISION,CUSTOM_REFUND,CUSTOM_CREDIT,CUSTOM_ERROR,CUSTOM_OUTPUT,CUSTOM_METRICS customStyle
```

## 🧩 Componentes Detalhados

### Tools Layer Architecture

```mermaid
graph LR
    subgraph "Tools Layer"
        direction TB
        
        subgraph "Data Access Tools"
            GPH[📋 get_purchase_history<br/>🎯 Customer Lookup<br/>📊 History Retrieval]
        end
        
        subgraph "Business Logic Tools"
            CRE[✅ check_refund_eligibility<br/>🔍 Policy Validation<br/>⚖️ Rules Engine]
        end
        
        subgraph "Processing Tools"
            PR[💳 process_refund<br/>💰 Payment Processing<br/>📧 Notification]
        end
        
        subgraph "Core Services"
            DB[(📊 Customer Database)]
            RULES[(📋 Business Rules)]
            PAYMENT[(💳 Payment Gateway)]
        end
    end
    
    GPH --> DB
    CRE --> RULES
    PR --> PAYMENT
    
    subgraph "Agents"
        AGENT1[🤖 Any Agent Pattern]
        AGENT2[🤖 Any Agent Pattern]
        AGENT3[🤖 Any Agent Pattern]
    end
    
    AGENT1 & AGENT2 & AGENT3 --> GPH & CRE & PR
    
    classDef toolStyle fill:#e8f5e8,stroke:#2e7d2e,stroke-width:2px
    classDef serviceStyle fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef agentStyle fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    
    class GPH,CRE,PR toolStyle
    class DB,RULES,PAYMENT serviceStyle
    class AGENT1,AGENT2,AGENT3 agentStyle
```

### Prompts Engine Architecture

```mermaid
graph TB
    subgraph "Prompts Engine"
        direction LR
        
        subgraph "Core Prompts"
            TOP[🎯 top_level_prompt<br/>Main Coordinator<br/>Full Process Flow]
        end
        
        subgraph "Specialized Prompts"
            PH[📋 purchase_history<br/>Data Retrieval<br/>Format Standardization]
            
            CE[✅ check_eligibility<br/>Sequential Version<br/>History Dependent]
            
            CEP[⚡ check_eligibility_parallel<br/>Parallel Version<br/>Assumes INSURED]
            
            PR[💳 process_refund<br/>Final Processing<br/>Success/Failure]
        end
        
        subgraph "Prompt Features"
            PERSONALITY[😊 Natura Personality<br/>Friendly & Professional]
            LOCALIZATION[🇧🇷 Brazilian Portuguese<br/>Local Context]
            INSTRUCTIONS[📝 Step-by-Step<br/>Clear Instructions]
            FORMATTING[📋 Output Formatting<br/>Structured Responses]
        end
    end
    
    TOP --> PH & CE & CEP & PR
    PH & CE & CEP & PR --> PERSONALITY & LOCALIZATION & INSTRUCTIONS & FORMATTING
    
    subgraph "Agent Integration"
        SA_AGENT[🔵 Single Agent] --> TOP
        MA_COORD[🟠 Multi Coordinator] --> TOP
        MA_SUB[🟠 Multi Sub-Agents] --> PH & CE & PR
        SEQ_AGENTS[🟡 Sequential Agents] --> PH & CE & PR
        PAR_AGENTS[🟢 Parallel Agents] --> PH & CEP & PR
        CUSTOM_AGENTS[🟣 Custom Agents] --> PH & CEP & PR
    end
    
    classDef coreStyle fill:#e3f2fd,stroke:#1976d2,stroke-width:3px
    classDef specialStyle fill:#e8f5e8,stroke:#2e7d2e,stroke-width:2px
    classDef featureStyle fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef agentStyle fill:#fce4ec,stroke:#c2185b,stroke-width:2px
    
    class TOP coreStyle
    class PH,CE,CEP,PR specialStyle
    class PERSONALITY,LOCALIZATION,INSTRUCTIONS,FORMATTING featureStyle
    class SA_AGENT,MA_COORD,MA_SUB,SEQ_AGENTS,PAR_AGENTS,CUSTOM_AGENTS agentStyle
```

## 🔄 Data Flow Architecture

### Complete Data Flow Through System

```mermaid
graph TD
    subgraph "Input Processing"
        USER_INPUT[👤 User Input<br/>"Massini - produto danificado"]
        PARSE[🔍 Input Parsing<br/>Name Extraction<br/>Reason Extraction]
    end
    
    subgraph "Agent Processing"
        AGENT[🤖 Selected Agent Pattern<br/>Business Logic Processing]
        
        subgraph "Tool Calls"
            T1[📋 get_purchase_history("Massini")]
            T2[✅ check_refund_eligibility("DAMAGED", "INSURED")]
            T3[💳 process_refund(74.80, "NAT002-20250610")]
        end
        
        subgraph "Data Transformation"
            CONVERT[🔄 Reason Mapping<br/>"danificado" → DAMAGED]
            EXTRACT[📤 Data Extraction<br/>shipping_method: INSURED]
            VALIDATE[✔️ Policy Validation<br/>INSURED + DAMAGED = ✅]
        end
    end
    
    subgraph "Data Storage"
        SESSION[📝 Session State<br/>purchase_history: [...]<br/>is_refund_eligible: true]
        LOGS[📋 Audit Logs<br/>Compliance Recording]
        CACHE[⚡ Cache Updates<br/>Performance Optimization]
    end
    
    subgraph "Output Generation"
        RESPONSE[📤 Formatted Response<br/>Natura Branding<br/>Emojis + Thanks]
        NOTIFY[📧 Notifications<br/>Email Confirmation<br/>SMS Updates]
    end
    
    USER_INPUT --> PARSE
    PARSE --> AGENT
    AGENT --> T1 --> EXTRACT
    AGENT --> CONVERT --> T2 --> VALIDATE
    VALIDATE --> T3
    
    T1 & T2 & T3 --> SESSION
    SESSION --> LOGS & CACHE
    SESSION --> RESPONSE
    RESPONSE --> NOTIFY
    
    classDef inputStyle fill:#e8f5e8,stroke:#2e7d2e,stroke-width:2px
    classDef processStyle fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef storageStyle fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef outputStyle fill:#fce4ec,stroke:#c2185b,stroke-width:2px
    
    class USER_INPUT,PARSE inputStyle
    class AGENT,T1,T2,T3,CONVERT,EXTRACT,VALIDATE processStyle
    class SESSION,LOGS,CACHE storageStyle
    class RESPONSE,NOTIFY outputStyle
```

## 🚀 Deployment Architecture

### Production Deployment Scenario

```mermaid
graph TB
    subgraph "Load Balancing"
        LB[⚖️ Load Balancer<br/>AWS ALB / GCP Load Balancer]
    end
    
    subgraph "Web Tier"
        WEB1[🌐 Web Server 1<br/>React/Next.js Frontend]
        WEB2[🌐 Web Server 2<br/>React/Next.js Frontend]
        WEB3[🌐 Web Server 3<br/>React/Next.js Frontend]
    end
    
    subgraph "API Gateway Tier"
        API1[🔌 API Gateway 1<br/>Request Routing]
        API2[🔌 API Gateway 2<br/>Request Routing]
    end
    
    subgraph "Agent Processing Tier"
        direction LR
        
        subgraph "Agent Cluster A"
            A1[🤖 Agent Instance 1]
            A2[🤖 Agent Instance 2]
        end
        
        subgraph "Agent Cluster B"
            B1[🤖 Agent Instance 3]
            B2[🤖 Agent Instance 4]
        end
    end
    
    subgraph "Data Tier"
        PRIMARY[(📊 Primary Database<br/>Customer Data)]
        REPLICA[(📊 Read Replica<br/>Performance)]
        REDIS[(⚡ Redis Cache<br/>Session & Performance)]
    end
    
    subgraph "External Services"
        GEMINI[🤖 Google Gemini API<br/>LLM Processing]
        PAYMENT[💳 Payment Gateway<br/>Refund Processing]
        NOTIFY[📧 Notification Service<br/>SendGrid / AWS SES]
    end
    
    subgraph "Monitoring & Security"
        MONITOR[📊 Monitoring<br/>Prometheus/Grafana]
        LOGS[📋 Centralized Logs<br/>ELK Stack]
        SECURITY[🔒 Security<br/>WAF / Auth]
    end
    
    %% Connections
    LB --> WEB1 & WEB2 & WEB3
    WEB1 & WEB2 & WEB3 --> API1 & API2
    API1 & API2 --> A1 & A2 & B1 & B2
    
    A1 & A2 & B1 & B2 --> PRIMARY
    A1 & A2 & B1 & B2 --> REPLICA
    A1 & A2 & B1 & B2 --> REDIS
    
    A1 & A2 & B1 & B2 --> GEMINI
    A1 & A2 & B1 & B2 --> PAYMENT
    A1 & A2 & B1 & B2 --> NOTIFY
    
    MONITOR --> A1 & A2 & B1 & B2
    LOGS --> A1 & A2 & B1 & B2
    SECURITY --> API1 & API2
    
    classDef lbStyle fill:#e8f5e8,stroke:#2e7d2e,stroke-width:3px
    classDef webStyle fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef agentStyle fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef dataStyle fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef externalStyle fill:#fce4ec,stroke:#c2185b,stroke-width:2px
    classDef opsStyle fill:#fff8e1,stroke:#f9a825,stroke-width:2px
    
    class LB lbStyle
    class WEB1,WEB2,WEB3,API1,API2 webStyle
    class A1,A2,B1,B2 agentStyle
    class PRIMARY,REPLICA,REDIS dataStyle
    class GEMINI,PAYMENT,NOTIFY externalStyle
    class MONITOR,LOGS,SECURITY opsStyle
```

## 📊 Performance & Scalability

### System Capacity Planning

```mermaid
graph LR
    subgraph "Traffic Patterns"
        PEAK[🔝 Peak Hours<br/>1000 req/min<br/>Business Hours]
        NORMAL[📊 Normal Load<br/>200 req/min<br/>Regular Traffic]
        LOW[📉 Low Traffic<br/>50 req/min<br/>Night Hours]
    end
    
    subgraph "Agent Pattern Performance"
        SINGLE[🔵 Single Agent<br/>⏱️ 3-5s<br/>🔧 1 instance/req]
        MULTI[🟠 Multi Agent<br/>⏱️ 5-8s<br/>🔧 3 instances/req]
        PARALLEL[🟢 Parallel<br/>⏱️ 4-6s<br/>🔧 2 instances/req]
        CUSTOM[🟣 Custom<br/>⏱️ 6-12s<br/>🔧 3-5 instances/req]
    end
    
    subgraph "Scaling Strategy"
        AUTO[🔄 Auto Scaling<br/>CPU/Memory Based<br/>Response Time Based]
        HORIZONTAL[📈 Horizontal Scale<br/>Add More Instances<br/>Load Distribution]
        VERTICAL[⬆️ Vertical Scale<br/>Increase Instance Size<br/>Better Performance]
    end
    
    PEAK --> SINGLE & MULTI & PARALLEL & CUSTOM
    NORMAL --> SINGLE & MULTI & PARALLEL & CUSTOM
    LOW --> SINGLE & MULTI & PARALLEL & CUSTOM
    
    SINGLE & MULTI & PARALLEL & CUSTOM --> AUTO
    AUTO --> HORIZONTAL & VERTICAL
    
    classDef trafficStyle fill:#e8f5e8,stroke:#2e7d2e,stroke-width:2px
    classDef agentStyle fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef scaleStyle fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    
    class PEAK,NORMAL,LOW trafficStyle
    class SINGLE,MULTI,PARALLEL,CUSTOM agentStyle
    class AUTO,HORIZONTAL,VERTICAL scaleStyle
```

## 🔐 Security Architecture

### Security Layers

```mermaid
graph TB
    subgraph "Security Perimeter"
        WAF[🛡️ Web Application Firewall<br/>DDoS Protection<br/>Bot Detection]
        CDN[🌐 Content Delivery Network<br/>Edge Security<br/>SSL Termination]
    end
    
    subgraph "Application Security"
        AUTH[🔐 Authentication<br/>OAuth 2.0 / JWT<br/>Multi-Factor Auth]
        AUTHZ[✅ Authorization<br/>Role-Based Access<br/>Permission Management]
        ENCRYPT[🔒 Encryption<br/>Data at Rest<br/>Data in Transit]
    end
    
    subgraph "Data Protection"
        PII[👤 PII Protection<br/>Customer Data<br/>LGPD Compliance]
        AUDIT[📋 Audit Logging<br/>Access Tracking<br/>Compliance Reports]
        BACKUP[💾 Secure Backups<br/>Encrypted Storage<br/>Disaster Recovery]
    end
    
    subgraph "API Security"
        RATE[⏱️ Rate Limiting<br/>Abuse Prevention<br/>Fair Usage]
        VALIDATE[✔️ Input Validation<br/>Injection Prevention<br/>Data Sanitization]
        MONITOR[👁️ Security Monitoring<br/>Threat Detection<br/>Incident Response]
    end
    
    WAF --> AUTH
    CDN --> AUTH
    AUTH --> AUTHZ
    AUTHZ --> ENCRYPT
    
    ENCRYPT --> PII
    PII --> AUDIT
    AUDIT --> BACKUP
    
    ENCRYPT --> RATE
    RATE --> VALIDATE
    VALIDATE --> MONITOR
    
    classDef perimeterStyle fill:#ffebee,stroke:#d32f2f,stroke-width:3px
    classDef appStyle fill:#e8f5e8,stroke:#2e7d2e,stroke-width:2px
    classDef dataStyle fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef apiStyle fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    
    class WAF,CDN perimeterStyle
    class AUTH,AUTHZ,ENCRYPT appStyle
    class PII,AUDIT,BACKUP dataStyle
    class RATE,VALIDATE,MONITOR apiStyle
```

Esta documentação de arquitetura fornece uma visão completa e detalhada do sistema de reembolso Natura, desde os componentes básicos até estratégias de deployment e segurança em produção.
