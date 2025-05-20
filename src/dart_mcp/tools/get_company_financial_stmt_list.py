# 설계 방향 및 원칙:
# - 핵심 책임: 특정 기업의 공시 정보 목록 조회를 위한 사용자 친화적 인터페이스 제공.
#              내부적으로 DART API 클라이언트 모듈을 호출하여 데이터를 조회합니다.
# - 설계 원칙: SRP (단일 책임 원칙), DIP (의존관계 역전 원칙).
#              API 클라이언트의 기능을 감싸고, 필요시 추가적인 유틸리티나 로직을 통합할 수 있는 지점.
# - 기술적 고려사항: 비동기 함수로 구현하여 API 클라이언트의 비동기 특성을 그대로 활용.
#                  API 클라이언트 모듈과의 인터페이스(파라미터, 반환 타입) 일관성 유지.
# - 사용 시 고려사항: 이 함수는 네트워크를 통해 외부 API를 호출하므로, 실행 시간에 네트워크 상태와 API 서버 상태에 영향을 받습니다.
#                  오류 처리는 호출하는 쪽에서도 필요에 따라 추가적으로 고려해야 합니다.

from typing import Any

# API 클라이언트 모듈의 함수를 import
from dart_mcp.api_clients.dart.financial_stmt_list import (
    get_company_financial_stmt_list as fetch_disclosure_list_from_api,
)


async def get_company_financial_stmt_list(
    corp_code: str, start_date: str, end_date: str
) -> tuple[list[dict[str, Any]], str | None]:
    """
    특정 기업의 정기 재무 공시 정보를 조회합니다.

    이 함수는 내부적으로 API 클라이언트 모듈을 호출하여 실제 데이터 조회를 수행합니다.

    Args:
        corp_code: 조회할 기업의 고유 코드 (공시정보시스템에서 발급된 8자리 문자열).
        start_date: 검색 시작일 (YYYYMMDD 형식).
        end_date: 검색 종료일 (YYYYMMDD 형식).

    Returns:
        Tuple[List[Dict[str, Any]], Optional[str]]:
            조회 성공 시 (공시 목록 리스트, None), 실패 시 (빈 리스트, 오류 메시지 문자열).
            공시 목록의 각 항목은 API 응답의 'list' 필드에 있는 딕셔너리 형태입니다.
            (예시: [{'corp_code': '00126380', 'corp_name': '삼성전자', ...}, ...])
    """
    # API 클라이언트의 함수를 호출하고 결과를 반환
    return await fetch_disclosure_list_from_api(
        corp_code=corp_code, start_date=start_date, end_date=end_date
    )
