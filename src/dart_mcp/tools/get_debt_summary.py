"""
### 설계 방향 및 원칙
- **핵심 책임**: 기업의 주요 부채 관련 정보(각종 채권 미상환 잔액, 채무증권 발행 실적)를 통합적으로 제공합니다.
- **설계 원칙**:
    - SRP(단일 책임 원칙): 부채 요약 정보 제공이라는 단일 책임을 갖습니다.
    - OCP(개방-폐쇄 원칙): 향후 새로운 부채 관련 정보 항목이 추가될 경우, 기존 코드를 수정하기보다는 새로운 항목을 추가하는 방식으로 확장 가능하도록 고려합니다.
- **기술적 고려사항**:
    - 비동기 처리: DART API 호출은 `async/await`를 사용하여 비동기적으로 처리합니다.
    - 오류 처리: 각 API 호출의 예외를 적절히 처리하여 안정성을 높입니다.
- **사용 시 고려사항**:
    - `corp_code`, `bsns_year`, `reprt_code`는 필수 인자입니다.
    - 반환되는 딕셔너리의 키는 한글로 명시되어 각 정보를 명확히 구분합니다.
"""

from typing import Any

from dart_mcp.api_clients.dart.debt_info import (
    get_commercial_paper_outstanding_balance,
    get_contingent_capital_securities_outstanding_balance,
    get_corporate_bonds_outstanding_balance,
    get_debt_securities_issuance_status,
    get_new_capital_securities_outstanding_balance,
    get_short_term_bonds_outstanding_balance,
)


async def get_debt_summary(
    corp_code: str, bsns_year: str, reprt_code: str
) -> dict[str, Any]:
    """
    기업의 주요 부채 관련 정보를 통합하여 조회합니다.

    Args:
        corp_code (str): 공시대상회사의 고유번호(8자리).
        bsns_year (str): 사업연도(4자리).
        reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011).

    Returns:
        Dict[str, Any]: 부채 관련 정보들을 담고 있는 딕셔너리.
                        {
                            "회사채 미상환 잔액": ...,
                            "기업어음증권 미상환 잔액": ...,
                            "조건부자본증권 미상환 잔액": ...,
                            "하이브리드증권 미상환 잔액": ...,
                            "단기사채 미상환 잔액": ...,
                            "채무증권 발행실적": ...
                        }
    """
    corporate_bonds_data = await get_corporate_bonds_outstanding_balance(
        corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
    )
    commercial_paper_data = await get_commercial_paper_outstanding_balance(
        corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
    )
    contingent_capital_data = (
        await get_contingent_capital_securities_outstanding_balance(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        )
    )
    new_capital_securities_data = await get_new_capital_securities_outstanding_balance(
        corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
    )
    short_term_bonds_data = await get_short_term_bonds_outstanding_balance(
        corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
    )
    debt_issuance_data = await get_debt_securities_issuance_status(
        corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
    )

    return {
        "회사채 미상환 잔액": corporate_bonds_data,
        "기업어음증권 미상환 잔액": commercial_paper_data,
        "조건부자본증권 미상환 잔액": contingent_capital_data,
        "신종자본증권 미상환 잔액": new_capital_securities_data,
        "단기사채 미상환 잔액": short_term_bonds_data,
        "채무증권 발행실적": debt_issuance_data,
    }
