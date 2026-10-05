from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    jwt_secret: str
    frontend_url: str
    frontend_prod_url: str
    port: int
    database_url: str
    jwt_algorithm: str = "HS256"
    jwt_expires_mins: int = 1400 #1 Day
    env: str
    github_client_id: str
    github_client_secret: str
    github_redirect_uri: str

    model_config = SettingsConfigDict(env_file=".env")


envVariables = Settings()