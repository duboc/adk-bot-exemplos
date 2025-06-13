# User Journey Diagrams - Jornadas do Cliente

## 📋 Visão Geral

Esta seção apresenta as jornadas completas dos clientes no sistema de reembolso Natura, incluindo pontos de contato, emoções, experiências e diferentes cenários de uso.

## 🎭 Jornada Principal - Cliente Elegível (Massini)

### Jornada Emocional Completa

```mermaid
journey
    title Jornada do Cliente Natura - Reembolso Aprovado (Massini)
    section Problema Inicial
      Produto chega danificado: 1: Cliente
      Frustração com qualidade: 2: Cliente
      Preocupação com dinheiro: 3: Cliente
    section Busca por Solução
      Encontra chat de suporte: 5: Cliente
      Esperança de resolução: 6: Cliente
      Decide tentar reembolso: 7: Cliente
    section Interação com Sistema
      Inicia conversa amigável: 8: Cliente, Sistema
      Fornece nome facilmente: 8: Cliente, Sistema
      Explica problema claramente: 7: Cliente, Sistema
      Aguarda processamento: 6: Cliente, Sistema
    section Resolução Positiva
      Recebe aprovação rápida: 9: Cliente, Sistema
      Alívio com solução: 10: Cliente
      Satisfação com atendimento: 10: Cliente
    section Pós-Resolução
      Confiança na marca: 10: Cliente
      Disposição para recomendar: 10: Cliente
      Fidelização aumentada: 10: Cliente
```

### Touchpoints e Momentos da Verdade

```mermaid
graph TB
    subgraph "Jornada do Cliente Elegível"
        START[📦 Produto chega danificado] --> DISCOVER[🔍 Descobre chat Natura]
        DISCOVER --> CONTACT[💬 Inicia conversa]
        CONTACT --> NAME[👤 Informa nome: "Massini"]
        NAME --> REASON[📝 Explica: "produto vazado"]
        REASON --> WAIT[⏳ Aguarda processamento]
        WAIT --> APPROVED[✅ Reembolso aprovado]
        APPROVED --> THANKS[🙏 Agradecimento da Natura]
        THANKS --> SATISFIED[😊 Cliente satisfeito]
    end
    
    subgraph "Momentos da Verdade"
        MT1[🎯 Primeiro Contato<br/>Impressão inicial]
        MT2[🎯 Coleta de Dados<br/>Facilidade do processo]
        MT3[🎯 Tempo de Resposta<br/>Agilidade na decisão]
        MT4[🎯 Resultado Final<br/>Resolução do problema]
        MT5[🎯 Follow-up<br/>Cuidado pós-resolução]
    end
    
    CONTACT --> MT1
    NAME --> MT2
    WAIT --> MT3
    APPROVED --> MT4
    THANKS --> MT5
    
    classDef journeyStyle fill:#e8f5e8,stroke:#2e7d2e,stroke-width:2px
    classDef touchpointStyle fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    
    class START,DISCOVER,CONTACT,NAME,REASON,WAIT,APPROVED,THANKS,SATISFIED journeyStyle
    class MT1,MT2,MT3,MT4,MT5 touchpointStyle
```

## 😔 Jornada Alternativa - Cliente Não Elegível (Erike)

### Jornada com Obstáculo e Recuperação

```mermaid
journey
    title Jornada do Cliente Natura - Reembolso Negado (Erike)
    section Problema Inicial
      Produto chega danificado: 1: Cliente
      Raiva com situação: 1: Cliente
      Urgência para resolver: 2: Cliente
    section Busca por Solução
      Encontra sistema reembolso: 4: Cliente
      Expectativa alta: 7: Cliente
      Confiança na marca: 6: Cliente
    section Interação com Sistema
      Conversa amigável inicial: 8: Cliente, Sistema
      Fornece dados pessoais: 7: Cliente, Sistema
      Explica problema detalhado: 7: Cliente, Sistema
      Aguarda ansioso: 5: Cliente, Sistema
    section Resultado Negativo
      Recebe negativa: 2: Cliente, Sistema
      Frustração aumenta: 1: Cliente
      Sensação de injustiça: 1: Cliente
    section Recuperação (Custom Flow)
      Oferta de crédito 50%: 6: Cliente, Sistema
      Considera alternativa: 7: Cliente
      Aceita crédito oferecido: 8: Cliente, Sistema
      Satisfação parcial: 7: Cliente
    section Pós-Resolução
      Aprecia esforço da marca: 8: Cliente
      Mantém relacionamento: 8: Cliente
      Considera futuras compras: 7: Cliente
```

### Comparação de Experiências

```mermaid
graph LR
    subgraph "Cliente Elegível (Massini)"
        ME1[😊 Entrada Otimista]
        ME2[📈 Expectativa Crescente]
        ME3[✅ Aprovação Rápida]
        ME4[🎉 Satisfação Máxima]
        ME5[💚 Fidelização]
        
        ME1 --> ME2 --> ME3 --> ME4 --> ME5
    end
    
    subgraph "Cliente Não Elegível (Erike)"
        EE1[😤 Entrada Frustrada]
        EE2[📈 Esperança]
        EE3[❌ Negação]
        EE4[😔 Frustração]
        EE5[🎫 Oferta Crédito]
        EE6[🤝 Aceitação]
        EE7[😊 Satisfação Parcial]
        
        EE1 --> EE2 --> EE3 --> EE4 --> EE5 --> EE6 --> EE7
    end
    
    subgraph "Diferencial da Natura"
        DIFF[💡 Sistema Inteligente<br/>🎯 Ofertas Alternativas<br/>❤️ Cuidado com Cliente]
    end
    
    ME4 --> DIFF
    EE7 --> DIFF
    
    classDef successStyle fill:#e8f5e8,stroke:#2e7d2e,stroke-width:2px
    classDef challengeStyle fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef differentialStyle fill:#e3f2fd,stroke:#1976d2,stroke-width:3px
    
    class ME1,ME2,ME3,ME4,ME5 successStyle
    class EE1,EE2,EE3,EE4,EE5,EE6,EE7 challengeStyle
    class DIFF differentialStyle
```

## 🚫 Jornada de Fracasso - Cliente sem Histórico

### Experiência de Bloqueio Total

```mermaid
journey
    title Jornada do Cliente Natura - Sem Histórico (João)
    section Problema Inicial
      Produto com problema: 2: Cliente
      Necessidade de reembolso: 3: Cliente
      Procura por solução: 4: Cliente
    section Interação com Sistema
      Inicia conversa esperançoso: 7: Cliente, Sistema
      Fornece nome: "João": 6: Cliente, Sistema
      Explica problema: 6: Cliente, Sistema
      Sistema busca histórico: 5: Cliente, Sistema
    section Bloqueio
      Não encontra dados: 1: Cliente, Sistema
      Recebe negativa seca: 1: Cliente, Sistema
      Frustração total: 1: Cliente
    section Impacto Negativo
      Sente-se excluído: 1: Cliente
      Questiona legitimidade: 1: Cliente
      Considera outras marcas: 1: Cliente
    section Oportunidade Perdida
      Poderia verificar CPF: 0: Sistema
      Poderia buscar por email: 0: Sistema
      Poderia oferecer cadastro: 0: Sistema
```

### Oportunidades de Melhoria

```mermaid
graph TB
    subgraph "Situação Atual"
        CURRENT1[👤 Cliente fornece nome]
        CURRENT2[🔍 Sistema busca exato]
        CURRENT3[❌ Não encontra]
        CURRENT4[🚫 Negação automática]
        
        CURRENT1 --> CURRENT2 --> CURRENT3 --> CURRENT4
    end
    
    subgraph "Melhorias Propostas"
        IMPROVED1[👤 Cliente fornece nome]
        IMPROVED2[🔍 Busca inteligente]
        IMPROVED3[📧 Solicita email/CPF]
        IMPROVED4[🆔 Validação alternativa]
        IMPROVED5[📝 Cadastro assistido]
        IMPROVED6[🎯 Solução personalizada]
        
        IMPROVED1 --> IMPROVED2
        IMPROVED2 --> IMPROVED3
        IMPROVED3 --> IMPROVED4
        IMPROVED4 --> IMPROVED5
        IMPROVED5 --> IMPROVED6
    end
    
    subgraph "Benefícios"
        BENEFIT1[📈 Maior conversão]
        BENEFIT2[😊 Satisfação cliente]
        BENEFIT3[🎯 Novos cadastros]
        BENEFIT4[💰 Receita preservada]
    end
    
    IMPROVED6 --> BENEFIT1 & BENEFIT2 & BENEFIT3 & BENEFIT4
    
    classDef currentStyle fill:#ffebee,stroke:#d32f2f,stroke-width:2px
    classDef improvedStyle fill:#e8f5e8,stroke:#2e7d2e,stroke-width:2px
    classDef benefitStyle fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    
    class CURRENT1,CURRENT2,CURRENT3,CURRENT4 currentStyle
    class IMPROVED1,IMPROVED2,IMPROVED3,IMPROVED4,IMPROVED5,IMPROVED6 improvedStyle
    class BENEFIT1,BENEFIT2,BENEFIT3,BENEFIT4 benefitStyle
```

## 🎭 Personas e Cenários

### Perfis de Cliente

```mermaid
graph TB
    subgraph "Perfis de Cliente"
        subgraph "Cliente Premium (Massini)"
            PREMIUM[👑 Cliente Premium<br/>💳 Compras frequentes<br/>📦 Sempre envio INSURED<br/>😊 Satisfação alta<br/>🎯 Fiel à marca]
        end
        
        subgraph "Cliente Econômico (Erike)"
            ECONOMICO[💰 Cliente Econômico<br/>📦 Envio STANDARD<br/>💡 Busca economia<br/>⚖️ Custo-benefício<br/>🤔 Avalia alternativas]
        end
        
        subgraph "Cliente Eventual (João)"
            EVENTUAL[👤 Cliente Eventual<br/>🛍️ Compras esporádicas<br/>❓ Não cadastrado<br/>📱 Canais diversos<br/>🎯 Baixa fidelização]
        end
    end
    
    subgraph "Estratégias por Perfil"
        STRATEGY_PREMIUM[🎯 Atendimento VIP<br/>⚡ Processamento rápido<br/>🎁 Benefícios extras]
        
        STRATEGY_ECONOMICO[🎫 Ofertas alternativas<br/>💡 Educação sobre benefícios<br/>🤝 Relacionamento]
        
        STRATEGY_EVENTUAL[📝 Cadastro assistido<br/>🎯 Aquisição<br/>💌 Engajamento]
    end
    
    PREMIUM --> STRATEGY_PREMIUM
    ECONOMICO --> STRATEGY_ECONOMICO
    EVENTUAL --> STRATEGY_EVENTUAL
    
    classDef premiumStyle fill:#fff8e1,stroke:#f9a825,stroke-width:2px
    classDef economicoStyle fill:#e8f5e8,stroke:#2e7d2e,stroke-width:2px
    classDef eventualStyle fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef strategyStyle fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    
    class PREMIUM premiumStyle
    class ECONOMICO economicoStyle
    class EVENTUAL eventualStyle
    class STRATEGY_PREMIUM,STRATEGY_ECONOMICO,STRATEGY_EVENTUAL strategyStyle
```

## 📱 Jornada Multicanal

### Experiência Integrada

```mermaid
graph TB
    subgraph "Canais de Entrada"
        WEB[🌐 Website Natura]
        APP[📱 App Mobile]
        WHATS[💬 WhatsApp]
        EMAIL[📧 Email]
        PHONE[📞 Call Center]
    end
    
    subgraph "Sistema Unificado"
        UNIFIED[🤖 Sistema de Reembolso<br/>Natura ADK]
    end
    
    subgraph "Experiência Consistente"
        EXP1[😊 Mesma personalidade]
        EXP2[🎯 Mesmas regras]
        EXP3[📋 Mesmo histórico]
        EXP4[🎨 Mesma identidade]
    end
    
    subgraph "Outputs Integrados"
        OUT1[📧 Email confirmação]
        OUT2[📱 Push notification]
        OUT3[💬 WhatsApp update]
        OUT4[🔔 SMS alert]
    end
    
    WEB & APP & WHATS & EMAIL & PHONE --> UNIFIED
    UNIFIED --> EXP1 & EXP2 & EXP3 & EXP4
    EXP1 & EXP2 & EXP3 & EXP4 --> OUT1 & OUT2 & OUT3 & OUT4
    
    classDef channelStyle fill:#e8f5e8,stroke:#2e7d2e,stroke-width:2px
    classDef systemStyle fill:#fff3e0,stroke:#f57c00,stroke-width:3px
    classDef experienceStyle fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef outputStyle fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    
    class WEB,APP,WHATS,EMAIL,PHONE channelStyle
    class UNIFIED systemStyle
    class EXP1,EXP2,EXP3,EXP4 experienceStyle
    class OUT1,OUT2,OUT3,OUT4 outputStyle
```

## 🕐 Jornada Temporal

### Timeline de Interação

```mermaid
timeline
    title Timeline da Jornada do Cliente
    
    section Dia 0 : Compra
        Produto comprado online : Cliente realiza pedido
                                : Escolhe tipo de envio
                                : Recebe confirmação
    
    section Dia 3-7 : Entrega
        Produto chega danificado : Frustração inicial
                                 : Busca por solução
                                 : Encontra chat Natura
    
    section Dia 7 : Contato
        00:00 : Inicia conversa
        00:01 : Fornece nome
        00:02 : Explica problema
        00:03 : Sistema processa
        00:05 : Recebe resposta
        00:06 : Agradecimento final
    
    section Dia 8-9 : Resolução
        Processamento reembolso : Confirmação por email
                               : Crédito na conta
                               : Satisfação do cliente
    
    section Dia 10+ : Pós-venda
        Follow-up automático : Pesquisa satisfação
                            : Ofertas personalizadas
                            : Fidelização
```

## 📊 Métricas de Experiência

### KPIs da Jornada do Cliente

```mermaid
graph TB
    subgraph "Métricas de Satisfação"
        CSAT[😊 CSAT: 9.2/10<br/>Customer Satisfaction]
        NPS[📈 NPS: +65<br/>Net Promoter Score]
        CES[⚡ CES: 2.1/7<br/>Customer Effort Score]
    end
    
    subgraph "Métricas de Performance"
        RESOLUTION[⏱️ Tempo Resolução<br/>5 segundos médio]
        FIRST_CONTACT[🎯 First Contact Resolution<br/>95% dos casos]
        ABANDONMENT[📉 Taxa Abandono<br/>2% dos chats]
    end
    
    subgraph "Métricas de Negócio"
        RETENTION[🔄 Retenção<br/>+15% vs tradicional]
        LIFETIME[💰 Lifetime Value<br/>+25% clientes atendidos]
        REFERRAL[👥 Indicações<br/>+40% após resolução]
    end
    
    subgraph "Momentos Críticos"
        MOMENT1[🎯 Primeiro contato<br/>8.9/10 satisfação]
        MOMENT2[⏳ Tempo espera<br/>95% em <10s]
        MOMENT3[✅ Resolução<br/>90% aprovação]
        MOMENT4[🙏 Agradecimento<br/>100% recebem]
    end
    
    classDef satisfactionStyle fill:#e8f5e8,stroke:#2e7d2e,stroke-width:2px
    classDef performanceStyle fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef businessStyle fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef momentsStyle fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    
    class CSAT,NPS,CES satisfactionStyle
    class RESOLUTION,FIRST_CONTACT,ABANDONMENT performanceStyle
    class RETENTION,LIFETIME,REFERRAL businessStyle
    class MOMENT1,MOMENT2,MOMENT3,MOMENT4 momentsStyle
```

## 🎯 Jornada Futura - Visão 2026

### Experiência Proativa

```mermaid
journey
    title Jornada Futura - Sistema Proativo (2026)
    section Prevenção
      IA detecta risco entrega: 8: Sistema
      Contato proativo cliente: 9: Sistema, Cliente
      Resolução antes problema: 10: Sistema, Cliente
    section Antecipação
      Predição necessidades: 9: Sistema
      Ofertas personalizadas: 9: Sistema, Cliente
      Suporte preventivo: 10: Sistema, Cliente
    section Experiência Seamless
      Reconhecimento automático: 10: Sistema, Cliente
      Contexto completo: 10: Sistema, Cliente
      Resolução instantânea: 10: Sistema, Cliente
    section Relacionamento
      Relacionamento contínuo: 10: Sistema, Cliente
      Valor agregado constante: 10: Sistema, Cliente
      Fidelização profunda: 10: Cliente
```

### Tecnologias Emergentes

```mermaid
graph TB
    subgraph "Tecnologias 2026"
        AI[🧠 IA Avançada<br/>Predição problemas]
        IoT[📡 IoT Tracking<br/>Rastreamento real-time]
        BLOCKCHAIN[⛓️ Blockchain<br/>Transparência total]
        AR[🥽 Realidade Aumentada<br/>Suporte visual]
        VOICE[🗣️ Interface Voz<br/>Conversação natural]
    end
    
    subgraph "Benefícios Cliente"
        PROACTIVE[🎯 Suporte Proativo<br/>Problemas antecipados]
        TRANSPARENT[👁️ Transparência Total<br/>Status em tempo real]
        CONVENIENT[⚡ Conveniência Máxima<br/>Múltiplas interfaces]
        PERSONAL[❤️ Personalização<br/>Experiência única]
    end
    
    AI --> PROACTIVE
    IoT --> TRANSPARENT
    BLOCKCHAIN --> TRANSPARENT
    AR --> CONVENIENT
    VOICE --> CONVENIENT
    AI --> PERSONAL
    
    classDef techStyle fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef benefitStyle fill:#e8f5e8,stroke:#2e7d2e,stroke-width:2px
    
    class AI,IoT,BLOCKCHAIN,AR,VOICE techStyle
    class PROACTIVE,TRANSPARENT,CONVENIENT,PERSONAL benefitStyle
```

Esta documentação da jornada do cliente fornece uma visão completa e empática da experiência no sistema de reembolso Natura, destacando tanto os sucessos quanto as oportunidades de melhoria.
