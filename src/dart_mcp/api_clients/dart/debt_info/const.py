from enum import Enum

from dart_mcp.settings.config import Settings

BASE_URL = Settings.BASE_URL
API_KEY = Settings.DART_API_KEY


class urls(Enum):
    """DART API 엔드포인트 URL 템플릿을 정의하는 Enum 클래스입니다."""

    GET_DEBT_SECURITIES_ISSUANCE_STATUS: str = f"{BASE_URL}/detScritsIsuAcmslt.json?crtfc_key={API_KEY}&corp_code={{corp_code}}&bsns_year={{bsns_year}}&reprt_code={{reprt_code}}"

    GET_COMMERCIAL_PAPER_OUTSTANDING_BALANCE: str = f"{BASE_URL}/entrprsBilScritsNrdmpBlce.json?crtfc_key={API_KEY}&corp_code={{corp_code}}&bsns_year={{bsns_year}}&reprt_code={{reprt_code}}"

    GET_SHORT_TERM_BONDS_OUTSTANDING_BALANCE: str = f"{BASE_URL}/srtpdPsndbtNrdmpBlce.json?crtfc_key={API_KEY}&corp_code={{corp_code}}&bsns_year={{bsns_year}}&reprt_code={{reprt_code}}"

    GET_CORPORATE_BONDS_OUTSTANDING_BALANCE: str = f"{BASE_URL}/cprndNrdmpBlce.json?crtfc_key={API_KEY}&corp_code={{corp_code}}&bsns_year={{bsns_year}}&reprt_code={{reprt_code}}"

    GET_HYBRID_SECURITIES_OUTSTANDING_BALANCE: str = f"{BASE_URL}/newCaplScritsNrdmpBlce.json?crtfc_key={API_KEY}&corp_code={{corp_code}}&bsns_year={{bsns_year}}&reprt_code={{reprt_code}}"

    GET_CONTINGENT_CAPITAL_SECURITIES_OUTSTANDING_BALANCE: str = f"{BASE_URL}/cndlCaplScritsNrdmpBlce.json?crtfc_key={API_KEY}&corp_code={{corp_code}}&bsns_year={{bsns_year}}&reprt_code={{reprt_code}}"
