from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    GOOGLE_APPLICATION_CREDENTIALS: str | None = Field(
        default=None, env="GOOGLE_APPLICATION_CREDENTIALS")
    GOOGLE_APPLICATION_CREDENTIALS_FILE_PATH: str | None = Field(
        default=None, env="GOOGLE_APPLICATION_CREDENTIALS_FILE_PATH"
    )
    GUEST_SPREADSHEET_ID: str = Field(
        env="GUEST_SPREADSHEET_ID"
    )
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
