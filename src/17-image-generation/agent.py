import logging
import base64
import datetime
import os
import json
import asyncio
from typing import Optional, Dict, Any
import google.genai.types as types
from google import genai
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.tool_context import ToolContext
from google.adk.artifacts import InMemoryArtifactService
from google.adk.sessions import InMemorySessionService

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s:%(lineno)d] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def log_image_details(operation: str, image_data, mime_type: str = None, filename: str = None):
    """Log detailed information about image operations"""
    try:
        details = {
            "operation": operation,
            "timestamp": datetime.datetime.now().isoformat(),
            "filename": filename,
            "mime_type": mime_type,
            "size_bytes": len(image_data) if image_data else 0,
            "size_mb": round(len(image_data) / (1024 * 1024), 2) if image_data else 0
        }
        logger.info(f"Image Operation Details: {json.dumps(details, indent=2)}")
    except Exception as e:
        logger.error(f"Error logging image details: {e}")

def log_api_request(operation: str, model: str, content_parts: int = 0, **kwargs):
    """Log API request details"""
    try:
        request_details = {
            "operation": operation,
            "model": model,
            "content_parts": content_parts,
            "timestamp": datetime.datetime.now().isoformat(),
            "additional_params": kwargs
        }
        logger.info(f"API Request: {json.dumps(request_details, indent=2)}")
    except Exception as e:
        logger.error(f"Error logging API request: {e}")

def log_api_response(operation: str, success: bool, response_data: Dict[str, Any] = None, error: str = None):
    """Log API response details"""
    try:
        response_details = {
            "operation": operation,
            "success": success,
            "timestamp": datetime.datetime.now().isoformat(),
            "error": error,
            "response_summary": response_data
        }
        logger.info(f"API Response: {json.dumps(response_details, indent=2)}")
    except Exception as e:
        logger.error(f"Error logging API response: {e}")

async def retry_with_backoff(
    func, 
    operation_name: str,
    max_retries: int = 3, 
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0
):
    """Retry function with exponential backoff and detailed logging"""
    for attempt in range(max_retries):
        try:
            logger.info(f"Starting {operation_name} - Attempt {attempt + 1}/{max_retries}")
            result = await func()
            logger.info(f"{operation_name} succeeded on attempt {attempt + 1}")
            return result
        except Exception as e:
            logger.error(f"{operation_name} attempt {attempt + 1} failed: {str(e)}", exc_info=True)
            
            if attempt == max_retries - 1:
                logger.error(f"{operation_name} failed after {max_retries} attempts")
                raise
            
            delay = initial_delay * (backoff_factor ** attempt)
            logger.warning(f"Retrying {operation_name} in {delay}s...")
            await asyncio.sleep(delay)

# --- Callback to save uploaded image as artifact ---
async def _save_uploaded_image_as_artifact(callback_context: CallbackContext):
    """Extracts image data from incoming message and saves as artifact for editing."""
    logger.info("--- Entering _save_uploaded_image_as_artifact callback ---")
    
    try:
        user_content = callback_context.user_content
        logger.debug(f"User content type: {type(user_content)}")
        logger.debug(f"User content has parts: {hasattr(user_content, 'parts') if user_content else False}")

        if not user_content or not user_content.parts:
            logger.info("Callback: No content or parts found in user_content.")
            return

        logger.info(f"Processing {len(user_content.parts)} content parts")

        # Look for image in user content
        for i, part in enumerate(user_content.parts):
            logger.debug(f"Processing part {i}: {type(part)}")
            logger.debug(f"Part has inline_data: {hasattr(part, 'inline_data')}")
            
            if hasattr(part, 'inline_data') and getattr(part.inline_data, 'mime_type', '').startswith('image/'):
                mime_type = part.inline_data.mime_type
                logger.info(f"Found image with mime_type: {mime_type}")
                
                # Extract and log image data details
                image_bytes = None
                if hasattr(part.inline_data, 'data') and isinstance(part.inline_data.data, (bytes, bytearray)):
                    image_bytes = part.inline_data.data
                    logger.debug(f"Image data is bytes/bytearray, size: {len(image_bytes)} bytes")
                elif hasattr(part.inline_data, 'data') and isinstance(part.inline_data.data, str):
                    logger.debug(f"Image data is string, attempting base64 decode...")
                    try:
                        # Try to decode if it's base64
                        image_bytes = base64.b64decode(part.inline_data.data)
                        logger.debug(f"Successfully decoded base64 image, size: {len(image_bytes)} bytes")
                    except Exception as decode_error:
                        logger.error(f"Failed to decode image data: {decode_error}")
                        continue
                
                if image_bytes:
                    # Log image details before processing
                    log_image_details("image_upload_processing", image_bytes, mime_type)
                    
                    try:
                        # Create artifact from image using the exact structure from docs
                        image_artifact = types.Part(
                            inline_data=types.Blob(
                                mime_type=mime_type,
                                data=image_bytes
                            )
                        )
                        logger.debug("Created image artifact structure")
                        
                        # Determine filename based on mime type with unique timestamp
                        extension = mime_type.split('/')[-1] if '/' in mime_type else 'jpg'
                        if extension == 'jpeg':
                            extension = 'jpg'
                        
                        # Generate unique filename with timestamp
                        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
                        filename = f"uploaded_image_{timestamp}.{extension}"
                        logger.info(f"Generated filename: {filename}")
                        
                        # Save as artifact
                        logger.debug("Attempting to save artifact...")
                        version = await callback_context.save_artifact(
                            filename=filename,
                            artifact=image_artifact
                        )
                        logger.info(f"Successfully saved image as artifact '{filename}' version {version}")
                        
                        # Log successful save
                        log_image_details("image_upload_saved", image_bytes, mime_type, filename)
                        
                        # Store filename in state for the tool to use
                        current_state = callback_context.state.to_dict()
                        logger.debug(f"Current state keys: {list(current_state.keys())}")
                        current_state['last_uploaded_image'] = filename
                        callback_context.state.update(current_state)
                        logger.info(f"Updated state with last_uploaded_image: {filename}")
                        
                        break
                        
                    except ValueError as e:
                        logger.error(f"ValueError saving artifact: {e}. Is ArtifactService configured in Runner?", exc_info=True)
                    except Exception as e:
                        logger.error(f"Unexpected error saving artifact: {e}", exc_info=True)
                else:
                    logger.warning(f"No image bytes extracted from part {i}")
            else:
                logger.debug(f"Part {i} is not an image (mime_type: {getattr(getattr(part, 'inline_data', None), 'mime_type', 'N/A')})")
    
    except Exception as e:
        logger.error(f"Critical error in _save_uploaded_image_as_artifact: {e}", exc_info=True)
    finally:
        logger.info("--- Exiting _save_uploaded_image_as_artifact callback ---")

# --- Tool to generate images from text prompts ---
async def generate_image_tool(tool_context: ToolContext, prompt: str) -> str:
    """
    Generates an image from a text description using Gemini 2.5 Flash Image Preview.
    
    Args:
        tool_context: The tool context with access to artifacts
        prompt: Text description of the image to generate
        
    Returns:
        str: Success message with generation details
    """
    logger.info(f"Starting image generation with prompt: {prompt}")
    
    try:
        # Initialize Gemini client with Vertex AI
        client = genai.Client(
            vertexai=True,
            api_key=os.environ.get("GOOGLE_CLOUD_API_KEY"),
        )
        
        model = "gemini-2.5-flash-image-preview"
        
        # Create content with the text prompt
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=prompt)
                ]
            ),
        ]
        
        # Configure generation settings
        generate_content_config = types.GenerateContentConfig(
            temperature=1,
            top_p=0.95,
            max_output_tokens=32768,
            response_modalities=["TEXT", "IMAGE"],
            safety_settings=[
                types.SafetySetting(
                    category="HARM_CATEGORY_HATE_SPEECH",
                    threshold="OFF"
                ),
                types.SafetySetting(
                    category="HARM_CATEGORY_DANGEROUS_CONTENT",
                    threshold="OFF"
                ),
                types.SafetySetting(
                    category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    threshold="OFF"
                ),
                types.SafetySetting(
                    category="HARM_CATEGORY_HARASSMENT",
                    threshold="OFF"
                )
            ],
        )
        
        # Log API request details
        log_api_request(
            operation="image_generation",
            model=model,
            content_parts=len(contents[0].parts),
            prompt_length=len(prompt),
            temperature=generate_content_config.temperature,
            top_p=generate_content_config.top_p
        )
        
        logger.info("Calling Gemini 2.5 Flash Image Preview for generation...")
        
        # Define the API call function for retry logic
        async def make_api_call():
            return client.models.generate_content(
                model=model,
                contents=contents,
                config=generate_content_config,
            )
        
        # Generate content with retry logic
        try:
            response = await retry_with_backoff(
                make_api_call,
                "image_generation_api_call",
                max_retries=3,
                initial_delay=2.0
            )
            
            # Log successful response
            response_summary = {
                "has_candidates": bool(response and response.candidates),
                "num_candidates": len(response.candidates) if response and response.candidates else 0,
            }
            log_api_response("image_generation", True, response_summary)
            
        except Exception as api_error:
            # Log failed response
            log_api_response("image_generation", False, error=str(api_error))
            raise
        
        # Extract generated image from response
        if response and response.candidates:
            for candidate in response.candidates:
                if candidate.content and candidate.content.parts:
                    for part in candidate.content.parts:
                        # Look for generated image
                        if hasattr(part, 'inline_data') and getattr(part.inline_data, 'mime_type', '').startswith('image/'):
                            logger.info(f"Found generated image with mime_type: {part.inline_data.mime_type}")
                            
                            # Create unique filename for generated image
                            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
                            extension = part.inline_data.mime_type.split('/')[-1] if '/' in part.inline_data.mime_type else 'png'
                            if extension == 'jpeg':
                                extension = 'jpg'
                            filename = f"generated_image_{timestamp}.{extension}"
                            
                            # Save generated image as artifact
                            version = await tool_context.save_artifact(
                                filename=filename,
                                artifact=part
                            )
                            
                            logger.info(f"Successfully saved generated image as artifact '{filename}' version {version}")
                            
                            # Update state with last generated image
                            current_state = tool_context.state.to_dict()
                            current_state['last_generated_image'] = filename
                            tool_context.state.update(current_state)
                            
                            # Create response
                            response_text = f"🎨 **Imagem gerada com sucesso!** 🎨\n\n"
                            response_text += f"📋 **Detalhes da geração:**\n"
                            response_text += f"• **Prompt:** {prompt}\n"
                            response_text += f"• **Modelo:** Gemini 2.5 Flash Image Preview\n"
                            response_text += f"• **Tipo:** {part.inline_data.mime_type}\n"
                            response_text += f"• **Tamanho:** {len(part.inline_data.data)} bytes\n"
                            response_text += f"• **Arquivo:** {filename}\n\n"
                            response_text += "✅ A imagem foi salva como artifact e está pronta para visualização.\n"
                            response_text += "🔧 Use `edit_image_tool` para fazer modificações na imagem gerada.\n"
                            response_text += "📂 Use `list_generated_images_tool` para ver todas as imagens criadas."
                            
                            return response_text
        
        logger.error("No image found in generation response")
        return f"❌ Não foi possível gerar a imagem. O modelo retornou uma resposta sem imagem.\n\nPrompt usado: {prompt}"
        
    except Exception as e:
        logger.error(f"Error during image generation: {e}", exc_info=True)
        return f"❌ Erro durante a geração da imagem: {str(e)}\n\nVerifique se o Vertex AI está configurado corretamente e se você tem acesso ao modelo Gemini 2.5 Flash Image Preview."

# --- Tool to edit existing images ---
async def edit_image_tool(tool_context: ToolContext, editing_instructions: str, filename: Optional[str] = None) -> str:
    """
    Edits an existing image based on text instructions using Gemini 2.5 Flash Image Preview.
    
    Args:
        tool_context: The tool context with access to artifacts
        editing_instructions: Instructions for how to edit the image
        filename: Optional specific filename to edit. If not provided, uses the most recent image.
        
    Returns:
        str: Success message with editing details
    """
    logger.info(f"Starting image editing with instructions: {editing_instructions}")
    
    try:
        target_filename = filename
        
        # If no specific filename provided, find the most recent image
        if not target_filename:
            current_state = tool_context.state.to_dict()
            # First try last uploaded image, then last generated image
            target_filename = current_state.get('last_uploaded_image') or current_state.get('last_generated_image')
            
            # If still no filename, search for the most recent image artifact
            if not target_filename:
                artifacts = await tool_context.list_artifacts()
                image_artifacts = [name for name in artifacts if 
                                 (name.startswith('uploaded_image_') or name.startswith('generated_image_')) and 
                                 (name.endswith('.jpg') or name.endswith('.png') or name.endswith('.jpeg') or name.endswith('.gif') or name.endswith('.webp'))]
                
                if image_artifacts:
                    # Sort by timestamp (newest first)
                    image_artifacts.sort(reverse=True)
                    target_filename = image_artifacts[0]
                    logger.info(f"Found most recent image artifact: {target_filename}")
                else:
                    return "📂 Nenhuma imagem encontrada para edição. Por favor, envie uma imagem ou gere uma nova imagem primeiro."
        
        # Load the source image artifact
        source_image_artifact = await tool_context.load_artifact(filename=target_filename)
        
        if not source_image_artifact or not source_image_artifact.inline_data:
            return f"❌ Não foi possível carregar a imagem '{target_filename}'. Verifique se o arquivo existe nos artifacts."
        
        logger.info(f"Successfully loaded source image: {target_filename}")
        
        # Initialize Gemini client with Vertex AI
        client = genai.Client(
            vertexai=True,
            api_key=os.environ.get("GOOGLE_CLOUD_API_KEY"),
        )
        
        model = "gemini-2.5-flash-image-preview"
        
        # Create content with both the image and editing instructions
        contents = [
            types.Content(
                role="user",
                parts=[
                    source_image_artifact,  # The source image
                    types.Part.from_text(text=editing_instructions)
                ]
            ),
        ]
        
        # Configure generation settings
        generate_content_config = types.GenerateContentConfig(
            temperature=1,
            top_p=0.95,
            max_output_tokens=32768,
            response_modalities=["TEXT", "IMAGE"],
            safety_settings=[
                types.SafetySetting(
                    category="HARM_CATEGORY_HATE_SPEECH",
                    threshold="OFF"
                ),
                types.SafetySetting(
                    category="HARM_CATEGORY_DANGEROUS_CONTENT",
                    threshold="OFF"
                ),
                types.SafetySetting(
                    category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    threshold="OFF"
                ),
                types.SafetySetting(
                    category="HARM_CATEGORY_HARASSMENT",
                    threshold="OFF"
                )
            ],
        )
        
        # Log API request details
        log_api_request(
            operation="image_editing",
            model=model,
            content_parts=len(contents[0].parts),
            instructions_length=len(editing_instructions),
            source_image=target_filename,
            temperature=generate_content_config.temperature,
            top_p=generate_content_config.top_p
        )
        
        logger.info("Calling Gemini 2.5 Flash Image Preview for editing...")
        
        # Define the API call function for retry logic
        async def make_api_call():
            return client.models.generate_content(
                model=model,
                contents=contents,
                config=generate_content_config,
            )
        
        # Generate edited content with retry logic
        try:
            response = await retry_with_backoff(
                make_api_call,
                "image_editing_api_call",
                max_retries=3,
                initial_delay=2.0
            )
            
            # Log successful response
            response_summary = {
                "has_candidates": bool(response and response.candidates),
                "num_candidates": len(response.candidates) if response and response.candidates else 0,
            }
            log_api_response("image_editing", True, response_summary)
            
        except Exception as api_error:
            # Log failed response
            log_api_response("image_editing", False, error=str(api_error))
            raise
        
        # Extract edited image from response
        if response and response.candidates:
            for candidate in response.candidates:
                if candidate.content and candidate.content.parts:
                    for part in candidate.content.parts:
                        # Look for edited image
                        if hasattr(part, 'inline_data') and getattr(part.inline_data, 'mime_type', '').startswith('image/'):
                            logger.info(f"Found edited image with mime_type: {part.inline_data.mime_type}")
                            
                            # Create unique filename for edited image
                            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
                            extension = part.inline_data.mime_type.split('/')[-1] if '/' in part.inline_data.mime_type else 'png'
                            if extension == 'jpeg':
                                extension = 'jpg'
                            filename = f"edited_image_{timestamp}.{extension}"
                            
                            # Save edited image as artifact
                            version = await tool_context.save_artifact(
                                filename=filename,
                                artifact=part
                            )
                            
                            logger.info(f"Successfully saved edited image as artifact '{filename}' version {version}")
                            
                            # Update state with last edited image
                            current_state = tool_context.state.to_dict()
                            current_state['last_edited_image'] = filename
                            tool_context.state.update(current_state)
                            
                            # Create response
                            response_text = f"✂️ **Imagem editada com sucesso!** ✂️\n\n"
                            response_text += f"📋 **Detalhes da edição:**\n"
                            response_text += f"• **Imagem original:** {target_filename}\n"
                            response_text += f"• **Instruções:** {editing_instructions}\n"
                            response_text += f"• **Modelo:** Gemini 2.5 Flash Image Preview\n"
                            response_text += f"• **Tipo:** {part.inline_data.mime_type}\n"
                            response_text += f"• **Tamanho:** {len(part.inline_data.data)} bytes\n"
                            response_text += f"• **Arquivo editado:** {filename}\n\n"
                            response_text += "✅ A imagem editada foi salva como artifact e está pronta para visualização.\n"
                            response_text += "🔄 Use `edit_image_tool` novamente para fazer mais modificações.\n"
                            response_text += "📂 Use `list_generated_images_tool` para ver todas as imagens criadas."
                            
                            return response_text
        
        logger.error("No image found in editing response")
        return f"❌ Não foi possível editar a imagem. O modelo retornou uma resposta sem imagem.\n\nInstruções usadas: {editing_instructions}"
        
    except ValueError as e:
        logger.error(f"Error loading image artifact: {e}")
        return "❌ Erro ao carregar a imagem. Certifique-se de que o ArtifactService está configurado corretamente."
    except Exception as e:
        logger.error(f"Error during image editing: {e}", exc_info=True)
        return f"❌ Erro durante a edição da imagem: {str(e)}\n\nVerifique se o Vertex AI está configurado corretamente e se você tem acesso ao modelo Gemini 2.5 Flash Image Preview."

# --- Tool to list generated/edited images ---
async def list_generated_images_tool(tool_context: ToolContext) -> str:
    """
    Lists all generated and edited images in the current session.
    
    Args:
        tool_context: The tool context with access to artifacts
        
    Returns:
        str: List of available generated/edited images
    """
    logger.info("Listing generated and edited images")
    
    try:
        artifacts = await tool_context.list_artifacts()
        
        if not artifacts:
            return "📂 Nenhum artifact encontrado na sessão atual.\n\n⚠️ **Nota**: Se você gerou imagens mas não vê artifacts, certifique-se de que o Runner foi configurado com um ArtifactService (como InMemoryArtifactService ou GcsArtifactService)."
        
        # Filter for generated, edited, and uploaded images
        generated_images = [name for name in artifacts if name.startswith('generated_image_')]
        edited_images = [name for name in artifacts if name.startswith('edited_image_')]
        uploaded_images = [name for name in artifacts if name.startswith('uploaded_image_')]
        
        if not generated_images and not edited_images and not uploaded_images:
            return "📂 Nenhuma imagem encontrada nos artifacts.\n\n💡 **Dica**: Use `generate_image_tool` para criar novas imagens ou envie uma imagem para edição."
        
        response = "📂 **Imagens disponíveis:**\n\n"
        
        if generated_images:
            response += "🎨 **Imagens Geradas:**\n"
            for image_name in sorted(generated_images, reverse=True):
                response += f"• {image_name}\n"
                try:
                    artifact = await tool_context.load_artifact(filename=image_name)
                    if artifact and artifact.inline_data:
                        response += f"  - Tipo: {artifact.inline_data.mime_type}\n"
                        response += f"  - Tamanho: {len(artifact.inline_data.data)} bytes\n"
                except:
                    pass
            response += "\n"
        
        if edited_images:
            response += "✂️ **Imagens Editadas:**\n"
            for image_name in sorted(edited_images, reverse=True):
                response += f"• {image_name}\n"
                try:
                    artifact = await tool_context.load_artifact(filename=image_name)
                    if artifact and artifact.inline_data:
                        response += f"  - Tipo: {artifact.inline_data.mime_type}\n"
                        response += f"  - Tamanho: {len(artifact.inline_data.data)} bytes\n"
                except:
                    pass
            response += "\n"
        
        if uploaded_images:
            response += "📤 **Imagens Enviadas:**\n"
            for image_name in sorted(uploaded_images, reverse=True):
                response += f"• {image_name}\n"
                try:
                    artifact = await tool_context.load_artifact(filename=image_name)
                    if artifact and artifact.inline_data:
                        response += f"  - Tipo: {artifact.inline_data.mime_type}\n"
                        response += f"  - Tamanho: {len(artifact.inline_data.data)} bytes\n"
                except:
                    pass
            response += "\n"
        
        response += "🔧 **Comandos úteis:**\n"
        response += "• `show_generated_image_tool` - Exibir imagem específica\n"
        response += "• `generate_image_tool` - Gerar nova imagem\n"
        response += "• `edit_image_tool` - Editar imagem existente"
        
        return response
        
    except ValueError as e:
        logger.error(f"Error listing artifacts: {e}. Is ArtifactService configured?")
        return "❌ Erro ao listar artifacts. O ArtifactService não está configurado no Runner.\n\n📝 **Como corrigir**:\nAo criar o Runner, adicione um artifact_service:\n```python\nfrom google.adk.artifacts import InMemoryArtifactService\n\nrunner = Runner(\n    agent=agent,\n    app_name='image_generator',\n    artifact_service=InMemoryArtifactService()\n)\n```"
    except Exception as e:
        logger.error(f"Unexpected error listing artifacts: {e}", exc_info=True)
        return f"Ocorreu um erro inesperado ao listar artifacts: {str(e)}"

# --- Tool to display/show specific image artifact ---
async def show_generated_image_tool(tool_context: ToolContext, filename: Optional[str] = None) -> str:
    """
    Loads and displays a specific generated/edited image artifact back to the user.
    
    Args:
        tool_context: The tool context with access to artifacts
        filename: Optional specific filename to load. If not provided, shows the most recent image.
        
    Returns:
        str: Success message indicating the image is ready for display
    """
    logger.info(f"Loading image artifact for display: {filename}")
    
    try:
        target_filename = filename
        
        # If no specific filename provided, find the most recent image
        if not target_filename:
            current_state = tool_context.state.to_dict()
            # Try in order: last edited, last generated, last uploaded
            target_filename = (current_state.get('last_edited_image') or 
                             current_state.get('last_generated_image') or 
                             current_state.get('last_uploaded_image'))
            
            # If still no filename, search for the most recent image artifact
            if not target_filename:
                artifacts = await tool_context.list_artifacts()
                image_artifacts = [name for name in artifacts if 
                                 (name.startswith('generated_image_') or name.startswith('edited_image_') or name.startswith('uploaded_image_')) and 
                                 (name.endswith('.jpg') or name.endswith('.png') or name.endswith('.jpeg') or name.endswith('.gif') or name.endswith('.webp'))]
                
                if image_artifacts:
                    # Sort by timestamp (newest first)
                    image_artifacts.sort(reverse=True)
                    target_filename = image_artifacts[0]
                    logger.info(f"Found most recent image artifact: {target_filename}")
                else:
                    return "📂 Nenhuma imagem encontrada nos artifacts. Por favor, gere uma imagem ou envie uma imagem primeiro para que eu possa exibi-la."
        
        # Load the image artifact to verify it exists and get details
        image_artifact = await tool_context.load_artifact(filename=target_filename)
        
        if not image_artifact or not image_artifact.inline_data:
            return f"❌ Não foi possível carregar a imagem '{target_filename}'. Verifique se o arquivo existe nos artifacts."
        
        logger.info(f"Successfully loaded image artifact: {target_filename}")
        
        # Determine image type based on filename prefix
        image_type = "Gerada" if target_filename.startswith('generated_image_') else \
                    "Editada" if target_filename.startswith('edited_image_') else \
                    "Enviada"
        
        # Create response with image details and instruction to display
        response = f"🖼️ **Imagem {image_type} carregada com sucesso: {target_filename}**\n\n"
        response += f"📋 **Detalhes:**\n"
        response += f"• **Tipo:** {image_artifact.inline_data.mime_type}\n"
        response += f"• **Tamanho:** {len(image_artifact.inline_data.data)} bytes\n"
        response += f"• **Arquivo:** {target_filename}\n"
        response += f"• **Categoria:** Imagem {image_type}\n\n"
        response += "✅ A imagem está pronta para ser exibida pelo sistema.\n"
        response += "📄 Use `list_generated_images_tool` para ver todas as imagens disponíveis.\n"
        response += "🎨 Use `generate_image_tool` para criar uma nova imagem.\n"
        response += "✂️ Use `edit_image_tool` para editar esta ou outra imagem."
        
        return response
        
    except ValueError as e:
        logger.error(f"Error loading image artifact: {e}")
        return "❌ Erro ao carregar a imagem. Certifique-se de que o ArtifactService está configurado corretamente."
    except Exception as e:
        logger.error(f"Unexpected error in show_generated_image_tool: {e}", exc_info=True)
        return f"❌ Erro inesperado ao carregar a imagem: {str(e)}"

# Create the Image Generation Agent
image_generator = Agent(
    name="image_generator",
    model="gemini-2.5-flash",
    description="AI assistant specialized in image generation and editing using Gemini 2.5 Flash Image Preview",
    instruction=(
        "Você é um assistente de IA especializado em geração e edição de imagens usando o Gemini 2.5 Flash Image Preview! "
        "Seu papel é criar imagens incríveis a partir de descrições de texto e editar imagens existentes conforme as instruções EXATAS do usuário.\n\n"
        
        "🎯 **PRINCÍPIO FUNDAMENTAL: FIDELIDADE AO PEDIDO**\n"
        "- SEMPRE interprete e execute EXATAMENTE o que o usuário solicita\n"
        "- NUNCA adicione elementos não solicitados ou interpretações próprias\n"
        "- SEMPRE pergunte para esclarecimento se o pedido for ambíguo\n"
        "- FOQUE em melhorar apenas a execução do que foi pedido\n\n"
        
        "🎨 **GERAÇÃO DE IMAGENS:**\n"
        "- Use `generate_image_tool` para criar imagens a partir de prompts de texto\n"
        "- Interprete fielmente qualquer tipo de descrição: simples, complexa, criativa ou poética\n"
        "- Aceite estilos específicos: fotorrealista, anime, pintura, cartoon, abstrato, etc.\n"
        "- Se o prompt for muito vago, peça detalhes específicos ao invés de assumir\n"
        "- Salve automaticamente as imagens geradas como artifacts\n\n"
        
        "✂️ **EDIÇÃO DE IMAGENS - EXECUÇÃO PRECISA:**\n"
        "- Use `edit_image_tool` para modificar imagens conforme instruções ESPECÍFICAS\n"
        "- **Edições Simples**: 'Deixe mais claro' → apenas ajusta brilho, NÃO adiciona elementos\n"
        "- **Edições Criativas**: 'Transforme em estilo cyberpunk' → aplica estilo mantendo composição original\n"
        "- **Adições Específicas**: 'Adicione um gato' → adiciona APENAS um gato, nada mais\n"
        "- **Transformações Artísticas**: 'Estilo Van Gogh' → aplica técnica pictórica específica\n"
        "- **Correções Precisas**: 'Remova a pessoa da esquerda' → remove APENAS essa pessoa\n"
        "- Trabalhe com a imagem mais recente se não especificado qual editar\n"
        "- Mantenha o histórico de versões através dos artifacts\n\n"
        
        "🔍 **INTERPRETAÇÃO INTELIGENTE:**\n"
        "- Entenda nuances: 'mais colorido' = aumentar saturação, NÃO adicionar arco-íris\n"
        "- Reconheça estilos: 'steampunk', 'minimalista', 'barroco', 'cyberpunk', etc.\n"
        "- Interprete transformações: 'como se fosse uma pintura', 'versão cartoon', 'estilo vintage'\n"
        "- Respeite modificadores: 'sutilmente', 'drasticamente', 'levemente', 'completamente'\n"
        "- Aceite descrições poéticas mas mantenha foco no essencial solicitado\n\n"
        
        "📂 **GERENCIAMENTO:**\n"
        "- Use `list_generated_images_tool` para mostrar todas as imagens criadas/editadas\n"
        "- Use `show_generated_image_tool` para exibir imagens específicas\n"
        "- Organize as imagens por tipo: geradas, editadas, enviadas\n"
        "- Forneça informações detalhadas sobre cada imagem\n\n"
        
        "💡 **INTERAÇÃO COM O USUÁRIO:**\n"
        "- Se o pedido for ambíguo, pergunte especificamente o que deseja\n"
        "- Confirme interpretação em casos complexos: 'Entendi que você quer X, está correto?'\n"
        "- Explique o que você pode fazer se o usuário não souber como começar\n"
        "- Forneça feedback detalhado sobre o processo de geração/edição\n"
        "- Ofereça refinamentos baseados no resultado, mas sempre perguntando primeiro\n\n"
        
        "📝 **EXEMPLOS DE INTERPRETAÇÃO CORRETA:**\n"
        "✅ CORRETO:\n"
        "- 'Deixe mais colorido' → Aumenta saturação das cores existentes\n"
        "- 'Adicione um sol' → Adiciona APENAS um sol na posição adequada\n"
        "- 'Estilo anime' → Transforma mantendo composição mas com características anime\n"
        "- 'Remova o carro' → Remove APENAS o carro, mantém resto da cena\n\n"
        "❌ INCORRETO:\n"
        "- 'Deixe mais colorido' → Adicionar arco-íris, flores, borboletas (elementos não solicitados)\n"
        "- 'Adicione um sol' → Adicionar também nuvens, pássaros, paisagem (extras não pedidos)\n"
        "- 'Estilo anime' → Mudar completamente a cena, adicionar personagens não solicitados\n\n"
        
        "🎯 **SEMPRE:**\n"
        "- Use emojis para tornar a conversa mais visual e agradável 🖼️\n"
        "- Seja detalhista sobre o processo e resultados\n"
        "- Responda sempre em português brasileiro\n"
        "- Execute EXATAMENTE o que foi solicitado, sem adições criativas próprias\n"
        "- Se houver erro, explique e sugira alternativas respeitando o pedido original\n"
        "- Organize as informações de forma clara e inspiradora\n"
        "- Quando em dúvida, SEMPRE pergunte ao invés de assumir"
    ),
    tools=[generate_image_tool, edit_image_tool, list_generated_images_tool, show_generated_image_tool],
    before_agent_callback=_save_uploaded_image_as_artifact
)

logger.info(f"Image generator agent '{image_generator.name}' initialized with Gemini 2.5 Flash Image Preview capabilities.")

# Export the agent
root_agent = image_generator
