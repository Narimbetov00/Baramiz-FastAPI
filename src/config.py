from pydantic_settings import BaseSettings,SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL:str
    JWT_SECRET:str
    JWT_ALGORITHM:str
    REDIS_URL:str
    DOMAIN:str
    PG_HOST:str
    PG_USER:str
    PG_PSW:str
    PG_DB:str

    model_config = SettingsConfigDict(
        env_file = ".env",
        extra = "ignore"
    )
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.DATABASE_URL.startswith("postgresql://"):
            self.DATABASE_URL = self.DATABASE_URL.replace("postgresql://", "postgres://")
                
        if "sslmode=require" not in self.DATABASE_URL:
                self.DATABASE_URL += "?sslmode=require"

Config = Settings()