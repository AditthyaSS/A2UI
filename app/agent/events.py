"""AG-UI Event Helpers - Utilities for emitting agent events."""

import json
from typing import Any
from app.schemas.events import (
    AgentMessageEvent,
    AgentLoadingEvent,
    UIRenderEvent,
    UIUpdateEvent,
    AgentErrorEvent,
    AGUIEvent
)


def format_event(event: AGUIEvent) -> str:
    """Format an AG-UI event for Server-Sent Events (SSE) streaming.
    
    Args:
        event: AG-UI event to format
        
    Returns:
        SSE-formatted event string
    """
    event_json = event.model_dump_json()
    return f"data: {event_json}\n\n"


def create_loading_event(message: str = "Processing...") -> AgentLoadingEvent:
    """Create an agent loading event.
    
    Args:
        message: Loading message to display
        
    Returns:
        AgentLoadingEvent instance
    """
    return AgentLoadingEvent(
        payload={"status": "processing", "message": message}
    )


def create_message_event(text: str) -> AgentMessageEvent:
    """Create an agent message event.
    
    Args:
        text: Message text
        
    Returns:
        AgentMessageEvent instance
    """
    return AgentMessageEvent(
        payload={"text": text}
    )


def create_render_event(dashboard: dict[str, Any]) -> UIRenderEvent:
    """Create a UI render event with A2UI dashboard specification.
    
    Args:
        dashboard: A2UI dashboard specification
        
    Returns:
        UIRenderEvent instance
    """
    return UIRenderEvent(payload=dashboard)


def create_update_event(update: dict[str, Any]) -> UIUpdateEvent:
    """Create a UI update event with partial A2UI specification.
    
    Args:
        update: Partial A2UI update specification
        
    Returns:
        UIUpdateEvent instance
    """
    return UIUpdateEvent(payload=update)


def create_error_event(error: str, code: str = "AGENT_ERROR") -> AgentErrorEvent:
    """Create an agent error event.
    
    Args:
        error: Error message
        code: Error code
        
    Returns:
        AgentErrorEvent instance
    """
    return AgentErrorEvent(
        payload={"error": error, "code": code}
    )
