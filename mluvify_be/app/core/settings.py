from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseModel):
    name: str


class Settings(BaseSettings):
    app: 

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        arbitrary_types_allowed=True,
        env_nested_delimiter="__",
    )


settings: Settings = Settings()
