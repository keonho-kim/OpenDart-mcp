import logging
from typing import Any

from dart_mcp.api_clients.base.dart import _call_regular_report_api_template

from .const import urls
from .mapping import CorpClassMapping

logger = logging.getLogger(__name__)


async def get_capital_increase_or_decrease_status(
    corp_code: str, bsns_year: str, reprt_code: str
) -> list[dict[str, Any]]:
    """증자(감자) 현황 API (irdsSttus)를 호출합니다.

    Args:
        corp_code (str): 공시대상회사의 고유번호(8자리).
        bsns_year (str): 사업연도(4자리).
        reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011).

    Returns:
        list[dict[str, Any]]: 증자(감자) 현황 정보 리스트.
            각 딕셔너리는 다음 키를 포함합니다:
            - corp_name (str): 법인명
            - isu_dcrs_de (str): 주식발행 감소일자
            - isu_dcrs_stle (str): 발행 감소 형태
            - isu_dcrs_stock_knd (str): 발행 감소 주식 종류
            - isu_dcrs_qy (str): 발행 감소 수량 (정수형으로 변환 필요 시 주의)
            - isu_dcrs_mstvdv_fval_amount (str): 발행 감소 주당 액면 가액 (정수형으로 변환 필요 시 주의)
            - isu_dcrs_mstvdv_amount (str): 발행 감소 주당 가액 (정수형으로 변환 필요 시 주의)
            - stlm_dt (str): 결산기준일 (YYYY-MM-DD)
            - corp_cls_nm (str): 법인구분명 (매핑된 한글명: 유가증권, 코스닥, 코넥스, 기타, 알 수 없음)
    """
    raw_list = await _call_regular_report_api_template(
        final_url=urls.GET_CAPITAL_INCREASE_OR_DECREASE_STATUS.value.format(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        ),
        api_name_for_logging="get_capital_increase_or_decrease_status",
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


async def get_dividend_status(
    corp_code: str, bsns_year: str, reprt_code: str
) -> list[dict[str, Any]]:
    """배당에 관한 사항 API (alotMatter)를 호출합니다.

    Args:
        corp_code (str): 공시대상회사의 고유번호(8자리).
        bsns_year (str): 사업연도(4자리).
        reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011).

    Returns:
        list[dict[str, Any]]: 배당에 관한 사항 정보 리스트.
            각 딕셔너리는 다음 키를 포함합니다:
            - corp_name (str): 법인명
            - se (str): 구분 (예: 유상증자(주주배정), 전환권행사 등)
            - stock_knd (str): 주식 종류 (예: 보통주 등)
            - thstrm (str): 당기 (정수형으로 변환 필요 시 주의)
            - frmtrm (str): 전기 (정수형으로 변환 필요 시 주의)
            - lwfr (str): 전전기 (정수형으로 변환 필요 시 주의)
            - stlm_dt (str): 결산기준일 (YYYY-MM-DD)
            - corp_cls_nm (str): 법인구분명 (매핑된 한글명: 유가증권, 코스닥, 코넥스, 기타, 알 수 없음)
    """
    raw_list = await _call_regular_report_api_template(
        final_url=urls.GET_DIVIDEND_STATUS.value.format(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        ),
        api_name_for_logging="get_dividend_status",
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


async def get_acquisition_of_treasury_stock(
    corp_code: str, bsns_year: str, reprt_code: str
) -> list[dict[str, Any]]:
    """자기주식 취득 및 처분현황 API (tesstkAcqsDspsSttus)를 호출합니다.

    Args:
        corp_code (str): 공시대상회사의 고유번호(8자리).
        bsns_year (str): 사업연도(4자리).
        reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011).

    Returns:
        list[dict[str, Any]]: 자기주식 취득 및 처분현황 정보 리스트.
            각 딕셔너리는 다음 키를 포함합니다:
            - corp_name (str): 법인명
            - acqs_mth1 (str): 취득방법 대분류 (예: 배당가능이익범위 이내 취득)
            - acqs_mth2 (str): 취득방법 중분류 (예: 직접취득)
            - acqs_mth3 (str): 취득방법 소분류 (예: 장내직접취득)
            - stock_knd (str): 주식 종류 (예: 보통주)
            - bsis_qy (str): 기초 수량 (정수형으로 변환 필요 시 주의)
            - change_qy_acqs (str): 변동 수량 취득 (정수형으로 변환 필요 시 주의)
            - change_qy_dsps (str): 변동 수량 처분 (정수형으로 변환 필요 시 주의)
            - change_qy_incnr (str): 변동 수량 소각 (정수형으로 변환 필요 시 주의)
            - trmend_qy (str): 기말 수량 (정수형으로 변환 필요 시 주의)
            - rm (str): 비고
            - stlm_dt (str): 결산기준일 (YYYY-MM-DD)
            - corp_cls_nm (str): 법인구분명 (매핑된 한글명: 유가증권, 코스닥, 코넥스, 기타, 알 수 없음)
    """
    raw_list = await _call_regular_report_api_template(
        final_url=urls.GET_ACQUISITION_OF_TREASURY_STOCK.value.format(
            corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
        ),
        api_name_for_logging="get_acquisition_of_treasury_stock",
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


async def get_largest_shareholder(
    corp_code: str, bsns_year: str, reprt_code: str
) -> list[dict[str, Any]]:
    """최대주주 현황 API (hyslrSttus)를 호출합니다.

    Args:
        corp_code (str): 공시대상회사의 고유번호(8자리).
        bsns_year (str): 사업연도(4자리).
        reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011).

    Returns:
        list[dict[str, Any]]: 최대주주 현황 정보 리스트.
            각 딕셔너리는 다음 키를 포함합니다:
            - corp_name (str): 법인명
            - nm (str): 성명
            - relate (str): 관계
            - stock_knd (str): 주식 종류
            - bsis_posesn_stock_co (str): 기초 소유 주식 수
            - bsis_posesn_stock_qota_rt (str): 기초 소유 주식 지분 율
            - trmend_posesn_stock_co (str): 기말 소유 주식 수
            - trmend_posesn_stock_qota_rt (str): 기말 소유 주식 지분 율
            - rm (str): 비고
            - stlm_dt (str): 결산기준일 (YYYY-MM-DD)
            - corp_cls_nm (str): 법인구분명 (매핑된 한글명)
    """
    base_url_template = urls.GET_LARGEST_SHAREHOLDER.value
    final_url = base_url_template.format(
        corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
    )
    raw_list = await _call_regular_report_api_template(
        final_url=final_url,
        api_name_for_logging="get_largest_shareholder",
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


async def get_largest_shareholder_changes(
    corp_code: str, bsns_year: str, reprt_code: str
) -> list[dict[str, Any]]:
    """최대주주 변동현황 API (hyslrChgSttus)를 호출합니다.

    Args:
        corp_code (str): 공시대상회사의 고유번호(8자리).
        bsns_year (str): 사업연도(4자리).
        reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011).

    Returns:
        list[dict[str, Any]]: 최대주주 변동현황 정보 리스트.
            각 딕셔너리는 다음 키를 포함합니다:
            - corp_name (str): 법인명
            - change_on (str): 변동 일
            - mxmm_shrholdr_nm (str): 최대 주주 명
            - posesn_stock_co (str): 소유 주식 수
            - qota_rt (str): 지분 율
            - change_cause (str): 변동 원인
            - rm (str): 비고
            - stlm_dt (str): 결산기준일 (YYYY-MM-DD)
            - corp_cls_nm (str): 법인구분명 (매핑된 한글명)
    """
    base_url_template = urls.GET_LARGEST_SHAREHOLDER_CHANGES.value
    final_url = base_url_template.format(
        corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
    )
    raw_list = await _call_regular_report_api_template(
        final_url=final_url,
        api_name_for_logging="get_largest_shareholder_changes",
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


async def get_minor_stock_status(
    corp_code: str, bsns_year: str, reprt_code: str
) -> list[dict[str, Any]]:
    """소액주주 현황 API (mrhlSttus)를 호출합니다.

    Args:
        corp_code (str): 공시대상회사의 고유번호(8자리).
        bsns_year (str): 사업연도(4자리).
        reprt_code (str): 보고서 코드 (1분기: 11013, 반기: 11012, 3분기: 11014, 사업: 11011).

    Returns:
        list[dict[str, Any]]: 소액주주 현황 정보 리스트.
            각 딕셔너리는 다음 키를 포함합니다:
            - corp_name (str): 법인명
            - se (str): 구분
            - shrholdr_co (str): 주주수
            - shrholdr_tot_co (str): 전체 주주수
            - shrholdr_rate (str): 주주 비율
            - hold_stock_co (str): 보유 주식수
            - stock_tot_co (str): 총발행 주식수
            - hold_stock_rate (str): 보유 주식 비율
            - stlm_dt (str): 결산기준일 (YYYY-MM-DD)
            - corp_cls_nm (str): 법인구분명 (매핑된 한글명)
    """
    base_url_template = urls.GET_MINOR_STOCK_STATUS.value
    final_url = base_url_template.format(
        corp_code=corp_code, bsns_year=bsns_year, reprt_code=reprt_code
    )
    raw_list = await _call_regular_report_api_template(
        final_url=final_url,
        api_name_for_logging="get_minor_stock_status",
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
