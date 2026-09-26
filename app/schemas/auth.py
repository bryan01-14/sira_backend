from pydantic import BaseModel, Field
from typing import Optional

class OtpRequest(BaseModel):
    phone_number: str = Field(..., example="+2250708091011", description="Numéro de téléphone de l'usager")

class OtpResponse(BaseModel):
    message: str
    phone_number: str
    expires_in_seconds: int = 600
    otp_code: str = Field(..., description="Code OTP généré transmis directement à l'application")
    code: str = Field(..., description="Alias du code OTP pour l'application mobile")
    mock_code: Optional[str] = None

class OtpVerifyRequest(BaseModel):
    phone_number: str = Field(..., example="+2250708091011")
    code: str = Field(..., example="123456")
    full_name: Optional[str] = Field(None, example="Aka Abraham")
    role: Optional[str] = Field("WORKER", example="STUDENT")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    is_new_user: bool
    user: dict
