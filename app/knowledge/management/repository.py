from abc import ABC, abstractmethod
from app.knowledge.management.models import (
    KnowledgeSource,
    KnowledgeGroup,
    KnowledgeGroupAlreadyExists
)
from bson.objectid import ObjectId
from bson.datetime_ms import DatetimeMS
from pymongo.asynchronous.database import AsyncDatabase, AsyncCollection
from pymongo.errors import DuplicateKeyError

class AbstractKnowledgeGroupRepository(ABC):
    @abstractmethod
    async def save(self, group: KnowledgeGroup) -> None:
        """Save a knowledge group with all its sources"""
        pass

    @abstractmethod
    async def get_by_id(self, group_id: str) -> KnowledgeGroup | None:
        """Get a complete knowledge group with all its sources loaded"""
        pass

    @abstractmethod
    async def list_all(self) -> list[KnowledgeGroup]:
        """List all knowledge groups with their sources loaded"""
        pass

    @abstractmethod
    async def delete(self, group_id: str) -> None:
        """Delete a knowledge group and all its sources"""
        pass

class AbstractKnowledgeVectorRepository(ABC):
    @abstractmethod
    async def add(self, content: str, embedding: list[float]) -> None:
        """Add a knowledge vector entry"""
        pass


class MongoKnowledgeGroupRepository(AbstractKnowledgeGroupRepository):
    def __init__(self, db: AsyncDatabase):
        self.db: AsyncDatabase = db
        self.knowledge_groups: AsyncCollection = self.db.get_collection("knowledgeGroups")
        self.knowledge_sources: AsyncCollection = self.db.get_collection("knowledgeSources")

    async def save(self, group: KnowledgeGroup) -> None:
        """Save a knowledge group with all its sources"""
        # First, save or update the group document
        entry_data = {
            "groupId": group.group_id,
            "title": group.name,
            "description": group.description,
            "owner": group.owner,
            "createdAt": DatetimeMS(group.created_at),
            "updatedAt": DatetimeMS(group.updated_at)
        }

        try:
            # Use upsert to handle both insert and update
            await self.knowledge_groups.update_one(
                {"groupId": group.group_id},
                {"$set": entry_data},
                upsert=True
            )
        except DuplicateKeyError:
            raise KnowledgeGroupAlreadyExists(f"Knowledge entry with group_id '{group.group_id}' already exists")

        # Get the group document to get the ObjectId
        group_doc = await self.knowledge_groups.find_one({"groupId": group.group_id})
        if not group_doc:
            raise RuntimeError(f"Failed to save knowledge group '{group.group_id}'")

        # Remove existing sources for this group
        await self.knowledge_sources.delete_many({"groupId": group.group_id})

        # Insert all sources from the aggregate
        if group.sources:
            source_documents = []
            for source in group.sources:
                source_data = {
                    "_id": ObjectId(),
                    "groupId": group.group_id,
                    "parent_group_id": group_doc["_id"],
                    "name": source.name,
                    "type": source.type,
                    "location": source.location
                }
                source_documents.append(source_data)
            
            await self.knowledge_sources.insert_many(source_documents)

    async def get_by_id(self, group_id: str) -> KnowledgeGroup | None:
        """Get a complete knowledge group with all its sources loaded"""
        # Get group document
        group_doc = await self.knowledge_groups.find_one({"groupId": group_id})
        if not group_doc:
            return None
        
        # Create group instance
        group = KnowledgeGroup(
            group_id=group_doc["groupId"],
            name=group_doc["title"],
            description=group_doc["description"],
            owner=group_doc["owner"],
            created_at=group_doc["createdAt"],
            updated_at=group_doc["updatedAt"]
        )
        
        # Load and add all sources
        cursor = self.knowledge_sources.find({"groupId": group_id})
        async for source_doc in cursor:
            source = KnowledgeSource(
                name=source_doc["name"],
                type=source_doc["type"],
                location=source_doc["location"]
            )
            group.add_source(source)
        
        return group

    async def list_all(self) -> list[KnowledgeGroup]:
        """List all knowledge groups with their sources loaded"""
        cursor = self.knowledge_groups.find()
        groups = []

        async for group_doc in cursor:
            # Create group instance
            group = KnowledgeGroup(
                group_id=group_doc["groupId"],
                name=group_doc["title"],
                description=group_doc["description"],
                owner=group_doc["owner"],
                created_at=group_doc["createdAt"],
                updated_at=group_doc["updatedAt"]
            )
            
            # Load and add all sources
            source_cursor = self.knowledge_sources.find({"groupId": group.group_id})
            async for source_doc in source_cursor:
                source = KnowledgeSource(
                    name=source_doc["name"],
                    type=source_doc["type"],
                    location=source_doc["location"]
                )
                group.add_source(source)
            
            groups.append(group)

        return groups

    async def delete(self) -> None:
        raise NotImplementedError()

