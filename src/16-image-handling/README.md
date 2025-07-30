# Image Handling Agent

Este exemplo demonstra como criar um agente ADK especializado em processamento e análise de imagens usando Gemini AI, com sistema de artifacts para armazenamento e gerenciamento de imagens.

## 🎯 Funcionalidades

### ✨ Principais Recursos

- **📤 Upload automático de imagens**: Salva automaticamente imagens enviadas como artifacts
- **🔍 Análise inteligente**: Usa Gemini AI para análise detalhada de imagens
- **📂 Gerenciamento de artifacts**: Lista e gerencia imagens armazenadas
- **🖼️ Visualização de imagens**: Carrega e exibe imagens previamente salvas
- **🏷️ Nomeação única**: Sistema de timestamps para evitar sobrescrita de arquivos

### 🛠️ Ferramentas Disponíveis

1. **`analyze_image_tool`**: Análise completa de imagens usando Gemini AI
2. **`list_artifacts_tool`**: Lista todos os artifacts (imagens) na sessão
3. **`show_image_tool`**: Carrega e exibe imagens específicas dos artifacts

## 🏗️ Arquitetura

### 📋 Componentes Principais

```python
# Callback para salvar imagens automaticamente
_save_uploaded_image_as_artifact()

# Ferramentas de análise e gerenciamento
analyze_image_tool()
list_artifacts_tool() 
show_image_tool()

# Agente principal
image_analyzer = Agent(...)
```

### 🔄 Fluxo de Funcionamento

1. **Upload**: Usuário envia uma imagem
2. **Callback**: `_save_uploaded_image_as_artifact` detecta e salva a imagem
3. **Nomeação**: Gera nome único com timestamp (`uploaded_image_YYYYMMDD_HHMMSS_mmm.ext`)
4. **Armazenamento**: Salva como artifact no sistema ADK
5. **Estado**: Atualiza estado com filename da última imagem
6. **Análise**: Ferramentas podem processar a imagem salva

## 🚀 Como Usar

### 📦 Configuração Inicial

```python
from google.adk.artifacts import InMemoryArtifactService
from google.adk.runners import Runner

# Importante: Configure um ArtifactService
runner = Runner(
    agent=agent,
    app_name='image_analyzer',
    artifact_service=InMemoryArtifactService()  # Obrigatório!
)
```

### 💬 Exemplos de Uso

#### 1. Análise de Imagem
```
Usuário: [envia uma imagem]
Agente: 🔍 Análise de Imagem Concluída! 🔍

**Descrição Geral**: Vejo uma paisagem montanhosa...
**Objetos e Elementos**: Montanhas, árvores, céu azul...
**Cores e Composição**: Tons azuis dominantes...
```

#### 2. Listar Imagens Salvas
```
Usuário: "Liste as imagens disponíveis"
Agente: 📂 Artifacts disponíveis:

• uploaded_image_20250730_114523_456.jpg
  - Tipo: image/jpeg
  - Tamanho: 245760 bytes
• uploaded_image_20250730_115201_789.png
  - Tipo: image/png
  - Tamanho: 189432 bytes
```

#### 3. Exibir Imagem Específica
```
Usuário: "Mostre a imagem uploaded_image_20250730_114523_456.jpg"
Agente: 🖼️ Imagem carregada com sucesso: uploaded_image_20250730_114523_456.jpg

📋 Detalhes:
• Tipo: image/jpeg
• Tamanho: 245760 bytes
• Arquivo: uploaded_image_20250730_114523_456.jpg
```

## 🔧 Detalhes Técnicos

### 📝 Sistema de Nomeação

- **Formato**: `uploaded_image_YYYYMMDD_HHMMSS_mmm.{extensão}`
- **Exemplo**: `uploaded_image_20250730_114523_456.jpg`
- **Componentes**:
  - `YYYY`: Ano (2025)
  - `MM`: Mês (07)
  - `DD`: Dia (30)
  - `HH`: Hora (11)
  - `MM`: Minuto (45)
  - `SS`: Segundo (23)
  - `mmm`: Milissegundos (456)

### 🎨 Tipos de Imagem Suportados

- **JPEG/JPG** (`.jpg`, `.jpeg`)
- **PNG** (`.png`)
- **GIF** (`.gif`)
- **WebP** (`.webp`)

### 🔍 Análise Detalhada

A ferramenta `analyze_image_tool` fornece:

1. **Descrição Geral**: Visão geral do conteúdo
2. **Objetos e Elementos**: Identificação de elementos presentes
3. **Cores e Composição**: Análise visual e estética
4. **Contexto e Ambiente**: Interpretação do cenário
5. **Detalhes Técnicos**: Qualidade, iluminação, foco
6. **Interpretação**: Significado e comunicação
7. **Observações Adicionais**: Detalhes relevantes extras

## 📊 Gerenciamento de Estado

### 🗂️ Estado da Sessão

```python
state = {
    'last_uploaded_image': 'uploaded_image_20250730_114523_456.jpg'
}
```

### 🔄 Recuperação Inteligente

1. **Primeira tentativa**: Verifica `state['last_uploaded_image']`
2. **Segunda tentativa**: Busca artifacts com padrão `uploaded_image_*`
3. **Ordenação**: Por timestamp (mais recente primeiro)
4. **Fallback**: Retorna mensagem de erro se nenhuma imagem encontrada

## ⚠️ Tratamento de Erros

### 🚨 Erros Comuns

1. **ArtifactService não configurado**
   ```
   ❌ Erro ao listar artifacts. O ArtifactService não está configurado no Runner.
   ```

2. **Imagem não encontrada**
   ```
   ❌ Não foi possível carregar a imagem 'filename.jpg'. 
   Verifique se o arquivo existe nos artifacts.
   ```

3. **Erro na análise**
   ```
   Ocorreu um erro durante a análise: [detalhes]. 
   Por favor, verifique se o Vertex AI está configurado corretamente.
   ```

### 🛡️ Estratégias de Recuperação

- **Logging detalhado** para debugging
- **Mensagens de erro claras** para o usuário
- **Fallbacks inteligentes** para busca de imagens
- **Validação de dados** antes do processamento

## 🔧 Configuração Avançada

### 🌐 Integração com Vertex AI

```python
# Cliente Gemini configurado automaticamente
client = genai.Client()

# Configuração de geração
config = types.GenerateContentConfig(
    temperature=0.7,
    max_output_tokens=2048,
)
```

### 📚 Dependências

```python
import logging
import base64
import datetime
from typing import Optional
import google.genai.types as types
from google import genai
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.tool_context import ToolContext
from google.adk.artifacts import InMemoryArtifactService
from google.adk.sessions import InMemorySessionService
```

## 🎯 Casos de Uso

### 📷 Análise de Fotografias
- Identificação de objetos e pessoas
- Análise de composição e qualidade
- Descrição detalhada de cenários

### 📄 Processamento de Documentos
- Análise de documentos escaneados
- Extração de informações visuais
- Identificação de texto e elementos

### 🎨 Análise Artística
- Interpretação de obras de arte
- Análise de cores e estilos
- Contexto histórico e cultural

### 🏢 Aplicações Empresariais
- Análise de produtos
- Controle de qualidade visual
- Catalogação de imagens

## 📈 Exemplo Completo

```python
# 1. Configurar o runner com ArtifactService
from google.adk.artifacts import InMemoryArtifactService
from google.adk.runners import Runner

runner = Runner(
    agent=image_analyzer,
    app_name='image_analyzer',
    artifact_service=InMemoryArtifactService()
)

# 2. Executar o agente
# O usuário envia uma imagem via interface
# O callback automaticamente salva a imagem
# As ferramentas ficam disponíveis para análise

# 3. Fluxo típico:
# - Upload automático → callback salva como artifact
# - Análise automática → analyze_image_tool processa
# - Gerenciamento → list_artifacts_tool e show_image_tool
```

## 🔗 Recursos Relacionados

- [Documentação ADK Artifacts](https://google.github.io/adk-docs/artifacts/)
- [Google Gemini AI Documentation](https://ai.google.dev/docs)
- [Vertex AI Integration Guide](https://cloud.google.com/vertex-ai/docs)

---

**💡 Dica**: Sempre configure um `ArtifactService` no Runner para habilitar o armazenamento de imagens!
