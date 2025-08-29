
from app.knowledge.models import KnowledgeEntry, KnowledgeEntryAlreadyExists
from pymongo.asynchronous.database import AsyncDatabase, AsyncCollection
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId

class MongoKnowledgeRepository():
    def __init__(self, db: AsyncDatabase):
        self.db: AsyncDatabase = db
        self.knowledge_entries: AsyncCollection = self.db.get_collection("knowledgeEntries")


    async def add_knowledge_entry(self, entry: KnowledgeEntry) -> None:
        entry_data = {
            "_id": ObjectId(),
            "title": entry.title,
            "description": entry.description,
            "owner": entry.owner,
            "createdAt": entry.created_at.isoformat(),
            "updatedAt": entry.updated_at.isoformat()
        }

        await self.knowledge_entries.update_one({"_id": entry_data["_id"]}, {"$set": entry_data}, upsert=True)


    async def get_knowledge_entry_by_title(self, title: str) -> KnowledgeEntry | None:
        try:
            data = await self.knowledge_entries.find_one({"title": title})
        except DuplicateKeyError:
            raise KnowledgeEntryAlreadyExists(f"Knowledge entry with title '{title}' already exists")
            
        if data:
            return KnowledgeEntry(
                title=data["title"],
                description=data["description"],
                owner=data["owner"],
                created_at=data["createdAt"],
                updated_at=data["updatedAt"]
            )
        
        return None
    
