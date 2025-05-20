from enum import Enum

from dart_mcp.settings.config import Settings

BASE_URL = Settings.BASE_URL
API_KEY = Settings.DART_API_KEY


class urls(Enum):
    """DART API 엔드포인트 URL 템플릿을 정의하는 Enum 클래스입니다."""

    GET_INVESTMENT_IN_SUBSIDIARIES: str = f"{BASE_URL}/otrCprInvstmntSttus.json?crtfc_key={API_KEY}&corp_code={{corp_code}}&bsns_year={{bsns_year}}&reprt_code={{reprt_code}}"

    GET_PUBLIC_OFFERING_FUND_USAGE_DETAILS: str = f"{BASE_URL}/pssrpCptalUseDtls.json?crtfc_key={API_KEY}&corp_code={{corp_code}}&bsns_year={{bsns_year}}&reprt_code={{reprt_code}}"

    GET_PRIVATE_PLACEMENT_FUND_USAGE_DETAILS: str = f"{BASE_URL}/prvsrpCptalUseDtls.json?crtfc_key={API_KEY}&corp_code={{corp_code}}&bsns_year={{bsns_year}}&reprt_code={{reprt_code}}"
