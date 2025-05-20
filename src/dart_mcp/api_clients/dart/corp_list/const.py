from enum import Enum

from dart_mcp.settings.config import Settings

BASE_URL = Settings.BASE_URL
API_KEY = Settings.DART_API_KEY


class urls(Enum):
    FETCH_COMPANY_LIST: str = f"{BASE_URL}/corpCode.xml?crtfc_key={API_KEY}"
