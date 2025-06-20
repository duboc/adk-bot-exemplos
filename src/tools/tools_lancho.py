import logging
import requests
import json
from typing import List, Dict, Any

# Configurar logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Constantes
FANTASTIC_FAST_FOOD_API_URL = "https://api-lanchos-713488125678.us-central1.run.app/api/v1/fantastic-fast-food/orders"


def finalize_order(order_items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Finalizar pedido enviando os itens para a API do Comida Rápida Fantástica.

    Args:
        order_items: Lista de itens do pedido, cada item deve conter:
                    - productName (str): Nome exato do produto
                    - quantity (int): Quantidade do produto

    Returns:
        Dicionário com o resultado da operação:
        - status: "SUCCESS" ou "ERROR"
        - data: Dados da resposta da API (se sucesso)
        - message: Mensagem de erro (se erro)
        - orderId: ID do pedido (se disponível)
    """
    try:
        logger.info(f"Finalizando pedido com {len(order_items)} itens")
        
        # Validar entrada
        if not order_items:
            logger.error("Lista de itens do pedido está vazia")
            return {
                "status": "ERROR",
                "message": "Lista de itens do pedido não pode estar vazia"
            }
        
        # Validar estrutura dos itens
        for item in order_items:
            if not isinstance(item, dict) or "productName" not in item or "quantity" not in item:
                logger.error(f"Item inválido na estrutura: {item}")
                return {
                    "status": "ERROR",
                    "message": "Cada item deve conter 'productName' e 'quantity'"
                }
        
        # Preparar payload para a API
        payload = {
            "items": order_items
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        logger.info(f"Enviando pedido para API: {FANTASTIC_FAST_FOOD_API_URL}")
        logger.debug(f"Payload: {json.dumps(payload, indent=2)}")
        
        # Fazer requisição para a API
        response = requests.post(
            FANTASTIC_FAST_FOOD_API_URL,
            headers=headers,
            json=payload,
            timeout=30  # Timeout de 30 segundos
        )
        
        logger.info(f"Resposta da API - Status Code: {response.status_code}")
        
        # Verificar se a requisição foi bem-sucedida
        if response.status_code == 200 or response.status_code == 201:
            response_data = response.json()
            logger.info("Pedido finalizado com sucesso")
            logger.debug(f"Resposta da API: {response_data}")
            
            return {
                "status": "SUCCESS",
                "data": response_data,
                "orderId": response_data.get("orderId") or response_data.get("id")
            }
        else:
            logger.error(f"Erro na API - Status: {response.status_code}, Resposta: {response.text}")
            return {
                "status": "ERROR",
                "message": f"Erro no servidor: {response.status_code} - {response.text}"
            }
            
    except requests.exceptions.Timeout:
        logger.error("Timeout na requisição para a API")
        return {
            "status": "ERROR",
            "message": "Timeout na conexão com o servidor. Tente novamente."
        }
    
    except requests.exceptions.ConnectionError:
        logger.error("Erro de conexão com a API")
        return {
            "status": "ERROR",
            "message": "Erro de conexão com o servidor. Verifique sua internet."
        }
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro na requisição: {str(e)}")
        return {
            "status": "ERROR",
            "message": f"Erro na requisição: {str(e)}"
        }
    
    except json.JSONDecodeError as e:
        logger.error(f"Erro ao decodificar resposta JSON: {str(e)}")
        return {
            "status": "ERROR",
            "message": "Erro na resposta do servidor"
        }
    
    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}")
        return {
            "status": "ERROR",
            "message": f"Erro inesperado: {str(e)}"
        }


def get_menu_item_info(product_name: str) -> Dict[str, Any]:
    """
    Obter informações sobre um item do menu (função de utilidade).

    Args:
        product_name: Nome do produto

    Returns:
        Dicionário com informações do produto ou None se não encontrado
    """
    # Menu simplificado para validação
    menu_items = {
        "Clásica CRF": {"price": 3.00, "category": "sandwich"},
        "Clásica con Queso CRF": {"price": 3.50, "category": "sandwich"},
        "Doble Delicia CRF": {"price": 5.00, "category": "sandwich"},
        "Torre de Sabor CRF": {"price": 5.50, "category": "sandwich"},
        "Rey Tocino CRF": {"price": 6.00, "category": "sandwich"},
        "Gran Rey CRF": {"price": 4.50, "category": "sandwich"},
        "Pollo Fantástico Crujiente": {"price": 4.00, "category": "sandwich"},
        "Hamburguesa Vegetal Fantástica": {"price": 5.00, "category": "sandwich"},
        "Hamburguesita con Queso": {"price": 1.50, "category": "sandwich"},
        "Doble Queso Económica": {"price": 2.50, "category": "sandwich"},
        "Papitas Fantásticas (Medianas)": {"price": 2.00, "category": "side"},
        "Aros de Cebolla Dorados (M)": {"price": 2.50, "category": "side"},
        "Bocaditos de Pollo Mágicos (6u)": {"price": 2.50, "category": "side"},
        "Papas Mágicas (para compartir)": {"price": 4.00, "category": "side"},
        "Batido Fantasía (Choc. Croc.)": {"price": 3.00, "category": "dessert"},
        "Batido Clásico de Chocolate": {"price": 2.50, "category": "dessert"},
        "Copa Helada Clásica (Choc/Fresa)": {"price": 1.50, "category": "dessert"},
        "Conito Helado": {"price": 1.00, "category": "dessert"},
        "Mezcla Mágica (Trocitos Croc.)": {"price": 2.50, "category": "dessert"},
        "Refresco (Mediano)": {"price": 1.50, "category": "beverage"},
        "Agua Embotellada": {"price": 1.00, "category": "beverage"},
        "Jugo de Naranja (Pequeño)": {"price": 2.00, "category": "beverage"}
    }
    
    return menu_items.get(product_name)
