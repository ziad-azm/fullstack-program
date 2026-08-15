from datetime import datetime
from enum import Enum
from typing import Annotated, Optional

from pydantic import BaseModel, Field, StringConstraints


class TicketStatus(str, Enum):
    open = "open"
    in_progress = "in_progress"
    closed = "closed"


class TicketPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


# Whitespace is stripped before the length checks run, so "   " is rejected as empty.
Title = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=150)]
Description = Annotated[str, StringConstraints(max_length=2000)]


class TicketIn(BaseModel):
    title: Title
    description: Optional[Description] = None
    status: TicketStatus = TicketStatus.open
    priority: TicketPriority = TicketPriority.medium


class TicketUpdate(BaseModel):
    title: Optional[Title] = None
    description: Optional[Description] = None
    status: Optional[TicketStatus] = None
    priority: Optional[TicketPriority] = None


class TicketOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: TicketStatus
    priority: TicketPriority
    created_at: datetime
