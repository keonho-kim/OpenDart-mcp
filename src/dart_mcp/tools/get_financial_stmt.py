from typing import Any

from dart_mcp.api_clients.dart.financial_stmt import get_financial_statement


async def get_financial_stmt(
    corp_code: str, bsns_year: str, reprt_code: str, fs_div: str
) -> list[dict[str, Any]]:
    """DART API를 통해 특정 기업의 재무제표를 조회하고, 주요 코드 값을 한글 명칭으로 변환하며, 불필요한 원본 코드 필드를 제거합니다.

    Args:
        corp_code (str): 공시대상회사의 고유번호(8자리).
        bsns_year (str): 사업연도(4자리). 2015년 이후 부터 정보제공.
        reprt_code (str): 보고서 코드 (5자리).
            - 1분기보고서 : "11013"
            - 반기보고서 : "11012"
            - 3분기보고서 : "11014"
            - 사업보고서 : "11011"
        fs_div (str): 개별/연결구분 ("OFS": 재무제표, "CFS": 연결재무제표).
    """
    return await get_financial_statement(
        corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code, fs_div=fs_div
    )
