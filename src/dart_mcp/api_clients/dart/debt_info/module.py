# 설계 방향 및 원칙:
# - 핵심 책임: DART API의 채무 관련 엔드포인트들을 호출하고, 기본적인 응답 처리를 수행합니다.
# - 설계 원칙: SRP (단일 책임 원칙) - 각 함수는 하나의 API 엔드포인트 호출을 책임집니다.
#             OCP (개방-폐쇄 원칙) - 새로운 API 엔드포인트 추가 시 기존 함수 수정 없이 새 함수를 추가할 수 있습니다.
#             DRY (Don't Repeat Yourself) - 공통 API 호출 로직은 base 모듈의 템플릿 함수를 사용합니다.
# - 기술적 고려사항: 비동기 처리를 위해 httpx.AsyncClient를 사용 (실제 사용은 base 모듈에서).
#                 로깅을 통해 API 호출 및 응답 상태를 기록합니다.
#                 타입 힌트를 사용하여 코드의 명확성을 높입니다 (Python 3.9+ 스타일 사용).
# - 사용 시 고려사항: 각 함수의 반환값은 현재 DART API의 'list' 필드를 그대로 반환하며, 추가적인 데이터 가공이 필요할 수 있습니다. ('반환값 작업 필요' 주석 참고)
#                 API 호출 실패 또는 데이터 부재 시 빈 리스트를 반환합니다.

import logging
from typing import Any

from dart_mcp.api_clients.base.dart import _call_regular_report_api_template

from .const import urls
from .mapping import CorpClassMapping

logger = logging.getLogger(__name__)


async def get_debt_securities_issuance_status(
    corp_code: str, bsns_year: str, reprt_code: str
) -> list[dict[str, Any]]:
    """채무증권 발행실적 API (detScritsIsuAcmslt)를 호출합니다.

    Args:
        corp_code (str): 공시대상회사의 고유번호(8자리).
        bsns_year (str): 사업연도(4자리).
        reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011).

    Returns:
        list[dict[str, Any]]: 채무증권 발행실적 정보 리스트.
            각 딕셔너리는 다음 키를 포함합니다:
            - corp_name (str): 회사명
            - isu_cmpny (str): 발행회사
            - scrits_knd_nm (str): 증권종류
            - isu_mth_nm (str): 발행방법
            - isu_de (str): 발행일자 (YYYYMMDD)
            - facvalu_totamt (str): 권면(전자등록)총액
            - intrt (str): 이자율
            - evl_grad_instt (str): 평가등급(평가기관)
            - mtd (str): 만기일 (YYYYMMDD)
            - repy_at (str): 상환여부
            - mngt_cmpny (str): 주관회사
            - stlm_dt (str): 결산기준일 (YYYY-MM-DD)
            - corp_cls_nm (str): 법인구분명 (매핑된 한글명)
    """
    raw_list = await _call_regular_report_api_template(
        final_url=urls.GET_DEBT_SECURITIES_ISSUANCE_STATUS.value.format(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        ),
        api_name_for_logging="get_debt_securities_issuance_status",
        corp_code_for_logging=corp_code,
    )

    processed_list = []
    keys_to_remove = ["rcept_no", "corp_code", "corp_cls"]
    if raw_list:
        for item in raw_list:
            item["corp_cls_nm"] = CorpClassMapping.get_korean_name(item.get("corp_cls"))
            for key_to_remove in keys_to_remove:
                item.pop(key_to_remove, None)
            processed_list.append(item)
    return processed_list


async def get_commercial_paper_outstanding_balance(
    corp_code: str, bsns_year: str, reprt_code: str
) -> list[dict[str, Any]]:
    """기업어음증권 미상환 잔액 API (entrprsBilScritsNrdmpBlce)를 호출합니다.

    Args:
        corp_code (str): 공시대상회사의 고유번호(8자리).
        bsns_year (str): 사업연도(4자리).
        reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011).

    Returns:
        list[dict[str, Any]]: 기업어음증권 미상환 잔액 정보 리스트.
            각 딕셔너리는 다음 키를 포함합니다:
            - corp_name (str): 회사명
            - remndr_exprtn1 (str): 잔여만기
            - remndr_exprtn2 (str): 잔여만기
            - de10_below (str): 10일 이하 금액
            - de10_excess_de30_below (str): 10일초과 30일이하 금액
            - de30_excess_de90_below (str): 30일초과 90일이하 금액
            - de90_excess_de180_below (str): 90일초과 180일이하 금액
            - de180_excess_yy1_below (str): 180일초과 1년이하 금액
            - yy1_excess_yy2_below (str): 1년초과 2년이하 금액
            - yy2_excess_yy3_below (str): 2년초과 3년이하 금액
            - yy3_excess (str): 3년 초과 금액
            - sm (str): 합계 금액
            - stlm_dt (str): 결산기준일 (YYYY-MM-DD)
            - corp_cls_nm (str): 법인구분명 (매핑된 한글명)
    """
    raw_list = await _call_regular_report_api_template(
        final_url=urls.GET_COMMERCIAL_PAPER_OUTSTANDING_BALANCE.value.format(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        ),
        api_name_for_logging="get_commercial_paper_outstanding_balance",
        corp_code_for_logging=corp_code,
    )

    processed_list = []
    keys_to_remove = ["rcept_no", "corp_code", "corp_cls"]
    if raw_list:
        for item in raw_list:
            item["corp_cls_nm"] = CorpClassMapping.get_korean_name(item.get("corp_cls"))
            for key_to_remove in keys_to_remove:
                item.pop(key_to_remove, None)
            processed_list.append(item)
    return processed_list


async def get_short_term_bonds_outstanding_balance(
    corp_code: str, bsns_year: str, reprt_code: str
) -> list[dict[str, Any]]:
    """단기사채 미상환 잔액 API (srtpdPsndbtNrdmpBlce)를 호출합니다.

    Args:
        corp_code (str): 공시대상회사의 고유번호(8자리).
        bsns_year (str): 사업연도(4자리).
        reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011).

    Returns:
        list[dict[str, Any]]: 단기사채 미상환 잔액 정보 리스트.
            각 딕셔너리는 다음 키를 포함합니다:
            - corp_name (str): 회사명
            - remndr_exprtn1 (str): 잔여만기
            - remndr_exprtn2 (str): 잔여만기
            - de10_below (str): 10일 이하 금액
            - de10_excess_de30_below (str): 10일초과 30일이하 금액
            - de30_excess_de90_below (str): 30일초과 90일이하 금액
            - de90_excess_de180_below (str): 90일초과 180일이하 금액
            - de180_excess_yy1_below (str): 180일초과 1년이하 금액
            - sm (str): 합계 금액
            - isu_lmt (str): 발행 한도
            - remndr_lmt (str): 잔여 한도
            - stlm_dt (str): 결산기준일 (YYYY-MM-DD)
            - corp_cls_nm (str): 법인구분명 (매핑된 한글명)
    """
    raw_list = await _call_regular_report_api_template(
        final_url=urls.GET_SHORT_TERM_BONDS_OUTSTANDING_BALANCE.value.format(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        ),
        api_name_for_logging="get_short_term_bonds_outstanding_balance",
        corp_code_for_logging=corp_code,
    )

    processed_list = []
    keys_to_remove = ["rcept_no", "corp_code", "corp_cls"]
    if raw_list:
        for item in raw_list:
            item["corp_cls_nm"] = CorpClassMapping.get_korean_name(item.get("corp_cls"))
            for key_to_remove in keys_to_remove:
                item.pop(key_to_remove, None)
            processed_list.append(item)
    return processed_list


async def get_corporate_bonds_outstanding_balance(
    corp_code: str, bsns_year: str, reprt_code: str
) -> list[dict[str, Any]]:
    """회사채 미상환 잔액 API (cprndNrdmpBlce)를 호출합니다.

    Args:
        corp_code (str): 공시대상회사의 고유번호(8자리).
        bsns_year (str): 사업연도(4자리).
        reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011).

    Returns:
        list[dict[str, Any]]: 회사채 미상환 잔액 정보 리스트.
            각 딕셔너리는 다음 키를 포함합니다:
            - corp_name (str): 회사명
            - remndr_exprtn1 (str): 잔여만기
            - remndr_exprtn2 (str): 잔여만기
            - yy1_below (str): 1년 이하 금액
            - yy1_excess_yy2_below (str): 1년초과 2년이하 금액
            - yy2_excess_yy3_below (str): 2년초과 3년이하 금액
            - yy3_excess_yy4_below (str): 3년초과 4년이하 금액
            - yy4_excess_yy5_below (str): 4년초과 5년이하 금액
            - yy5_excess_yy10_below (str): 5년초과 10년이하 금액
            - yy10_excess (str): 10년초과 금액
            - sm (str): 합계 금액
            - stlm_dt (str): 결산기준일 (YYYY-MM-DD)
            - corp_cls_nm (str): 법인구분명 (매핑된 한글명)
    """
    raw_list = await _call_regular_report_api_template(
        final_url=urls.GET_CORPORATE_BONDS_OUTSTANDING_BALANCE.value.format(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        ),
        api_name_for_logging="get_corporate_bonds_outstanding_balance",
        corp_code_for_logging=corp_code,
    )

    processed_list = []
    keys_to_remove = ["rcept_no", "corp_code", "corp_cls"]
    if raw_list:
        for item in raw_list:
            item["corp_cls_nm"] = CorpClassMapping.get_korean_name(item.get("corp_cls"))
            for key_to_remove in keys_to_remove:
                item.pop(key_to_remove, None)
            processed_list.append(item)
    return processed_list


async def get_new_capital_securities_outstanding_balance(
    corp_code: str, bsns_year: str, reprt_code: str
) -> list[dict[str, Any]]:
    """신종자본증권 미상환 잔액 API (newCaplScritsNrdmpBlce)를 호출합니다.

    Args:
        corp_code (str): 공시대상회사의 고유번호(8자리).
        bsns_year (str): 사업연도(4자리).
        reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011).

    Returns:
        list[dict[str, Any]]: 신종자본증권 미상환 잔액 정보 리스트.
            각 딕셔너리는 다음 키를 포함합니다:
            - corp_name (str): 회사명
            - remndr_exprtn1 (str): 잔여만기
            - remndr_exprtn2 (str): 잔여만기
            - yy1_below (str): 1년 이하 금액
            - yy1_excess_yy5_below (str): 1년초과 5년이하 금액
            - yy5_excess_yy10_below (str): 5년초과 10년이하 금액
            - yy10_excess_yy15_below (str): 10년초과 15년이하 금액
            - yy15_excess_yy20_below (str): 15년초과 20년이하 금액
            - yy20_excess_yy30_below (str): 20년초과 30년이하 금액
            - yy30_excess (str): 30년초과 금액
            - sm (str): 합계 금액
            - stlm_dt (str): 결산기준일 (YYYY-MM-DD)
            - corp_cls_nm (str): 법인구분명 (매핑된 한글명)
    """
    raw_list = await _call_regular_report_api_template(
        final_url=urls.GET_HYBRID_SECURITIES_OUTSTANDING_BALANCE.value.format(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        ),
        api_name_for_logging="get_hybrid_securities_outstanding_balance",
        corp_code_for_logging=corp_code,
    )

    processed_list = []
    keys_to_remove = ["rcept_no", "corp_code", "corp_cls"]
    if raw_list:
        for item in raw_list:
            item["corp_cls_nm"] = CorpClassMapping.get_korean_name(item.get("corp_cls"))
            for key_to_remove in keys_to_remove:
                item.pop(key_to_remove, None)
            processed_list.append(item)
    return processed_list


async def get_contingent_capital_securities_outstanding_balance(
    corp_code: str, bsns_year: str, reprt_code: str
) -> list[dict[str, Any]]:
    """조건부 자본증권 미상환 잔액 API (cndlCaplScritsNrdmpBlce)를 호출합니다.

    Args:
        corp_code (str): 공시대상회사의 고유번호(8자리).
        bsns_year (str): 사업연도(4자리).
        reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011).

    Returns:
        list[dict[str, Any]]: 조건부 자본증권 미상환 잔액 정보 리스트.
            각 딕셔너리는 다음 키를 포함합니다:
            - corp_name (str): 회사명
            - remndr_exprtn1 (str): 잔여만기
            - remndr_exprtn2 (str): 잔여만기
            - yy1_below (str): 1년 이하 금액
            - yy1_excess_yy2_below (str): 1년초과 2년이하 금액
            - yy2_excess_yy3_below (str): 2년초과 3년이하 금액
            - yy3_excess_yy4_below (str): 3년초과 4년이하 금액
            - yy4_excess_yy5_below (str): 4년초과 5년이하 금액
            - yy5_excess_yy10_below (str): 5년초과 10년이하 금액
            - yy10_excess_yy20_below (str): 10년초과 20년이하 금액
            - yy20_excess_yy30_below (str): 20년초과 30년이하 금액
            - yy30_excess (str): 30년초과 금액
            - sm (str): 합계 금액
            - stlm_dt (str): 결산기준일 (YYYY-MM-DD)
            - corp_cls_nm (str): 법인구분명 (매핑된 한글명)
    """
    raw_list = await _call_regular_report_api_template(
        final_url=urls.GET_CONTINGENT_CAPITAL_SECURITIES_OUTSTANDING_BALANCE.value.format(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        ),
        api_name_for_logging="get_contingent_capital_securities_outstanding_balance",
        corp_code_for_logging=corp_code,
    )

    processed_list = []
    keys_to_remove = ["rcept_no", "corp_code", "corp_cls"]
    if raw_list:
        for item in raw_list:
            item["corp_cls_nm"] = CorpClassMapping.get_korean_name(item.get("corp_cls"))
            for key_to_remove in keys_to_remove:
                item.pop(key_to_remove, None)
            processed_list.append(item)
    return processed_list
