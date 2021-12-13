import datetime
import uuid
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Film:
    title: str
    description: str
    creation_date: datetime.datetime
    certificate: str
    file_path: str
    type: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    rating: float = field(default=0.0)
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class Genre:
    name: str
    description: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class Film_Genre:
    Film_Id: uuid.UUID
    Genre_Id: uuid.UUID
    created_at: datetime.datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class Person:
    full_name: str
    birth_date: datetime.datetime
    created_at: datetime.datetime
    updated_at: datetime.datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class Film_Person:
    Film_Id: uuid.UUID
    Person_Id: uuid.UUID
    role: str
    created_at: datetime.datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)
