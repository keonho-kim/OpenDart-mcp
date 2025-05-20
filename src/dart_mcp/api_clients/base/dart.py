# 설계 방향 및 원칙:
# - 핵심 책임: DART API의 정기보고서 내 주요 정보 관련 엔드포인트 호출을 위한 공통 템플릿을 제공합니다.
# - 설계 원칙: DRY (Don't Repeat Yourself) - 중복되는 API 호출 로직을 통합하여 관리합니다.
# - 기술적 고려사항: 비동기 처리를 위해 httpx.AsyncClient를 사용합니다.
# 로깅을 통해 API 호출 및 응답 상태를 기록합니다.
# 타입 힌트를 사용하여 코드의 명확성을 높입니다. (Python 3.9+ 스타일 사용)
# - 사용 시 고려사항: 이 함수는 DART API의 공통적인 응답 구조를 처리하며,
# 'list' 필드를 반환하거나 오류/데이터 없음 시 빈 리스트를 반환합니다.
# 특정 API의 세부적인 데이터 가공은 이 함수를 호출하는 쪽에서 처리해야 합니다.

import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)


async def _call_regular_report_api_template(
    final_url: str,
    api_name_for_logging: str,
    corp_code_for_logging: str,
) -> list[dict[str, Any]]:
    """
    DART 정기보고서 API 호출을 위한 일반 템플릿 함수입니다.

    Args:
        final_url (str): 최종 API 요청 URL.
        api_name_for_logging (str): 로깅을 위한 API 이름 (함수명 등).
        corp_code_for_logging (str): 로깅을 위한 회사 코드.

    Returns:
        list[dict[str, Any]]: API 응답의 'list' 항목 또는 에러/데이터 없음 시 빈 리스트.
    """
    logger.info(
        f"Requesting DART API '{api_name_for_logging}' from URL: {final_url} for corp_code: {corp_code_for_logging}"
    )
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(final_url)
            response.raise_for_status()  # HTTP 4xx or 5xx 응답에 대해 예외 발생

            data = response.json()
            logger.debug(
                f"DART API '{api_name_for_logging}' Raw Response for {corp_code_for_logging}: {data}"
            )

            status_code = data.get("status")
            message = data.get("message")

            if status_code == "000":
                logger.info(
                    f"DART API '{api_name_for_logging}' Call Successful for {corp_code_for_logging}: {message}"
                )
                # 반환값 작업 필요 (이 주석은 이 함수를 사용하는 각 모듈 함수 내에 있어야 합니다.)
                return data.get("list", [])
            elif status_code == "013":  # 데이터가 없는 경우
                logger.info(
                    f"DART API '{api_name_for_logging}': No data found for {corp_code_for_logging}. Message: {message}"
                )
                return []
            else:  # 그 외 API 자체 에러 (status != "000" and status != "013")
                logger.error(
                    f"DART API '{api_name_for_logging}' Error for {corp_code_for_logging}: status={status_code}, message={message}"
                )
                return []

    except httpx.HTTPStatusError as e:
        logger.error(
            f"HTTP error occurred while requesting DART API '{api_name_for_logging}' for {corp_code_for_logging} from {final_url}: {e!r}"
        )
        return []
    except httpx.RequestError as e:  # 네트워크 문제 등 요청 관련 예외
        logger.error(
            f"Request error occurred while requesting DART API '{api_name_for_logging}' for {corp_code_for_logging} from {final_url}: {e!r}"
        )
        return []
    except Exception as e:  # JSON 파싱 오류 등 기타 예외
        logger.error(
            f"An unexpected error occurred while processing DART API '{api_name_for_logging}' response for {corp_code_for_logging} from {final_url}: {e!r}"
        )
        return []
