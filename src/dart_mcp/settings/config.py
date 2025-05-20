import os

from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

env_path = find_dotenv(filename='.env', usecwd=True, raise_error_if_not_found=False)

if env_path:
    load_dotenv(dotenv_path=env_path, verbose=True, override=True)



class _Settings(BaseSettings):

    BASE_URL: str = "https://opendart.fss.or.kr/api"
    DART_API_KEY: str = ""  
    
    ELASTIC_HOST:str = ""
    ELASTIC_USERNAME:str = ""
    ELASTIC_PASSWORD:str = ""
    ELASTIC_CA_CERT_PATH:str = ""
    
    model_config = SettingsConfigDict(
        env_file=find_dotenv(filename='.env', usecwd=True, raise_error_if_not_found=True),
        env_file_encoding="utf-8",  
        extra="ignore"  
    )

Settings = _Settings()