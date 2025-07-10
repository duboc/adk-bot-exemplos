# 10 - Before Agent Callback - Magic 8-Ball Example

This example demonstrates the `before_agent_callback` functionality in Google ADK using a fun Magic 8-Ball theme. The callback can control the agent's behavior and potentially skip the agent's execution based on session state.

## 🔮 What This Example Shows

This implementation showcases:

- **Before Agent Callback**: How to use `before_agent_callback` to intercept agent execution
- **Session State Management**: Using session state to control agent behavior
- **Conditional Agent Execution**: Skipping agent execution based on callback logic
- **InMemoryRunner**: Using the InMemoryRunner for session management
- **Custom Tools**: Creating a simple `get_magic_answer` tool
- **Fun Character**: Madame Mystique, a mystical Magic 8-Ball fortune teller

## 🎭 How It Works

### The Callback Function

The `check_agent_mood()` callback function:

1. **Checks Session State**: Looks for an `agent_mood` value in the session state
2. **Conditional Logic**: 
   - If `agent_mood` is `"grumpy"`: Returns a grumpy response and skips the agent
   - Otherwise: Returns `None` to allow normal agent execution

### Two Demo Scenarios

1. **Happy Session** (`agent_mood: "happy"`):
   - Callback allows normal execution
   - Agent uses the `get_magic_answer` tool
   - Responds with mystical Magic 8-Ball answers

2. **Grumpy Session** (`agent_mood: "grumpy"`):
   - Callback intercepts execution
   - Returns grumpy responses directly
   - Agent's main logic is completely bypassed

## 🛠️ Key Components

### Magic 8-Ball Tool
```python
def get_magic_answer(question: str) -> str:
    """Get a mystical answer from the Magic 8-Ball"""
```
- Returns random mystical responses with emojis
- 20 different possible answers (positive, neutral, negative)

### Callback Function
```python
def check_agent_mood(callback_context: CallbackContext) -> Optional[types.Content]:
    """Check agent mood and potentially skip execution"""
```
- Accesses session state via `callback_context.state.to_dict()`
- Returns `types.Content` to skip agent or `None` to proceed

### Agent Setup
```python
magic_8_ball_agent = LlmAgent(
    name="MysticMagic8Ball",
    model=GEMINI_MODEL,
    instruction=MAGIC_8_BALL_PROMPT,
    tools=[get_magic_answer],
    before_agent_callback=check_agent_mood  # Key callback assignment
)
```

## 🚀 Running the Example

### Prerequisites
1. Install Google ADK: `pip install google-adk`
2. Set your API key: `export GOOGLE_API_KEY="your-api-key-here"`

### Option 1: Run the Test Script
```bash
cd src/10-agent-before-callback/
python test_callback.py
```

### Option 2: Run in Jupyter/Colab
```python
from agent import main
await main()
```

### Option 3: Import and Use
```python
from src.agent import magic_8_ball_agent
# Use the agent in your own code
```

## 📋 Expected Output

### Happy Session Output
```
🌟 SCENARIO 1: Happy Magic 8-Ball Session (Agent Runs Normally)
============================================================

[🔮 Callback] Checking mood for agent: MysticMagic8Ball
[😊 Callback] Agent MysticMagic8Ball is in a happy mood! Proceeding with mystical powers.

🎭 Final Response: ✨ Greetings, seeker of wisdom! 🔮 The cosmic forces have heard your question about having a great day...

*The mystical energies swirl around the crystal ball* 

🌟 Magic reveals: Without a doubt!

The universe has spoken! The stars are perfectly aligned for you today! ⭐ The ancient wisdom suggests that positive energy flows strongly in your direction. 

Would you like to ask the Magic 8-Ball another question? The mystical realm awaits! 🌙✨
```

### Grumpy Session Output
```
😤 SCENARIO 2: Grumpy Magic 8-Ball Session (Callback Skips Agent)
============================================================

[🔮 Callback] Checking mood for agent: MysticMagic8Ball
[😤 Callback] Agent MysticMagic8Ball is in a grumpy mood! Skipping normal execution.

😠 Final Response: 😤 The Magic 8-Ball is having a terrible day and refuses to answer questions!
```

## 🎯 Key Learning Points

1. **Callback Control**: Callbacks can completely override agent behavior
2. **Session State**: Use session state to maintain context across interactions
3. **Conditional Logic**: Implement business rules in callbacks
4. **Error Handling**: Callbacks can prevent problematic agent executions
5. **User Experience**: Callbacks can provide alternative responses when needed

## 🔧 Customization Ideas

- **Different Moods**: Add more mood states (sleepy, excited, confused)
- **Time-based Logic**: Skip agent during certain hours
- **User Permissions**: Check user roles before allowing execution
- **Rate Limiting**: Implement usage limits in callbacks
- **A/B Testing**: Route different users to different agent behaviors

## 📚 Related Documentation

- [Google ADK Agents Documentation](https://google.github.io/adk-docs/agents/)
- [Callback Context API](https://google.github.io/adk-docs/agents/callbacks/)
- [InMemoryRunner Documentation](https://google.github.io/adk-docs/runners/)

This example provides a fun and educational way to understand how `before_agent_callback` can be used to create sophisticated agent control flows! 🔮✨
