from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "bets"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_DRIVER: str = "postgresql+asyncpg"
    REDIS_STORAGE_HOST: str = "localhost"
    REDIS_STORAGE_PORT: int = 6379
    REDIS_STORAGE_DB: int = 0
    BROKER_URL: str = "amqp://guest:guest@localhost:5672"

    @property
    def db_url(self):
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
