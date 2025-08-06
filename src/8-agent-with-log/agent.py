"""
1 - Single Agent Refund System for Natura
"""

import logging
from typing import List, Dict, Any, Optional
from google.adk.agents import Agent

from tools.tools import get_purchase_history, check_refund_eligibility, process_refund
from tools.prompts import top_level_prompt

logger = logging.getLogger(__name__)

GEMINI_MODEL = "gemini-2.5-flash"

root_agent = Agent(
    model=GEMINI_MODEL,
    name="RefundSingleAgent",
    description="Customer refund single-agent for Natura company",
    instruction=top_level_prompt,
    tools=[get_purchase_history, check_refund_eligibility, process_refund],
)

logger.info(f"Initialized {root_agent.name}")
