"""
Session State Management Example

Demonstrates ADK session state features including:
- Session-scoped state (no prefix)
- User-scoped state (user: prefix)
- App-scoped state (app: prefix)
- Temporary invocation state (temp: prefix)
- State injection in agent instructions using {key} syntax
"""

from .agent import root_agent

__all__ = ["root_agent"]
