# 설계 방향 및 원칙:
# - 핵심 책임: DART API의 투자 관련 엔드포인트들을 호출하고, 기본적인 응답 처리를 수행합니다.
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

logger = logging.getLogger(__name__)


async def get_investment_in_subsidiaries(
    corp_code: str, bsns_year: str, reprt_code: str
) -> list[dict[str, Any]]:
    """타법인 출자현황 API (otrCprInvstmntSttus)를 호출합니다.

    Args:
        corp_code (str): 공시대상회사의 고유번호(8자리).
        bsns_year (str): 사업연도(4자리).
        reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011).

    Returns:
        list[dict[str, Any]]: 타법인 출자현황 정보 리스트.
            각 딕셔너리는 다음 키를 포함합니다:
            - corp_name (str): 회사명
            - inv_prm (str): 법인명 (출자 대상 법인)
            - frst_acqs_de (str): 최초 취득 일자 (YYYYMMDD)
            - invstmnt_purps (str): 출자 목적
            - frst_acqs_amount (str): 최초 취득 금액
            - bsis_blce_qy (str): 기초 잔액 수량
            - bsis_blce_qota_rt (str): 기초 잔액 지분 율
            - bsis_blce_acntbk_amount (str): 기초 잔액 장부 가액
            - incrs_dcrs_acqs_dsps_qy (str): 증가 감소 취득 처분 수량
            - incrs_dcrs_acqs_dsps_amount (str): 증가 감소 취득 처분 금액
            - incrs_dcrs_evl_lstmn (str): 증가 감소 평가 손액
            - trmend_blce_qy (str): 기말 잔액 수량
            - trmend_blce_qota_rt (str): 기말 잔액 지분 율
            - trmend_blce_acntbk_amount (str): 기말 잔액 장부 가액
            - recent_bsns_year_fnnr_sttus_tot_assets (str): 최근 사업 연도 재무 현황 총 자산
            - recent_bsns_year_fnnr_sttus_thstrm_ntpf (str): 최근 사업 연도 재무 현황 당기 순이익
            - stlm_dt (str): 결산기준일 (YYYY-MM-DD)
    """
    raw_list = await _call_regular_report_api_template(
        final_url=urls.GET_INVESTMENT_IN_SUBSIDIARIES.value.format(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        ),
        api_name_for_logging="get_investment_in_subsidiaries",
        corp_code_for_logging=corp_code,
    )

    processed_list = []
    keys_to_remove = ["rcept_no", "corp_code", "corp_cls"]
    if raw_list:
        for item in raw_list:
            # 현재 API에서는 corp_cls에 대한 명시적 매핑 필요 없음
            for key_to_remove in keys_to_remove:
                item.pop(key_to_remove, None)
            processed_list.append(item)
    return processed_list


async def get_public_offering_fund_usage_details(
    corp_code: str, bsns_year: str, reprt_code: str
) -> list[dict[str, Any]]:
    """공모자금의 사용내역 API (pssrpCptalUseDtls)를 호출합니다.

    Args:
        corp_code (str): 공시대상회사의 고유번호(8자리).
        bsns_year (str): 사업연도(4자리).
        reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011).

    Returns:
        list[dict[str, Any]]: 공모자금의 사용내역 정보 리스트.
            각 딕셔너리는 다음 키를 포함합니다:
            - corp_name (str): 회사명
            - se_nm (str): 구분
            - tm (str): 회차
            - pay_de (str): 납입일 (YYYYMMDD, 2019년 12월 9일부터 추가됨)
            - pay_amount (str): 납입금액
            - rs_cptal_use_plan_useprps (str): 증권신고서 등의 자금사용 계획(사용용도) (2018년 1월 19일부터 추가됨)
            - rs_cptal_use_plan_prcure_amount (str): 증권신고서 등의 자금사용 계획(조달금액) (2018년 1월 19일부터 추가됨)
            - real_cptal_use_dtls_cn (str): 실제 자금사용 내역(내용) (2018년 1월 19일부터 추가됨)
            - real_cptal_use_dtls_amount (str): 실제 자금사용 내역(금액) (2018년 1월 19일부터 추가됨)
            - dffrnc_occrrnc_resn (str): 차이발생 사유 등
            - stlm_dt (str): 결산기준일 (YYYY-MM-DD)
            (원본 필드 rcept_no, corp_code, corp_cls는 제거됩니다.)
    """
    raw_list = await _call_regular_report_api_template(
        final_url=urls.GET_PUBLIC_OFFERING_FUND_USAGE_DETAILS.value.format(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        ),
        api_name_for_logging="get_public_offering_fund_usage_details",
        corp_code_for_logging=corp_code,
    )

    processed_list = []
    keys_to_remove = [
        "rcept_no",
        "corp_code",
        "corp_cls",
        "on_dclrt_cptal_use_plan",
        "real_cptal_use_sttus",
    ]
    if raw_list:
        for item in raw_list:
            for key_to_remove in keys_to_remove:
                item.pop(key_to_remove, None)  # 이전 버전 필드도 제거 시도
            processed_list.append(item)
    return processed_list


async def get_private_placement_fund_usage_details(
    corp_code: str, bsns_year: str, reprt_code: str
) -> list[dict[str, Any]]:
    """사모자금의 사용내역 API (prvsrpCptalUseDtls)를 호출합니다.

    Args:
        corp_code (str): 공시대상회사의 고유번호(8자리).
        bsns_year (str): 사업연도(4자리).
        reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011).

    Returns:
        list[dict[str, Any]]: 사모자금의 사용내역 정보 리스트.
            각 딕셔너리는 다음 키를 포함합니다:
            - corp_name (str): 회사명
            - se_nm (str): 구분
            - tm (str): 회차
            - pay_de (str): 납입일 (YYYYMMDD, 2019년 12월 9일부터 추가됨)
            - pay_amount (str): 납입금액 (2019년 12월 9일부터 추가된 `pay_amount`와 동일한 의미일 수 있으나, 명세상 구분되어 있어 그대로 포함)
            - mtrpt_cptal_use_plan_useprps (str): 주요사항보고서의 자금사용 계획(사용용도) (2018년 1월 19일부터 추가됨)
            - mtrpt_cptal_use_plan_prcure_amount (str): 주요사항보고서의 자금사용 계획(조달금액) (2018년 1월 19일부터 추가됨)
            - real_cptal_use_dtls_cn (str): 실제 자금사용 내역(내용) (2018년 1월 19일부터 추가됨)
            - real_cptal_use_dtls_amount (str): 실제 자금사용 내역(금액) (2018년 1월 19일부터 추가됨)
            - dffrnc_occrrnc_resn (str): 차이발생 사유 등
            - stlm_dt (str): 결산기준일 (YYYY-MM-DD)
    """
    raw_list = await _call_regular_report_api_template(
        final_url=urls.GET_PRIVATE_PLACEMENT_FUND_USAGE_DETAILS.value.format(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        ),
        api_name_for_logging="get_private_placement_fund_usage_details",
        corp_code_for_logging=corp_code,
    )

    processed_list = []
    keys_to_remove = [
        "rcept_no",
        "corp_code",
        "corp_cls",
        "cptal_use_plan",
        "real_cptal_use_sttus",
    ]
    if raw_list:
        for item in raw_list:
            for key_to_remove in keys_to_remove:
                item.pop(key_to_remove, None)  # 이전 버전 필드도 제거 시도
            processed_list.append(item)
    return processed_list
