from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")
    GOOGLE_APPLICATION_CREDENTIALS: str | None = Field(
        default=None, env="GOOGLE_APPLICATION_CREDENTIALS")
    GOOGLE_APPLICATION_CREDENTIALS_FILE_PATH: str | None = Field(
        default=None, env="GOOGLE_APPLICATION_CREDENTIALS_FILE_PATH"
    )
    GUEST_SPREADSHEET_ID: str | None = Field(
        env="GUEST_SPREADSHEET_ID"
    )
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    REPOSITORY_TYPE: str = Field(
        default="sqlite",
        env="REPOSITORY_TYPE",
        description="The type of repository to use. Can be 'sqlite' or 'gsheets'.",
    )
    SQLITE_DATABASE_PATH: str = Field(
        default="sqlite:///./data.db",
        env="SQLITE_DATABASE_PATH",
        description="The path to the SQLite database file.",
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
