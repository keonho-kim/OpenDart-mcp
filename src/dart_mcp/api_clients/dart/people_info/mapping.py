# 설계 방향 및 원칙:
# - 핵심 책임: DART API 응답 중 임직원/보수 관련 정보의 코드화된 값들을 가독성 있는 한글 명칭으로 매핑합니다.
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
    UNKNOWN = ("UNKNOWN", "알 수 없음")

    @classmethod
    def get_korean_name(cls, code: str | None) -> str:
        if code is None:
            return cls.UNKNOWN.value[1]
        for member in cls:
            if member.value[0] == code:
                return member.value[1]
        return cls.UNKNOWN.value[1]


class GenderMapping(Enum):
    """성별 코드(sexdstn)를 한글 명칭으로 매핑합니다."""

    MALE = ("남", "남성")
    FEMALE = ("여", "여성")
    UNKNOWN = ("UNKNOWN", "알 수 없음")

    @classmethod
    def get_korean_name(cls, code: str | None) -> str:
        if code is None:
            return cls.UNKNOWN.value[1]
        for member in cls:
            # API 응답값이 '남', '여'로 직접 오므로 첫번째 값이 아닌 두번째 값으로 비교할 수도 있으나,
            # 다른 매핑과의 일관성을 위해 API 응답값을 코드로 간주하고 매핑합니다.
            # 만약 API가 항상 '남성', '여성'이 아닌 '남', '여'로만 준다면, member.value[0] == code로 비교합니다.
            # 제공된 명세에는 '남'으로 되어있어, 코드를 '남'으로 가정합니다.
            if member.value[0] == code:  # API 응답이 '남', '여'인 경우
                return member.value[1]
        return cls.UNKNOWN.value[1]


class RegisteredExecutiveMapping(Enum):
    """등기임원여부(rgist_exctv_at)를 한글 명칭으로 매핑합니다."""

    REGISTERED = ("등기임원", "등기임원")
    UNREGISTERED = ("미등기임원", "미등기임원")
    # API 명세에 "등기임원, 미등기임원 등"으로 되어 있어, 실제 값을 코드로 사용
    UNKNOWN = ("UNKNOWN", "알 수 없음")

    @classmethod
    def get_korean_name(cls, code: str | None) -> str:
        if code is None:
            return cls.UNKNOWN.value[1]
        for member in cls:
            if member.value[0] == code:
                return member.value[1]
        # '등'을 처리하기 위한 로직 (예: '사외이사 등'과 같이 '등'이 붙는 경우)
        if code.endswith(" 등"):
            original_code = code[:-2]
            for member_check in cls:
                if member_check.value[0] == original_code:
                    return member_check.value[1] + " 등"
        return code  # 매핑되지 않으면 원본 반환 또는 UNKNOWN 처리


class FullTimeExecutiveMapping(Enum):
    """상근여부(fte_at)를 한글 명칭으로 매핑합니다."""

    FULL_TIME = ("상근", "상근")
    PART_TIME = ("비상근", "비상근")
    # API 명세에 "상근, 비상근"으로 되어 있어, 실제 값을 코드로 사용
    UNKNOWN = ("UNKNOWN", "알 수 없음")

    @classmethod
    def get_korean_name(cls, code: str | None) -> str:
        if code is None:
            return cls.UNKNOWN.value[1]
        for member in cls:
            if member.value[0] == code:
                return member.value[1]
        return code  # 매핑되지 않으면 원본 반환 또는 UNKNOWN 처리
