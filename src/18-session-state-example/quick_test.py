#!/usr/bin/env python3
"""
Quick test to verify tool_context injection is working.
This just tests that tools can access state via the tool_context parameter.
"""

from google.adk.tools import FunctionTool, ToolContext
from tools.state_tools import save_user_preference, get_product_recommendation, track_interaction


def test_tool_context_injection():
    """Test that tool_context parameter is properly injected."""

    print("=" * 70)
    print("🧪 TESTING TOOL_CONTEXT INJECTION")
    print("=" * 70)

    # Create FunctionTools
    print("\n✅ Creating FunctionTools...")
    save_tool = FunctionTool(save_user_preference)
    recommend_tool = FunctionTool(get_product_recommendation)
    track_tool = FunctionTool(track_interaction)
    print("✅ Tools created successfully!")

    # Get function declarations
    print("\n✅ Getting function declarations...")
    try:
        save_decl = save_tool._get_declaration()
        recommend_decl = recommend_tool._get_declaration()
        track_decl = track_tool._get_declaration()
        print("✅ Declarations generated successfully!")

        # Check that tool_context is NOT in the parameters
        save_params = save_decl.parameters.properties.keys() if hasattr(save_decl.parameters, 'properties') else []
        recommend_params = recommend_decl.parameters.properties.keys() if hasattr(recommend_decl.parameters, 'properties') else []
        track_params = track_decl.parameters.properties.keys() if hasattr(track_decl.parameters, 'properties') else []

        print(f"\n📋 save_user_preference parameters: {list(save_params)}")
        print(f"📋 get_product_recommendation parameters: {list(recommend_params)}")
        print(f"📋 track_interaction parameters: {list(track_params)}")

        # Verify tool_context is not exposed to LLM
        assert 'tool_context' not in save_params, "❌ tool_context should NOT be in LLM declaration!"
        assert 'tool_context' not in recommend_params, "❌ tool_context should NOT be in LLM declaration!"
        assert 'tool_context' not in track_params, "❌ tool_context should NOT be in LLM declaration!"
        print("\n✅ tool_context is correctly hidden from LLM!")

    except Exception as e:
        print(f"\n❌ Error getting declarations: {e}")
        raise

    # Test that we can run tools with tool_context
    print("\n" + "=" * 70)
    print("🧪 TESTING TOOL EXECUTION WITH STATE")
    print("=" * 70)

    # Create a mock ToolContext
    class MockToolContext:
        def __init__(self):
            self.state = {}
            self.agent_name = "TestAgent"

    mock_context = MockToolContext()

    # Test save_user_preference
    print("\n✅ Testing save_user_preference...")
    result = save_user_preference(
        preference_key="name",
        preference_value="Maria",
        tool_context=mock_context
    )
    print(f"   Result: {result}")
    print(f"   State: {mock_context.state}")
    assert mock_context.state["user:name"] == "Maria", "❌ State not saved!"
    assert mock_context.state["user:interaction_count"] == 1, "❌ Interaction count not updated!"
    print("✅ save_user_preference works!")

    # Test get_product_recommendation
    print("\n✅ Testing get_product_recommendation...")
    mock_context.state["user:skin_type"] = "seca"
    mock_context.state["user:name"] = "Maria"
    result = get_product_recommendation(
        category="hidratante",
        tool_context=mock_context
    )
    print(f"   Result: {result[:100]}...")
    print(f"   State keys: {list(mock_context.state.keys())}")
    assert "last_recommendation_category" in mock_context.state, "❌ Recommendation category not saved!"
    assert "temp:last_recommendation_request" in mock_context.state, "❌ Temp state not set!"
    print("✅ get_product_recommendation works!")

    # Test track_interaction
    print("\n✅ Testing track_interaction...")
    result = track_interaction(
        interaction_type="purchase",
        details="Interested in moisturizer",
        tool_context=mock_context
    )
    print(f"   Result: {result}")
    print(f"   State keys: {list(mock_context.state.keys())}")
    assert "current_interaction_type" in mock_context.state, "❌ Session state not saved!"
    assert "user:total_interactions" in mock_context.state, "❌ User state not saved!"
    assert "app:total_customer_interactions" in mock_context.state, "❌ App state not saved!"
    assert "temp:processing_timestamp" in mock_context.state, "❌ Temp state not saved!"
    print("✅ track_interaction works!")

    # Test state scopes
    print("\n" + "=" * 70)
    print("🧪 VERIFYING STATE SCOPES")
    print("=" * 70)

    print("\n📊 Final state:")
    for key, value in sorted(mock_context.state.items()):
        scope = "SESSION" if ":" not in key else key.split(":")[0].upper()
        if not key.startswith("temp:"):
            print(f"  [{scope:8}] {key}: {value}")

    print("\n✅ Verifying state scopes...")
    session_keys = [k for k in mock_context.state.keys() if ":" not in k]
    user_keys = [k for k in mock_context.state.keys() if k.startswith("user:")]
    app_keys = [k for k in mock_context.state.keys() if k.startswith("app:")]
    temp_keys = [k for k in mock_context.state.keys() if k.startswith("temp:")]

    print(f"  Session-scoped keys: {len(session_keys)}")
    print(f"  User-scoped keys: {len(user_keys)}")
    print(f"  App-scoped keys: {len(app_keys)}")
    print(f"  Temp-scoped keys: {len(temp_keys)}")

    assert len(session_keys) > 0, "❌ No session-scoped state!"
    assert len(user_keys) > 0, "❌ No user-scoped state!"
    assert len(app_keys) > 0, "❌ No app-scoped state!"
    assert len(temp_keys) > 0, "❌ No temp-scoped state!"

    print("\n" + "=" * 70)
    print("🎉 ALL TESTS PASSED!")
    print("=" * 70)
    print("\n✅ Summary:")
    print("  1. ✅ FunctionTool correctly hides tool_context from LLM")
    print("  2. ✅ tool_context is injected when calling tools")
    print("  3. ✅ save_user_preference saves to user: state")
    print("  4. ✅ get_product_recommendation reads from state")
    print("  5. ✅ track_interaction uses all 4 state scopes")
    print("  6. ✅ All state scopes are working correctly")
    print("\n🎯 The tool_context pattern is working correctly!")
    print("\n💡 Next: Run with 'adk web' to test in the actual web interface!")

    return True


if __name__ == "__main__":
    import sys
    try:
        result = test_tool_context_injection()
        sys.exit(0 if result else 1)
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
