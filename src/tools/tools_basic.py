import logging
from typing import List, Dict, Any, Optional
import google.genai.types as types
from google import genai

client = genai.Client()


# Configurar logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)



def analyze_url_content(url: str, question: Optional[str] = None) -> Dict[str, Any]:
    try:
        logger.info(f"Analisando conteúdo da URL: {url}")
        
        # Validar URL
        if not url or not url.startswith(("http://", "https://")):
            logger.error(f"URL inválida: {url}")
            return {
                "status": "ERROR",
                "message": "URL deve começar com http:// ou https://"
            }
        
        # Se não foi fornecida uma pergunta, usar um prompt padrão
        if question is None:
            question = "Extraia todo o conteúdo deste website"
        
        contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_uri(
                    file_uri=url,
                    mime_type="text/plain"
                ),
                types.Part(text=question)
            ]
        )
    ]

        response = client.models.generate_content(model='gemini-2.5-flash', contents=contents)
        return {
            "status": "SUCCESS",
            "content": response.text
        }
        
    except Exception as e:
        logger.error(f"Erro ao analisar URL {url}: {str(e)}")
        return {
            "status": "ERROR",
            "message": f"Erro ao processar URL: {str(e)}"
        }
