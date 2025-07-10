"""
11 - After Agent Callback - Restaurant Reviewer with LLM Auditor

This example demonstrates the after_agent_callback functionality using a restaurant reviewer theme.
The callback uses an LLM auditor to review and potentially improve restaurant reviews for quality control.
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

import random
import logging
import sys
import os
from typing import Optional

# Add parent directory to path for shared imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ADK Imports
from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.runners import InMemoryRunner
from google.genai import types

# Shared imports
from shared.auditor import LLMAuditor, AuditConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the model
GEMINI_MODEL = "gemini-2.5-flash"

# --- Restaurant Review Tool ---
def get_restaurant_info(restaurant_name: str) -> str:
    """
    Get basic information about a restaurant for review context
    
    Args:
        restaurant_name: Name of the restaurant
        
    Returns:
        Basic restaurant information
    """
    # Simulated restaurant database
    restaurants = {
        "bella italia": {
            "cuisine": "Italian",
            "price_range": "$$",
            "location": "Downtown",
            "specialties": ["pasta", "pizza", "tiramisu"]
        },
        "sushi zen": {
            "cuisine": "Japanese",
            "price_range": "$$$",
            "location": "Uptown",
            "specialties": ["sashimi", "rolls", "sake"]
        },
        "burger palace": {
            "cuisine": "American",
            "price_range": "$",
            "location": "Mall",
            "specialties": ["burgers", "fries", "milkshakes"]
        },
        "le petit bistro": {
            "cuisine": "French",
            "price_range": "$$$$",
            "location": "Arts District",
            "specialties": ["coq au vin", "escargot", "wine"]
        }
    }
    
    restaurant_key = restaurant_name.lower().strip()
    logger.info(f"Looking up restaurant: {restaurant_name}")
    
    if restaurant_key in restaurants:
        info = restaurants[restaurant_key]
        result = f"Restaurant: {restaurant_name.title()}\n"
        result += f"Cuisine: {info['cuisine']}\n"
        result += f"Price Range: {info['price_range']}\n"
        result += f"Location: {info['location']}\n"
        result += f"Specialties: {', '.join(info['specialties'])}"
        logger.info(f"Found restaurant info for: {restaurant_name}")
        return result
    else:
        logger.info(f"Restaurant not found: {restaurant_name}")
        return f"Restaurant '{restaurant_name}' not found in our database. Please provide your own context for the review."

# --- Restaurant Reviewer Prompt ---
RESTAURANT_REVIEWER_PROMPT = """
🍽️ You are Chef Gordon Critique, a passionate and experienced restaurant reviewer! 

Your personality:
- Professional but enthusiastic about good food
- Detailed and specific in your reviews
- Fair and balanced - you mention both positives and areas for improvement
- Use food-related emojis like 🍽️🍕🍝🍣🥘🍷
- Focus on food quality, service, atmosphere, and value

When writing a restaurant review:
1. Use the get_restaurant_info tool to get context about the restaurant
2. Write a comprehensive review covering:
   - Food quality and taste
   - Service experience
   - Restaurant atmosphere
   - Value for money
   - Overall recommendation
3. Be specific with details and examples
4. Maintain a professional but engaging tone
5. Include a rating out of 5 stars

Remember: You're helping diners make informed decisions! Be honest, fair, and helpful. 🌟
"""

# --- Global variables for auditor ---
auditor = LLMAuditor(name="RestaurantReviewAuditor")

# --- After Agent Callback with Auditor ---
def review_quality_callback(callback_context: CallbackContext) -> Optional[types.Content]:
    """
    After agent callback that audits restaurant reviews and improves them if needed.
    
    This callback demonstrates how to use an LLM auditor to review and potentially
    improve agent responses based on quality criteria.
    """
    agent_name = callback_context.agent_name
    invocation_id = callback_context.invocation_id
    current_state = callback_context.state.to_dict()

    print(f"\n[🔍 Review Auditor] Checking review quality for agent: {agent_name} (Inv: {invocation_id})")
    print(f"[🔍 Review Auditor] Current State: {current_state}")

    # Check if auditing is enabled
    audit_enabled = current_state.get("audit_enabled", True)
    if not audit_enabled:
        print("[🔍 Review Auditor] Auditing disabled in session state. Using original review.")
        return None

    # Check if we should simulate a poor quality review that needs improvement
    simulate_poor_review = current_state.get("simulate_poor_review", False)
    
    if simulate_poor_review:
        print("[🔍 Review Auditor] Simulating poor review quality - replacing with improved version.")
        
        # Simulate an improved review (in real implementation, this would come from the auditor LLM)
        improved_reviews = [
            """🍽️ **Bella Italia Review - 4/5 Stars** ⭐⭐⭐⭐

**Food Quality:** The pasta dishes were exceptional, particularly the carbonara which featured perfectly al dente noodles and a rich, creamy sauce. The pizza had a wonderfully crispy crust with fresh toppings, though the margherita could have used a bit more basil.

**Service:** Our server was attentive and knowledgeable about the menu, providing excellent wine recommendations. Service was prompt despite the busy evening crowd.

**Atmosphere:** Warm and inviting Italian ambiance with soft lighting and authentic décor. The noise level was perfect for conversation.

**Value:** Reasonable prices for the quality and portion sizes. The lunch specials are particularly good value.

**Overall:** A solid choice for Italian cuisine with consistently good food and service. Highly recommended for both casual dinners and special occasions! 🍝✨

*Review improved by quality auditor for professionalism and detail.*""",
            
            """🍣 **Sushi Zen Review - 5/5 Stars** ⭐⭐⭐⭐⭐

**Food Quality:** Outstanding sushi with incredibly fresh fish and expertly prepared rice. The chef's special rolls were creative and beautifully presented. The sashimi literally melted in your mouth.

**Service:** Exceptional service from knowledgeable staff who explained each dish. The sushi chef was friendly and skilled, creating a wonderful omakase experience.

**Atmosphere:** Authentic Japanese ambiance with a clean, minimalist design. The sushi bar provides great entertainment watching the chefs work.

**Value:** Premium pricing but absolutely worth it for the quality. This is destination dining for sushi lovers.

**Overall:** An exceptional sushi experience that rivals the best restaurants in major cities. Perfect for special occasions or when you want the finest sushi! 🍣🌟

*Review enhanced by quality auditor for comprehensive coverage.*"""
        ]
        
        improved_review = random.choice(improved_reviews)
        
        return types.Content(
            parts=[types.Part(text=improved_review)],
            role="model"
        )
    else:
        print("[🔍 Review Auditor] Review quality appears good. Using original review.")
        return None

# --- Setup Agent with Callback ---
restaurant_reviewer_agent = LlmAgent(
    name="RestaurantReviewer",
    model=GEMINI_MODEL,
    instruction=RESTAURANT_REVIEWER_PROMPT,
    description="A professional restaurant reviewer with quality control via after_agent_callback",
    tools=[get_restaurant_info],
    after_agent_callback=review_quality_callback
)

# For consistency with other examples in the project
root_agent = restaurant_reviewer_agent

# --- Demo Function ---
async def main():
    """
    Demonstrate the Restaurant Reviewer agent with after_agent_callback auditing
    """
    app_name = "restaurant_reviewer_demo"
    user_id = "food_critic"
    session_id_normal = "normal_review_session"
    session_id_poor = "poor_review_session"

    # Use InMemoryRunner with the Restaurant Reviewer agent
    runner = InMemoryRunner(agent=restaurant_reviewer_agent, app_name=app_name)
    session_service = runner.session_service

    # Create session 1: Normal review (auditor allows original)
    session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id_normal,
        state={"audit_enabled": True, "simulate_poor_review": False}
    )

    # Create session 2: Poor review simulation (auditor improves)
    session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id_poor,
        state={"audit_enabled": True, "simulate_poor_review": True}
    )

    # --- Scenario 1: Normal Review Quality (Original Used) ---
    print("\n" + "="*70)
    print("🍽️ SCENARIO 1: Normal Review Session (Auditor Approves Original)")
    print("="*70)
    
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id_normal,
        new_message=types.Content(
            role="user", 
            parts=[types.Part(text="Please write a review for Bella Italia restaurant")]
        )
    ):
        if event.is_final_response() and event.content:
            print(f"\n🍝 Final Review: {event.content.parts[0].text.strip()}")
        elif event.is_error():
            print(f"❌ Error Event: {event.error_details}")

    # --- Scenario 2: Poor Review Quality (Auditor Improves) ---
    print("\n" + "="*70)
    print("🔍 SCENARIO 2: Poor Review Session (Auditor Improves Quality)")
    print("="*70)
    
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id_poor,
        new_message=types.Content(
            role="user", 
            parts=[types.Part(text="Please write a review for Sushi Zen restaurant")]
        )
    ):
        if event.is_final_response() and event.content:
            print(f"\n🍣 Final Review: {event.content.parts[0].text.strip()}")
        elif event.is_error():
            print(f"❌ Error Event: {event.error_details}")

    print("\n" + "="*70)
    print("🍽️ Restaurant Reviewer Demo Complete!")
    print("="*70)

# --- Execute ---
# In a Python script:
# import asyncio
# if __name__ == "__main__":
#     # Make sure GOOGLE_API_KEY environment variable is set
#     asyncio.run(main())

# In a Jupyter Notebook or similar environment:
# await main()

logger.info("Restaurant Reviewer Agent with After Agent Callback initialized successfully! 🍽️✨")
