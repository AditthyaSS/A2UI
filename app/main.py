"""AGUI - FastAPI server with AG-UI event streaming."""

import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import AsyncGenerator, Optional

from app.config import settings
from app.agent.brain import AgentBrain
from app.agent.ui_decider import UIDecider
from app.agent.events import (
    format_event,
    create_loading_event,
    create_message_event,
    create_render_event,
    create_error_event
)

# Try to import GitHub connector
try:
    from app.connectors.github_connector import GitHubConnector
    github_connector = GitHubConnector(
        token=settings.GITHUB_TOKEN,
        cache_ttl=settings.CACHE_TTL
    )
except Exception as e:
    print(f"GitHub connector unavailable: {e}")
    github_connector = None


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Autonomous agentic product intelligence system"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    """Request model for agent queries."""
    query: str
    username: Optional[str] = None  # Optional GitHub username


# Initialize agent components with GitHub connector
brain = AgentBrain(github_connector=github_connector)
ui_decider = UIDecider()


async def agent_stream(query: str, username: Optional[str] = None) -> AsyncGenerator[str, None]:
    """Generate AG-UI event stream for a query.
    
    Pipeline:
    1. Emit loading event
    2. Reason about query (intent + insights)
    3. Decide UI components
    4. Emit message event with summary
    5. Emit render event with A2UI dashboard
    
    Args:
        query: User's natural language query
        username: Optional GitHub username
        
    Yields:
        SSE-formatted AG-UI events
    """
    try:
        # Step 1: Emit loading
        loading_event = create_loading_event("Analyzing your request...")
        yield format_event(loading_event)
        await asyncio.sleep(settings.STREAM_DELAY)
        
        # Step 2: Reasoning
        loading_event = create_loading_event("Extracting insights...")
        yield format_event(loading_event)
        await asyncio.sleep(settings.STREAM_DELAY)
        
        reasoning = brain.reason(query, username)
        
        # Step 3: UI Decision
        loading_event = create_loading_event("Composing dashboard...")
        yield format_event(loading_event)
        await asyncio.sleep(settings.STREAM_DELAY)
        
        dashboard = ui_decider.decide_ui(reasoning)
        
        # Step 4: Emit summary message
        message_event = create_message_event(reasoning.summary)
        yield format_event(message_event)
        await asyncio.sleep(settings.STREAM_DELAY)
        
        # Step 5: Emit dashboard
        render_event = create_render_event(dashboard)
        yield format_event(render_event)
        
    except Exception as e:
        # Handle errors gracefully
        error_event = create_error_event(
            error=str(e),
            code="PROCESSING_ERROR"
        )
        yield format_event(error_event)


@app.post("/agent/stream")
async def stream_agent_response(request: QueryRequest):
    """Stream AG-UI events for a user query.
    
    This is the primary endpoint for AGUI.
    Accepts a natural language query and streams AG-UI events.
    
    Args:
        request: Query request with optional username
        
    Returns:
        Server-Sent Events stream
    """
    return StreamingResponse(
        agent_stream(request.query, request.username),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Disable proxy buffering
        }
    )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": "Autonomous agentic product intelligence system",
        "endpoints": {
            "stream": "POST /agent/stream - Stream AG-UI events",
            "health": "GET /health - Health check"
        },
        "protocol": "AG-UI",
        "specification": "A2UI",
        "github_connected": gh boolean_connector is not None
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=settings.DEBUG)
