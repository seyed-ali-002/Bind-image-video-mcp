from pydantic import BaseModel, Field


class ExportRequest(BaseModel):
    asset_ids: list[str] = Field(min_length=1, max_length=100)
