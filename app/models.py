from pydantic import BaseModel
from typing import Optional


class PreviewResponse(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    domain: Optional[str] = None


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
    og_title: Optional[str] = None
    twitter_title: Optional[str] = None
    og_type: Optional[str] = None
    preview: Optional[PreviewResponse] = None


class BatchMetadataRequest(BaseModel):
    urls: list[str]


class BatchMetadataResponse(BaseModel):
    results: list[MetadataResponse]