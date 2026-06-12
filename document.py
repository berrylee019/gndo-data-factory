from pydantic import BaseModel

class NuclearDocument(BaseModel):
    title: str
    source: str
    reactor: str
    document_type: str
    year: int | None = None
    file_path: str
