"""
7 - Single Agent Refund System for Natura with Tracing
"""

import logging
from typing import List, Dict, Any, Optional
from google.adk.agents import Agent
from vertexai.preview.reasoning_engines import AdkApp

from tools.tools import get_purchase_history, check_refund_eligibility, process_refund
from tools.prompts import top_level_prompt

logger = logging.getLogger(__name__)

GEMINI_MODEL = "gemini-2.5-flash-preview-05-20"

# Create the agent
root_agent = Agent(
    model=GEMINI_MODEL,
    name="RefundSingleAgent",
    description="Customer refund single-agent for Natura company",
    instruction=top_level_prompt,
    tools=[get_purchase_history, check_refund_eligibility, process_refund],
)

# Wrap agent with AdkApp to enable tracing
app = AdkApp(
    agent=root_agent,     # Required.
    enable_tracing=True,  # Optional.
)

logger.info(f"Initialized {root_agent.name} with tracing enabled")
