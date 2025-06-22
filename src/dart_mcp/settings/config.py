from pydantic_settings import BaseSettings, SettingsConfigDict
from dart_mcp.db.sqlite import SQLiteDB

class _Settings(BaseSettings):
    BASE_URL: str = "https://opendart.fss.or.kr/api"
    DART_API_KEY: str
    DB_PATH: str = "sqlite/dart.db"
    COMPANY_LIST_TABLE: str = "dart_corp_list"

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        extra="ignore",
    )


Settings = _Settings()
DB_INSTANCE = SQLiteDB(db_path=Settings.DB_PATH)
