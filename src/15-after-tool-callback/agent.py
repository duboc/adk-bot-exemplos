"""
15 - After Tool Callback - Calculator Service with Result Validation

This example demonstrates the after_tool_callback functionality using a calculator service theme.
The callback validates and enhances calculation results with detailed explanations.
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
import math
from typing import Optional, Dict, Any
from copy import deepcopy

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

# --- Calculator Tools ---
def basic_calculator(expression: str) -> Dict[str, Any]:
    """
    Perform basic arithmetic calculations
    
    Args:
        expression: Mathematical expression to evaluate
        
    Returns:
        Dictionary with calculation result and metadata
    """
    logger.info(f"Calculating expression: {expression}")
    
    try:
        # Simple safety check - only allow basic math operations
        allowed_chars = set("0123456789+-*/()., ")
        if not all(c in allowed_chars for c in expression):
            raise ValueError("Expression contains invalid characters")
        
        # Evaluate the expression
        result = eval(expression)
        
        response = {
            "result": result,
            "expression": expression,
            "type": "basic_arithmetic",
            "status": "success"
        }
        
        logger.info(f"Calculation successful: {expression} = {result}")
        return response
        
    except Exception as e:
        error_response = {
            "result": None,
            "expression": expression,
            "type": "basic_arithmetic",
            "status": "error",
            "error": str(e)
        }
        logger.error(f"Calculation failed: {expression} - {e}")
        return error_response

def scientific_calculator(operation: str, *args) -> Dict[str, Any]:
    """
    Perform scientific calculations
    
    Args:
        operation: Scientific operation (sin, cos, tan, log, sqrt, etc.)
        *args: Arguments for the operation
        
    Returns:
        Dictionary with calculation result and metadata
    """
    logger.info(f"Scientific calculation: {operation} with args {args}")
    
    try:
        operation = operation.lower()
        
        if operation == "sin" and len(args) == 1:
            result = math.sin(math.radians(args[0]))
        elif operation == "cos" and len(args) == 1:
            result = math.cos(math.radians(args[0]))
        elif operation == "tan" and len(args) == 1:
            result = math.tan(math.radians(args[0]))
        elif operation == "log" and len(args) == 1:
            result = math.log10(args[0])
        elif operation == "ln" and len(args) == 1:
            result = math.log(args[0])
        elif operation == "sqrt" and len(args) == 1:
            result = math.sqrt(args[0])
        elif operation == "power" and len(args) == 2:
            result = math.pow(args[0], args[1])
        elif operation == "factorial" and len(args) == 1:
            result = math.factorial(int(args[0]))
        else:
            raise ValueError(f"Unsupported operation: {operation} with {len(args)} arguments")
        
        response = {
            "result": result,
            "operation": operation,
            "arguments": args,
            "type": "scientific",
            "status": "success"
        }
        
        logger.info(f"Scientific calculation successful: {operation}({args}) = {result}")
        return response
        
    except Exception as e:
        error_response = {
            "result": None,
            "operation": operation,
            "arguments": args,
            "type": "scientific",
            "status": "error",
            "error": str(e)
        }
        logger.error(f"Scientific calculation failed: {operation}({args}) - {e}")
        return error_response

def unit_converter(value: float, from_unit: str, to_unit: str) -> Dict[str, Any]:
    """
    Convert between different units
    
    Args:
        value: Value to convert
        from_unit: Source unit
        to_unit: Target unit
        
    Returns:
        Dictionary with conversion result and metadata
    """
    logger.info(f"Converting {value} from {from_unit} to {to_unit}")
    
    # Conversion factors to base units
    length_conversions = {
        "mm": 0.001, "cm": 0.01, "m": 1.0, "km": 1000.0,
        "inch": 0.0254, "ft": 0.3048, "yard": 0.9144, "mile": 1609.34
    }
    
    weight_conversions = {
        "g": 1.0, "kg": 1000.0, "lb": 453.592, "oz": 28.3495
    }
    
    temperature_conversions = {
        "celsius": lambda x: x,
        "fahrenheit": lambda x: (x - 32) * 5/9,
        "kelvin": lambda x: x - 273.15
    }
    
    try:
        from_unit = from_unit.lower()
        to_unit = to_unit.lower()
        
        # Length conversions
        if from_unit in length_conversions and to_unit in length_conversions:
            base_value = value * length_conversions[from_unit]
            result = base_value / length_conversions[to_unit]
            unit_type = "length"
            
        # Weight conversions
        elif from_unit in weight_conversions and to_unit in weight_conversions:
            base_value = value * weight_conversions[from_unit]
            result = base_value / weight_conversions[to_unit]
            unit_type = "weight"
            
        # Temperature conversions (simplified)
        elif from_unit in temperature_conversions and to_unit in temperature_conversions:
            if from_unit == "celsius" and to_unit == "fahrenheit":
                result = (value * 9/5) + 32
            elif from_unit == "fahrenheit" and to_unit == "celsius":
                result = (value - 32) * 5/9
            elif from_unit == "celsius" and to_unit == "kelvin":
                result = value + 273.15
            elif from_unit == "kelvin" and to_unit == "celsius":
                result = value - 273.15
            else:
                result = value  # Same unit
            unit_type = "temperature"
            
        else:
            raise ValueError(f"Unsupported conversion: {from_unit} to {to_unit}")
        
        response = {
            "result": result,
            "original_value": value,
            "from_unit": from_unit,
            "to_unit": to_unit,
            "type": "unit_conversion",
            "unit_type": unit_type,
            "status": "success"
        }
        
        logger.info(f"Conversion successful: {value} {from_unit} = {result} {to_unit}")
        return response
        
    except Exception as e:
        error_response = {
            "result": None,
            "original_value": value,
            "from_unit": from_unit,
            "to_unit": to_unit,
            "type": "unit_conversion",
            "status": "error",
            "error": str(e)
        }
        logger.error(f"Conversion failed: {value} {from_unit} to {to_unit} - {e}")
        return error_response

# Create tool instances
basic_calc_tool = FunctionTool(func=basic_calculator)
scientific_calc_tool = FunctionTool(func=scientific_calculator)
unit_converter_tool = FunctionTool(func=unit_converter)

# --- Calculator Service Prompt ---
CALCULATOR_SERVICE_PROMPT = """
🧮 You are Professor Calculate, a brilliant mathematician and calculation expert!

Your personality:
- Precise and methodical with calculations
- Educational and explanatory
- Use math-related emojis like 🧮📊📈📉🔢➕➖✖️➗
- Always show your work and explain results
- Provide context for what calculations mean

When performing calculations:
1. Use basic_calculator for arithmetic expressions
2. Use scientific_calculator for advanced math functions
3. Use unit_converter for unit conversions
4. Always explain the calculation process
5. Provide context for what the result means
6. Show alternative ways to express the answer when relevant

Remember: Mathematics is about understanding, not just getting answers! 🌟
"""

# --- Global variables for auditor ---
auditor = LLMAuditor(name="CalculatorAuditor")

# --- After Tool Callback with Result Validation ---
def calculation_validator_callback(tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response: Dict) -> Optional[Dict]:
    """
    After tool callback that validates and enhances calculation results.
    
    This callback demonstrates how to inspect and modify tool results
    for improved accuracy and user experience.
    """
    agent_name = tool_context.agent_name
    tool_name = tool.name
    session_state = tool_context.session_state.to_dict() if tool_context.session_state else {}

    print(f"\n[🔍 Calculation Validator] Reviewing result from tool '{tool_name}' in agent '{agent_name}'")
    print(f"[🔍 Calculation Validator] Tool args: {args}")
    print(f"[🔍 Calculation Validator] Original result: {tool_response}")
    print(f"[🔍 Calculation Validator] Session state: {session_state}")

    # Check if validation is enabled
    validation_enabled = session_state.get("validation_enabled", True)
    if not validation_enabled:
        print("[🔍 Calculation Validator] Validation disabled in session state. Using original result.")
        return None

    # Create enhanced response
    enhanced_response = deepcopy(tool_response)
    
    # Check if we should add detailed explanations
    add_explanations = session_state.get("add_explanations", False)
    
    if tool_response.get("status") == "success":
        result = tool_response.get("result")
        
        # Add validation and enhancement based on tool type
        if tool_name == "basic_calculator":
            expression = tool_response.get("expression", "")
            
            # Add step-by-step breakdown for complex expressions
            if any(op in expression for op in ["*", "/", "(", ")"]):
                enhanced_response["step_by_step"] = f"Evaluating: {expression}"
                enhanced_response["explanation"] = "Complex arithmetic expression evaluated following order of operations (PEMDAS)"
            
            # Add alternative representations
            if isinstance(result, float):
                if result.is_integer():
                    enhanced_response["alternative_forms"] = {
                        "integer": int(result),
                        "decimal": result,
                        "fraction": f"{int(result)}/1"
                    }
                else:
                    # Try to represent as a simple fraction
                    from fractions import Fraction
                    try:
                        frac = Fraction(result).limit_denominator(1000)
                        enhanced_response["alternative_forms"] = {
                            "decimal": result,
                            "fraction": str(frac),
                            "percentage": f"{result * 100:.2f}%" if abs(result) <= 1 else None
                        }
                    except:
                        pass
            
            if add_explanations:
                enhanced_response["detailed_explanation"] = f"""
🧮 **Calculation Analysis:**
- Expression: {expression}
- Result: {result}
- Type: Basic arithmetic
- Precision: {len(str(result).split('.')[-1]) if '.' in str(result) else 0} decimal places
- Mathematical validity: ✅ Verified
"""

        elif tool_name == "scientific_calculator":
            operation = tool_response.get("operation", "")
            arguments = tool_response.get("arguments", [])
            
            # Add mathematical context
            context_info = {
                "sin": "Sine function - ratio of opposite to hypotenuse in right triangle",
                "cos": "Cosine function - ratio of adjacent to hypotenuse in right triangle", 
                "tan": "Tangent function - ratio of opposite to adjacent in right triangle",
                "log": "Base-10 logarithm",
                "ln": "Natural logarithm (base e)",
                "sqrt": "Square root function",
                "power": "Exponentiation operation",
                "factorial": "Product of all positive integers up to n"
            }
            
            if operation in context_info:
                enhanced_response["mathematical_context"] = context_info[operation]
            
            # Add precision and range information
            enhanced_response["precision_info"] = {
                "significant_digits": 10,
                "range_valid": True,
                "units": "radians converted from degrees" if operation in ["sin", "cos", "tan"] else "standard"
            }
            
            if add_explanations:
                enhanced_response["detailed_explanation"] = f"""
🔬 **Scientific Calculation Analysis:**
- Operation: {operation}
- Input(s): {arguments}
- Result: {result}
- Context: {context_info.get(operation, 'Advanced mathematical operation')}
- Accuracy: High precision calculation ✅
"""

        elif tool_name == "unit_converter":
            original_value = tool_response.get("original_value")
            from_unit = tool_response.get("from_unit")
            to_unit = tool_response.get("to_unit")
            unit_type = tool_response.get("unit_type")
            
            # Add conversion verification
            enhanced_response["conversion_verification"] = {
                "conversion_factor": result / original_value if original_value != 0 else None,
                "reverse_conversion": original_value,
                "unit_system": "metric" if from_unit in ["mm", "cm", "m", "km", "g", "kg"] else "imperial"
            }
            
            # Add practical context
            practical_context = {
                "length": "Useful for measuring distances, heights, and dimensions",
                "weight": "Useful for cooking, shipping, and scientific measurements", 
                "temperature": "Important for weather, cooking, and scientific applications"
            }
            
            if unit_type in practical_context:
                enhanced_response["practical_context"] = practical_context[unit_type]
            
            if add_explanations:
                enhanced_response["detailed_explanation"] = f"""
🔄 **Unit Conversion Analysis:**
- Original: {original_value} {from_unit}
- Converted: {result} {to_unit}
- Type: {unit_type} conversion
- Accuracy: Verified conversion factors ✅
- Practical use: {practical_context.get(unit_type, 'General measurement')}
"""

        # Add general enhancements
        enhanced_response["validation_status"] = "✅ Result validated and enhanced"
        enhanced_response["enhanced_by"] = "calculation_validator_callback"
        
        print(f"[🔍 Calculation Validator] Enhanced result with additional context and validation.")
        return enhanced_response
    
    elif tool_response.get("status") == "error":
        # Enhance error responses with helpful suggestions
        error_msg = tool_response.get("error", "Unknown error")
        
        enhanced_response["error_help"] = "❌ Calculation failed. Please check your input and try again."
        enhanced_response["suggestions"] = [
            "Verify that all numbers are valid",
            "Check for proper syntax in expressions",
            "Ensure units are supported for conversions",
            "Try breaking complex calculations into smaller steps"
        ]
        
        print(f"[🔍 Calculation Validator] Enhanced error response with helpful suggestions.")
        return enhanced_response
    
    print("[🔍 Calculation Validator] No enhancements needed. Using original result.")
    return None

# --- Setup Agent with Callback ---
calculator_service_agent = LlmAgent(
    name="CalculatorService",
    model=GEMINI_MODEL,
    instruction=CALCULATOR_SERVICE_PROMPT,
    description="A professional calculator service with result validation via after_tool_callback",
    tools=[basic_calc_tool, scientific_calc_tool, unit_converter_tool],
    after_tool_callback=calculation_validator_callback
)

# For consistency with other examples in the project
root_agent = calculator_service_agent

# --- Demo Function ---
async def main():
    """
    Demonstrate the Calculator Service agent with after_tool_callback validation
    """
    app_name = "calculator_service_demo"
    user_id = "math_user"
    session_id_basic = "basic_calculation_session"
    session_id_enhanced = "enhanced_calculation_session"
    session_id_error = "error_handling_session"

    # Use InMemoryRunner with the Calculator Service agent
    runner = InMemoryRunner(agent=calculator_service_agent, app_name=app_name)
    session_service = runner.session_service

    # Create session 1: Basic validation (validator enhances minimally)
    session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id_basic,
        state={"validation_enabled": True, "add_explanations": False}
    )

    # Create session 2: Enhanced validation (validator adds detailed explanations)
    session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id_enhanced,
        state={"validation_enabled": True, "add_explanations": True}
    )

    # Create session 3: Error handling (validator enhances error responses)
    session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id_error,
        state={"validation_enabled": True, "add_explanations": True}
    )

    # --- Scenario 1: Basic Calculation (Minimal Enhancement) ---
    print("\n" + "="*70)
    print("🧮 SCENARIO 1: Basic Calculation Session (Minimal Enhancement)")
    print("="*70)
    
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id_basic,
        new_message=types.Content(
            role="user", 
            parts=[types.Part(text="Calculate 15 * 8 + 32 / 4")]
        )
    ):
        if event.is_final_response() and event.content:
            print(f"\n📊 Final Response: {event.content.parts[0].text.strip()}")
        elif event.is_error():
            print(f"❌ Error Event: {event.error_details}")

    # --- Scenario 2: Enhanced Calculation (Detailed Enhancement) ---
    print("\n" + "="*70)
    print("🔬 SCENARIO 2: Enhanced Calculation Session (Detailed Enhancement)")
    print("="*70)
    
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id_enhanced,
        new_message=types.Content(
            role="user", 
            parts=[types.Part(text="Calculate sin(45) and convert 100 feet to meters")]
        )
    ):
        if event.is_final_response() and event.content:
            print(f"\n🔬 Final Response: {event.content.parts[0].text.strip()}")
        elif event.is_error():
            print(f"❌ Error Event: {event.error_details}")

    # --- Scenario 3: Error Handling (Enhanced Error Response) ---
    print("\n" + "="*70)
    print("❌ SCENARIO 3: Error Handling Session (Enhanced Error Response)")
    print("="*70)
    
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id_error,
        new_message=types.Content(
            role="user", 
            parts=[types.Part(text="Calculate sqrt(-1) and divide by zero")]
        )
    ):
        if event.is_final_response() and event.content:
            print(f"\n⚠️ Final Response: {event.content.parts[0].text.strip()}")
        elif event.is_error():
            print(f"❌ Error Event: {event.error_details}")

    print("\n" + "="*70)
    print("🧮 Calculator Service Demo Complete!")
    print("="*70)

# --- Execute ---
# In a Python script:
# import asyncio
# if __name__ == "__main__":
#     # Make sure GOOGLE_API_KEY environment variable is set
#     asyncio.run(main())

# In a Jupyter Notebook or similar environment:
# await main()

logger.info("Calculator Service Agent with After Tool Callback initialized successfully! 🧮✨")
