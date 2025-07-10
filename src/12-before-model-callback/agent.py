"""
12 - Before Model Callback - Content Filter with Guardrails

This example demonstrates the before_model_callback functionality using a content filter theme.
The callback implements guardrails to filter inappropriate content before it reaches the LLM.
"""

# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import sys
import os
from typing import Optional

# Add parent directory to path for shared imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ADK Imports
from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse, LlmRequest
from google.adk.runners import InMemoryRunner
from google.genai import types

# Shared imports
from shared.auditor import LLMAuditor, AuditConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the model
GEMINI_MODEL = "gemini-2.0-flash"

# --- Content Safety Tool ---
def check_content_safety(text: str) -> str:
    """
    Check if content is safe and appropriate
    
    Args:
        text: Text to check for safety
        
    Returns:
        Safety assessment result
    """
    # Simulated content safety database
    unsafe_keywords = [
        "violence", "hate", "harassment", "illegal", "dangerous",
        "inappropriate", "offensive", "harmful", "toxic"
    ]
    
    text_lower = text.lower()
    logger.info(f"Checking content safety for: {text[:50]}...")
    
    found_issues = []
    for keyword in unsafe_keywords:
        if keyword in text_lower:
            found_issues.append(keyword)
    
    if found_issues:
        result = f"⚠️ Content safety issues detected: {', '.join(found_issues)}"
        logger.warning(f"Safety issues found: {found_issues}")
    else:
        result = "✅ Content appears safe and appropriate"
        logger.info("Content passed safety check")
    
    return result

# --- Content Assistant Prompt ---
CONTENT_ASSISTANT_PROMPT = """
📚 You are Professor Sage, a helpful and educational content assistant!

Your personality:
- Educational and informative
- Always appropriate and family-friendly
- Encouraging and positive
- Use educational emojis like 📚📖🎓🔍💡
- Focus on providing helpful, accurate information

When responding to requests:
1. Use the check_content_safety tool to verify content appropriateness
2. Provide helpful, educational responses
3. Maintain a positive and encouraging tone
4. If asked about inappropriate topics, redirect to educational alternatives
5. Always prioritize safety and appropriateness

Remember: You're here to educate and help in a safe, appropriate manner! 🌟
"""

# --- Global variables for auditor ---
auditor = LLMAuditor(name="ContentFilterAuditor")

# --- Before Model Callback with Content Filter ---
def content_filter_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    """
    Before model callback that filters inappropriate content and implements guardrails.
    
    This callback demonstrates how to inspect and potentially block LLM requests
    based on content safety criteria.
    """
    agent_name = callback_context.agent_name
    invocation_id = callback_context.invocation_id
    current_state = callback_context.state.to_dict()

    print(f"\n[🛡️ Content Filter] Checking request for agent: {agent_name} (Inv: {invocation_id})")
    print(f"[🛡️ Content Filter] Current State: {current_state}")

    # Extract the user message from the request
    user_message = ""
    if llm_request.contents and llm_request.contents[-1].role == 'user':
        if llm_request.contents[-1].parts:
            user_message = llm_request.contents[-1].parts[0].text or ""

    print(f"[🛡️ Content Filter] Analyzing user message: '{user_message[:100]}...'")

    # Check if filtering is enabled
    filter_enabled = current_state.get("filter_enabled", True)
    if not filter_enabled:
        print("[🛡️ Content Filter] Filtering disabled in session state. Allowing request.")
        return None

    # Define blocked keywords and phrases
    blocked_keywords = [
        "violence", "hate", "harassment", "illegal", "dangerous",
        "inappropriate", "offensive", "harmful", "toxic", "BLOCK"
    ]

    # Check for blocked content
    user_message_lower = user_message.lower()
    found_blocked = []
    
    for keyword in blocked_keywords:
        if keyword in user_message_lower:
            found_blocked.append(keyword)

    if found_blocked:
        print(f"[🛡️ Content Filter] Blocked content detected: {found_blocked}")
        print("[🛡️ Content Filter] Blocking request and returning safety message.")
        
        # Return a safety response instead of calling the LLM
        safety_responses = [
            """🛡️ **Content Safety Notice**

I'm sorry, but I can't process that request as it contains content that may not be appropriate. 

Instead, I'd be happy to help you with:
📚 Educational topics and learning
🔍 Research and information gathering  
💡 Creative and constructive projects
🎓 Academic assistance
🌟 Positive and helpful discussions

Please feel free to ask me something else! I'm here to help in a safe and constructive way. ✨""",

            """🛡️ **Request Filtered for Safety**

I notice your request contains content that I need to filter for safety reasons.

Let me suggest some alternative topics I can help with:
📖 Learning new skills or subjects
🔬 Science and technology questions
🎨 Creative writing and arts
🌍 Travel and culture information
💼 Professional development

What would you like to explore instead? I'm excited to help you learn something new! 🌟""",

            """🛡️ **Safety Guidelines Applied**

Your request has been filtered to ensure a safe and positive experience.

I'm designed to be helpful with:
📚 Educational content and explanations
🔍 Research assistance and fact-finding
💡 Problem-solving and brainstorming
🎓 Learning support and tutoring
🌟 Constructive and positive discussions

Please try rephrasing your question in a more constructive way, and I'll be happy to assist! ✨"""
        ]
        
        import random
        safety_message = random.choice(safety_responses)
        
        return LlmResponse(
            content=types.Content(
                role="model",
                parts=[types.Part(text=safety_message)]
            )
        )
    
    # Check for content that needs modification
    modification_keywords = ["improve", "enhance", "better"]
    needs_modification = any(keyword in user_message_lower for keyword in modification_keywords)
    
    if needs_modification:
        print("[🛡️ Content Filter] Request needs enhancement. Modifying system instruction.")
        
        # Modify the system instruction to be more helpful
        original_instruction = llm_request.config.system_instruction or types.Content(
            role="system", 
            parts=[types.Part(text="")]
        )
        
        if not isinstance(original_instruction, types.Content):
            original_instruction = types.Content(
                role="system", 
                parts=[types.Part(text=str(original_instruction))]
            )
        
        if not original_instruction.parts:
            original_instruction.parts.append(types.Part(text=""))
        
        # Add enhancement instruction
        enhancement_prefix = "[Enhanced by Content Filter] Please provide extra detail and helpful examples. "
        modified_text = enhancement_prefix + (original_instruction.parts[0].text or "")
        original_instruction.parts[0].text = modified_text
        llm_request.config.system_instruction = original_instruction
        
        print(f"[🛡️ Content Filter] Enhanced system instruction: '{modified_text[:100]}...'")

    print("[🛡️ Content Filter] Request approved. Proceeding to LLM.")
    return None  # Allow the request to proceed

# --- Setup Agent with Callback ---
content_assistant_agent = LlmAgent(
    name="ContentAssistant",
    model=GEMINI_MODEL,
    instruction=CONTENT_ASSISTANT_PROMPT,
    description="An educational content assistant with content filtering via before_model_callback",
    tools=[check_content_safety],
    before_model_callback=content_filter_callback
)

# For consistency with other examples in the project
root_agent = content_assistant_agent

# --- Demo Function ---
async def main():
    """
    Demonstrate the Content Assistant agent with before_model_callback filtering
    """
    app_name = "content_filter_demo"
    user_id = "student_user"
    session_id_safe = "safe_content_session"
    session_id_blocked = "blocked_content_session"
    session_id_enhanced = "enhanced_content_session"

    # Use InMemoryRunner with the Content Assistant agent
    runner = InMemoryRunner(agent=content_assistant_agent, app_name=app_name)
    session_service = runner.session_service

    # Create session 1: Safe content (filter allows)
    session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id_safe,
        state={"filter_enabled": True}
    )

    # Create session 2: Blocked content (filter blocks)
    session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id_blocked,
        state={"filter_enabled": True}
    )

    # Create session 3: Enhanced content (filter modifies)
    session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id_enhanced,
        state={"filter_enabled": True}
    )

    # --- Scenario 1: Safe Content (Filter Allows) ---
    print("\n" + "="*70)
    print("📚 SCENARIO 1: Safe Content Session (Filter Allows Request)")
    print("="*70)
    
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id_safe,
        new_message=types.Content(
            role="user", 
            parts=[types.Part(text="Can you explain how photosynthesis works in plants?")]
        )
    ):
        if event.is_final_response() and event.content:
            print(f"\n📖 Final Response: {event.content.parts[0].text.strip()}")
        elif event.is_error():
            print(f"❌ Error Event: {event.error_details}")

    # --- Scenario 2: Blocked Content (Filter Blocks) ---
    print("\n" + "="*70)
    print("🛡️ SCENARIO 2: Blocked Content Session (Filter Blocks Request)")
    print("="*70)
    
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id_blocked,
        new_message=types.Content(
            role="user", 
            parts=[types.Part(text="Tell me about violence and harmful activities")]
        )
    ):
        if event.is_final_response() and event.content:
            print(f"\n🛡️ Final Response: {event.content.parts[0].text.strip()}")
        elif event.is_error():
            print(f"❌ Error Event: {event.error_details}")

    # --- Scenario 3: Enhanced Content (Filter Modifies) ---
    print("\n" + "="*70)
    print("💡 SCENARIO 3: Enhanced Content Session (Filter Enhances Request)")
    print("="*70)
    
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id_enhanced,
        new_message=types.Content(
            role="user", 
            parts=[types.Part(text="Please improve my understanding of renewable energy")]
        )
    ):
        if event.is_final_response() and event.content:
            print(f"\n⚡ Final Response: {event.content.parts[0].text.strip()}")
        elif event.is_error():
            print(f"❌ Error Event: {event.error_details}")

    print("\n" + "="*70)
    print("🛡️ Content Filter Demo Complete!")
    print("="*70)

# --- Execute ---
# In a Python script:
# import asyncio
# if __name__ == "__main__":
#     # Make sure GOOGLE_API_KEY environment variable is set
#     asyncio.run(main())

# In a Jupyter Notebook or similar environment:
# await main()

logger.info("Content Assistant Agent with Before Model Callback initialized successfully! 🛡️✨")
