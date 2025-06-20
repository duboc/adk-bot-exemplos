"""
8 - Single Agent Refund System for Natura with Google Cloud Logging
"""

import logging
import os
import json
from typing import List, Dict, Any, Optional
from google.adk.agents import Agent
import google.cloud.logging

from tools.tools import get_purchase_history, check_refund_eligibility, process_refund
from tools.prompts import top_level_prompt

logger = logging.getLogger(__name__)

GEMINI_MODEL = "gemini-2.5-flash-preview-05-20"


class NaturaAgentWithLogging:
    
    def set_up(self):
        """Set up Google Cloud Logging for the agent"""
        self.logging_client = google.cloud.logging.Client(project="PROJECT_ID")
        self.logging_client.setup_logging(
            name="natura-refund-agent-log",  # the ID of the logName in Cloud Logging.
            resource=google.cloud.logging.Resource(
                type="aiplatform.googleapis.com/ReasoningEngine",
                labels={
                    "location": "LOCATION",
                    "resource_container": "PROJECT_ID",
                    "reasoning_engine_id": os.environ.get("GOOGLE_CLOUD_AGENT_ENGINE_ID", ""),
                },
            ),
        )
        
        logger.info("Google Cloud Logging configured for Natura Refund Agent")

    def query(self, input: Dict):
        """Process query with detailed logging"""
        logging_extras = {
            "labels": {"agent": "natura-refund", "system": "customer-service"},
            "trace": "TRACE_ID",
        }

        # Log the incoming request
        logging.info(
            json.dumps({
                "event": "query_received",
                "input": input,
                "agent": "RefundSingleAgent"
            }),
            extra=logging_extras,
        )
        
        try:
            # Log processing start
            logging.info(
                json.dumps({
                    "event": "query_processing",
                    "status": "started",
                    "model": GEMINI_MODEL
                }),
                extra=logging_extras,
            )
            
            # Here you would typically call: response = root_agent.query(input)
            # For demonstration, we'll simulate a response
            response = {"message": "Olá! Sou o assistente de reembolso da Natura. Como posso ajudá-lo?"}
            
            # Log successful completion
            logging.info(
                json.dumps({
                    "event": "query_completed",
                    "status": "success",
                    "response_length": len(str(response))
                }),
                extra=logging_extras,
            )
            
            return response
            
        except Exception as e:
            # Log errors
            logging.error(
                json.dumps({
                    "event": "query_error",
                    "error": str(e),
                    "error_type": type(e).__name__
                }),
                extra=logging_extras,
            )
            raise


# Initialize the logging helper
natura_logging = NaturaAgentWithLogging()

# Create the main agent
root_agent = Agent(
    model=GEMINI_MODEL,
    name="RefundSingleAgent",
    description="Customer refund single-agent for Natura company",
    instruction=top_level_prompt,
    tools=[get_purchase_history, check_refund_eligibility, process_refund],
)

logger.info(f"Initialized {root_agent.name} with Google Cloud Logging support")
