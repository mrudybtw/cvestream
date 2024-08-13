from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId

class CVE(BaseModel):
    id: str = Field(..., alias="_id")
    cve_id: str
    description: str
    published_date: str
    last_modified_date: str
    cvss_score: Optional[float]
    cvss_vector: Optional[str]
    references: List[str]
    vulnerable_configuration: List[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
