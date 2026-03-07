from pydantic import BaseModel
from typing import Optional


class MetadataResponse(BaseModel):
    status: str = "success"
    title: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    favicon: Optional[str] = None
    site_name: Optional[str] = None
    domain: Optional[str] = None
    url: str
    error: Optional[str] = None


class BatchMetadataRequest(BaseModel):
    urls: list[str]


class BatchMetadataResponse(BaseModel):
    results: list[MetadataResponse]