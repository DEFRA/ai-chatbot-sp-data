from fastapi import APIRouter, Depends, HTTPException, status
from datetime import date
from pymongo.asynchronous.database import AsyncDatabase

import app.knowledge.schemas as knowledge_schemas
import app.knowledge.service as knowledge_service

from app.knowledge.models import KnowledgeEntry
from app.common.mongo import get_db

router = APIRouter(tags=["knowledge"])

@router.post("/knowledge/entries", status_code=status.HTTP_201_CREATED)
async def create_entry(entry: knowledge_schemas.KnowledgeEntryRequest, db: AsyncDatabase = Depends(get_db)):
    """
    Create a new knowledge entry.
    
    Args:
        entry: The knowledge entry request data
        db: Database dependency injection
        
    Returns:
        Success message with the created entry ID
    """

    knowledge_entry = KnowledgeEntry(
        title=entry.title,
        description=entry.description,
        owner=entry.owner,
        created_at=date.today(),
        updated_at=date.today()
    )
    
    await knowledge_service.create_knowledge_entry(db, knowledge_entry)
    

@router.get("/knowledge/entries/{title}", response_model=knowledge_schemas.KnowledgeEntryResponse)
async def get_entry(title: str, db: AsyncDatabase = Depends(get_db)):
    """
    Retrieve a knowledge entry by its title.
    
    Args:
        title: The title of the knowledge entry to retrieve
        db: Database dependency injection
        
    Returns:
        The knowledge entry response data or None if not found
    """

    try:
        return await knowledge_service.find_knowledge_entry(db, title)
    except knowledge_service.KnowledgeEntryNotFound:
        raise HTTPException(status_code=404, detail=f"Knowledge entry with title '{title}' not found")
