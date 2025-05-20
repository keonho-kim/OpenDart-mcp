import logging
from typing import Any

import httpx

from .const import urls
from .mapping import FinancialStatementDivisionName, ReportCodeName

logger = logging.getLogger(__name__)


async def get_financial_statement(
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

    Returns:
        list[dict[str, Any]]: 조회 및 가공된 재무제표 정보 리스트.
            각 항목에는 reprt_name_kr, sj_div_name_kr 키가 추가되고,
            원본 코드 필드(rcept_no, reprt_code, corp_code, sj_div)는 제거됩니다.
            API 응답이 성공적이지 않거나 데이터가 없는 경우 빈 리스트를 반환합니다.
    """
    base_url_template = urls.GET_COMPANY_FINANCIAL_STMT.value

    final_url = base_url_template.format(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code,
        fs_div=fs_div,
    )

    logger.info(f"Requesting DART financial statement from URL: {final_url}")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(final_url)
            response.raise_for_status()

            data = response.json()
            logger.debug(f"DART API Raw Response: {data}")

            status_code = data.get("status")
            message = data.get("message")

            if status_code == "000":
                logger.info(f"DART API Call Successful: {message}")
                raw_list = data.get("list", [])
                processed_list = []
                keys_to_remove = ["rcept_no", "reprt_code", "corp_code", "sj_div"]
                for item in raw_list:
                    item["reprt_name_kr"] = ReportCodeName.get_korean_name_by_code(
                        item.get("reprt_code")
                    )
                    item["sj_div_name_kr"] = (
                        FinancialStatementDivisionName.get_korean_name_by_code(
                            item.get("sj_div")
                        )
                    )

                    for key_to_remove in keys_to_remove:
                        item.pop(key_to_remove, None)

                    processed_list.append(item)
                return processed_list
            elif status_code == "013":
                logger.info(f"DART API: No data found. Message: {message}")
                return []
            else:
                logger.error(f"DART API Error: status={status_code}, message={message}")
                return []

    except httpx.HTTPStatusError as e:
        logger.error(
            f"HTTP error occurred while requesting DART API for {corp_code}: {e!r}"
        )
        return []
    except httpx.RequestError as e:
        logger.error(
            f"Request error occurred while requesting DART API for {corp_code}: {e!r}"
        )
        return []
    except Exception as e:
        logger.error(
            f"An unexpected error occurred while processing DART API response for {corp_code}: {e!r}"
        )
        return []
