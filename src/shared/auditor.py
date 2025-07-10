"""
Shared LLM Auditor Framework for Callback Examples

This module provides a reusable auditor system that can review and improve
agent responses using LLM-powered quality control.
"""

import logging
from typing import Dict, Optional, Any
from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.runners import InMemoryRunner
from google.genai import types

logger = logging.getLogger(__name__)

class LLMAuditor:
    """
    LLM-powered auditor that can review and improve agent responses
    """
    
    def __init__(self, model: str = "gemini-2.0-flash", name: str = "ResponseAuditor"):
        self.model = model
        self.name = name
        self._auditor_agent = None
    
    def _get_auditor_agent(self, audit_criteria: str) -> LlmAgent:
        """Create or get the auditor agent with specific criteria"""
        if self._auditor_agent is None:
            audit_prompt = f"""
You are a professional response auditor and editor. Your job is to review responses and improve them when necessary.

AUDIT CRITERIA:
{audit_criteria}

When reviewing a response, you should:
1. Analyze the response against the criteria
2. Determine if improvements are needed
3. If improvements are needed, provide a better version
4. Always maintain the original intent and tone while improving quality

Respond in this exact JSON format:
{{
    "needs_improvement": true/false,
    "improved_response": "your improved version here (only if needs_improvement is true)",
    "audit_notes": "brief explanation of what was improved or why no improvement was needed"
}}

Be concise but thorough in your analysis.
"""
            
            self._auditor_agent = LlmAgent(
                name=self.name,
                model=self.model,
                instruction=audit_prompt,
                description="LLM auditor for response quality control"
            )
        
        return self._auditor_agent
    
    async def audit_response(self, original_response: str, audit_criteria: str) -> Dict[str, Any]:
        """
        Audit a response and return improvement suggestions
        
        Args:
            original_response: The response to audit
            audit_criteria: Specific criteria for this audit
            
        Returns:
            Dict with keys: needs_improvement, improved_response, audit_notes
        """
        try:
            auditor = self._get_auditor_agent(audit_criteria)
            
            # Create a simple runner for the auditor
            runner = InMemoryRunner(agent=auditor, app_name="auditor_app")
            session_service = runner.session_service
            
            # Create session for audit
            session_service.create_session(
                app_name="auditor_app",
                user_id="auditor_user",
                session_id="audit_session"
            )
            
            # Send the response for audit
            audit_request = f"Please audit this response:\n\n{original_response}"
            
            audit_result = None
            async for event in runner.run_async(
                user_id="auditor_user",
                session_id="audit_session",
                new_message=types.Content(
                    role="user",
                    parts=[types.Part(text=audit_request)]
                )
            ):
                if event.is_final_response() and event.content:
                    audit_result = event.content.parts[0].text.strip()
                    break
            
            if audit_result:
                # Try to parse JSON response
                import json
                try:
                    return json.loads(audit_result)
                except json.JSONDecodeError:
                    # Fallback if JSON parsing fails
                    logger.warning(f"Failed to parse audit result as JSON: {audit_result}")
                    return {
                        "needs_improvement": False,
                        "improved_response": "",
                        "audit_notes": f"Audit completed but response format was invalid: {audit_result[:100]}..."
                    }
            else:
                return {
                    "needs_improvement": False,
                    "improved_response": "",
                    "audit_notes": "Audit failed - no response from auditor"
                }
                
        except Exception as e:
            logger.error(f"Audit failed with error: {e}")
            return {
                "needs_improvement": False,
                "improved_response": "",
                "audit_notes": f"Audit failed due to error: {str(e)}"
            }
    
    def create_audit_callback(self, audit_criteria: str):
        """
        Create an after_agent_callback function that uses this auditor
        
        Args:
            audit_criteria: The criteria to use for auditing
            
        Returns:
            A callback function suitable for after_agent_callback
        """
        async def audit_callback(callback_context: CallbackContext) -> Optional[types.Content]:
            """
            After agent callback that audits and potentially improves responses
            """
            agent_name = callback_context.agent_name
            invocation_id = callback_context.invocation_id
            current_state = callback_context.state.to_dict()
            
            print(f"\n[🔍 Auditor] Reviewing response from agent: {agent_name} (Inv: {invocation_id})")
            
            # Check if auditing is enabled in session state
            audit_enabled = current_state.get("audit_enabled", True)
            if not audit_enabled:
                print("[🔍 Auditor] Auditing disabled in session state. Skipping audit.")
                return None
            
            # Get the original response from the agent
            # Note: In a real implementation, you'd need to capture the agent's response
            # For now, we'll simulate this or use a different approach
            print("[🔍 Auditor] Auditing is enabled but response capture not implemented in this callback.")
            print("[🔍 Auditor] This callback demonstrates the framework structure.")
            
            # Return None to use original response
            return None
        
        return audit_callback


class AuditConfig:
    """Configuration class for different audit criteria"""
    
    RESTAURANT_REVIEW = """
    - Professional and constructive tone
    - Specific details about food, service, and atmosphere
    - Balanced perspective (both positives and areas for improvement)
    - Helpful for other diners
    - Free of offensive language
    - Proper grammar and spelling
    """
    
    CONTENT_FILTER = """
    - No inappropriate, offensive, or harmful content
    - Respectful and inclusive language
    - Age-appropriate content
    - No personal attacks or harassment
    - Factually accurate information
    - Clear and understandable language
    """
    
    TRANSLATION_QUALITY = """
    - Accurate translation of meaning
    - Natural flow in target language
    - Proper grammar and syntax
    - Cultural appropriateness
    - Maintains original tone and style
    - No mistranslations or omissions
    """
    
    WEATHER_SERVICE = """
    - Accurate and current weather information
    - Clear and easy to understand
    - Includes relevant details (temperature, conditions, etc.)
    - Appropriate warnings for severe weather
    - Professional and helpful tone
    - Properly formatted data
    """
    
    CALCULATION_ACCURACY = """
    - Mathematically correct results
    - Clear step-by-step explanations
    - Proper units and formatting
    - Appropriate precision for the context
    - Easy to verify calculations
    - Professional presentation
    """


# Utility functions for common callback patterns
def create_simple_audit_callback(auditor: LLMAuditor, criteria: str):
    """
    Create a simple audit callback that can be used with after_agent_callback
    """
    def callback(callback_context: CallbackContext) -> Optional[types.Content]:
        print(f"[🔍 Auditor] Simple audit callback triggered for {callback_context.agent_name}")
        # This is a placeholder - actual implementation would need to capture
        # the agent's response and audit it
        return None
    
    return callback


logger.info("LLM Auditor framework initialized")
