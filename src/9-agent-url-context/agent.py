"""
1 - Single Agent Refund System for Natura
"""

import logging
from typing import List, Dict, Any, Optional
from google.adk.agents import Agent

from tools.tools_basic import analyze_url_content
from tools.prompts_basic import top_level_prompt

logger = logging.getLogger(__name__)

GEMINI_MODEL = "gemini-2.5-flash"

root_agent = Agent(
    model=GEMINI_MODEL,
    name="AnalizeURL",
    description="Agent to analyze all the content from a website",
    instruction=top_level_prompt,
    tools=[analyze_url_content],
)

logger.info(f"Initialized {root_agent.name}")
