"""AG-UI Event Schemas - Protocol specification for agent communication."""

from pydantic import BaseModel, Field
from typing import Literal, Any, Optional
from enum import Enum


class EventType(str, Enum):
    """AG-UI event types."""
    AGENT_MESSAGE = "agent.message"
    AGENT_LOADING = "agent.loading"
    UI_RENDER = "ui.render"
    UI_UPDATE = "ui.update"
    AGENT_ERROR = "agent.error"


class AgentMessageEvent(BaseModel):
    """Agent explanation or summary message."""
    type: Literal["agent.message"] = "agent.message"
    payload: dict[str, Any] = Field(
        description="Message content",
        examples=[{"text": "Analyzing GitHub activity..."}]
    )


class AgentLoadingEvent(BaseModel):
    """Agent processing state indicator."""
    type: Literal["agent.loading"] = "agent.loading"
    payload: dict[str, Any] = Field(
        description="Loading state information",
        examples=[{"status": "processing", "message": "Fetching data..."}]
    )


class UIRenderEvent(BaseModel):
    """Full dashboard render event."""
    type: Literal["ui.render"] = "ui.render"
    payload: dict[str, Any] = Field(
        description="Complete A2UI dashboard specification"
    )


class UIUpdateEvent(BaseModel):
    """Partial UI update event."""
    type: Literal["ui.update"] = "ui.update"
    payload: dict[str, Any] = Field(
        description="Partial A2UI update specification"
    )


class AgentErrorEvent(BaseModel):
    """Error reporting event."""
    type: Literal["agent.error"] = "agent.error"
    payload: dict[str, Any] = Field(
        description="Error details",
        examples=[{"error": "Data source unavailable", "code": "DATA_ERROR"}]
    )


# Union type for all events
AGUIEvent = (
    AgentMessageEvent |
    AgentLoadingEvent |
    UIRenderEvent |
    UIUpdateEvent |
    AgentErrorEvent
)
