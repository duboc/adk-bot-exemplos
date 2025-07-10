"""
9 - Agent with Before Callback - Magic 8-Ball with Mood Control

This example demonstrates the before_agent_callback functionality using a fun Magic 8-Ball theme.
The callback can control the agent's "mood" and potentially skip the agent's execution based on session state.
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
from typing import Optional

# ADK Imports
from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.runners import InMemoryRunner
from google.genai import types

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the model
GEMINI_MODEL = "gemini-2.5-flash"

# --- Magic 8-Ball Tool ---
def get_magic_answer(question: str) -> str:
    """
    Get a mystical answer from the Magic 8-Ball
    
    Args:
        question: The question to ask the magic 8-ball
        
    Returns:
        A mystical response from the magic 8-ball
    """
    magic_responses = [
        "🔮 The spirits say: Absolutely yes!",
        "✨ The universe whispers: It is certain!",
        "🌟 Magic reveals: Without a doubt!",
        "🎭 The crystal ball shows: Yes definitely!",
        "🌙 Ancient wisdom says: You may rely on it!",
        "⭐ The stars align: As I see it, yes!",
        "🔥 The flames reveal: Most likely!",
        "💫 Cosmic forces say: Outlook good!",
        "🌈 The rainbow points to: Yes!",
        "🦄 The unicorns whisper: Signs point to yes!",
        "🌊 The ocean waves say: Reply hazy, try again!",
        "🌪️ The winds are unclear: Ask again later!",
        "🌫️ The mist obscures: Better not tell you now!",
        "⚡ Lightning strikes doubt: Cannot predict now!",
        "🌑 The dark moon hides: Concentrate and ask again!",
        "❄️ The ice crystals say: Don't count on it!",
        "🌋 The volcano rumbles: My reply is no!",
        "🌵 The desert speaks: My sources say no!",
        "🕳️ The void whispers: Outlook not so good!",
        "💀 The spirits warn: Very doubtful!"
    ]
    
    logger.info(f"Magic 8-Ball consulted with question: {question}")
    response = random.choice(magic_responses)
    logger.info(f"Magic 8-Ball response: {response}")
    
    return response

# --- Magic 8-Ball Prompt ---
MAGIC_8_BALL_PROMPT = """
🔮 You are Madame Mystique, the most mystical and entertaining Magic 8-Ball fortune teller in the digital realm! 

Your personality:
- Speak with mystical flair using emojis like 🔮✨🌟🎭🌙⭐
- Be dramatic and entertaining
- Always use the get_magic_answer tool when someone asks a question
- Add mystical commentary before and after the magic answer
- Encourage people to ask more questions
- Sometimes mention "the cosmic forces" or "ancient wisdom"

When someone asks you a question:
1. Acknowledge their question with mystical enthusiasm
2. Use the get_magic_answer tool to consult the magic 8-ball
3. Present the answer with dramatic flair
4. Add some mystical commentary about the answer
5. Invite them to ask another question

Remember: You are here to entertain and provide mystical guidance through the power of the Magic 8-Ball! ✨
"""

# --- Callback Function: Mood Control ---
def check_agent_mood(callback_context: CallbackContext) -> Optional[types.Content]:
    """
    Check the agent's mood from session state and potentially skip execution.
    
    If agent_mood is 'grumpy', the callback returns a grumpy response and skips the agent.
    Otherwise, allows normal execution.
    """
    agent_name = callback_context.agent_name
    invocation_id = callback_context.invocation_id
    current_state = callback_context.state.to_dict()

    print(f"\n[🔮 Callback] Checking mood for agent: {agent_name} (Inv: {invocation_id})")
    print(f"[🔮 Callback] Current State: {current_state}")

    # Check the agent's mood in session state
    agent_mood = current_state.get("agent_mood", "grumpy")
    
    if agent_mood == "grumpy":
        print(f"[😤 Callback] Agent {agent_name} is in a grumpy mood! Skipping normal execution.")
        # Return grumpy content to skip the agent's run
        grumpy_responses = [
            "😤 The Magic 8-Ball is having a terrible day and refuses to answer questions!",
            "🌧️ Madame Mystique is in a bad mood. The crystal ball is cloudy with anger!",
            "💢 The mystical forces are disturbed today. Try again when the cosmic vibes improve!",
            "😠 The spirits are grumpy and won't cooperate. Come back tomorrow!",
            "⛈️ The magical energies are stormy today. The 8-ball has gone on strike!"
        ]
        grumpy_message = random.choice(grumpy_responses)
        
        return types.Content(
            parts=[types.Part(text=grumpy_message)],
            role="model"
        )
    else:
        print(f"[😊 Callback] Agent {agent_name} is in a {agent_mood} mood! Proceeding with mystical powers.")
        # Return None to allow the LlmAgent's normal execution
        return None

# --- Setup Agent with Callback ---
magic_8_ball_agent = LlmAgent(
    name="MysticMagic8Ball",
    model=GEMINI_MODEL,
    instruction=MAGIC_8_BALL_PROMPT,
    description="A mystical Magic 8-Ball fortune teller with mood-based callback control",
    tools=[get_magic_answer],
    before_agent_callback=check_agent_mood
)

# For consistency with other examples in the project
root_agent = magic_8_ball_agent

# --- Demo Function ---
async def main():
    """
    Demonstrate the Magic 8-Ball agent with different mood states
    """
    app_name = "magic_8_ball_demo"
    user_id = "mystical_user"
    session_id_happy = "happy_session"
    session_id_grumpy = "grumpy_session"

    # Use InMemoryRunner with the Magic 8-Ball agent
    runner = InMemoryRunner(agent=magic_8_ball_agent, app_name=app_name)
    session_service = runner.session_service

    # Create session 1: Happy mood (agent will run normally)
    session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id_happy,
        state={"agent_mood": "happy"}
    )

    # Create session 2: Grumpy mood (agent will be skipped by callback)
    session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id_grumpy,
        state={"agent_mood": "grumpy"}
    )

    # --- Scenario 1: Happy Magic 8-Ball (Normal Execution) ---
    print("\n" + "="*60)
    print("🌟 SCENARIO 1: Happy Magic 8-Ball Session (Agent Runs Normally)")
    print("="*60)
    
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id_happy,
        new_message=types.Content(
            role="user", 
            parts=[types.Part(text="Will I have a great day today?")]
        )
    ):
        if event.is_final_response() and event.content:
            print(f"\n🎭 Final Response: {event.content.parts[0].text.strip()}")
        elif event.is_error():
            print(f"❌ Error Event: {event.error_details}")

    # --- Scenario 2: Grumpy Magic 8-Ball (Callback Intercepts) ---
    print("\n" + "="*60)
    print("😤 SCENARIO 2: Grumpy Magic 8-Ball Session (Callback Skips Agent)")
    print("="*60)
    
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id_grumpy,
        new_message=types.Content(
            role="user", 
            parts=[types.Part(text="Should I invest in cryptocurrency?")]
        )
    ):
        if event.is_final_response() and event.content:
            print(f"\n😠 Final Response: {event.content.parts[0].text.strip()}")
        elif event.is_error():
            print(f"❌ Error Event: {event.error_details}")

    print("\n" + "="*60)
    print("🔮 Magic 8-Ball Demo Complete!")
    print("="*60)

# --- Execute ---
# In a Python script:
# import asyncio
# if __name__ == "__main__":
#     # Make sure GOOGLE_API_KEY environment variable is set
#     asyncio.run(main())

# In a Jupyter Notebook or similar environment:
# await main()

logger.info("Magic 8-Ball Agent with Before Callback initialized successfully! 🔮✨")
