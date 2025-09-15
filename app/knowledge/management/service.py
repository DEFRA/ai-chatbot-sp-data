from app.knowledge.management.models import KnowledgeGroup, KnowledgeGroupNotFound

from app.knowledge.management.repository import AbstractKnowledgeRepository

from logging import getLogger

logger = getLogger(__name__)

async def create_knowledge_group(repository: AbstractKnowledgeRepository, group: KnowledgeGroup) -> None:
    """
    Create a new knowledge entry in the database.
    
    Args:
        repository: The repository instance
        entry: The knowledge entry domain model to create
    """
    logger.info(f"Creating knowledge entry: {group.name}")
  
    await repository.add_knowledge_group(group)

    if group._sources:
        await repository.add_knowledge_sources(group.group_id, group._sources)

    logger.info(f"Knowledge entry created successfully: {group.name}")


async def list_knowledge_groups(repository: AbstractKnowledgeRepository) -> list[KnowledgeGroup]:
    """
    List all knowledge entries in the database.
    
    Args:
        repository: The repository instance
        
    Returns:
        A list of knowledge entries
    """
    entries = await repository.list_knowledge_groups()

    return entries


async def find_knowledge_group(repository: AbstractKnowledgeRepository, group_id: str) -> KnowledgeGroup:
    """
    Find a knowledge entry by its group ID.
    
    Args:
        repository: The repository instance
        group_id: The group ID of the knowledge entry to find
        
    Returns:
        The found knowledge entry
        
    Raises:
        KnowledgeGroupNotFound: If no entry is found with the given group ID
    """
    entry = await repository.get_knowledge_group_by_id(group_id)

    if entry:
        entry._sources = await repository.get_knowledge_sources_by_group_id(entry.group_id)

        return entry
    
    raise KnowledgeGroupNotFound(f"Knowledge entry with group ID '{group_id}' not found")

