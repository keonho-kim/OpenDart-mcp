"""
### 설계 방향 및 원칙
- **핵심 책임**: 기업의 주요 투자 활동 관련 정보(타법인 출자, 사모/공모 자금 사용 내역)를 통합적으로 제공합니다.
- **설계 원칙**:
    - SRP(단일 책임 원칙): 투자 요약 정보 제공이라는 단일 책임을 갖습니다.
    - OCP(개방-폐쇄 원칙): 향후 새로운 투자 관련 정보 항목이 추가될 경우, 기존 코드를 수정하기보다는 새로운 항목을 추가하는 방식으로 확장 가능하도록 고려합니다. (예: 딕셔너리 키 추가)
- **기술적 고려사항**:
    - 비동기 처리: DART API 호출은 네트워크 I/O 작업이므로 `async/await`를 사용하여 비동기적으로 처리하여 효율성을 높입니다.
    - 오류 처리: 각 API 호출 시 발생할 수 있는 예외를 적절히 처리하여, 일부 정보 조회에 실패하더라도 가능한 다른 정보는 반환할 수 있도록 고려할 수 있습니다. (현재는 기본 에러 전파)
- **사용 시 고려사항**:
    - `corp_code`, `bsns_year`, `reprt_code`는 필수 인자입니다.
    - 반환되는 딕셔너리의 키 값은 한글로 명시되어 있어, 해당 키를 통해 각 정보를 명확히 구분할 수 있습니다.
"""

from typing import Any

from dart_mcp.api_clients.dart.investment_info import (
    get_investment_in_subsidiaries,
    get_private_placement_fund_usage_details,
    get_public_offering_fund_usage_details,
)


async def get_investment_summary(
    corp_code: str, bsns_year: str, reprt_code: str
) -> dict[str, Any]:
    """
    기업의 주요 투자 관련 정보 (타법인 출자현황, 사모자금 사용내역, 공모자금 사용내역)를
    통합하여 조회합니다.

    Args:
        corp_code (str): 공시대상회사의 고유번호(8자리).
        bsns_year (str): 사업연도(4자리).
        reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011).

    Returns:
        Dict[str, Any]: 투자 관련 정보들을 담고 있는 딕셔너리.
                        조회 실패 시 해당 키의 값은 None 또는 에러 메시지가 될 수 있습니다.
                        (현재는 에러 발생 시 그대로 전파)
                        {
                            "타법인 출자현황": [결과 리스트] or 에러,
                            "사모자금 사용내역": [결과 리스트] or 에러,
                            "공모자금 사용내역": [결과 리스트] or 에러
                        }
    """
    investment_in_subsidiaries_data = await get_investment_in_subsidiaries(
        corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
    )
    private_placement_fund_data = await get_private_placement_fund_usage_details(
        corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
    )
    public_offering_fund_data = await get_public_offering_fund_usage_details(
        corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
    )

    return {
        "타법인 출자현황": investment_in_subsidiaries_data,
        "사모자금 사용내역": private_placement_fund_data,
        "공모자금 사용내역": public_offering_fund_data,
    }
