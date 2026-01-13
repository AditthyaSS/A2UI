"""AGUI UI Decision Logic - Insight-to-component mapping."""

from typing import Any
from app.agent.brain import Insight, ReasoningResult


class UIDecider:
    """Decides which UI components are needed based on insights.
    
    Maps insight types to UI components:
    - total → KPI cards
    - trend → Line charts
    - ranking → Tables
    - distribution → Pie charts
    - comparison → Bar charts
    """
    
    def decide_ui(self, reasoning: ReasoningResult) -> dict[str, Any]:
        """Transform reasoning result into A2UI dashboard specification.
        
        Args:
            reasoning: Result from reasoning engine
            
        Returns:
            A2UI dashboard specification
        """
        # Initialize dashboard structure
        dashboard: dict[str, Any] = {
            "type": "dashboard",
            "title": self._generate_dashboard_title(reasoning),
            "children": []
        }
        
        # Group insights by type
        totals = [i for i in reasoning.insights if i.insight_type == "total"]
        trends = [i for i in reasoning.insights if i.insight_type == "trend"]
        rankings = [i for i in reasoning.insights if i.insight_type == "ranking"]
        distributions = [i for i in reasoning.insights if i.insight_type == "distribution"]
        
        # Build UI components based on insights
        
        # 1. KPI Cards for totals (if present)
        if totals:
            kpi_grid = self._create_kpi_grid(totals)
            dashboard["children"].append(kpi_grid)
        
        # 2. Trend charts (if present)
        if trends:
            for trend in trends:
                chart = self._create_line_chart(trend)
                dashboard["children"].append(chart)
        
        # 3. Distribution charts (if present)
        if distributions:
            for dist in distributions:
                chart = self._create_pie_chart(dist)
                dashboard["children"].append(chart)
        
        # 4. Ranking tables (if present)
        if rankings:
            for ranking in rankings:
                table = self._create_table(ranking)
                dashboard["children"].append(table)
        
        return dashboard
    
    def _generate_dashboard_title(self, reasoning: ReasoningResult) -> str:
        """Generate appropriate dashboard title based on intent.
        
        Args:
            reasoning: Reasoning result
            
        Returns:
            Dashboard title
        """
        intent = reasoning.intent
        
        if intent.focus_area == "github":
            if intent.intent_type == "overview":
                return "GitHub Activity Overview"
            elif intent.intent_type == "trend":
                return "GitHub Trends"
            elif intent.intent_type == "highlight":
                return "GitHub Highlights"
            else:
                return "GitHub Analytics"
        
        return "Dashboard"
    
    def _create_kpi_grid(self, totals: list[Insight]) -> dict[str, Any]:
        """Create KPI card grid from total insights.
        
        Args:
            totals: List of total-type insights
            
        Returns:
            Grid component with KPI cards
        """
        cards = []
        
        for insight in totals:
            card = {
                "type": "card",
                "title": insight.title,
                "value": insight.value,
                "subtitle": insight.context
            }
            cards.append(card)
        
        return {
            "type": "grid",
            "columns": min(len(cards), 3),  # Max 3 columns
            "children": cards
        }
    
    def _create_line_chart(self, trend: Insight) -> dict[str, Any]:
        """Create line chart from trend insight.
        
        Args:
            trend: Trend-type insight
            
        Returns:
            Line chart component
        """
        return {
            "type": "lineChart",
            "title": trend.title,
            "dataKey": "trend_data",
            "data": trend.value if isinstance(trend.value, list) else [],
            "xAxisKey": "date",
            "yAxisKey": "commits"
        }
    
    def _create_pie_chart(self, distribution: Insight) -> dict[str, Any]:
        """Create pie chart from distribution insight.
        
        Args:
            distribution: Distribution-type insight
            
        Returns:
            Pie chart component
        """
        return {
            "type": "pieChart",
            "title": distribution.title,
            "dataKey": "distribution_data",
            "data": distribution.value if isinstance(distribution.value, list) else [],
            "nameKey": "language",
            "valueKey": "percentage"
        }
    
    def _create_table(self, ranking: Insight) -> dict[str, Any]:
        """Create table from ranking insight.
        
        Args:
            ranking: Ranking-type insight
            
        Returns:
            Table component
        """
        # Extract columns from first data item
        data = ranking.value if isinstance(ranking.value, list) else []
        columns = []
        
        if data and len(data) > 0:
            # Get column names from first item
            first_item = data[0]
            if isinstance(first_item, dict):
                columns = [key.capitalize() for key in first_item.keys()]
        
        return {
            "type": "table",
            "title": ranking.title,
            "columns": columns if columns else ["Name", "Value"],
            "data": data
        }
