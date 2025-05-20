# 설계 방향 및 원칙:
# - 핵심 책임: DART API의 임직원/보수 관련 엔드포인트들을 호출하고, 기본적인 응답 처리를 수행합니다.
# - 설계 원칙: SRP (단일 책임 원칙) - 각 함수는 하나의 API 엔드포인트 호출을 책임집니다.
# OCP (개방-폐쇄 원칙) - 새로운 API 엔드포인트 추가 시 기존 함수 수정 없이 새 함수를 추가할 수 있습니다.
# - 기술적 고려사항: 비동기 처리를 위해 httpx.AsyncClient를 사용합니다.
# 로깅을 통해 API 호출 및 응답 상태를 기록합니다.
# 타입 힌트를 사용하여 코드의 명확성을 높입니다.
# - 사용 시 고려사항: 각 함수의 반환값은 현재 DART API의 'list' 필드를 그대로 반환하며, 추가적인 데이터 가공이 필요할 수 있습니다. ('반환값 작업 필요' 주석 참고)
# API 호출 실패 또는 데이터 부재 시 빈 리스트를 반환합니다.

import logging
from typing import Any

from dart_mcp.api_clients.base.dart import _call_regular_report_api_template

from .const import urls
from .mapping import (
    CorpClassMapping,
    FullTimeExecutiveMapping,
    GenderMapping,
    RegisteredExecutiveMapping,
)

logger = logging.getLogger(__name__)


async def get_company_excutives(
    corp_code: str, bsns_year: str, reprt_code: str
) -> list[dict[str, Any]]:
    """임원 현황 API (exctvSttus)를 호출합니다.

    Args:
        corp_code (str): 공시대상회사의 고유번호(8자리).
        bsns_year (str): 사업연도(4자리).
        reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011).

    Returns:
        list[dict[str, Any]]: 임원 현황 정보 리스트.
            각 딕셔너리는 다음 키를 포함합니다:
            - corp_name (str): 법인명
            - nm (str): 성명
            - birth_ym (str): 출생 년월 (YYYY년 MM월)
            - ofcps (str): 직위
            - chrg_job (str): 담당 업무
            - main_career (str): 주요 경력
            - mxmm_shrholdr_relate (str): 최대 주주 관계
            - hffc_pd (str): 재직 기간
            - tenure_end_on (str): 임기 만료 일
            - stlm_dt (str): 결산기준일 (YYYY-MM-DD)
            - sexdstn_nm (str): 성별명 (매핑된 한글명: 남성, 여성, 알 수 없음)
            - rgist_exctv_at_nm (str): 등기 임원 여부명 (매핑된 한글명 또는 원본값)
            - fte_at_nm (str): 상근 여부명 (매핑된 한글명 또는 원본값)
            - corp_cls_nm (str): 법인구분명 (매핑된 한글명)
    """
    raw_list = await _call_regular_report_api_template(
        final_url=urls.GET_COMPANY_EXCUTIVES.value.format(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        ),
        api_name_for_logging="get_company_excutives",
        corp_code_for_logging=corp_code,
    )

    processed_list = []
    keys_to_remove = [
        "rcept_no",
        "corp_code",
        "corp_cls",
        "sexdstn",
        "rgist_exctv_at",
        "fte_at",
    ]
    if raw_list:
        for item in raw_list:
            item["corp_cls_nm"] = CorpClassMapping.get_korean_name(item.get("corp_cls"))
            item["sexdstn_nm"] = GenderMapping.get_korean_name(item.get("sexdstn"))
            item["rgist_exctv_at_nm"] = RegisteredExecutiveMapping.get_korean_name(
                item.get("rgist_exctv_at")
            )
            item["fte_at_nm"] = FullTimeExecutiveMapping.get_korean_name(
                item.get("fte_at")
            )

            for key_to_remove in keys_to_remove:
                item.pop(key_to_remove, None)
            processed_list.append(item)
    return processed_list


async def get_company_employees(
    corp_code: str, bsns_year: str, reprt_code: str
) -> list[dict[str, Any]]:
    """직원 현황 API (empSttus)를 호출합니다.

    Args:
        corp_code (str): 공시대상회사의 고유번호(8자리).
        bsns_year (str): 사업연도(4자리).
        reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011).

    Returns:
        list[dict[str, Any]]: 직원 현황 정보 리스트.
            각 딕셔너리는 다음 키를 포함합니다:
            - corp_name (str): 법인명
            - fo_bbm (str): 사업부문
            - rgllbr_co (str): 정규직 수
            - rgllbr_abacpt_labrr_co (str): 정규직 단시간 근로자 수
            - cnttk_co (str): 계약직 수
            - cnttk_abacpt_labrr_co (str): 계약직 단시간 근로자 수
            - sm (str): 합계
            - avrg_cnwk_sdytrn (str): 평균 근속 연수
            - fyer_salary_totamt (str): 연간 급여 총액
            - jan_salary_am (str): 1인평균 급여 액
            - rm (str): 비고
            - stlm_dt (str): 결산기준일 (YYYY-MM-DD)
            - sexdstn_nm (str): 성별명 (매핑된 한글명: 남성, 여성, 알 수 없음)
            - corp_cls_nm (str): 법인구분명 (매핑된 한글명)
    """
    raw_list = await _call_regular_report_api_template(
        final_url=urls.GET_COMPANY_EMPLOYEES.value.format(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        ),
        api_name_for_logging="get_company_employees",
        corp_code_for_logging=corp_code,
    )

    processed_list = []
    keys_to_remove = [
        "rcept_no",
        "corp_code",
        "corp_cls",
        "sexdstn",
        "reform_bfe_emp_co_rgllbr",
        "reform_bfe_emp_co_cnttk",
        "reform_bfe_emp_co_etc",
    ]
    if raw_list:
        for item in raw_list:
            item["corp_cls_nm"] = CorpClassMapping.get_korean_name(item.get("corp_cls"))
            item["sexdstn_nm"] = GenderMapping.get_korean_name(item.get("sexdstn"))
            for key_to_remove in keys_to_remove:
                item.pop(key_to_remove, None)
            processed_list.append(item)
    return processed_list


async def get_individual_compensation_of_directors_and_auditors(
    corp_code: str, bsns_year: str, reprt_code: str
) -> list[dict[str, Any]]:
    """이사·감사 전체의 보수현황 API (hmvAuditAllSttus)를 호출합니다.

    Args:
        corp_code (str): 공시대상회사의 고유번호(8자리).
        bsns_year (str): 사업연도(4자리).
        reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011).

    Returns:
        list[dict[str, Any]]: 이사·감사 전체의 보수현황 정보 리스트.
            각 딕셔너리는 다음 키를 포함합니다:
            - corp_name (str): 법인명
            - nmpr (str): 인원수
            - mendng_totamt (str): 보수 총액
            - jan_avrg_mendng_am (str): 1인 평균 보수 액
            - rm (str): 비고
            - stlm_dt (str): 결산기준일 (YYYY-MM-DD)
            - corp_cls_nm (str): 법인구분명 (매핑된 한글명)
    """
    raw_list = await _call_regular_report_api_template(
        final_url=urls.GET_INDIVIDUAL_COMPENSATION_OF_DIRECTORS_AND_AUDITORS.value.format(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        ),
        api_name_for_logging="get_individual_compensation_of_directors_and_auditors",
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


async def get_individual_compensation_of_unregular_executive_officers(
    corp_code: str, bsns_year: str, reprt_code: str
) -> list[dict[str, Any]]:
    """미등기임원 보수현황 API (unrstExctvMendngSttus)를 호출합니다.

    Args:
        corp_code (str): 공시대상회사의 고유번호(8자리).
        bsns_year (str): 사업연도(4자리).
        reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011).

    Returns:
        list[dict[str, Any]]: 미등기임원 보수현황 정보 리스트.
            각 딕셔너리는 다음 키를 포함합니다:
            - corp_name (str): 회사명
            - se (str): 구분 (통상 '미등기임원')
            - nmpr (str): 인원수
            - fyer_salary_totamt (str): 연간급여 총액
            - jan_salary_am (str): 1인평균 급여액
            - rm (str): 비고
            - stlm_dt (str): 결산기준일 (YYYY-MM-DD)
            - corp_cls_nm (str): 법인구분명 (매핑된 한글명)
    """
    raw_list = await _call_regular_report_api_template(
        final_url=urls.GET_INDIVIDUAL_COMPENSATION_OF_UNREGULAR_EXECUTIVE_OFFICERS.value.format(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        ),
        api_name_for_logging="get_individual_compensation_of_unregular_executive_officers",
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


async def get_outside_directors_info_and_chages(
    corp_code: str, bsns_year: str, reprt_code: str
) -> list[dict[str, Any]]:
    """사외이사 및 그 변동현황 API (outcmpnyDrctrNdChangeSttus)를 호출합니다.

    Args:
        corp_code (str): 공시대상회사의 고유번호(8자리).
        bsns_year (str): 사업연도(4자리).
        reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011).

    Returns:
        list[dict[str, Any]]: 사외이사 및 그 변동현황 정보 리스트.
            각 딕셔너리는 다음 키를 포함합니다:
            - corp_name (str): 회사명
            - drctr_co (str): 이사의 수
            - otcmp_drctr_co (str): 사외이사 수
            - apnt (str): 사외이사 변동현황(선임)
            - rlsofc (str): 사외이사 변동현황(해임)
            - mdstrm_resig (str): 사외이사 변동현황(중도퇴임)
            - stlm_dt (str): 결산기준일 (YYYY-MM-DD)
            - corp_cls_nm (str): 법인구분명 (매핑된 한글명)
    """
    raw_list = await _call_regular_report_api_template(
        final_url=urls.GET_OUTSIDE_DIRECTORS_INFO_AND_CHAGES.value.format(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        ),
        api_name_for_logging="get_outside_directors_info_and_chages",
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


async def get_top_five_individual_compensation(
    corp_code: str, bsns_year: str, reprt_code: str
) -> list[dict[str, Any]]:
    """개인별 보수지급 금액(보수 상위 5명) API (indvdlByPay)를 호출합니다.

    Args:
        corp_code (str): 공시대상회사의 고유번호(8자리).
        bsns_year (str): 사업연도(4자리).
        reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011).

    Returns:
        list[dict[str, Any]]: 개인별 보수지급 금액(보수 상위 5명) 정보 리스트.
            각 딕셔너리는 다음 키를 포함합니다:
            - corp_name (str): 법인명
            - nm (str): 이름
            - ofcps (str): 직위
            - mendng_totamt (str): 보수 총액
            - mendng_totamt_ct_incls_mendng (str): 보수 총액 비 포함 보수
            - stlm_dt (str): 결산기준일 (YYYY-MM-DD)
            - corp_cls_nm (str): 법인구분명 (매핑된 한글명)
    """
    raw_list = await _call_regular_report_api_template(
        final_url=urls.GET_TOP_FIVE_INDIVIDUAL_COMPENSATION.value.format(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        ),
        api_name_for_logging="get_top_five_individual_compensation",
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
