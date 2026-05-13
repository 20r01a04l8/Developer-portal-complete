from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    app_name: str
    app_version: str
    environment: str

    auth_service_url: str
    project_service_url: str
    task_service_url: str

    jwt_secret_key: str
    jwt_algorithm: str = "HS256"

    log_level: str = "INFO"
    log_format: str = "json"

    cors_origins: str
    api_prefix: str = "/api/v1"

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]


settings = Settings()
