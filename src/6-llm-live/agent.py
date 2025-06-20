"""
6 - Felix CRF Fast Food Ordering System - Live Agent
"""

import logging
from typing import List, Dict, Any, Optional
from google.adk.agents import Agent

from tools.tools_lancho import finalize_order, get_menu_item_info
from tools.prompts_lancho import felix_crf_agent

logger = logging.getLogger(__name__)

GEMINI_MODEL = "gemini-2.0-flash-live-preview-04-09"
#GEMINI_MODEL = "gemini-2.5-flash-preview-05-20"
#GEMINI_MODEL = "gemini-2.5-flash-preview-native-audio-dialog"  
#GEMINI_MODEL = "gemini-2.0-flash-live-001"

root_agent = Agent(
    model=GEMINI_MODEL,
    name="FelixCRF",
    description="Félix, el Amigo del Sabor - Fast food ordering agent for Comida Rápida Fantástica",
    instruction=felix_crf_agent['personality'],
    tools=[finalize_order, get_menu_item_info],
)

logger.info(f"Initialized {root_agent.name} - ¡Listo para crear experiencias fantásticas!")
