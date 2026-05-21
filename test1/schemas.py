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
    success: bool
    statusCode: int
    message: Optional[str] = None
    data: Optional[Any] = None
    error: Optional[ErrorDetail] = None
    requestId: Optional[str] = None
    responseTimestamp: datetime
    processingTimeMs: int
