# Image Generation and Editing Agent

Este exemplo demonstra como criar um agente ADK especializado em geração e edição de imagens usando o **Gemini 2.5 Flash Image Preview**, com sistema de artifacts para armazenamento e gerenciamento de imagens criadas.

## 🎯 Funcionalidades

### ✨ Principais Recursos

- **🎨 Geração de imagens**: Cria imagens a partir de descrições de texto usando Gemini 2.5 Flash Image Preview
- **✂️ Edição de imagens**: Modifica imagens existentes com base em instruções textuais
- **📤 Upload automático**: Salva automaticamente imagens enviadas como artifacts para edição
- **📂 Gerenciamento avançado**: Lista e gerencia imagens geradas, editadas e enviadas
- **🖼️ Visualização**: Carrega e exibe imagens específicas dos artifacts
- **🏷️ Nomeação inteligente**: Sistema de timestamps para organização automática

### 🛠️ Ferramentas Disponíveis

1. **`generate_image_tool`**: Geração de imagens a partir de prompts de texto
2. **`edit_image_tool`**: Edição de imagens baseada em instruções textuais
3. **`list_generated_images_tool`**: Lista todas as imagens por categoria (geradas/editadas/enviadas)
4. **`show_generated_image_tool`**: Carrega e exibe imagens específicas dos artifacts

## 🏗️ Arquitetura

### 📋 Componentes Principais

```python
# Callback para salvar imagens automaticamente
_save_uploaded_image_as_artifact()

# Ferramentas de geração e edição
generate_image_tool()    # Criar imagens do zero
edit_image_tool()        # Modificar imagens existentes
list_generated_images_tool()   # Listar por categoria
show_generated_image_tool()    # Exibir imagens específicas

# Agente principal com Gemini 2.5 Flash Image Preview
image_generator = Agent(...)
```

### 🔄 Fluxo de Funcionamento

#### Para Geração de Imagens:
1. **Prompt**: Usuário fornece descrição textual
2. **Geração**: `generate_image_tool` chama Gemini 2.5 Flash Image Preview
3. **Nomeação**: Gera nome único (`generated_image_YYYYMMDD_HHMMSS_mmm.ext`)
4. **Armazenamento**: Salva como artifact no sistema ADK
5. **Estado**: Atualiza estado com referência à última imagem gerada

#### Para Edição de Imagens:
1. **Upload/Seleção**: Usuário envia imagem ou especifica uma existente
2. **Callback**: `_save_uploaded_image_as_artifact` detecta e salva imagem enviada
3. **Edição**: `edit_image_tool` aplica instruções usando Gemini 2.5 Flash Image Preview
4. **Nomeação**: Gera nome único (`edited_image_YYYYMMDD_HHMMSS_mmm.ext`)
5. **Armazenamento**: Salva versão editada como novo artifact

## 🚀 Como Usar

### 📦 Configuração Inicial

```python
from google.adk.artifacts import InMemoryArtifactService
from google.adk.runners import Runner
import os

# Configure as variáveis de ambiente
os.environ["GOOGLE_CLOUD_API_KEY"] = "sua_api_key_aqui"

# Importante: Configure um ArtifactService
runner = Runner(
    agent=image_generator,
    app_name='image_generator',
    artifact_service=InMemoryArtifactService()  # Obrigatório!
)
```

### 💬 Exemplos de Uso

#### 1. Geração de Imagem
```
Usuário: "Gere uma imagem de um pôr do sol sobre montanhas com um lago"
Agente: 🎨 Imagem gerada com sucesso! 🎨

📋 Detalhes da geração:
• Prompt: Gere uma imagem de um pôr do sol sobre montanhas com um lago
• Modelo: Gemini 2.5 Flash Image Preview
• Tipo: image/png
• Tamanho: 1,234,567 bytes
• Arquivo: generated_image_20250730_143256_789.png

✅ A imagem foi salva como artifact e está pronta para visualização.
```

#### 2. Edição de Imagem
```
Usuário: [envia uma foto] "Adicione um arco-íris colorido no céu"
Agente: ✂️ Imagem editada com sucesso! ✂️

📋 Detalhes da edição:
• Imagem original: uploaded_image_20250730_143145_123.jpg
• Instruções: Adicione um arco-íris colorido no céu
• Modelo: Gemini 2.5 Flash Image Preview
• Tipo: image/png
• Tamanho: 1,456,789 bytes
• Arquivo editado: edited_image_20250730_143312_456.png
```

#### 3. Listar Imagens por Categoria
```
Usuário: "Liste todas as imagens disponíveis"
Agente: 📂 Imagens disponíveis:

🎨 Imagens Geradas:
• generated_image_20250730_143256_789.png
  - Tipo: image/png
  - Tamanho: 1,234,567 bytes
• generated_image_20250730_142145_321.png
  - Tipo: image/png
  - Tamanho: 987,654 bytes

✂️ Imagens Editadas:
• edited_image_20250730_143312_456.png
  - Tipo: image/png
  - Tamanho: 1,456,789 bytes

📤 Imagens Enviadas:
• uploaded_image_20250730_143145_123.jpg
  - Tipo: image/jpeg
  - Tamanho: 2,345,678 bytes
```

#### 4. Exibir Imagem Específica
```
Usuário: "Mostre a imagem generated_image_20250730_143256_789.png"
Agente: 🖼️ Imagem Gerada carregada com sucesso: generated_image_20250730_143256_789.png

📋 Detalhes:
• Tipo: image/png
• Tamanho: 1,234,567 bytes
• Arquivo: generated_image_20250730_143256_789.png
• Categoria: Imagem Gerada

✅ A imagem está pronta para ser exibida pelo sistema.
```

## 🔧 Detalhes Técnicos

### 🤖 Modelo Gemini 2.5 Flash Image Preview

```python
model = "gemini-2.5-flash-image-preview"

# Configuração de geração
generate_content_config = types.GenerateContentConfig(
    temperature=1,                          # Criatividade máxima
    top_p=0.95,                            # Diversidade alta
    max_output_tokens=32768,               # Tokens para texto + metadados
    response_modalities=["TEXT", "IMAGE"], # Resposta multimodal
    safety_settings=[...]                  # Configurações permissivas
)
```

### 📝 Sistema de Nomeação

- **Imagens Geradas**: `generated_image_YYYYMMDD_HHMMSS_mmm.{extensão}`
- **Imagens Editadas**: `edited_image_YYYYMMDD_HHMMSS_mmm.{extensão}`
- **Imagens Enviadas**: `uploaded_image_YYYYMMDD_HHMMSS_mmm.{extensão}`

**Exemplo**: `generated_image_20250730_143256_789.png`
- `YYYY`: Ano (2025)
- `MM`: Mês (07)
- `DD`: Dia (30)
- `HH`: Hora (14)
- `MM`: Minuto (32)
- `SS`: Segundo (56)
- `mmm`: Milissegundos (789)

### 🎨 Tipos de Imagem Suportados

- **PNG** (`.png`) - Formato padrão para imagens geradas
- **JPEG/JPG** (`.jpg`, `.jpeg`) - Comum em uploads
- **GIF** (`.gif`) - Suporte a animações
- **WebP** (`.webp`) - Formato moderno e eficiente

### 🔍 Capacidades de Geração

O **Gemini 2.5 Flash Image Preview** pode gerar:

1. **Paisagens e Cenários**
   - Natureza, cidades, ambientes fantásticos
   - Diferentes estilos: realista, cartoon, artístico

2. **Retratos e Pessoas**
   - Pessoas individuais ou grupos
   - Diferentes etnias, idades, estilos

3. **Objetos e Produtos**
   - Itens do cotidiano, produtos comerciais
   - Visualizações conceituais

4. **Arte e Ilustrações**
   - Estilos artísticos diversos
   - Composições abstratas e conceituais

5. **Texto em Imagens**
   - Adição de textos e logos
   - Tipografia criativa

### ✂️ Capacidades de Edição

O modelo pode aplicar diversas modificações:

1. **Adições**
   - Novos elementos na cena
   - Textos e overlays
   - Objetos e pessoas

2. **Modificações**
   - Cores e iluminação
   - Estilos artísticos
   - Composição e enquadramento

3. **Transformações**
   - Filtros e efeitos
   - Mudanças de estilo
   - Conversões artísticas

## 📊 Gerenciamento de Estado

### 🗂️ Estado da Sessão

```python
state = {
    'last_uploaded_image': 'uploaded_image_20250730_143145_123.jpg',
    'last_generated_image': 'generated_image_20250730_143256_789.png',
    'last_edited_image': 'edited_image_20250730_143312_456.png'
}
```

### 🔄 Recuperação Inteligente de Imagens

**Para edição automática** (quando nenhum filename específico é fornecido):

1. **Primeira tentativa**: Verifica `state['last_uploaded_image']`
2. **Segunda tentativa**: Verifica `state['last_generated_image']`
3. **Terceira tentativa**: Busca artifacts com padrão de imagem
4. **Ordenação**: Por timestamp (mais recente primeiro)
5. **Fallback**: Retorna mensagem de erro se nenhuma imagem encontrada

**Para exibição automática**:

1. **Primeira tentativa**: Verifica `state['last_edited_image']`
2. **Segunda tentativa**: Verifica `state['last_generated_image']`
3. **Terceira tentativa**: Verifica `state['last_uploaded_image']`
4. **Quarta tentativa**: Busca qualquer artifact de imagem
5. **Fallback**: Solicita geração ou upload de imagem

## ⚠️ Tratamento de Erros

### 🚨 Erros Comuns

1. **ArtifactService não configurado**
   ```
   ❌ Erro ao listar artifacts. O ArtifactService não está configurado no Runner.
   ```

2. **Modelo não disponível**
   ```
   ❌ Erro durante a geração da imagem: Modelo gemini-2.5-flash-image-preview não encontrado.
   Verifique se você tem acesso ao modelo.
   ```

3. **API Key inválida**
   ```
   ❌ Erro durante a geração: Authentication failed.
   Verifique se o GOOGLE_CLOUD_API_KEY está correto.
   ```

4. **Imagem não encontrada**
   ```
   ❌ Não foi possível carregar a imagem 'filename.png'. 
   Verifique se o arquivo existe nos artifacts.
   ```

5. **Falha na geração**
   ```
   ❌ Não foi possível gerar a imagem. O modelo retornou uma resposta sem imagem.
   Prompt usado: [prompt]
   ```

### 🛡️ Estratégias de Recuperação

- **Logging detalhado** para debugging técnico
- **Mensagens de erro claras** para o usuário final
- **Fallbacks inteligentes** para busca de imagens
- **Validação robusta** antes do processamento
- **Configurações de segurança permissivas** para criatividade máxima

## 🔧 Configuração Avançada

### 🌐 Integração com Vertex AI

```python
# Cliente Gemini com Vertex AI
client = genai.Client(
    vertexai=True,
    api_key=os.environ.get("GOOGLE_CLOUD_API_KEY"),
)

# Configurações de segurança permissivas para criatividade
safety_settings = [
    types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
    types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"),
    types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"),
    types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF")
]
```

### 📚 Dependências

```python
import logging
import base64
import datetime
import os
from typing import Optional
import google.genai.types as types
from google import genai
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.tool_context import ToolContext
from google.adk.artifacts import InMemoryArtifactService
from google.adk.sessions import InMemorySessionService
```

### 🔑 Variáveis de Ambiente

```bash
# API Key para Gemini via Vertex AI
export GOOGLE_CLOUD_API_KEY="sua_api_key_aqui"

# Opcional: Configurações do Google Cloud
export GOOGLE_CLOUD_PROJECT="seu_projeto_gcp"
export GOOGLE_APPLICATION_CREDENTIALS="caminho/para/service-account.json"
```

## 🎯 Casos de Uso

### 🎨 Criação de Conteúdo

- **Marketing**: Banners, posts para redes sociais
- **Design**: Mockups, protótipos visuais
- **Educação**: Ilustrações para materiais didáticos
- **Arte**: Criações artísticas personalizadas

### ✂️ Edição Profissional

- **Retoque**: Melhorias em fotos existentes
- **Composição**: Adição de elementos a cenas
- **Branding**: Inserção de logos e textos
- **Estilização**: Aplicação de filtros artísticos

### 🏢 Aplicações Empresariais

- **E-commerce**: Visualização de produtos
- **Imobiliário**: Renderizações conceituais
- **Arquitetura**: Visualizações de projetos
- **Publicidade**: Campanhas visuais criativas

### 🎓 Uso Educacional

- **Storytelling**: Ilustrações para narrativas
- **Ciências**: Diagramas e visualizações
- **História**: Recriações históricas
- **Arte**: Exploração de estilos artísticos

## 📈 Exemplo Completo de Uso

```python
# 1. Configurar o runner com ArtifactService
from google.adk.artifacts import InMemoryArtifactService
from google.adk.runners import Runner
import os

# Configurar ambiente
os.environ["GOOGLE_CLOUD_API_KEY"] = "sua_api_key_aqui"

runner = Runner(
    agent=image_generator,
    app_name='image_generator',
    artifact_service=InMemoryArtifactService()
)

# 2. Executar o agente
# Usuário: "Gere uma imagem de um gato robô futurista"
# Agente: [usa generate_image_tool] → salva como artifact → exibe resultado

# 3. Editar a imagem gerada
# Usuário: "Adicione asas de borboleta ao gato robô"
# Agente: [usa edit_image_tool] → aplica modificações → salva nova versão

# 4. Gerenciar imagens
# Usuário: "Liste todas as imagens criadas"
# Agente: [usa list_generated_images_tool] → mostra categorias organizadas

# 5. Fluxo completo demonstrado:
# Geração → Edição → Listagem → Visualização → Nova geração/edição
```

## 🔗 Recursos Relacionados

- [Documentação ADK Artifacts](https://google.github.io/adk-docs/artifacts/)
- [Gemini 2.5 Flash Image Preview](https://ai.google.dev/docs)
- [Vertex AI Integration Guide](https://cloud.google.com/vertex-ai/docs)
- [Google GenAI Python Client](https://github.com/google-ai-python/google-genai)

## 🆚 Comparação com Exemplo 16 (Image Handling)

| Aspecto | Exemplo 16 (Análise) | Exemplo 17 (Geração/Edição) |
|---------|---------------------|------------------------------|
| **Foco** | Análise de imagens | Geração e edição de imagens |
| **Modelo** | gemini-2.5-flash | gemini-2.5-flash-image-preview |
| **Input** | Apenas imagens enviadas | Texto + imagens enviadas/geradas |
| **Output** | Análise textual | Novas imagens + metadados |
| **Ferramentas** | 3 (análise, lista, exibe) | 4 (gera, edita, lista, exibe) |
| **Artifacts** | Imagens enviadas | Imagens geradas/editadas/enviadas |
| **Modalidade** | TEXT | TEXT + IMAGE |

## 📊 Melhorias de Logging e Monitoramento

### 🔍 Sistema de Logging Aprimorado

Este agente implementa um sistema abrangente de logging para melhor visibilidade e debugging:

#### **Componentes de Logging**

1. **log_image_details()**: Registra detalhes sobre operações de imagem
   - Tamanho, formato, nome do arquivo
   - Timestamps precisos
   - Contexto da operação

2. **log_api_request()**: Monitora chamadas da API
   - Parâmetros da requisição
   - Timing e tentativas
   - Modelo e configurações

3. **log_api_response()**: Analisa respostas da API
   - Status de sucesso/falha
   - Dados de resposta
   - Contexto de erro

4. **retry_with_backoff()**: Lógica de retry robusta
   - Backoff exponencial (2s inicial)
   - Máximo de 3 tentativas
   - Logging detalhado de cada tentativa

#### **Exemplo de Logs**

```
2025-09-29 15:20:00 - INFO - [_save_uploaded_image_as_artifact:95] - Found image with mime_type: image/png
2025-09-29 15:20:00 - DEBUG - Image data is bytes/bytearray, size: 1024000 bytes
2025-9-29 15:20:01 - INFO - API Request: {
  "operation": "image_generation",
  "model": "gemini-2.5-flash-image-preview",
  "content_parts": 1,
  "prompt_length": 45,
  "temperature": 1,
  "top_p": 0.95
}
2025-09-29 15:20:03 - INFO - image_generation_api_call succeeded on attempt 1
```

#### **Benefícios**

- **🐛 Debugging Melhorado**: Logs detalhados facilitam identificação de problemas
- **📈 Monitoramento**: Visibilidade completa do comportamento do sistema
- **🔄 Recuperação Automática**: Retry automático para falhas transitórias
- **👤 UX Aprimorada**: Mensagens de erro mais informativas
- **⚡ Performance**: Tracking de timing e taxas de sucesso

#### **Configuração de Logging**

```python
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s:%(lineno)d] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
```

Para mais detalhes, consulte: [`LOGGING_IMPROVEMENTS.md`](./LOGGING_IMPROVEMENTS.md)

## 🎯 Melhorias no Prompt - Fidelidade ao Pedido

### 🔍 **Princípio Fundamental: Execução Precisa**

O agente foi aprimorado com foco na **interpretação e execução fiel** dos pedidos do usuário:

#### **Características Principais**

1. **🎯 Fidelidade Total ao Pedido**
   - Executa EXATAMENTE o que o usuário solicita
   - Não adiciona elementos não solicitados
   - Interpreta nuances e modificadores ("sutilmente", "drasticamente")

2. **🧠 Interpretação Inteligente**
   - Entende pedidos simples: "deixe mais claro" → ajusta apenas brilho
   - Aceita pedidos criativos: "estilo cyberpunk" → aplica estilo mantendo composição
   - Reconhece estilos: steampunk, minimalista, anime, vintage, etc.

3. **❓ Clarificação Ativa**
   - Pergunta quando o pedido é ambíguo
   - Confirma interpretação em casos complexos
   - Prefere perguntar ao invés de assumir

#### **Exemplos de Comportamento Correto**

```
✅ CORRETO:
Usuário: "Deixe mais colorido"
Agente: Aumenta saturação das cores existentes

Usuário: "Adicione um sol"  
Agente: Adiciona APENAS um sol na posição adequada

Usuário: "Estilo anime"
Agente: Aplica características anime mantendo composição original

❌ INCORRETO:
Usuário: "Deixe mais colorido"
Agente: Adiciona arco-íris, flores e borboletas (não solicitados)

Usuário: "Adicione um sol"
Agente: Adiciona sol + nuvens + pássaros (extras não pedidos)
```

#### **Capacidades de Interpretação**

- **Modificadores**: "sutilmente", "drasticamente", "levemente", "completamente"
- **Estilos Artísticos**: Van Gogh, Monet, cubismo, surrealismo, pop art
- **Gêneros Visuais**: cyberpunk, steampunk, vintage, futurista, minimalista
- **Transformações**: "como se fosse uma pintura", "versão cartoon", "fotorrealista"
- **Correções Específicas**: "remova X", "mude cor de Y", "adicione Z"

### 🚀 **Benefícios da Melhoria**

- **🎨 Resultados Previsíveis**: O usuário obtém exatamente o que pediu
- **⚡ Eficiência**: Menos iterações para chegar ao resultado desejado  
- **🎯 Precisão**: Interpretação fiel de pedidos simples e complexos
- **🤝 Colaboração**: Agente pergunta quando há dúvidas
- **🎭 Criatividade Controlada**: Aceita pedidos criativos sem adicionar elementos extras

Para mais detalhes, consulte: [`LOGGING_IMPROVEMENTS.md`](./LOGGING_IMPROVEMENTS.md)

---

**💡 Dica Principal**: Este exemplo utiliza o modelo **Gemini 2.5 Flash Image Preview** que é específico para geração e edição de imagens. Certifique-se de ter acesso a este modelo em sua conta Google Cloud/Vertex AI!

**🎨 Dica Criativa**: Experimente prompts detalhados e específicos para obter melhores resultados. O modelo responde bem a descrições ricas em detalhes visuais, estilos artísticos e elementos compositivos.
