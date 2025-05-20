# 설계 방향 및 원칙:
# - 핵심 책임: 특정 기업의 공시 정보 목록을 DART API를 통해 조회
# - 설계 원칙: SRP (단일 책임 원칙) - API 연동 및 결과 처리 담당, DIP (의존관계 역전 원칙) - httpx 같은 구체적인 HTTP 클라이언트보다는 추상화된 인터페이스를 사용하는 것이 이상적이나, 현재 규모에서는 직접 사용
# - 기술적 고려사항: 비동기 HTTP 요청 (httpx.AsyncClient), API 응답 상태 및 DART 자체 오류 코드 처리
# - 사용 시 고려사항: 네트워크 오류, API 서버 오류, DART 응답 형식 변경 가능성에 대한 예외 처리

from typing import Any

import httpx

from .const import urls


async def get_company_financial_stmt_list(
    corp_code: str, start_date: str, end_date: str
) -> tuple[list[dict[str, Any]], str | None]:
    """특정 기업의 공시 정보를 DART API를 통해 비동기적으로 조회합니다.

    Args:
        corp_code: 조회할 기업의 고유 코드 (공시정보시스템에서 발급된 8자리 문자열).
        start_date: 검색 시작일 (YYYYMMDD 형식).
        end_date: 검색 종료일 (YYYYMMDD 형식).

    Returns:
        tuple[List[Dict[str, Any]], Optional[str]]:
            조회 성공 시 (공시 목록 리스트, None), 실패 시 (빈 리스트, 오류 메시지 문자열).
            공시 목록의 각 항목은 API 응답의 'list' 필드에 있는 딕셔너리 형태입니다.
    """

    url = urls.GET_COMPANY_FINANCIAL_STMT_LIST.value.format(
        corp_code=corp_code, start_date=start_date, end_date=end_date
    )

    try:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url)

                if response.status_code != 200:
                    return [], f"API 요청 실패: HTTP 상태 코드 {response.status_code}"

                try:
                    result = response.json()

                    if result.get("status") != "000":
                        status = result.get("status", "알 수 없음")
                        msg = result.get("message", "알 수 없는 오류")
                        return [], f"DART API 오류: {status} - {msg}"

                    return result.get("list", []), None
                except Exception as e:
                    return [], f"응답 JSON 파싱 오류: {str(e)}"
            except httpx.RequestError as e:
                return [], f"API 요청 중 네트워크 오류 발생: {str(e)}"
    except Exception as e:
        return [], f"공시 목록 조회 중 예상치 못한 오류 발생: {str(e)}"
