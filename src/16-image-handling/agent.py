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

logger = logging.getLogger(__name__)

# --- Callback to save uploaded image as artifact ---
async def _save_uploaded_image_as_artifact(callback_context: CallbackContext):
    """Extracts image data from incoming message and saves as artifact."""
    logger.info("--- Entering _save_uploaded_image_as_artifact callback ---")
    user_content = callback_context.user_content

    if not user_content or not user_content.parts:
        logger.info("Callback: No content or parts found in user_content.")
        return

    # Look for image in user content
    for i, part in enumerate(user_content.parts):
        if hasattr(part, 'inline_data') and getattr(part.inline_data, 'mime_type', '').startswith('image/'):
            mime_type = part.inline_data.mime_type
            logger.info(f"Found image with mime_type: {mime_type}")
            
            # Extract image data
            image_bytes = None
            if hasattr(part.inline_data, 'data') and isinstance(part.inline_data.data, (bytes, bytearray)):
                image_bytes = part.inline_data.data
            elif hasattr(part.inline_data, 'data') and isinstance(part.inline_data.data, str):
                try:
                    # Try to decode if it's base64
                    image_bytes = base64.b64decode(part.inline_data.data)
                except:
                    logger.error("Failed to decode image data")
                    continue
            
            if image_bytes:
                try:
                    # Create artifact from image using the exact structure from docs
                    image_artifact = types.Part(
                        inline_data=types.Blob(
                            mime_type=mime_type,
                            data=image_bytes
                        )
                    )
                    
                    # Determine filename based on mime type with unique timestamp
                    extension = mime_type.split('/')[-1] if '/' in mime_type else 'jpg'
                    if extension == 'jpeg':
                        extension = 'jpg'
                    
                    # Generate unique filename with timestamp
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]  # microseconds truncated to milliseconds
                    filename = f"uploaded_image_{timestamp}.{extension}"
                    
                    # Save as artifact
                    version = await callback_context.save_artifact(
                        filename=filename,
                        artifact=image_artifact
                    )
                    logger.info(f"Successfully saved image as artifact '{filename}' version {version}")
                    
                    # Store filename in state for the tool to use
                    current_state = callback_context.state.to_dict()
                    current_state['last_uploaded_image'] = filename
                    await callback_context.state.update(current_state)
                    
                    break
                    
                except ValueError as e:
                    logger.error(f"Error saving artifact: {e}. Is ArtifactService configured in Runner?")
                except Exception as e:
                    logger.error(f"Unexpected error saving artifact: {e}")
    
    logger.info("--- Exiting _save_uploaded_image_as_artifact callback ---")

# --- Tool to list available artifacts ---
async def list_artifacts_tool(tool_context: ToolContext) -> str:
    """
    Lists all available artifacts in the current session.
    
    Args:
        tool_context: The tool context with access to artifacts
        
    Returns:
        str: List of available artifacts
    """
    logger.info("Listing artifacts")
    
    try:
        artifacts = await tool_context.list_artifacts()
        
        if not artifacts:
            return "📂 Nenhum artifact encontrado na sessão atual.\n\n⚠️ **Nota**: Se você enviou uma imagem mas não vê artifacts, certifique-se de que o Runner foi configurado com um ArtifactService (como InMemoryArtifactService ou GcsArtifactService)."
        
        response = "📂 **Artifacts disponíveis:**\n\n"
        for artifact_name in artifacts:
            response += f"• {artifact_name}\n"
            
            # Try to get version info
            try:
                # Load to verify it exists
                artifact = await tool_context.load_artifact(filename=artifact_name)
                if artifact and artifact.inline_data:
                    response += f"  - Tipo: {artifact.inline_data.mime_type}\n"
                    response += f"  - Tamanho: {len(artifact.inline_data.data)} bytes\n"
            except:
                pass
        
        return response
        
    except ValueError as e:
        logger.error(f"Error listing artifacts: {e}. Is ArtifactService configured?")
        return "❌ Erro ao listar artifacts. O ArtifactService não está configurado no Runner.\n\n📝 **Como corrigir**:\nAo criar o Runner, adicione um artifact_service:\n```python\nfrom google.adk.artifacts import InMemoryArtifactService\n\nrunner = Runner(\n    agent=agent,\n    app_name='image_analyzer',\n    artifact_service=InMemoryArtifactService()\n)\n```"
    except Exception as e:
        logger.error(f"Unexpected error listing artifacts: {e}", exc_info=True)
        return f"Ocorreu um erro inesperado ao listar artifacts: {str(e)}"

# --- Tool to display/show image artifact ---
async def show_image_tool(tool_context: ToolContext, filename: Optional[str] = None) -> str:
    """
    Loads and displays an image artifact back to the user.
    
    Args:
        tool_context: The tool context with access to artifacts
        filename: Optional specific filename to load. If not provided, shows the most recent image.
        
    Returns:
        str: Success message indicating the image is ready for display
    """
    logger.info(f"Loading image artifact for display: {filename}")
    
    try:
        target_filename = filename
        
        # If no specific filename provided, find the most recent uploaded image
        if not target_filename:
            current_state = tool_context.state.to_dict()
            target_filename = current_state.get('last_uploaded_image')
            
            # If still no filename, search for the most recent image artifact
            if not target_filename:
                artifacts = await tool_context.list_artifacts()
                image_artifacts = [name for name in artifacts if name.startswith('uploaded_image_') and (name.endswith('.jpg') or name.endswith('.png') or name.endswith('.jpeg') or name.endswith('.gif') or name.endswith('.webp'))]
                
                if image_artifacts:
                    # Sort by timestamp (newest first)
                    image_artifacts.sort(reverse=True)
                    target_filename = image_artifacts[0]
                    logger.info(f"Found most recent image artifact: {target_filename}")
                else:
                    return "📂 Nenhuma imagem encontrada nos artifacts. Por favor, envie uma imagem primeiro para que eu possa exibi-la."
        
        # Load the image artifact to verify it exists and get details
        image_artifact = await tool_context.load_artifact(filename=target_filename)
        
        if not image_artifact or not image_artifact.inline_data:
            return f"❌ Não foi possível carregar a imagem '{target_filename}'. Verifique se o arquivo existe nos artifacts."
        
        logger.info(f"Successfully loaded image artifact: {target_filename}")
        
        # Create response with image details and instruction to display
        response = f"🖼️ **Imagem carregada com sucesso: {target_filename}**\n\n"
        response += f"📋 **Detalhes:**\n"
        response += f"• **Tipo:** {image_artifact.inline_data.mime_type}\n"
        response += f"• **Tamanho:** {len(image_artifact.inline_data.data)} bytes\n"
        response += f"• **Arquivo:** {target_filename}\n\n"
        response += "✅ A imagem está pronta para ser exibida pelo sistema.\n"
        response += "📄 Use `list_artifacts_tool` para ver todas as imagens disponíveis.\n"
        response += "🔍 Use `analyze_image_tool` para fazer análise detalhada da imagem."
        
        return response
        
    except ValueError as e:
        logger.error(f"Error loading image artifact: {e}")
        return "❌ Erro ao carregar a imagem. Certifique-se de que o ArtifactService está configurado corretamente."
    except Exception as e:
        logger.error(f"Unexpected error in show_image_tool: {e}", exc_info=True)
        return f"❌ Erro inesperado ao carregar a imagem: {str(e)}"

# --- Tool to analyze image using Vertex AI/Gemini ---
async def analyze_image_tool(tool_context: ToolContext) -> str:
    """
    Analyzes the uploaded image using Gemini through Vertex AI.
    
    Args:
        tool_context: The tool context with access to artifacts
        
    Returns:
        str: Comprehensive image analysis in Portuguese
    """
    logger.info("Starting image analysis with Gemini")
    
    try:
        # Get the filename from state or find the most recent uploaded image
        current_state = tool_context.state.to_dict()
        filename = current_state.get('last_uploaded_image')
        
        # If no filename in state, try to find the most recent uploaded image
        if not filename:
            artifacts = await tool_context.list_artifacts()
            image_artifacts = [name for name in artifacts if name.startswith('uploaded_image_') and (name.endswith('.jpg') or name.endswith('.png') or name.endswith('.jpeg') or name.endswith('.gif') or name.endswith('.webp'))]
            
            if image_artifacts:
                # Sort by timestamp (newest first) - the timestamp is in the filename
                image_artifacts.sort(reverse=True)
                filename = image_artifacts[0]
                logger.info(f"Found most recent image artifact: {filename}")
            else:
                logger.warning("No image artifacts found")
                return "Não encontrei nenhuma imagem para analisar. Por favor, envie uma imagem para que eu possa fazer a análise."
        
        # Load the user photo artifact
        photo_artifact = await tool_context.load_artifact(filename=filename)
        
        if not photo_artifact or not photo_artifact.inline_data:
            logger.warning(f"No photo artifact found with filename '{filename}'")
            return "Não encontrei nenhuma imagem para analisar. Por favor, envie uma imagem para que eu possa fazer a análise."
        
        logger.info(f"Successfully loaded photo artifact. MIME Type: {photo_artifact.inline_data.mime_type}")
        
        # Create content with image for Gemini analysis
        logger.info("Preparing image for Gemini analysis...")
        
        # Create the prompt for comprehensive image analysis
        analysis_prompt = """Por favor, analise esta imagem em detalhes e forneça:

1. **Descrição Geral**: O que você vê na imagem?
2. **Objetos e Elementos**: Liste os principais objetos, pessoas ou elementos presentes
3. **Cores e Composição**: Descreva as cores dominantes e a composição visual
4. **Contexto e Ambiente**: Onde a foto foi tirada? Qual é o cenário?
5. **Detalhes Técnicos**: Qualidade da imagem, iluminação, foco
6. **Interpretação**: O que esta imagem pode representar ou comunicar?
7. **Observações Adicionais**: Qualquer outro detalhe relevante

Forneça uma análise completa e detalhada em português."""

        try:
            # Initialize Gemini client (it will use Vertex AI based on env config)
            client = genai.Client()
            
            # Create the content with both text and image
            contents = [
                types.Content(
                    role="user",
                    parts=[
                        types.Part(text=analysis_prompt),
                        photo_artifact  # The image artifact
                    ]
                )
            ]
            
            # Generate response using Gemini
            logger.info("Calling Gemini for image analysis...")
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=contents,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=2048,
                )
            )
            
            # Extract the analysis text
            if response and response.text:
                analysis_text = response.text
                logger.info("Successfully received analysis from Gemini")
                
                # Format the response
                formatted_response = "🔍 **Análise de Imagem Concluída!** 🔍\n\n"
                formatted_response += analysis_text
                formatted_response += f"\n\n---\n💡 *Análise realizada com Gemini AI através do Vertex AI*"
                formatted_response += f"\n📎 *Imagem salva como artifact: {filename}*"
                
                return formatted_response
            else:
                logger.error("No text in Gemini response")
                return "Não recebi uma resposta válida do modelo. Por favor, tente novamente."
                
        except Exception as e:
            logger.error(f"Error during Gemini analysis: {e}", exc_info=True)
            return f"Ocorreu um erro durante a análise: {str(e)}. Por favor, verifique se o Vertex AI está configurado corretamente."
        
    except ValueError as e:
        logger.error(f"Error loading artifact: {e}. Is ArtifactService configured?")
        return "Erro ao carregar a imagem. Certifique-se de que o serviço está configurado corretamente."
    except Exception as e:
        logger.error(f"Unexpected error in analyze_image_tool: {e}", exc_info=True)
        return f"Ocorreu um erro inesperado durante a análise. Por favor, tente novamente."

# Create the Image Analysis Agent
image_analyzer = Agent(
    name="image_analyzer",
    model="gemini-2.5-flash",
    description="AI assistant specialized in comprehensive image analysis using Gemini",
    instruction=(
        "Você é um assistente de IA especializado em análise de imagens usando o Gemini! "
        "Seu papel é fornecer análises detalhadas e insights sobre qualquer imagem enviada pelo usuário.\n\n"
        
        "Quando o usuário enviar uma imagem:\n"
        "1. A imagem será automaticamente salva como artifact pelo callback\n"
        "2. Use a ferramenta analyze_image_tool para analisar a imagem\n"
        "3. Apresente os resultados de forma clara e estruturada\n"
        "4. Forneça insights úteis e observações relevantes\n"
        "5. Se solicitado, use list_artifacts_tool para mostrar artifacts salvos\n"
        "6. Use show_image_tool para exibir/mostrar imagens salvas de volta ao usuário\n\n"
        
        "Se o usuário não enviar imagem:\n"
        "- Peça educadamente para enviar uma imagem\n"
        "- Explique que você pode analisar qualquer tipo de imagem\n"
        "- Mencione exemplos: fotos, documentos, arte, objetos, pessoas, paisagens, etc.\n\n"
        
        "Sempre:\n"
        "- Use emojis para tornar a conversa mais agradável 🖼️\n"
        "- Seja detalhista e observador\n"
        "- Forneça análises úteis e informativas\n"
        "- Responda sempre em português brasileiro\n"
        "- Se houver erro na análise, sugira tentar novamente\n"
        "- Organize as informações de forma clara e fácil de entender"
    ),
    tools=[analyze_image_tool, list_artifacts_tool, show_image_tool],
    before_agent_callback=_save_uploaded_image_as_artifact
)

logger.info(f"Image analyzer agent '{image_analyzer.name}' initialized with analyze_image_tool and artifact-based image handling.")

# Export the agent
root_agent = image_analyzer
