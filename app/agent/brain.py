"""AGUI Reasoning Engine - Intent classification and insight extraction."""

from typing import Literal, Optional
from pydantic import BaseModel


class Intent(BaseModel):
    """Classified user intent."""
    intent_type: Literal["overview", "trend", "comparison", "highlight", "deep_dive"]
    focus_area: Optional[str] = None
    time_scope: Optional[str] = None
    

class Insight(BaseModel):
    """Extracted insight from data analysis."""
    insight_type: Literal["total", "trend", "ranking", "peak", "outlier", "distribution"]
    title: str
    value: int | float | str | list
    context: Optional[str] = None


class ReasoningResult(BaseModel):
    """Result of reasoning pipeline."""
    intent: Intent
    insights: list[Insight]
    summary: str


class AgentBrain:
    """Core reasoning engine for AGUI.
    
    Implements the reasoning pipeline:
    1. Intent Classification
    2. Data Planning
    3. Insight Extraction
    """
    
    def classify_intent(self, query: str) -> Intent:
        """Classify user intent from natural language query.
        
        Args:
            query: User's natural language request
            
        Returns:
            Classified intent
        """
        query_lower = query.lower()
        
        # Intent classification logic
        if any(word in query_lower for word in ["overview", "summary", "dashboard"]):
            intent_type = "overview"
        elif any(word in query_lower for word in ["trend", "over time", "growth", "progress"]):
            intent_type = "trend"
        elif any(word in query_lower for word in ["compare", "vs", "versus", "between"]):
            intent_type = "comparison"
        elif any(word in query_lower for word in ["highlight", "best", "top", "most"]):
            intent_type = "highlight"
        elif any(word in query_lower for word in ["deep dive", "detailed", "analyze", "breakdown"]):
            intent_type = "deep_dive"
        else:
            # Default to overview
            intent_type = "overview"
        
        # Extract focus area
        focus_area = None
        if "github" in query_lower:
            focus_area = "github"
        elif "activity" in query_lower:
            focus_area = "activity"
            
        return Intent(
            intent_type=intent_type,
            focus_area=focus_area,
            time_scope="recent"  # Default time scope
        )
    
    def extract_insights(self, intent: Intent) -> list[Insight]:
        """Extract insights based on intent.
        
        For Phase 1, this uses hardcoded insights for GitHub queries.
        In production, this would fetch real data and analyze it.
        
        Args:
            intent: Classified intent
            
        Returns:
            List of extracted insights
        """
        insights = []
        
        # For GitHub-focused queries, extract relevant insights
        if intent.focus_area == "github" or intent.intent_type == "overview":
            # Total metrics
            insights.append(Insight(
                insight_type="total",
                title="Total Commits",
                value=312,
                context="All-time contributions"
            ))
            
            insights.append(Insight(
                insight_type="total",
                title="Repositories",
                value=18,
                context="Active repositories"
            ))
            
            insights.append(Insight(
                insight_type="total",
                title="Top Language",
                value="Python",
                context="Most used programming language"
            ))
            
            # Trend data
            insights.append(Insight(
                insight_type="trend",
                title="Commits Over Time",
                value=[
                    {"date": "2024-01", "commits": 45},
                    {"date": "2024-02", "commits": 52},
                    {"date": "2024-03", "commits": 38},
                    {"date": "2024-04", "commits": 61},
                    {"date": "2024-05", "commits": 48},
                    {"date": "2024-06", "commits": 68}
                ],
                context="Monthly commit activity"
            ))
            
            # Ranking data
            insights.append(Insight(
                insight_type="ranking",
                title="Top Repositories",
                value=[
                    {"name": "dynQR", "stars": 124, "commits": 87},
                    {"name": "finora-app", "stars": 89, "commits": 56},
                    {"name": "finance_ai", "stars": 67, "commits": 43},
                    {"name": "ag-ui", "stars": 45, "commits": 32},
                    {"name": "portfolio", "stars": 23, "commits": 19}
                ],
                context="Repositories by activity and stars"
            ))
            
            # Distribution data
            insights.append(Insight(
                insight_type="distribution",
                title="Language Distribution",
                value=[
                    {"language": "Python", "percentage": 45},
                    {"language": "TypeScript", "percentage": 30},
                    {"language": "JavaScript", "percentage": 15},
                    {"language": "Dart", "percentage": 10}
                ],
                context="Code distribution by language"
            ))
        
        return insights
    
    def reason(self, query: str) -> ReasoningResult:
        """Execute complete reasoning pipeline.
        
        Args:
            query: User's natural language request
            
        Returns:
            Reasoning result with intent and insights
        """
        # Step 1: Classify intent
        intent = self.classify_intent(query)
        
        # Step 2 & 3: Data planning and insight extraction
        insights = self.extract_insights(intent)
        
        # Generate summary
        summary = self._generate_summary(intent, insights)
        
        return ReasoningResult(
            intent=intent,
            insights=insights,
            summary=summary
        )
    
    def _generate_summary(self, intent: Intent, insights: list[Insight]) -> str:
        """Generate human-readable summary of analysis.
        
        Args:
            intent: Classified intent
            insights: Extracted insights
            
        Returns:
            Summary text
        """
        total_insights = len([i for i in insights if i.insight_type == "total"])
        
        if intent.intent_type == "overview":
            return f"Analyzed {intent.focus_area or 'activity'} with {total_insights} key metrics"
        elif intent.intent_type == "trend":
            return f"Identified trends in {intent.focus_area or 'activity'}"
        elif intent.intent_type == "highlight":
            return f"Highlighted top performers in {intent.focus_area or 'activity'}"
        else:
            return f"Analyzed {intent.focus_area or 'data'}"
