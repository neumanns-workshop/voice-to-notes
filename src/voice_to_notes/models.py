from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ActionItem(BaseModel):
    """A specific actionable item extracted from the transcript."""
    description: str = Field(..., description="The action item description")
    priority: int = Field(1, ge=1, le=5, description="Priority level from 1 (lowest) to 5 (highest)")
    due_date: Optional[datetime] = Field(None, description="Optional due date for the action item")
    blockers: Optional[List[str]] = Field(None, description="Any dependencies or blockers for this action")
    status: str = Field("pending", description="Current status of the action item")

class TranscriptSummary(BaseModel):
    """A summary of the transcript content."""
    key_decisions: List[str] = Field(..., description="Key decisions or commitments made")
    blockers: List[str] = Field(..., description="Current blockers or dependencies")
    opportunities: List[str] = Field(..., description="Potential opportunities or ideas")
    risks: List[str] = Field(..., description="Identified risks or concerns")

class ProcessedTranscript(BaseModel):
    """The complete processed transcript output."""
    summary: TranscriptSummary = Field(..., description="Summary of key decisions and context")
    action_items: List[ActionItem] = Field(..., description="Extracted action items")
    metadata: dict = Field(
        default_factory=lambda: {
            "processed_at": datetime.now().isoformat(),
            "model_used": "ollama",
            "version": "1.0"
        },
        description="Metadata about the processing"
    )

class DailyTodoList(BaseModel):
    date: str
    action_items: List[ActionItem]
    key_decisions: List[str]
    blockers: List[str]
    opportunities: List[str]
    risks: List[str] 