from pydantic_settings import BaseSettings,SettingsConfigDict
from dotenv import load_dotenv
load_dotenv()
class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def DB_URL_ASP(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

settings = Settings()