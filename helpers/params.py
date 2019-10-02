from pydantic import BaseModel


class DestinationHost(BaseModel):
    url: str


class ScanNumber(BaseModel):
    scan_id: str