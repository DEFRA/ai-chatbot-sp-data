from pymongo.asynchronous.database import AsyncDatabase

from app.knowledge.models import KnowledgeEntry, KnowledgeEntryNotFound
from app.knowledge.repository import MongoKnowledgeRepository
from logging import getLogger

logger = getLogger(__name__)

async def create_knowledge_entry(db: AsyncDatabase, entry: KnowledgeEntry) -> None:
    """
    Create a new knowledge entry in the database.
    
    Args:
        db: The database connection
        knowledge_entry: The knowledge entry domain model to create
    """
    repository = MongoKnowledgeRepository(db)

    logger.info(f"Creating knowledge entry: {entry.title}")

    await repository.add_knowledge_entry(entry)

    logger.info(f"Knowledge entry created successfully: {entry.title}")


async def find_knowledge_entry(db: AsyncDatabase, title: str) -> KnowledgeEntry:
    """
    Find a knowledge entry by its title.
    
    Args:
        db: The database connection
        title: The title of the knowledge entry to find
        
    Returns:
        The found knowledge entry or None if not found
    """
    repository = MongoKnowledgeRepository(db)

    entry = await repository.get_knowledge_entry_by_title(title)

    if entry:
        return entry
    
    raise KnowledgeEntryNotFound(f"Knowledge entry with title '{title}' not found")

