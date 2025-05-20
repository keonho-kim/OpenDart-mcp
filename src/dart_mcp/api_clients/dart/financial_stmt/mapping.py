# 설계 방향 및 원칙:
# - 핵심 책임: DART API 응답 중 특정 코드 값에 대한 한글 명칭 매핑 정보 제공.
# - 설계 원칙:
#   - SRP (단일 책임 원칙): 각 Enum은 특정 코드 그룹의 매핑 정보만 책임짐.
#   - OCP (개방-폐쇄 원칙): 새로운 코드나 매핑 정보 추가 시 기존 코드 수정 최소화 (Enum 확장).
# - 기술적 고려사항: Python Enum 타입을 사용하여 코드와 의미를 명확하게 연결.
# - 사용 시 고려사항:
#   - API 응답 처리 시 이 Enum들을 활용하여 코드 값을 이해하기 쉬운 한글 명칭으로 변환.
#   - 존재하지 않는 코드 값에 대한 예외 처리 (e.g., try-except ValueError) 필요.

from enum import Enum


class ReportCodeName(Enum):
    """보고서 코드(reprt_code)에 대한 한글 명칭을 정의하는 Enum 클래스입니다."""

    QUARTER_1 = "11013"  # 1분기보고서
    HALF_YEAR = "11012"  # 반기보고서
    QUARTER_3 = "11014"  # 3분기보고서
    ANNUAL = "11011"  # 사업보고서

    @property
    def korean_name(self) -> str:
        """보고서 코드의 한글 명칭을 반환합니다."""
        return {
            ReportCodeName.QUARTER_1: "1분기보고서",
            ReportCodeName.HALF_YEAR: "반기보고서",
            ReportCodeName.QUARTER_3: "3분기보고서",
            ReportCodeName.ANNUAL: "사업보고서",
        }[self]

    @classmethod
    def get_korean_name_by_code(cls, code: str | None) -> str:
        """주어진 코드 값에 해당하는 한글 명칭을 반환합니다. 유효하지 않은 경우 원본 코드를 반환합니다."""
        if code is None:
            return "정보 없음"
        try:
            return cls(code).korean_name
        except ValueError:
            return code  # 매핑되는 Enum 멤버가 없으면 원본 코드 값 반환


class FinancialStatementDivisionName(Enum):
    """재무제표 구분(sj_div) 코드에 대한 한글 명칭을 정의하는 Enum 클래스입니다."""

    BALANCE_SHEET = "BS"  # 재무상태표
    INCOME_STATEMENT = "IS"  # 손익계산서
    COMPREHENSIVE_INCOME_STATEMENT = "CIS"  # 포괄손익계산서
    CASH_FLOW = "CF"  # 현금흐름표
    STATEMENT_OF_CHANGES_IN_EQUITY = "SCE"  # 자본변동표

    @property
    def korean_name(self) -> str:
        """재무제표 구분 코드의 한글 명칭을 반환합니다."""
        return {
            FinancialStatementDivisionName.BALANCE_SHEET: "재무상태표",
            FinancialStatementDivisionName.INCOME_STATEMENT: "손익계산서",
            FinancialStatementDivisionName.COMPREHENSIVE_INCOME_STATEMENT: "포괄손익계산서",
            FinancialStatementDivisionName.CASH_FLOW: "현금흐름표",
            FinancialStatementDivisionName.STATEMENT_OF_CHANGES_IN_EQUITY: "자본변동표",
        }[self]

    @classmethod
    def get_korean_name_by_code(cls, code: str | None) -> str:
        """주어진 코드 값에 해당하는 한글 명칭을 반환합니다. 유효하지 않은 경우 원본 코드를 반환합니다."""
        if code is None:
            return "정보 없음"
        try:
            return cls(code).korean_name
        except ValueError:
            return code  # 매핑되는 Enum 멤버가 없으면 원본 코드 값 반환
