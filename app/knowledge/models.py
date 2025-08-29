from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)
class KnowledgeSnapshot:
    """ A snapshot of a knowledge entry (ingestion event) at a specific point in time. """

    version: str
    timestamp: str
    raw_data_path: str
    status: str


@dataclass(frozen=True)
class KnowledgeSource:
    """ Represents the source of a knowledge entry. """

    name: str
    type: str
    location: str


class KnowledgeEntry:
    """ Represents a knowledge entry with its metadata and snapshots. """

    def __init__(self, 
                 title: str = None,
                 description: str = None,
                 owner: str = None,
                 created_at: date = None,
                 updated_at: date = None):
        self.title = title
        self.description = description
        self.owner = owner
        self.created_at = created_at
        self.updated_at = updated_at
        self.snapshots: set[KnowledgeSnapshot] = set()


    def __eq__(self, other):
        if not isinstance(other, KnowledgeEntry):
            return False

        return self.title == other.title


    def __hash__(self):
        return hash(self.title)


    def add_snapshot(self, snapshot: KnowledgeSnapshot):
        self.snapshots.add(snapshot)


class KnowledgeEntryAlreadyExists(Exception):
    """ Exception raised when a knowledge entry (duplicate title) already exists. """
    pass


class KnowledgeEntryNotFound(Exception):
    """ Exception raised when a knowledge entry is not found. """
    pass