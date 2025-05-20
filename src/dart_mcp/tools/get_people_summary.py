"""
### 설계 방향 및 원칙
- **핵심 책임**: 기업의 인적 자원 관련 주요 정보(직원 현황, 임원 현황, 보수 정보, 사외이사 정보 등)를 통합적으로 제공합니다.
- **설계 원칙**:
    - SRP(단일 책임 원칙): 인적 자원 요약 정보 제공이라는 단일 책임을 갖습니다.
    - OCP(개방-폐쇄 원칙): 향후 새로운 인적 자원 관련 정보 항목이 추가될 경우 유연하게 확장 가능하도록 합니다.
- **기술적 고려사항**:
    - 비동기 처리: DART API 호출은 `async/await`를 사용하여 비동기적으로 처리합니다.
    - 오류 처리: 각 API 호출의 예외를 적절히 처리하여 안정성을 높입니다.
- **사용 시 고려사항**:
    - `corp_code`, `bsns_year`, `reprt_code`는 필수 인자입니다.
    - 반환되는 딕셔너리의 키는 한글로 명시되어 각 정보를 명확히 구분합니다.
"""

from typing import Any

from dart_mcp.api_clients.dart.people_info import (
    get_company_employees,
    get_company_excutives,
    get_individual_compensation_of_directors_and_auditors,
    get_individual_compensation_of_unregular_executive_officers,
    get_outside_directors_info_and_chages,
    get_top_five_individual_compensation,
)


async def get_people_summary(
    corp_code: str, bsns_year: str, reprt_code: str
) -> dict[str, Any]:
    """
    기업의 주요 인적 자원 관련 정보를 통합하여 조회합니다.

    Args:
        corp_code (str): 공시대상회사의 고유번호(8자리).
        bsns_year (str): 사업연도(4자리).
        reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011).

    Returns:
        dict[str, Any]: 인적 자원 관련 정보들을 담고 있는 딕셔너리.
                        {
                            "직원 현황": ...,
                            "임원 현황": ...,
                            "이사·감사 전체 보수현황": ...,
                            "미등기임원 보수현황": ...,
                            "사외이사 및 그 변동현황": ...,
                            "개인별 보수지급 금액(상위 5명)": ...
                        }
    """
    employees_data = await get_company_employees(
        corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
    )
    executives_data = await get_company_excutives(
        corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
    )
    directors_compensation_data = (
        await get_individual_compensation_of_directors_and_auditors(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        )
    )
    unreg_exec_compensation_data = (
        await get_individual_compensation_of_unregular_executive_officers(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        )
    )
    outside_directors_data = await get_outside_directors_info_and_chages(
        corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
    )
    top_five_compensation_data = await get_top_five_individual_compensation(
        corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
    )

    return {
        "직원 현황": employees_data,
        "임원 현황": executives_data,
        "이사·감사 전체 보수현황": directors_compensation_data,
        "미등기임원 보수현황": unreg_exec_compensation_data,
        "사외이사 및 그 변동현황": outside_directors_data,
        "개인별 보수지급 금액(상위 5명)": top_five_compensation_data,
    }
