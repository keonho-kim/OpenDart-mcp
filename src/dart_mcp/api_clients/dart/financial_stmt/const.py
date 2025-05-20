from enum import Enum

from dart_mcp.settings.config import Settings

BASE_URL = Settings.BASE_URL
API_KEY = Settings.DART_API_KEY


class urls(Enum):
    """DART API 엔드포인트 URL 템플릿을 정의하는 Enum 클래스입니다."""

    GET_COMPANY_FINANCIAL_STMT: str = f"{BASE_URL}/fnlttSinglAcntAll.json?crtfc_key={API_KEY}&corp_code={{corp_code}}&bsns_year={{bsns_year}}&reprt_code={{reprt_code}}&fs_div={{fs_div}}"
