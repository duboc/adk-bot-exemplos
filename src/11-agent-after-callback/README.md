# 11 - After Agent Callback - Restaurant Reviewer with LLM Auditor

This example demonstrates the `after_agent_callback` functionality in Google ADK using a restaurant reviewer theme. The callback uses an LLM auditor to review and potentially improve restaurant reviews for quality control.

## 🍽️ What This Example Shows

This implementation showcases:

- **After Agent Callback**: How to use `after_agent_callback` to review and modify agent responses
- **LLM Auditor Integration**: Using a secondary LLM to audit and improve primary agent responses
- **Quality Control**: Implementing automated quality assurance for agent outputs
- **Session State Control**: Using session state to control auditor behavior
- **Restaurant Review Tool**: Custom tool for restaurant information lookup
- **Professional Character**: Chef Gordon Critique, a passionate restaurant reviewer

## 🎭 How It Works

### The After Agent Callback

The `review_quality_callback()` function:

1. **Runs After Agent Execution**: Called after the restaurant reviewer agent completes its response
2. **Checks Session State**: Looks for `audit_enabled` and `simulate_poor_review` flags
3. **Quality Control Logic**: 
   - If `simulate_poor_review` is `True`: Returns an improved review to replace the original
   - Otherwise: Returns `None` to use the original review

### Two Demo Scenarios

1. **Normal Review Session** (`simulate_poor_review: False`):
   - Agent writes a restaurant review
   - Callback approves the quality and uses original review
   - Demonstrates normal flow with auditor approval

2. **Poor Review Session** (`simulate_poor_review: True`):
   - Agent writes a restaurant review
   - Callback simulates poor quality detection
   - Returns a professionally improved review
   - Demonstrates auditor intervention and improvement

## 🛠️ Key Components

### Restaurant Information Tool
```python
def get_restaurant_info(restaurant_name: str) -> str:
    """Get basic information about a restaurant for review context"""
```
- Simulated restaurant database with cuisine, price range, location, and specialties
- Provides context for more informed reviews

### After Agent Callback
```python
def review_quality_callback(callback_context: CallbackContext) -> Optional[types.Content]:
    """After agent callback that audits restaurant reviews and improves them if needed"""
```
- Checks session state for auditor configuration
- Simulates quality assessment and improvement
- Returns improved content or None based on quality assessment

### LLM Auditor Framework
```python
from shared.auditor import LLMAuditor, AuditConfig
auditor = LLMAuditor(name="RestaurantReviewAuditor")
```
- Uses shared auditor framework for consistency
- Configured with restaurant review quality criteria
- Demonstrates integration pattern for all callback examples

### Agent Setup
```python
restaurant_reviewer_agent = LlmAgent(
    name="RestaurantReviewer",
    model=GEMINI_MODEL,
    instruction=RESTAURANT_REVIEWER_PROMPT,
    tools=[get_restaurant_info],
    after_agent_callback=review_quality_callback  # Key callback assignment
)
```

## 🚀 Running the Example

### Prerequisites
1. Install Google ADK: `pip install google-adk`
2. Set your API key: `export GOOGLE_API_KEY="your-api-key-here"`

### Option 1: Run the Test Script
```bash
cd src/11-agent-after-callback/
python test_demo.py
```

### Option 2: Run in Jupyter/Colab
```python
from agent import main
await main()
```

### Option 3: Import and Use
```python
from src.agent import restaurant_reviewer_agent
# Use the agent in your own code
```

## 📋 Expected Output

### Normal Review Session Output
```
🍽️ SCENARIO 1: Normal Review Session (Auditor Approves Original)
======================================================================

[🔍 Review Auditor] Checking review quality for agent: RestaurantReviewer
[🔍 Review Auditor] Review quality appears good. Using original review.

🍝 Final Review: [Original agent-generated restaurant review with professional tone and details]
```

### Poor Review Session Output
```
🔍 SCENARIO 2: Poor Review Session (Auditor Improves Quality)
======================================================================

[🔍 Review Auditor] Checking review quality for agent: RestaurantReviewer
[🔍 Review Auditor] Simulating poor review quality - replacing with improved version.

🍣 Final Review: 🍣 **Sushi Zen Review - 5/5 Stars** ⭐⭐⭐⭐⭐

**Food Quality:** Outstanding sushi with incredibly fresh fish and expertly prepared rice...

*Review enhanced by quality auditor for comprehensive coverage.*
```

## 🎯 Key Learning Points

1. **Post-Processing Control**: After agent callbacks can modify or replace agent responses
2. **Quality Assurance**: Implement automated quality control using LLM auditors
3. **Conditional Logic**: Use session state to control when auditing occurs
4. **Response Enhancement**: Improve agent outputs while maintaining original intent
5. **Professional Standards**: Ensure consistent quality across all agent responses

## 🔧 Customization Ideas

- **Real LLM Auditor**: Replace simulation with actual LLM-powered quality assessment
- **Multiple Quality Criteria**: Different audit standards for different types of reviews
- **User Feedback Integration**: Learn from user ratings to improve audit criteria
- **A/B Testing**: Compare original vs. audited responses for effectiveness
- **Domain-Specific Auditing**: Adapt for other domains (product reviews, technical documentation, etc.)

## 🍽️ Restaurant Database

The example includes a simulated restaurant database with:
- **Bella Italia**: Italian cuisine, downtown location
- **Sushi Zen**: Japanese cuisine, uptown location  
- **Burger Palace**: American cuisine, mall location
- **Le Petit Bistro**: French cuisine, arts district location

## 📚 Related Documentation

- [Google ADK Agents Documentation](https://google.github.io/adk-docs/agents/)
- [After Agent Callback API](https://google.github.io/adk-docs/agents/callbacks/)
- [LLM Auditor Framework](../shared/auditor.py)

This example demonstrates how `after_agent_callback` can be used to implement sophisticated quality control and response improvement systems! 🍽️✨
