# 설계 방향 및 원칙:
# - 핵심 책임: DART API 응답 중 주식 관련 정보의 코드화된 값들(예: 법인구분)을 가독성 있는 한글 명칭으로 매핑합니다.
# - 설계 원칙: SRP (단일 책임 원칙) - 각 Enum 클래스는 특정 코드 그룹의 매핑을 담당합니다.
# OCP (개방-폐쇄 원칙) - 새로운 코드 매핑 추가 시 기존 Enum 수정 또는 새 Enum 추가가 용이합니다.
# - 기술적 고려사항: Enum을 사용하여 코드와 명칭 간의 관계를 명확하게 정의합니다.
#                  존재하지 않는 코드에 대한 기본값을 제공하여 오류 발생을 방지합니다.
# - 사용 시 고려사항: API 응답 처리 시 이 매핑 클래스를 활용하여 코드 값을 변환합니다.

from enum import Enum


class CorpClassMapping(Enum):
    """법인구분 코드(corp_cls)를 한글 명칭으로 매핑합니다."""

    YUGA = ("Y", "유가증권")
    KOSDAQ = ("K", "코스닥")
    KONEX = ("N", "코넥스")
    OTHER = ("E", "기타")
    UNKNOWN = ("UNKNOWN", "알 수 없음")  # API 명세에 없는 값 또는 None일 경우 사용

    @classmethod
    def get_korean_name(cls, code: str | None) -> str:
        """주어진 코드에 해당하는 한글 법인구분명을 반환합니다.

        Args:
            code (str | None): 법인구분 코드 (Y, K, N, E 등).

        Returns:
            str: 매핑된 한글 법인구분명. 코드가 없거나 매핑되지 않으면 "알 수 없음"을 반환합니다.
        """
        if code is None:
            return cls.UNKNOWN.value[1]
        for member in cls:
            if member.value[0] == code:
                return member.value[1]
        return cls.UNKNOWN.value[1]
