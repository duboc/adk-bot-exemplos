"""
14 - Before Tool Callback - Weather Service with Permission Checks

This example demonstrates the before_tool_callback functionality using a weather service theme.
The callback implements permission checks and rate limiting before tool execution.
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
from typing import Optional, Dict, Any

# Add parent directory to path for shared imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ADK Imports
from google.adk.agents import LlmAgent
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.base_tool import BaseTool
from google.adk.tools import FunctionTool
from google.adk.runners import InMemoryRunner
from google.genai import types

# Shared imports
from shared.auditor import LLMAuditor, AuditConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the model
GEMINI_MODEL = "gemini-2.0-flash"

# --- Weather Service Tools ---
def get_current_weather(location: str) -> str:
    """
    Get current weather information for a location
    
    Args:
        location: City or location name
        
    Returns:
        Current weather information
    """
    # Simulated weather database
    weather_data = {
        "new york": {
            "temperature": "22°C",
            "condition": "Partly cloudy",
            "humidity": "65%",
            "wind": "15 km/h NW"
        },
        "london": {
            "temperature": "18°C", 
            "condition": "Light rain",
            "humidity": "80%",
            "wind": "12 km/h SW"
        },
        "tokyo": {
            "temperature": "26°C",
            "condition": "Sunny",
            "humidity": "55%",
            "wind": "8 km/h E"
        },
        "sydney": {
            "temperature": "20°C",
            "condition": "Overcast",
            "humidity": "70%",
            "wind": "18 km/h S"
        },
        "paris": {
            "temperature": "19°C",
            "condition": "Clear",
            "humidity": "60%",
            "wind": "10 km/h N"
        }
    }
    
    location_key = location.lower().strip()
    logger.info(f"Getting weather for: {location}")
    
    if location_key in weather_data:
        data = weather_data[location_key]
        result = f"🌤️ Current Weather in {location.title()}:\n"
        result += f"Temperature: {data['temperature']}\n"
        result += f"Condition: {data['condition']}\n"
        result += f"Humidity: {data['humidity']}\n"
        result += f"Wind: {data['wind']}"
        logger.info(f"Weather data found for: {location}")
    else:
        result = f"🌍 Weather data not available for {location}. Please try a major city like New York, London, Tokyo, Sydney, or Paris."
        logger.info(f"No weather data for: {location}")
    
    return result

def get_weather_forecast(location: str, days: int = 3) -> str:
    """
    Get weather forecast for a location
    
    Args:
        location: City or location name
        days: Number of days to forecast (1-7)
        
    Returns:
        Weather forecast information
    """
    # Simulated forecast data
    forecast_templates = {
        "new york": ["Sunny", "Partly cloudy", "Rain", "Cloudy", "Clear", "Thunderstorms", "Overcast"],
        "london": ["Light rain", "Overcast", "Partly cloudy", "Heavy rain", "Clear", "Drizzle", "Foggy"],
        "tokyo": ["Sunny", "Clear", "Partly cloudy", "Rain", "Humid", "Typhoon risk", "Hot"],
        "sydney": ["Overcast", "Sunny", "Windy", "Clear", "Rain", "Partly cloudy", "Warm"],
        "paris": ["Clear", "Cloudy", "Light rain", "Sunny", "Overcast", "Cool", "Mild"]
    }
    
    location_key = location.lower().strip()
    days = min(max(days, 1), 7)  # Limit to 1-7 days
    
    logger.info(f"Getting {days}-day forecast for: {location}")
    
    if location_key in forecast_templates:
        conditions = forecast_templates[location_key][:days]
        result = f"📅 {days}-Day Weather Forecast for {location.title()}:\n"
        for i, condition in enumerate(conditions, 1):
            result += f"Day {i}: {condition}\n"
        logger.info(f"Forecast generated for: {location}")
    else:
        result = f"📅 Forecast not available for {location}. Please try a major city."
        logger.info(f"No forecast data for: {location}")
    
    return result

def get_weather_alerts(location: str) -> str:
    """
    Get weather alerts and warnings for a location
    
    Args:
        location: City or location name
        
    Returns:
        Weather alerts and warnings
    """
    # Simulated alert data
    alert_data = {
        "new york": "⚠️ Heat advisory in effect until 8 PM",
        "london": "🌧️ Flood watch for low-lying areas",
        "tokyo": "🌀 Typhoon watch - monitor conditions",
        "sydney": "🔥 Fire danger rating: High",
        "paris": "❄️ Frost warning for tonight"
    }
    
    location_key = location.lower().strip()
    logger.info(f"Checking weather alerts for: {location}")
    
    if location_key in alert_data:
        result = f"🚨 Weather Alerts for {location.title()}:\n{alert_data[location_key]}"
        logger.warning(f"Weather alert found for: {location}")
    else:
        result = f"✅ No weather alerts for {location.title()}"
        logger.info(f"No alerts for: {location}")
    
    return result

# Create tool instances
weather_tool = FunctionTool(func=get_current_weather)
forecast_tool = FunctionTool(func=get_weather_forecast)
alerts_tool = FunctionTool(func=get_weather_alerts)

# --- Weather Service Prompt ---
WEATHER_SERVICE_PROMPT = """
🌤️ You are Dr. Stormy Forecast, a professional meteorologist and weather service expert!

Your personality:
- Knowledgeable and precise about weather
- Safety-conscious and helpful
- Use weather emojis like 🌤️⛅🌧️❄️🌪️⚡
- Provide clear, actionable weather information
- Always mention safety considerations for severe weather

When providing weather information:
1. Use get_current_weather for current conditions
2. Use get_weather_forecast for future predictions
3. Use get_weather_alerts for safety warnings
4. Explain what the weather means for daily activities
5. Provide safety advice for severe conditions
6. Be precise with measurements and timing

Remember: Weather safety is paramount - always prioritize user safety! 🌟
"""

# --- Global variables for auditor ---
auditor = LLMAuditor(name="WeatherServiceAuditor")

# --- Before Tool Callback with Permission Checks ---
def weather_permission_callback(tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext) -> Optional[Dict]:
    """
    Before tool callback that implements permission checks and rate limiting.
    
    This callback demonstrates how to inspect and potentially block tool execution
    based on permissions, rate limits, and other business rules.
    """
    agent_name = tool_context.agent_name
    tool_name = tool.name
    session_state = tool_context.session_state.to_dict() if tool_context.session_state else {}

    print(f"\n[🔐 Permission Check] Tool '{tool_name}' requested by agent '{agent_name}'")
    print(f"[🔐 Permission Check] Tool args: {args}")
    print(f"[🔐 Permission Check] Session state: {session_state}")

    # Check if tool execution is enabled
    tools_enabled = session_state.get("tools_enabled", True)
    if not tools_enabled:
        print("[🔐 Permission Check] Tools disabled in session state. Blocking tool execution.")
        return {"error": "🚫 Weather tools are currently disabled for this session."}

    # Check user permissions
    user_role = session_state.get("user_role", "basic")
    print(f"[🔐 Permission Check] User role: {user_role}")

    # Permission matrix
    tool_permissions = {
        "get_current_weather": ["basic", "premium", "admin"],
        "get_weather_forecast": ["premium", "admin"],
        "get_weather_alerts": ["basic", "premium", "admin"]
    }

    if tool_name in tool_permissions:
        allowed_roles = tool_permissions[tool_name]
        if user_role not in allowed_roles:
            print(f"[🔐 Permission Check] Access denied. Tool '{tool_name}' requires role: {allowed_roles}")
            return {
                "error": f"🚫 Access denied. Tool '{tool_name}' requires {'/'.join(allowed_roles)} access. Your role: {user_role}"
            }

    # Rate limiting check
    rate_limit_exceeded = session_state.get("rate_limit_exceeded", False)
    if rate_limit_exceeded:
        print("[🔐 Permission Check] Rate limit exceeded. Blocking tool execution.")
        return {
            "error": "⏰ Rate limit exceeded. Please wait before making more weather requests."
        }

    # Location validation for premium features
    if tool_name == "get_weather_forecast" and user_role == "premium":
        location = args.get("location", "").lower()
        restricted_locations = ["classified", "secret", "restricted"]
        if any(restricted in location for restricted in restricted_locations):
            print(f"[🔐 Permission Check] Restricted location detected: {location}")
            return {
                "error": "🚫 Weather data for this location is restricted."
            }

    # Argument modification for basic users
    if tool_name == "get_weather_forecast" and user_role == "basic":
        # Limit forecast days for basic users
        if "days" in args and args["days"] > 3:
            print("[🔐 Permission Check] Limiting forecast days for basic user.")
            args["days"] = 3
            print(f"[🔐 Permission Check] Modified args: {args}")

    # Special handling for blocked locations
    location = args.get("location", "").lower()
    if "block" in location:
        print(f"[🔐 Permission Check] Blocked location keyword detected: {location}")
        return {
            "result": "🚫 This location is blocked by the weather service administrator.",
            "blocked": True
        }

    print(f"[🔐 Permission Check] Permission granted for tool '{tool_name}'. Proceeding with execution.")
    return None  # Allow tool execution with potentially modified args

# --- Setup Agent with Callback ---
weather_service_agent = LlmAgent(
    name="WeatherService",
    model=GEMINI_MODEL,
    instruction=WEATHER_SERVICE_PROMPT,
    description="A professional weather service with permission checks via before_tool_callback",
    tools=[weather_tool, forecast_tool, alerts_tool],
    before_tool_callback=weather_permission_callback
)

# For consistency with other examples in the project
root_agent = weather_service_agent

# --- Demo Function ---
async def main():
    """
    Demonstrate the Weather Service agent with before_tool_callback permission checks
    """
    app_name = "weather_service_demo"
    user_id = "weather_user"
    session_id_basic = "basic_user_session"
    session_id_premium = "premium_user_session"
    session_id_blocked = "blocked_user_session"

    # Use InMemoryRunner with the Weather Service agent
    runner = InMemoryRunner(agent=weather_service_agent, app_name=app_name)
    session_service = runner.session_service

    # Create session 1: Basic user (limited permissions)
    session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id_basic,
        state={"tools_enabled": True, "user_role": "basic"}
    )

    # Create session 2: Premium user (full permissions)
    session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id_premium,
        state={"tools_enabled": True, "user_role": "premium"}
    )

    # Create session 3: Blocked user (tools disabled)
    session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id_blocked,
        state={"tools_enabled": False, "user_role": "basic"}
    )

    # --- Scenario 1: Basic User (Limited Access) ---
    print("\n" + "="*70)
    print("👤 SCENARIO 1: Basic User Session (Limited Tool Access)")
    print("="*70)
    
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id_basic,
        new_message=types.Content(
            role="user", 
            parts=[types.Part(text="Get current weather for New York and 7-day forecast")]
        )
    ):
        if event.is_final_response() and event.content:
            print(f"\n🌤️ Final Response: {event.content.parts[0].text.strip()}")
        elif event.is_error():
            print(f"❌ Error Event: {event.error_details}")

    # --- Scenario 2: Premium User (Full Access) ---
    print("\n" + "="*70)
    print("⭐ SCENARIO 2: Premium User Session (Full Tool Access)")
    print("="*70)
    
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id_premium,
        new_message=types.Content(
            role="user", 
            parts=[types.Part(text="Get weather forecast for Tokyo for 5 days and check alerts")]
        )
    ):
        if event.is_final_response() and event.content:
            print(f"\n🌏 Final Response: {event.content.parts[0].text.strip()}")
        elif event.is_error():
            print(f"❌ Error Event: {event.error_details}")

    # --- Scenario 3: Blocked User (Tools Disabled) ---
    print("\n" + "="*70)
    print("🚫 SCENARIO 3: Blocked User Session (Tools Disabled)")
    print("="*70)
    
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id_blocked,
        new_message=types.Content(
            role="user", 
            parts=[types.Part(text="What's the weather like in London?")]
        )
    ):
        if event.is_final_response() and event.content:
            print(f"\n🚫 Final Response: {event.content.parts[0].text.strip()}")
        elif event.is_error():
            print(f"❌ Error Event: {event.error_details}")

    print("\n" + "="*70)
    print("🌤️ Weather Service Demo Complete!")
    print("="*70)

# --- Execute ---
# In a Python script:
# import asyncio
# if __name__ == "__main__":
#     # Make sure GOOGLE_API_KEY environment variable is set
#     asyncio.run(main())

# In a Jupyter Notebook or similar environment:
# await main()

logger.info("Weather Service Agent with Before Tool Callback initialized successfully! 🌤️✨")
