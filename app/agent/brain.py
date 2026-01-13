"""AGUI Reasoning Engine - Intent classification and insight extraction."""

from typing import Literal, Optional
from pydantic import BaseModel


class Intent(BaseModel):
    """Classified user intent."""
    intent_type: Literal["overview", "trend", "comparison", "highlight", "deep_dive"]
    focus_area: Optional[str] = None
    time_scope: Optional[str] = None
    username: Optional[str] = None  # Extracted GitHub username
    

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
    
    def __init__(self, github_connector=None):
        """Initialize reasoning engine.
        
        Args:
            github_connector: Optional GitHub connector for real data
        """
        self.github_connector = github_connector
    
    def classify_intent(self, query: str) -> Intent:
        """Classify user intent from natural language query.
        
        Args:
            query: User's natural language request
            
        Returns:
            Classified intent with extracted username if found
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
        
        # Extract GitHub username from query
        username = None
        words = query.split()
        for i, word in enumerate(words):
            clean_word = word.rstrip("'s").rstrip("'s")
            if clean_word.replace("-", "").replace("_", "").isalnum():
                if i > 0 and words[i-1].lower() in ["for", "of", "user", "@"]:
                    username = clean_word
                    break
                elif word.endswith("'s") or word.endswith("'s"):
                    username = clean_word
                    break
            
        return Intent(
            intent_type=intent_type,
            focus_area=focus_area,
            time_scope="recent",  # Default time scope
            username=username
        )
    
    def extract_insights(self, intent: Intent, username: Optional[str] = None) -> list[Insight]:
        """Extract insights based on intent.
        
        Fetches real GitHub data if connector available, otherwise uses sample data.
        
        Args:
            intent: Classified intent
            username: Optional GitHub username override
            
        Returns:
            List of extracted insights
        """
        insights = []
        
        # Determine which username to use
        target_user = username or intent.username
        
        # Try to fetch real GitHub data
        if self.github_connector and target_user:
            try:
                github_data = self.github_connector.get_user_data(target_user)
                return self._insights_from_github_data(github_data)
            except Exception as e:
                # Fall back to sample data on error
                print(f"GitHub API error, using sample data: {e}")
        
        # Fall back to sample data
        return self._get_sample_insights(intent)
    
    def _insights_from_github_data(self, data) -> list[Insight]:
        """Convert GitHub data to insights.
        
        Args:
            data: GitHubUserData object
            
        Returns:
            List of insights
        """
        insights = []
        
        # Total metrics
        insights.append(Insight(
            insight_type="total",
            title="Total Commits",
            value=data.total_commits,
            context=f"Contributions by @{data.username}"
        ))
        
        insights.append(Insight(
            insight_type="total",
            title="Repositories",
            value=data.repo_count,
            context="Public repositories"
        ))
        
        insights.append(Insight(
            insight_type="total",
            title="Top Language",
            value=data.top_language,
            context="Most used programming language"
        ))
        
        # Trend data
        if data.commit_history:
            insights.append(Insight(
                insight_type="trend",
                title="Commits Over Time",
                value=data.commit_history,
                context="Recent commit activity"
            ))
        
        # Distribution data
        if data.language_distribution:
            insights.append(Insight(
                insight_type="distribution",
                title="Language Distribution",
                value=data.language_distribution,
                context="Code distribution by language"
            ))
        
        # Ranking data
        if data.top_repositories:
            insights.append(Insight(
                insight_type="ranking",
                title="Top Repositories",
                value=data.top_repositories,
                context="Most starred repositories"
            ))
        
        return insights
    
    def _get_sample_insights(self, intent: Intent) -> list[Insight]:
        """Get sample insights as fallback.
        
        Args:
            intent: Classified intent
            
        Returns:
            List of sample insights
        """
        insights = []
        
        # For GitHub-focused queries, extract relevant insights
        if intent.focus_area == "github" or intent.intent_type == "overview":
            # Total metrics
            insights.append(Insight(
                insight_type="total",
                title="Total Commits",
                value=312,
                context="All-time contributions (sample data)"
            ))
            
            insights.append(Insight(
                insight_type="total",
                title="Repositories",
                value=18,
                context="Active repositories (sample data)"
            ))
            
            insights.append(Insight(
                insight_type="total",
                title="Top Language",
                value="Python",
                context="Most used programming language (sample data)"
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
                context="Monthly commit activity (sample data)"
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
                context="Repositories by activity and stars (sample data)"
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
                context="Code distribution by language (sample data)"
            ))
        
        return insights
    
    def reason(self, query: str, username: Optional[str] = None) -> ReasoningResult:
        """Execute complete reasoning pipeline.
        
        Args:
            query: User's natural language request
            username: Optional GitHub username override
            
        Returns:
            Reasoning result with intent and insights
        """
        # Step 1: Classify intent
        intent = self.classify_intent(query)
        
        # Step 2 & 3: Data planning and insight extraction
        insights = self.extract_insights(intent, username)
        
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
        
        username_str = f" for @{intent.username}" if intent.username else ""
        
        if intent.intent_type == "overview":
            return f"Analyzed {intent.focus_area or 'activity'}{username_str} with {total_insights} key metrics"
        elif intent.intent_type == "trend":
            return f"Identified trends in {intent.focus_area or 'activity'}{username_str}"
        elif intent.intent_type == "highlight":
            return f"Highlighted top performers in {intent.focus_area or 'activity'}{username_str}"
        else:
            return f"Analyzed {intent.focus_area or 'data'}{username_str}"
