from enum import Enum

from dart_mcp.settings.config import Settings

BASE_URL = Settings.BASE_URL
API_KEY = Settings.DART_API_KEY


class urls(Enum):
    """DART API 엔드포인트 URL 템플릿을 정의하는 Enum 클래스입니다."""

    GET_COMPANY_EXCUTIVES: str = f"{BASE_URL}/exctvSttus.json?crtfc_key={API_KEY}&corp_code={{corp_code}}&bsns_year={{bsns_year}}&reprt_code={{reprt_code}}"

    GET_COMPANY_EMPLOYEES: str = f"{BASE_URL}/empSttus.json?crtfc_key={API_KEY}&corp_code={{corp_code}}&bsns_year={{bsns_year}}&reprt_code={{reprt_code}}"

    GET_INDIVIDUAL_COMPENSATION_OF_DIRECTORS_AND_AUDITORS: str = f"{BASE_URL}/hmvAuditAllSttus.json?crtfc_key={API_KEY}&corp_code={{corp_code}}&bsns_year={{bsns_year}}&reprt_code={{reprt_code}}"

    GET_INDIVIDUAL_COMPENSATION_OF_UNREGULAR_EXECUTIVE_OFFICERS: str = f"{BASE_URL}/unrstExctvMendngSttus.json?crtfc_key={API_KEY}&corp_code={{corp_code}}&bsns_year={{bsns_year}}&reprt_code={{reprt_code}}"

    GET_OUTSIDE_DIRECTORS_INFO_AND_CHAGES: str = f"{BASE_URL}/outcmpnyDrctrNdChangeSttus.json?crtfc_key={API_KEY}&corp_code={{corp_code}}&bsns_year={{bsns_year}}&reprt_code={{reprt_code}}"

    GET_TOP_FIVE_INDIVIDUAL_COMPENSATION: str = f"{BASE_URL}/indvdlByPay.json?crtfc_key={API_KEY}&corp_code={{corp_code}}&bsns_year={{bsns_year}}&reprt_code={{reprt_code}}"
