"""
Tools that demonstrate session state management in ADK.

These tools use the special 'tool_context' parameter name which is automatically
injected by ADK's FunctionTool. This allows tools to access and modify state.
"""

import logging
from typing import Dict, Any, List
from google.adk.tools import ToolContext

logger = logging.getLogger(__name__)

# Mock product database - Essencia products
PRODUCT_CATALOG = {
    "seca": [
        {"name": "Creme Hidratante Intensivo Essencia 250ml", "price": 45.90, "category": "hidratante"},
        {"name": "Óleo Nutritivo Essencia Argan 100ml", "price": 52.90, "category": "óleo"},
    ],
    "oleosa": [
        {"name": "Gel de Limpeza Purificante Essencia 200ml", "price": 35.90, "category": "limpeza"},
        {"name": "Protetor Solar Matte Essencia FPS 60", "price": 68.90, "category": "proteção"},
    ],
    "normal": [
        {"name": "Perfume Essencia Floral 75ml", "price": 95.90, "category": "perfume"},
        {"name": "Sabonete Líquido Essencia Lavanda 300ml", "price": 18.90, "category": "sabonete"},
    ],
}


def save_user_preference(preference_key: str, preference_value: str, tool_context: ToolContext) -> str:
    """
    Save a user preference to the session state with 'user:' prefix.
    This demonstrates user-scoped state that persists across sessions.

    Args:
        preference_key: The preference key (e.g., 'skin_type', 'favorite_category', 'name')
        preference_value: The preference value
        tool_context: Automatically injected by ADK (special parameter name)

    Returns:
        Confirmation message
    """
    # Use user: prefix for user-scoped state
    state_key = f"user:{preference_key}"
    tool_context.state[state_key] = preference_value

    # Also increment interaction count
    current_count = tool_context.state.get("user:interaction_count", 0)
    tool_context.state["user:interaction_count"] = current_count + 1

    logger.info(f"Saved user preference: {state_key} = {preference_value}")

    return f"✅ Preferência '{preference_key}' salva como '{preference_value}' no seu perfil!"


def get_product_recommendation(category: str = "geral", tool_context: ToolContext = None) -> str:
    """
    Get product recommendations based on user preferences stored in state.
    Demonstrates reading from user-scoped state.

    Args:
        category: Category to filter by (hidratante, perfume, limpeza, óleo, sabonete, or geral for all)
        tool_context: Automatically injected by ADK (special parameter name)

    Returns:
        Product recommendations as formatted text
    """
    # Read user preferences from state
    skin_type = tool_context.state.get("user:skin_type", "normal")
    user_name = tool_context.state.get("user:name", "Cliente")

    # Store temporary processing data with temp: prefix
    # This will be discarded after the invocation completes
    tool_context.state["temp:last_recommendation_request"] = category

    logger.info(f"Getting recommendations for skin_type={skin_type}, category={category}")

    # Get products based on skin type
    skin_type_normalized = skin_type.lower()
    if skin_type_normalized not in PRODUCT_CATALOG:
        skin_type_normalized = "normal"

    products = PRODUCT_CATALOG[skin_type_normalized]

    # Filter by category if specified and not "geral"
    if category != "geral":
        products = [p for p in products if category.lower() in p["category"].lower()]

    # Track that we made a recommendation (session-scoped state, no prefix)
    tool_context.state["last_recommendation_category"] = category

    # Format response
    if not products:
        return f"Não encontrei produtos na categoria '{category}' para pele {skin_type}."

    result = f"💄 Recomendações para {user_name} (pele {skin_type}):\n\n"
    for i, product in enumerate(products, 1):
        result += f"{i}. {product['name']} - R$ {product['price']:.2f}\n"

    return result


def track_interaction(interaction_type: str, details: str = "", tool_context: ToolContext = None) -> str:
    """
    Track customer interactions using different state scopes.
    Demonstrates session, user, app, and temp state.

    Args:
        interaction_type: Type of interaction (e.g., 'question', 'purchase', 'complaint')
        details: Additional details about the interaction
        tool_context: Automatically injected by ADK (special parameter name)

    Returns:
        Tracking confirmation with statistics
    """
    # Session-scoped: current conversation only (no prefix)
    tool_context.state["current_interaction_type"] = interaction_type
    tool_context.state["session_interaction_details"] = details

    # User-scoped: across all sessions for this user (user: prefix)
    total_interactions = tool_context.state.get("user:total_interactions", 0)
    tool_context.state["user:total_interactions"] = total_interactions + 1

    # App-scoped: shared across all users (app: prefix)
    # Useful for global metrics
    app_total = tool_context.state.get("app:total_customer_interactions", 0)
    tool_context.state["app:total_customer_interactions"] = app_total + 1

    # Temporary: only for current invocation (temp: prefix)
    # Will not persist after this agent response
    import datetime
    tool_context.state["temp:processing_timestamp"] = datetime.datetime.now().isoformat()
    tool_context.state["temp:interaction_processed"] = True

    logger.info(
        f"Tracked interaction: type={interaction_type}, "
        f"user_total={tool_context.state['user:total_interactions']}, "
        f"app_total={tool_context.state['app:total_customer_interactions']}"
    )

    return (
        f"✅ Interação rastreada!\n"
        f"Tipo: {interaction_type}\n"
        f"Total de suas interações: {tool_context.state['user:total_interactions']}\n"
        f"Total de interações no app: {tool_context.state['app:total_customer_interactions']}"
    )
