from datetime import datetime
from typing import Any

from fastmcp import FastMCP

from dart_mcp.settings.startup import fetch_dart_corp_list
from dart_mcp.tools import (
    find_company_corp_code_by_name,
    get_company_financial_stmt_list,
    get_debt_summary,
    get_financial_stmt,
    get_investment_summary,
    get_people_summary,
    get_stock_summary,
)

mcp = FastMCP(
    "DART:KOREA FINANCIAL INFORMATION",
    instructions="""
    이 서버는 대한민국 기업의 재무제표 데이터를 제공합니다.
    모든 조회 결과는 이해하기 쉬운 말로 설명해주셔야합니다.
    """,
)

fetch_dart_corp_list()


@mcp.tool()
async def get_today() -> str:
    """오늘 날짜를 조회합니다."""
    return datetime.now().strftime("%Y%m%d")


@mcp.tool()
async def find_company_by_name(
    corp_name: str,
    k: int = 10,
) -> list[dict[str, Any]]:
    """
    회사명을 이용하여 기업의 고유 코드를 조회합니다.
    회사를 조회 할 때는, LIKE 문을 사용하므로 이를 고려해서 입력해주세요

    Args:
        corp_name (str): 조회할 회사명
        k (int): 조회할 회사 수. 기본값은 10입니다.

    Returns:
        List[Dict[str, Any]]: 조회된 회사 정보를 유사도 순으로 정렬한 딕셔너리 리스트.
                               각 항목은 회사 정보를 담은 딕셔너리입니다.
                               결과가 없으면 빈 리스트를 반환합니다.
    """
    return await find_company_corp_code_by_name(corp_name, k=k)


@mcp.tool()
async def get_company_financial_statement_list(
    corp_code: str,
    start_date: str,
    end_date: str,
) -> list[dict[str, Any]]:
    """
    특정 기업의 정기 재무 공시 목록을 조회합니다.

    Args:
        corp_code: 조회할 기업의 고유 코드 (공시정보시스템에서 발급된 8자리 문자열).
        start_date: 검색 시작일 (YYYYMMDD 형식).
        end_date: 검색 종료일 (YYYYMMDD 형식). (2024년이라면 2025년 6월까지 조회)

    Returns:
        Tuple[List[Dict[str, Any]], Optional[str]]:
            조회 성공 시 (공시 목록 리스트, None), 실패 시 (빈 리스트, 오류 메시지 문자열).
            공시 목록의 각 항목은 API 응답의 'list' 필드에 있는 딕셔너리 형태입니다.
            (예시: [{'corp_code': '00126380', 'corp_name': '삼성전자', ...}, ...])
    """
    return await get_company_financial_stmt_list(corp_code, start_date, end_date)


@mcp.tool()
async def get_financial_statement(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    fs_div: str,
) -> list[dict[str, Any]]:
    """DART API를 통해 특정 기업의 재무제표를 조회합니다.

    조회 결과는
    (1) 숫자 단위를 1억 2천만원과 알아보기 쉽게 정리해주세요.
    (2) 조회 결과는 항상 상세하게 설명을 해주세요.

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
    return await get_financial_stmt(corp_code, bsns_year, reprt_code, fs_div)


@mcp.tool()
async def get_debt_information_summary_details(
    corp_code: str, bsns_year: str, reprt_code: str
) -> dict[str, Any]:
    """
    기업의 주요 부채 관련 정보 (회사채, 기업어음, 조건부자본증권, 신종자본증권,
    단기사채 미상환 잔액 및 채무증권 발행실적)를 통합하여 조회합니다.

    반환되는 딕셔너리의 각 키는 다음과 같습니다:
    - "회사채 미상환 잔액"
    - "기업어음증권 미상환 잔액"
    - "조건부자본증권 미상환 잔액"
    - "신종자본증권 미상환 잔액"
    - "단기사채 미상환 잔액"
    - "채무증권 발행실적"

    Args:
        corp_code (str): 공시대상회사의 고유번호(8자리).
        bsns_year (str): 사업연도(4자리).
        reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011).

    Returns:
        dict[str, Any]: 부채 관련 정보들을 담고 있는 딕셔너리.
    """
    return await get_debt_summary(corp_code, bsns_year, reprt_code)


@mcp.tool()
async def get_people_information_summary_details(
    corp_code: str, bsns_year: str, reprt_code: str
) -> dict[str, Any]:
    """
    기업의 주요 인적 자원 관련 정보 (직원 현황, 임원 현황, 이사·감사 전체 보수현황,
    미등기임원 보수현황, 사외이사 및 그 변동현황, 개인별 보수지급 금액(상위 5명))를
    통합하여 조회합니다.

    반환되는 딕셔너리의 각 키는 다음과 같습니다:
    - "직원 현황"
    - "임원 현황"
    - "이사·감사 전체 보수현황"
    - "미등기임원 보수현황"
    - "사외이사 및 그 변동현황"
    - "개인별 보수지급 금액(상위 5명)"

    Args:
        corp_code (str): 공시대상회사의 고유번호(8자리).
        bsns_year (str): 사업연도(4자리).
        reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011).

    Returns:
        dict[str, Any]: 인적 자원 관련 정보들을 담고 있는 딕셔너리.
    """
    return await get_people_summary(corp_code, bsns_year, reprt_code)


@mcp.tool()
async def get_stock_information_summary_details(
    corp_code: str, bsns_year: str, reprt_code: str
) -> dict[str, Any]:
    """
    기업의 주요 주식 관련 정보 (최대주주 현황, 최대주주 변동현황, 소액주주 현황,
    배당에 관한 사항, 증자(감자) 현황, 자기주식 취득 및 처분현황)를 통합하여 조회합니다.

    반환되는 딕셔너리의 각 키는 다음과 같습니다:
    - "최대주주 현황"
    - "최대주주 변동현황"
    - "소액주주 현황"
    - "배당에 관한 사항"
    - "증자(감자) 현황"
    - "자기주식 취득 및 처분현황"

    Args:
        corp_code (str): 공시대상회사의 고유번호(8자리).
        bsns_year (str): 사업연도(4자리).
        reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011).

    Returns:
        dict[str, Any]: 주식 관련 정보들을 담고 있는 딕셔너리.
    """
    return await get_stock_summary(corp_code, bsns_year, reprt_code)


@mcp.tool()
async def get_investment_information_summary_details(
    corp_code: str, bsns_year: str, reprt_code: str
) -> dict[str, Any]:
    """
    기업의 주요 투자 관련 정보 (타법인 출자현황, 사모자금 사용내역, 공모자금 사용내역)를
    통합하여 조회합니다.

    반환되는 딕셔너리의 각 키는 다음과 같습니다:
    - "타법인 출자현황"
    - "사모자금 사용내역"
    - "공모자금 사용내역"

    Args:
        corp_code (str): 공시대상회사의 고유번호(8자리).
        bsns_year (str): 사업연도(4자리).
        reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011).

    Returns:
        dict[str, Any]: 투자 관련 정보들을 담고 있는 딕셔너리.
    """
    return await get_investment_summary(corp_code, bsns_year, reprt_code)


if __name__ == "__main__":
    mcp.run(transport="stdio")
