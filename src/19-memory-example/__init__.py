"""
Memory Management Example

Demonstrates ADK's MemoryService for long-term agent memory:
- InMemoryMemoryService for prototyping and testing
- Long-term knowledge retrieval across conversations
- Using the load_memory tool to search past interactions
"""

from .agent import root_agent

__all__ = ["root_agent"]
