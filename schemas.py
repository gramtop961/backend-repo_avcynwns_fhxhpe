"""
Database Schemas for the portfolio app

Each Pydantic model corresponds to a MongoDB collection (lowercased class name).
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional

class Project(BaseModel):
    """Portfolio projects collection (collection name: "project")"""
    title: str = Field(..., description="Project title")
    slug: str = Field(..., description="URL-friendly unique identifier")
    category: str = Field(..., description="UI/UX, Branding, Web, Motion, etc.")
    tags: List[str] = Field(default_factory=list, description="Keywords/tags")
    short_description: str = Field(..., max_length=180, description="Short teaser text")
    description: str = Field(..., description="Longer case study text")
    images: List[HttpUrl] = Field(default_factory=list, description="Image URLs for the project")
    tools: List[str] = Field(default_factory=list, description="Tools used (Figma, Illustrator, etc.)")
    highlight: bool = Field(False, description="Whether to highlight this project")

class Message(BaseModel):
    """Contact messages collection (collection name: "message")"""
    name: str = Field(..., min_length=2, max_length=80)
    email: str = Field(..., pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    message: str = Field(..., min_length=10, max_length=2000)
    source: Optional[str] = Field(None, description="Where the message was sent from (cta, footer, sticky, etc.)")
