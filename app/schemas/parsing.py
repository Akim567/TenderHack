from pydantic import BaseModel, Field


class ParseJobRequest(BaseModel):
    source: str = Field(..., description="Data source identifier or URL to parse.")


class ParseJobResponse(BaseModel):
    job_id: str
    status: str = Field(default="queued")
