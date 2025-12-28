from dataclasses import dataclass
from typing import Optional

@dataclass
class Project:
    title: str
    program: str
    year: Optional[str]
    description: Optional[str]
    document_url: str
    source_page: str
