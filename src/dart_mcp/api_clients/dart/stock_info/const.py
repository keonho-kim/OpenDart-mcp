from enum import Enum

from dart_mcp.settings.config import Settings

BASE_URL = Settings.BASE_URL
API_KEY = Settings.DART_API_KEY


class urls(Enum):
    """DART API 엔드포인트 URL 템플릿을 정의하는 Enum 클래스입니다."""

    GET_CAPITAL_INCREASE_OR_DECREASE_STATUS: str = f"{BASE_URL}/irdsSttus.json?crtfc_key={API_KEY}&corp_code={{corp_code}}&bsns_year={{bsns_year}}&reprt_code={{reprt_code}}"

    GET_DIVIDEND_STATUS: str = f"{BASE_URL}/alotMatter.json?crtfc_key={API_KEY}&corp_code={{corp_code}}&bsns_year={{bsns_year}}&reprt_code={{reprt_code}}"

    GET_ACQUISITION_OF_TREASURY_STOCK: str = f"{BASE_URL}/tesstkAcqsDspsSttus.json?crtfc_key={API_KEY}&corp_code={{corp_code}}&bsns_year={{bsns_year}}&reprt_code={{reprt_code}}"

    GET_LARGEST_SHAREHOLDER: str = f"{BASE_URL}/hyslrSttus.json?crtfc_key={API_KEY}&corp_code={{corp_code}}&bsns_year={{bsns_year}}&reprt_code={{reprt_code}}"

    GET_LARGEST_SHAREHOLDER_CHANGES: str = f"{BASE_URL}/hyslrChgSttus.json?crtfc_key={API_KEY}&corp_code={{corp_code}}&bsns_year={{bsns_year}}&reprt_code={{reprt_code}}"

    GET_MINOR_STOCK_STATUS: str = f"{BASE_URL}/mrhlSttus.json?crtfc_key={API_KEY}&corp_code={{corp_code}}&bsns_year={{bsns_year}}&reprt_code={{reprt_code}}"
