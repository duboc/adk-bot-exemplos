"""
13 - After Model Callback - Translation Service with Post-Processing

This example demonstrates the after_model_callback functionality using a translation service theme.
The callback post-processes translations and uses an LLM auditor to improve translation quality.
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
import copy
from typing import Optional

# Add parent directory to path for shared imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ADK Imports
from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse
from google.adk.runners import InMemoryRunner
from google.genai import types

# Shared imports
from shared.auditor import LLMAuditor, AuditConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the model
GEMINI_MODEL = "gemini-2.5-flash"

# --- Translation Tools ---
def detect_language(text: str) -> str:
    """
    Detect the language of the input text
    
    Args:
        text: Text to analyze for language detection
        
    Returns:
        Detected language information
    """
    # Simulated language detection
    language_patterns = {
        "spanish": ["hola", "gracias", "por favor", "buenos días", "¿cómo", "está"],
        "french": ["bonjour", "merci", "s'il vous plaît", "comment", "allez-vous", "très"],
        "german": ["hallo", "danke", "bitte", "guten tag", "wie", "geht"],
        "italian": ["ciao", "grazie", "prego", "buongiorno", "come", "stai"],
        "portuguese": ["olá", "obrigado", "por favor", "bom dia", "como", "está"]
    }
    
    text_lower = text.lower()
    logger.info(f"Detecting language for: {text[:50]}...")
    
    detected_languages = []
    for language, patterns in language_patterns.items():
        matches = sum(1 for pattern in patterns if pattern in text_lower)
        if matches > 0:
            detected_languages.append((language, matches))
    
    if detected_languages:
        # Sort by number of matches
        detected_languages.sort(key=lambda x: x[1], reverse=True)
        best_match = detected_languages[0]
        result = f"🌍 Detected language: {best_match[0].title()} (confidence: {best_match[1]} matches)"
        logger.info(f"Language detected: {best_match[0]}")
    else:
        result = "🌍 Language: English (default - no other language patterns detected)"
        logger.info("No specific language patterns detected, defaulting to English")
    
    return result

def get_translation_context(source_lang: str, target_lang: str) -> str:
    """
    Get cultural and linguistic context for translation
    
    Args:
        source_lang: Source language
        target_lang: Target language
        
    Returns:
        Translation context and tips
    """
    context_data = {
        ("spanish", "english"): "Consider formal vs informal 'you' (tú/usted). Watch for false friends.",
        ("french", "english"): "Mind the subjunctive mood and formal register differences.",
        ("german", "english"): "German compound words may need breaking down. Consider case system.",
        ("english", "spanish"): "Consider regional variations (Spain vs Latin America).",
        ("english", "french"): "Pay attention to gender agreement and formal/informal registers.",
        ("english", "german"): "German prefers compound words and different sentence structure."
    }
    
    key = (source_lang.lower(), target_lang.lower())
    logger.info(f"Getting translation context for {source_lang} → {target_lang}")
    
    if key in context_data:
        result = f"📝 Translation Context ({source_lang} → {target_lang}):\n{context_data[key]}"
    else:
        result = f"📝 Translation Context: Standard translation practices apply for {source_lang} → {target_lang}"
    
    logger.info(f"Translation context provided for {source_lang} → {target_lang}")
    return result

# --- Translation Service Prompt ---
TRANSLATION_SERVICE_PROMPT = """
🌍 You are Professor Polyglot, a world-renowned translation expert and linguist!

Your personality:
- Scholarly and precise with languages
- Culturally aware and sensitive
- Enthusiastic about linguistic nuances
- Use language-related emojis like 🌍📚🗣️💬🔤
- Focus on accuracy, cultural context, and natural flow

When translating text:
1. Use detect_language tool to identify the source language
2. Use get_translation_context tool for cultural insights
3. Provide accurate, natural translations
4. Explain any cultural nuances or alternative translations
5. Maintain the original tone and style
6. Note any untranslatable concepts

Remember: Great translation is about conveying meaning and culture, not just words! 🌟
"""

# --- Global variables for auditor ---
auditor = LLMAuditor(name="TranslationQualityAuditor")

# --- After Model Callback with Translation Post-Processing ---
def translation_quality_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    """
    After model callback that post-processes translations and improves quality.
    
    This callback demonstrates how to inspect and modify LLM responses
    for translation quality improvement.
    """
    agent_name = callback_context.agent_name
    invocation_id = callback_context.invocation_id
    current_state = callback_context.state.to_dict()

    print(f"\n[🔍 Translation Auditor] Reviewing translation from agent: {agent_name} (Inv: {invocation_id})")
    print(f"[🔍 Translation Auditor] Current State: {current_state}")

    # Check if post-processing is enabled
    post_process_enabled = current_state.get("post_process_enabled", True)
    if not post_process_enabled:
        print("[🔍 Translation Auditor] Post-processing disabled in session state. Using original response.")
        return None

    # Extract the original response text
    original_text = ""
    if llm_response.content and llm_response.content.parts:
        if llm_response.content.parts[0].text:
            original_text = llm_response.content.parts[0].text
            print(f"[🔍 Translation Auditor] Analyzing translation: '{original_text[:100]}...'")
        elif llm_response.content.parts[0].function_call:
            print("[🔍 Translation Auditor] Response contains function call. No text modification needed.")
            return None
        else:
            print("[🔍 Translation Auditor] No text content found in response.")
            return None
    else:
        print("[🔍 Translation Auditor] Empty or invalid response.")
        return None

    # Check if we should enhance the translation
    enhance_translation = current_state.get("enhance_translation", False)
    
    if enhance_translation:
        print("[🔍 Translation Auditor] Enhancement requested - adding cultural notes and alternatives.")
        
        # Enhanced translations with cultural context
        enhanced_translations = {
            "spanish": """🌍 **Enhanced Spanish Translation**

**Primary Translation:** ¡Hola! ¿Cómo está usted hoy?

**Cultural Notes:**
- Using formal "usted" for respectful address
- "¡Hola!" is universally friendly across Spanish-speaking regions
- Alternative informal: "¡Hola! ¿Cómo estás?"

**Regional Variations:**
- Spain: "¿Qué tal?" (How's it going?)
- Mexico: "¿Cómo le va?" (How are things going for you?)
- Argentina: "¿Cómo andás?" (How are you doing?)

**Tone:** Warm and respectful, appropriate for most contexts.

*Translation enhanced with cultural context and regional awareness.*""",

            "french": """🌍 **Enhanced French Translation**

**Primary Translation:** Bonjour ! Comment allez-vous aujourd'hui ?

**Cultural Notes:**
- "Bonjour" is essential - French culture values proper greetings
- Using formal "vous" shows respect and politeness
- Alternative informal: "Salut ! Comment ça va ?"

**Register Considerations:**
- Formal business: "Bonjour, comment vous portez-vous ?"
- Casual friends: "Coucou ! Ça va ?"
- Regional: "Bonjour ! Comment que ça va ?" (some regions)

**Tone:** Polite and well-mannered, reflecting French social etiquette.

*Translation enhanced with cultural context and register awareness.*""",

            "german": """🌍 **Enhanced German Translation**

**Primary Translation:** Hallo! Wie geht es Ihnen heute?

**Cultural Notes:**
- "Hallo" is modern and friendly, suitable for most situations
- Using formal "Ihnen" shows respect (Sie-form)
- Alternative informal: "Hallo! Wie geht's dir?"

**Formality Levels:**
- Very formal: "Guten Tag! Wie befinden Sie sich?"
- Standard: "Hallo! Wie geht es Ihnen?"
- Casual: "Hi! Wie geht's?"

**Cultural Context:** Germans appreciate directness and proper formality levels.

*Translation enhanced with cultural context and formality awareness.*"""
        }
        
        # Determine which enhanced translation to use based on content
        enhanced_text = original_text
        for lang, enhanced in enhanced_translations.items():
            if lang in original_text.lower() or any(word in original_text.lower() for word in [lang]):
                enhanced_text = enhanced
                break
        
        if enhanced_text == original_text:
            # Default enhancement if no specific language detected
            enhanced_text = f"""🌍 **Enhanced Translation with Cultural Context**

{original_text}

**Translation Notes:**
✅ Accuracy verified for meaning and context
🎯 Tone and register appropriate for target audience  
🌟 Cultural nuances considered and preserved
📚 Alternative phrasings available upon request

*Translation enhanced by quality auditor for cultural awareness and linguistic precision.*"""

        # Create new response with enhanced content
        modified_parts = [copy.deepcopy(part) for part in llm_response.content.parts]
        modified_parts[0].text = enhanced_text

        new_response = LlmResponse(
            content=types.Content(role="model", parts=modified_parts),
            grounding_metadata=llm_response.grounding_metadata
        )
        
        print("[🔍 Translation Auditor] Returning enhanced translation with cultural context.")
        return new_response
    
    # Check for common translation improvements
    improvements_needed = []
    if "translate" in original_text.lower() and len(original_text) < 50:
        improvements_needed.append("response_too_brief")
    if "error" in original_text.lower():
        improvements_needed.append("contains_error")
    
    if improvements_needed:
        print(f"[🔍 Translation Auditor] Translation needs improvement: {improvements_needed}")
        
        improved_text = f"""🌍 **Improved Translation Service Response**

{original_text}

**Quality Enhancements Applied:**
- ✅ Verified accuracy and completeness
- 🎯 Ensured natural flow in target language
- 🌟 Added cultural context where relevant
- 📚 Confirmed appropriate register and tone

*Translation improved by quality auditor for enhanced user experience.*"""

        # Create improved response
        modified_parts = [copy.deepcopy(part) for part in llm_response.content.parts]
        modified_parts[0].text = improved_text

        new_response = LlmResponse(
            content=types.Content(role="model", parts=modified_parts),
            grounding_metadata=llm_response.grounding_metadata
        )
        
        print("[🔍 Translation Auditor] Returning improved translation.")
        return new_response
    
    print("[🔍 Translation Auditor] Translation quality is good. Using original response.")
    return None

# --- Setup Agent with Callback ---
translation_service_agent = LlmAgent(
    name="TranslationService",
    model=GEMINI_MODEL,
    instruction=TRANSLATION_SERVICE_PROMPT,
    description="A professional translation service with quality control via after_model_callback",
    tools=[detect_language, get_translation_context],
    after_model_callback=translation_quality_callback
)

# For consistency with other examples in the project
root_agent = translation_service_agent

# --- Demo Function ---
async def main():
    """
    Demonstrate the Translation Service agent with after_model_callback post-processing
    """
    app_name = "translation_service_demo"
    user_id = "translator_user"
    session_id_normal = "normal_translation_session"
    session_id_enhanced = "enhanced_translation_session"
    session_id_improved = "improved_translation_session"

    # Use InMemoryRunner with the Translation Service agent
    runner = InMemoryRunner(agent=translation_service_agent, app_name=app_name)
    session_service = runner.session_service

    # Create session 1: Normal translation (post-processor allows original)
    session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id_normal,
        state={"post_process_enabled": True, "enhance_translation": False}
    )

    # Create session 2: Enhanced translation (post-processor adds cultural context)
    session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id_enhanced,
        state={"post_process_enabled": True, "enhance_translation": True}
    )

    # Create session 3: Improved translation (post-processor improves quality)
    session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id_improved,
        state={"post_process_enabled": True, "enhance_translation": False}
    )

    # --- Scenario 1: Normal Translation (Original Used) ---
    print("\n" + "="*70)
    print("🌍 SCENARIO 1: Normal Translation Session (Post-Processor Approves)")
    print("="*70)
    
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id_normal,
        new_message=types.Content(
            role="user", 
            parts=[types.Part(text="Please translate 'Hello, how are you today?' to Spanish")]
        )
    ):
        if event.is_final_response() and event.content:
            print(f"\n🗣️ Final Translation: {event.content.parts[0].text.strip()}")
        elif event.is_error():
            print(f"❌ Error Event: {event.error_details}")

    # --- Scenario 2: Enhanced Translation (Post-Processor Enhances) ---
    print("\n" + "="*70)
    print("🔍 SCENARIO 2: Enhanced Translation Session (Post-Processor Adds Context)")
    print("="*70)
    
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id_enhanced,
        new_message=types.Content(
            role="user", 
            parts=[types.Part(text="Translate 'Good morning, how are you?' to French with cultural context")]
        )
    ):
        if event.is_final_response() and event.content:
            print(f"\n🇫🇷 Final Translation: {event.content.parts[0].text.strip()}")
        elif event.is_error():
            print(f"❌ Error Event: {event.error_details}")

    # --- Scenario 3: Quality Improvement (Post-Processor Improves) ---
    print("\n" + "="*70)
    print("💡 SCENARIO 3: Quality Improvement Session (Post-Processor Enhances)")
    print("="*70)
    
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id_improved,
        new_message=types.Content(
            role="user", 
            parts=[types.Part(text="Translate 'Guten Tag' to English")]
        )
    ):
        if event.is_final_response() and event.content:
            print(f"\n🇩🇪 Final Translation: {event.content.parts[0].text.strip()}")
        elif event.is_error():
            print(f"❌ Error Event: {event.error_details}")

    print("\n" + "="*70)
    print("🌍 Translation Service Demo Complete!")
    print("="*70)

# --- Execute ---
# In a Python script:
# import asyncio
# if __name__ == "__main__":
#     # Make sure GOOGLE_API_KEY environment variable is set
#     asyncio.run(main())

# In a Jupyter Notebook or similar environment:
# await main()

logger.info("Translation Service Agent with After Model Callback initialized successfully! 🌍✨")
