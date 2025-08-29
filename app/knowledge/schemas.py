from pydantic import BaseModel, Field
from typing import List

class KnowledgeSource(BaseModel):
    """ Model for a knowledge source. """
    
    type: str = Field(..., description="The type of the knowledge source", min_length=1, max_length=100)
    location: str = Field(..., description="The URL of the knowledge source", min_length=1, max_length=2048)


class KnowledgeEntryRequest(BaseModel):
    """ Request model for creating a knowledge entry. """
    
    title: str = Field(..., description="The title of the knowledge entry", min_length=1, max_length=255)
    description: str = Field(..., description="A description of the knowledge entry", min_length=1)
    owner: str = Field(..., description="The owner of the knowledge entry", min_length=1, max_length=255)
    sources: List[KnowledgeSource] = Field(..., description="List of knowledge sources", min_items=1)


class KnowledgeEntryResponse(BaseModel):
    """ Response model for a knowledge entry. """
    
    id: str = Field(..., description="The unique identifier of the knowledge entry")
    title: str = Field(..., description="The title of the knowledge entry")
    description: str = Field(..., description="A description of the knowledge entry")
    owner: str = Field(..., description="The owner of the knowledge entry")
    created_at: str = Field(..., description="The creation date of the knowledge entry in ISO format")
    updated_at: str = Field(..., description="The last update date of the knowledge entry in ISO format")
    sources: List[KnowledgeSource] = Field(..., description="List of knowledge sources")
