from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class Company(BaseModel):
    id: int
    description: Optional[str]
    headquarters: Optional[str]
    homepage: Optional[str]
    logo_path: Optional[str]
    name: Optional[str]
    origin_country: Optional[str]
    parent_company: Optional[Company] = None


Company.update_forward_refs()
