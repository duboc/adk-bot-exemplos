import logging
from typing import List, Dict, Any

# Configurar logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Constantes
ELIGIBLE_SHIPPING_METHODS = ["INSURED"]
ELIGIBLE_REASONS = ["DAMAGED", "NEVER_ARRIVED"]


def get_purchase_history(purchaser: str) -> List[Dict[str, Any]]:
    """
    Recuperar histórico de compras para um determinado cliente.

    Args:
        purchaser: Nome do cliente

    Returns:
        Lista de registros de compras contendo detalhes do pedido
    """
    # Banco de dados simulado do histórico de compras
    history_data = {
        "Erike": [
            {
                "order_id": "NAT001-20250415",
                "date": "2025-04-15",
                "items": [
                    {
                        "product_name": "Perfume Kaiak Feminino 100ml",
                        "quantity": 1,
                        "price": 89.90,
                    },
                    {
                        "product_name": "Creme Hidratante Tododia Algodão 400ml",
                        "quantity": 1,
                        "price": 32.90,
                    },
                ],
                "shipping_method": "STANDARD",
                "total_amount": 122.80,
            }
        ],
        "Massini": [
            {
                "order_id": "NAT002-20250610",
                "date": "2025-06-03",
                "items": [
                    {
                        "product_name": "Desodorante Natura Homem Humor 75ml",
                        "quantity": 1,
                        "price": 45.90,
                    },
                    {
                        "product_name": "Shampoo Plant Cachos Intensos 300ml",
                        "quantity": 1,
                        "price": 28.90,
                    },
                ],
                "shipping_method": "INSURED",
                "total_amount": 74.80,
            },
        ],
    }

    # Normalizar nome do comprador
    purchaser = purchaser.strip().title()

    logger.info(f"Recuperando histórico de compras para: {purchaser}")

    if purchaser not in history_data:
        logger.warning(f"Nenhum histórico de compras encontrado para: {purchaser}")
        return []

    history = history_data[purchaser]
    logger.info(f"Encontradas {len(history)} compra(s) para {purchaser}")
    return history


def check_refund_eligibility(reason: str, shipping_method: str) -> bool:
    """
    Verificar se uma solicitação de reembolso é elegível com base no motivo e método de envio.

    Args:
        reason: Motivo do reembolso
        shipping_method: Método de envio usado para o pedido

    Returns:
        True se o reembolso for elegível, False caso contrário
    """
    reason_upper = reason.strip().upper()
    shipping_upper = shipping_method.strip().upper()

    logger.info(
        f"Verificando elegibilidade para reembolso - Motivo: {reason_upper}, Envio: {shipping_upper}"
    )

    # Verificar elegibilidade com base no método de envio e motivo
    is_eligible = (
        shipping_upper in ELIGIBLE_SHIPPING_METHODS and reason_upper in ELIGIBLE_REASONS
    )

    logger.info(f"Resultado da elegibilidade para reembolso: {is_eligible}")
    return is_eligible


def process_refund(amount: float, order_id: str) -> str:
    """
    Processar um reembolso para o valor e pedido dados.

    Args:
        amount: Valor do reembolso em reais
        order_id: ID do pedido para reembolso

    Returns:
        Mensagem de sucesso com detalhes do reembolso
    """
    logger.info(f"Processando reembolso - Pedido: {order_id}, Valor: R${amount:.2f}")

    # Em um sistema real, isso interagiria com processadores de pagamento
    # Por enquanto, vamos simular um reembolso bem-sucedido
    refund_id = f"REF-{order_id}-{int(amount*100)}"
    logger.info(f"Reembolso processado com sucesso - ID do Reembolso: {refund_id}")

    return f"✅ Reembolso {refund_id} realizado com sucesso! Creditaremos R${amount:.2f} em sua conta em até 2 dias úteis."
