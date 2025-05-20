"""
### 설계 방향 및 원칙
- **핵심 책임**: 기업의 주식 관련 주요 정보(최대주주 현황/변동, 소액주주 현황, 배당, 증자/감자, 자기주식 취득/처분)를 통합적으로 제공합니다.
- **설계 원칙**:
    - SRP(단일 책임 원칙): 주식 요약 정보 제공이라는 단일 책임을 갖습니다.
    - OCP(개방-폐쇄 원칙): 향후 새로운 주식 관련 정보 항목이 추가될 경우 유연하게 확장 가능하도록 합니다.
- **기술적 고려사항**:
    - 비동기 처리: DART API 호출은 `async/await`를 사용하여 비동기적으로 처리합니다.
    - 오류 처리: 각 API 호출의 예외를 적절히 처리하여 안정성을 높입니다.
- **사용 시 고려사항**:
    - `corp_code`, `bsns_year`, `reprt_code`는 필수 인자입니다.
    - 반환되는 딕셔너리의 키는 한글로 명시되어 각 정보를 명확히 구분합니다.
"""

from typing import Any

from dart_mcp.api_clients.dart.stock_info import (
    get_acquisition_of_treasury_stock,
    get_capital_increase_or_decrease_status,
    get_dividend_status,
    get_largest_shareholder,
    get_largest_shareholder_changes,
    get_minor_stock_status,
)


async def get_stock_summary(
    corp_code: str, bsns_year: str, reprt_code: str
) -> dict[str, Any]:
    """
    기업의 주요 주식 관련 정보를 통합하여 조회합니다.

    Args:
        corp_code (str): 공시대상회사의 고유번호(8자리).
        bsns_year (str): 사업연도(4자리).
        reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011).

    Returns:
        dict[str, Any]: 주식 관련 정보들을 담고 있는 딕셔너리.
                        {
                            "최대주주 현황": ...,
                            "최대주주 변동현황": ...,
                            "소액주주 현황": ...,
                            "배당에 관한 사항": ...,
                            "증자(감자) 현황": ...,
                            "자기주식 취득 및 처분현황": ...
                        }
    """
    largest_shareholder_data = await get_largest_shareholder(
        corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
    )
    largest_shareholder_changes_data = await get_largest_shareholder_changes(
        corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
    )
    minor_stock_status_data = await get_minor_stock_status(
        corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
    )
    dividend_status_data = await get_dividend_status(
        corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
    )
    capital_change_data = await get_capital_increase_or_decrease_status(
        corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
    )
    treasury_stock_data = await get_acquisition_of_treasury_stock(
        corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
    )

    return {
        "최대주주 현황": largest_shareholder_data,
        "최대주주 변동현황": largest_shareholder_changes_data,
        "소액주주 현황": minor_stock_status_data,
        "배당에 관한 사항": dividend_status_data,
        "증자(감자) 현황": capital_change_data,
        "자기주식 취득 및 처분현황": treasury_stock_data,
    }
