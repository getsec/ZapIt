from pydantic import BaseModel


class DestinationHost(BaseModel):
    url: str


class SpiderStatus(BaseModel):
    scan_id: str