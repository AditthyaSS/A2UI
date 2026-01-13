"""A2UI Component Schemas - UI specification language for self-assembling dashboards."""

from pydantic import BaseModel, Field
from typing import Literal, Any, Optional


class KPICard(BaseModel):
    """KPI card component for displaying totals and key metrics."""
    type: Literal["card"] = "card"
    title: str = Field(description="Card title/label")
    value: int | float | str = Field(description="Primary metric value")
    subtitle: Optional[str] = Field(None, description="Secondary text or delta")
    trend: Optional[Literal["up", "down", "neutral"]] = Field(None, description="Trend indicator")


class LineChart(BaseModel):
    """Line chart component for trend visualization."""
    type: Literal["lineChart"] = "lineChart"
    title: str = Field(description="Chart title")
    dataKey: str = Field(description="Key for accessing data")
    data: Optional[list[dict[str, Any]]] = Field(None, description="Chart data points")
    xAxisKey: Optional[str] = Field(None, description="X-axis data key")
    yAxisKey: Optional[str] = Field(None, description="Y-axis data key")


class BarChart(BaseModel):
    """Bar chart component for comparisons."""
    type: Literal["barChart"] = "barChart"
    title: str = Field(description="Chart title")
    dataKey: str = Field(description="Key for accessing data")
    data: Optional[list[dict[str, Any]]] = Field(None, description="Chart data")
    xAxisKey: Optional[str] = Field(None, description="X-axis data key")
    yAxisKey: Optional[str] = Field(None, description="Y-axis data key")


class PieChart(BaseModel):
    """Pie chart component for distribution visualization."""
    type: Literal["pieChart"] = "pieChart"
    title: str = Field(description="Chart title")
    dataKey: str = Field(description="Key for accessing data")
    data: Optional[list[dict[str, Any]]] = Field(None, description="Chart data")
    nameKey: Optional[str] = Field(None, description="Name field key")
    valueKey: Optional[str] = Field(None, description="Value field key")


class TableColumn(BaseModel):
    """Table column definition."""
    header: str = Field(description="Column header")
    key: str = Field(description="Data key for this column")
    width: Optional[str] = Field(None, description="Column width")


class Table(BaseModel):
    """Table component for rankings and detailed data."""
    type: Literal["table"] = "table"
    title: str = Field(description="Table title")
    columns: list[str] | list[TableColumn] = Field(description="Column definitions")
    data: Optional[list[dict[str, Any]]] = Field(None, description="Row data")


class Text(BaseModel):
    """Text component for labels and descriptions."""
    type: Literal["text"] = "text"
    content: str = Field(description="Text content")
    variant: Optional[Literal["heading", "body", "caption"]] = Field("body", description="Text style")


class Divider(BaseModel):
    """Horizontal divider for visual separation."""
    type: Literal["divider"] = "divider"


class Grid(BaseModel):
    """Grid layout container."""
    type: Literal["grid"] = "grid"
    columns: int = Field(description="Number of columns", ge=1, le=12)
    children: list[Any] = Field(description="Child components")


class Section(BaseModel):
    """Section container for grouping related components."""
    type: Literal["section"] = "section"
    title: Optional[str] = Field(None, description="Section title")
    children: list[Any] = Field(description="Child components")


class Dashboard(BaseModel):
    """Root dashboard container."""
    type: Literal["dashboard"] = "dashboard"
    title: str = Field(description="Dashboard title")
    subtitle: Optional[str] = Field(None, description="Dashboard subtitle")
    children: list[Any] = Field(description="Dashboard components")


# Union type for all A2UI components
A2UIComponent = (
    Dashboard |
    Section |
    Grid |
    KPICard |
    LineChart |
    BarChart |
    PieChart |
    Table |
    Text |
    Divider
)
