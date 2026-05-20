from pydantic import BaseModel
from datetime import datetime
from typing import Any, Optional
from staticfloww import StaticPayload, Section

class MemberDetails(Section):
    member_no: str    

class MyGodSchema(StaticPayload):
    MemberDetails: Optional[MemberDetails] = None

class ErrorDetail(BaseModel):
    code: Optional[str] = None
    message: Optional[str] = None
    details: Optional[str] = None

class ApiResponse(BaseModel):
    Success: bool
    StatusCode: int
    Message: Optional[str] = None
    Data: Optional[Any] = None
    Error: Optional[ErrorDetail] = None
    RequestId: Optional[str] = None
    ResponseTimestamp: datetime
    ProcessingTimeMs: int
