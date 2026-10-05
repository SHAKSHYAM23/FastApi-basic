from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Each attribute is filled from an environment variable of the same name
    # (case-insensitive). The value here is only a fallback if .env lacks it.
    # Pydantic also converts types for you: "5" in .env becomes the float 5.0.
    database_url: str = "sqlite:///./tasks.db"
    wiki_user_agent: str = "FastAPILearningProject/1.0 (your-email@example.com)"
    external_api_timeout: float = 5.0

    model_config = SettingsConfigDict(env_file=".env")


# One shared instance, imported wherever configuration is needed
settings = Settings()

