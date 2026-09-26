from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import List, Optional, Union
import json

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

    PROJECT_NAME: str = "SIRA Backend API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "sira_super_secret_jwt_key_abidjan_2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 jours
    DATABASE_URL: str = "postgresql://postgres:47309688Ak%40@db.kmfukfzsdvkjskztrhzb.supabase.co:5432/postgres"

    # Supabase credentials
    SUPABASE_URL: Optional[str] = "https://kmfukfzsdvkjskztrhzb.supabase.co"
    SUPABASE_KEY: Optional[str] = "sb_publishable_I7GyLw2P3TXKhV02-byztg_hgBuhKn_"
    SUPABASE_PROJECT_REF: Optional[str] = "kmfukfzsdvkjskztrhzb"

    # Configuration OTP
    ORANGE_OTP_MOCK: bool = False
    DEFAULT_OTP_CODE: str = "123456"

    # AWS SNS & Pinpoint SMS-Voice Configuration
    AWS_REGION: str = "us-east-1"
    AWS_SNS_TOPIC_ARN: Optional[str] = "arn:aws:sns:us-east-1:868962733015:SIRA:802d6db5-74b7-425e-8d37-98170f78bbb1"
    AWS_SMS_SENDER_ID: Optional[str] = "SIRA"
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_SESSION_TOKEN: Optional[str] = None

    # Orange Developer API CI
    ORANGE_AUTH_HEADER: Optional[str] = "Basic MjB2RlBwbFVxaXlCb2xzbWYwekl2MThGeXpjd3RuRXg6VkRMQ0E0aG5JYjNFWmxtY2VCbmlyclZzSE9nNFdwT0Q0bUM1RWtkVFRyckk="
    ORANGE_CLIENT_ID: Optional[str] = "20vFPplUqiyBolsmf0zIv18FyzcwtnEx"
    ORANGE_CLIENT_SECRET: Optional[str] = "VDLCA4hnIb3EZlmceBnirrVsHOg4WpOD4mC5EkdTTrrI"
    ORANGE_SENDER_ADDRESS: Optional[str] = "tel:+2250000"

    # Twilio SMS Gateway (Alternative)
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    TWILIO_FROM_NUMBER: Optional[str] = None

    CORS_ORIGINS: Union[List[str], str] = ["*"]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            if v.startswith("[") and v.endswith("]"):
                try:
                    return json.loads(v)
                except Exception:
                    pass
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, list):
            return v
        return ["*"]

settings = Settings()

