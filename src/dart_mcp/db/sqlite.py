# 설계 방향 및 원칙:
#   - 핵심 책임: SQLite 데이터베이스 상호작용 캡슐화 (연결, CRUD, 트랜잭션 관리).
#   - 주요 특징: 컨텍스트 관리자 프로토콜(`with` 구문) 지원으로 안전한 자원 관리.
#              데이터 삽입 시 Pydantic 모델을 활용하여 타입 안정성 및 유효성 검사 강화.
#   - 사용시 핵심: `with` 구문을 통한 자동 커밋/롤백 또는 명시적 호출로 트랜잭션 관리.

import logging
import sqlite3
from typing import Any  # Dict, List 추가

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SQLiteDB:
    """
    SQLite DB 작업을 위한 래퍼. 컨텍스트 관리자 지원, Pydantic 모델 기반 타입 안정성 제공.
    데이터 삽입 시 Pydantic 모델 또는 Python 딕셔너리/리스트 사용 가능.
    """

    def __init__(self, db_path: str):
        """
        SQLiteDB 인스턴스를 초기화합니다.

        Args:
            db_path: SQLite 데이터베이스 파일 경로.
        """
        self.db_path = db_path
        self.conn: sqlite3.Connection | None = None  # Optional 사용
        self.cursor: sqlite3.Cursor | None = None  # Optional 사용

    def __enter__(self):
        """
        DB 연결 및 커서 생성 (컨텍스트 관리자 진입).

        Returns:
            SQLiteDB: 연결된 self 인스턴스.
        Raises:
            sqlite3.Error: 연결 실패 시.
        """
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = (
                sqlite3.Row
            )  # 컬럼 이름으로 접근 가능하도록 row_factory 설정
            self.cursor = self.conn.cursor()
            logger.info(f"'{self.db_path}'에 성공적으로 연결되었습니다.")
            return self
        except sqlite3.Error as e:
            logger.error(f"데이터베이스 연결 오류: {e}", exc_info=True)
            raise e

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        DB 연결 종료 및 트랜잭션 처리 (컨텍스트 관리자 종료).
        정상 시 커밋, 예외 발생 시 롤백.
        """
        if self.conn:
            try:
                if exc_type:
                    logger.warning(
                        f"예외 발생 ({exc_type.__name__ if exc_type else 'Unknown'}): {exc_val}, 변경사항을 롤백합니다.",
                        exc_info=(exc_type, exc_val, exc_tb),
                    )
                    self.conn.rollback()
                else:
                    logger.info("변경사항을 커밋합니다.")
                    self.conn.commit()
            except sqlite3.Error as e_trans:
                logger.error(
                    f"트랜잭션 처리(롤백/커밋) 중 오류: {e_trans}", exc_info=True
                )
                if not exc_type:  # 커밋 중 오류만 다시 발생
                    raise e_trans
            finally:
                try:
                    self.conn.close()
                    logger.info(f"'{self.db_path}' 연결이 닫혔습니다.")
                except sqlite3.Error as e_close:
                    logger.error(
                        f"데이터베이스 연결 종료 중 오류 발생: {e_close}", exc_info=True
                    )

    def execute_sql(self, sql_query: str, params: tuple[Any, ...] | None = None):
        """
        단일 DML/DDL SQL 쿼리를 실행합니다 (SELECT 문에는 부적합).

        Args:
            sql_query: 실행할 SQL 쿼리.
            params: 쿼리 파라미터 (선택 사항).

        Returns:
            int | None: INSERT 시 `lastrowid`, 그 외 DML은 `rowcount`.

        Raises:
            sqlite3.Error: DB 미연결 또는 SQL 실행 오류.
        """
        if not self.conn or not self.cursor:
            logger.error("데이터베이스 미연결 상태에서 SQL 실행 시도.")
            raise sqlite3.Error("데이터베이스에 연결되어 있지 않습니다.")

        try:
            self.cursor.execute(sql_query, params or ())
            logger.debug(f"SQL 실행 성공: {sql_query}, Params: {params}")
            return (
                self.cursor.lastrowid
                if "insert" in sql_query.lower()
                else self.cursor.rowcount
            )
        except sqlite3.Error as e:
            logger.error(f"SQL 실행 오류: {e}", exc_info=True)
            logger.error(f"실패한 쿼리: {sql_query}")
            if params:
                logger.error(f"파라미터: {params}")
            raise e

    def execute_script(self, sql_script: str) -> bool:
        """
        여러 SQL 문으로 구성된 스크립트를 실행합니다.

        Args:
            sql_script: 실행할 SQL 스크립트.

        Returns:
            True: 스크립트 실행 성공 시.

        Raises:
            sqlite3.Error: DB 미연결 또는 스크립트 실행 오류.
        """
        if not self.conn or not self.cursor:
            logger.error("데이터베이스 미연결 상태에서 SQL 스크립트 실행 시도.")
            raise sqlite3.Error("데이터베이스에 연결되어 있지 않습니다.")

        try:
            self.cursor.executescript(sql_script)
            logger.info(f"SQL 스크립트 실행 성공: {sql_script[:200]}...")
            return True
        except sqlite3.Error as e:
            logger.error(f"SQL 스크립트 실행 오류: {e}", exc_info=True)
            logger.error(f"실패한 스크립트 일부: {sql_script[:200]}...")
            raise e

    def fetch_one(
        self, sql_query: str, params: tuple[Any, ...] | None = None
    ) -> dict[str, Any] | None:
        """
        SELECT 쿼리 실행 후 한 행 반환 (딕셔너리 형태).

        Args:
            sql_query: 실행할 SELECT 쿼리.
            params: 쿼리 파라미터 (선택 사항).

        Returns:
            dict[str, Any] | None: 결과 행 (딕셔너리) 또는 None.

        Raises:
            sqlite3.Error: DB 미연결 또는 SQL 실행 오류.
        """
        if not self.conn or not self.cursor:
            logger.error("데이터베이스 미연결 상태에서 fetch_one 시도.")
            raise sqlite3.Error("데이터베이스에 연결되어 있지 않습니다.")

        try:
            self.cursor.execute(sql_query, params or ())
            row = self.cursor.fetchone()
            logger.debug(
                f"Fetch one 성공: {sql_query}, Params: {params}, Result: {'데이터 있음' if row else '데이터 없음'}"
            )
            return dict(row) if row else None
        except sqlite3.Error as e:
            logger.error(f"Fetch one 오류: {e}", exc_info=True)
            logger.error(f"실패한 쿼리: {sql_query}")
            if params:
                logger.error(f"파라미터: {params}")
            raise e

    def fetch_all(
        self, sql_query: str, params: tuple[Any, ...] | None = None
    ) -> list[dict[str, Any]]:
        """
        SELECT 쿼리 실행 후 모든 결과 행 리스트로 반환 (각 행은 딕셔너리 형태).

        Args:
            sql_query: 실행할 SELECT 쿼리.
            params: 쿼리 파라미터 (선택 사항).

        Returns:
            list[dict[str, Any]]: 결과 행 딕셔너리 리스트 (없으면 빈 리스트).

        Raises:
            sqlite3.Error: DB 미연결 또는 SQL 실행 오류.
        """
        if not self.conn or not self.cursor:
            logger.error("데이터베이스 미연결 상태에서 fetch_all 시도.")
            raise sqlite3.Error("데이터베이스에 연결되어 있지 않습니다.")

        try:
            self.cursor.execute(sql_query, params or ())
            rows = self.cursor.fetchall()
            logger.debug(
                f"Fetch all 성공: {sql_query}, Params: {params}, Results count: {len(rows)}"
            )
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            logger.error(f"Fetch all 오류: {e}", exc_info=True)
            logger.error(f"실패한 쿼리: {sql_query}")
            if params:
                logger.error(f"파라미터: {params}")
            raise e

    def commit(self):
        """
        명시적 커밋. `with` 구문 사용 시 자동 처리되므로 특수한 경우에만 사용.

        Raises:
            sqlite3.Error: DB 미연결 또는 커밋 오류.
        """
        if not self.conn:
            logger.warning("데이터베이스 미연결 상태에서 명시적 커밋 시도.")
            raise sqlite3.Error("데이터베이스에 연결되어 있지 않아 커밋할 수 없습니다.")
        try:
            self.conn.commit()
            logger.info("변경사항이 명시적으로 커밋되었습니다.")
        except sqlite3.Error as e:
            logger.error(f"명시적 커밋 오류: {e}", exc_info=True)
            raise e

    def rollback(self):
        """
        명시적 롤백. `with` 구문 사용 시 예외 발생 시 자동 처리.

        Raises:
            sqlite3.Error: DB 미연결 또는 롤백 오류.
        """
        if not self.conn:
            logger.warning("데이터베이스 미연결 상태에서 명시적 롤백 시도.")
            raise sqlite3.Error("데이터베이스에 연결되어 있지 않아 롤백할 수 없습니다.")
        try:
            self.conn.rollback()
            logger.info("변경사항이 명시적으로 롤백되었습니다.")
        except sqlite3.Error as e:
            logger.error(f"명시적 롤백 오류: {e}", exc_info=True)
            raise e

    def create_table(
        self,
        table_name: str,
        columns_schema: dict[str, str],
        drop_if_exists: bool = False,
    ) -> bool:
        """
        새 테이블 생성.

        Args:
            table_name: 테이블 이름.
            columns_schema: 컬럼 정의 딕셔너리. 예: {"id": "INTEGER PRIMARY KEY"}
            drop_if_exists: True 시 테이블 생성 전 기존 테이블 삭제.

        Returns:
            True: 테이블 생성 성공 (또는 이미 존재 시).

        Raises:
            sqlite3.Error: DB 미연결 또는 DDL 실행 오류.
        """
        if not self.conn or not self.cursor:
            logger.error("데이터베이스 미연결 상태에서 테이블 생성 시도.")
            raise sqlite3.Error("데이터베이스에 연결되어 있지 않습니다.")

        if drop_if_exists:
            try:
                drop_sql = f"DROP TABLE IF EXISTS {table_name}"
                self.execute_sql(drop_sql)
                logger.info(
                    f"테이블 '{table_name}'이(가) 존재하여 삭제되었습니다 (drop_if_exists=True)."
                )
            except sqlite3.Error as e:
                logger.error(
                    f"테이블 '{table_name}' 삭제 중 오류 (drop_if_exists=True): {e}",
                    exc_info=True,
                )
                raise e

        cols_def = ", ".join(
            [f"{name} {definition}" for name, definition in columns_schema.items()]
        )
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({cols_def})"

        try:
            self.execute_sql(create_table_sql)
            logger.info(
                f"테이블 '{table_name}'이(가) 성공적으로 생성(또는 이미 존재)되었습니다."
            )
            return True
        except sqlite3.Error as e:
            raise e

    def insert_one_dict(self, table_name: str, data_dict: dict[str, Any]) -> int | None:
        """
        딕셔너리 데이터로부터 단일 행 삽입.

        Args:
            table_name: 테이블 이름.
            data_dict: 삽입할 데이터 딕셔너리.

        Returns:
            int | None: 삽입된 행 ID (`lastrowid`).

        Raises:
            ValueError: `data_dict`가 비어있는 경우.
            sqlite3.Error: DB 미연결 또는 SQL 실행 오류.
        """
        if not data_dict:
            logger.warning("삽입할 딕셔너리 데이터가 없습니다.")
            raise ValueError("삽입할 데이터 딕셔너리가 비어있습니다.")

        columns = ", ".join(data_dict.keys())
        placeholders = ", ".join(["?"] * len(data_dict))
        values = tuple(data_dict.values())
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        try:
            last_row_id = self.execute_sql(sql, values)
            logger.info(
                f"테이블 '{table_name}'에 딕셔너리로부터 단일 행 삽입 성공. ID: {last_row_id}"
            )
            return last_row_id

        except sqlite3.Error as e:
            raise e

    def insert_many_dicts(
        self, table_name: str, data_list_of_dicts: list[dict[str, Any]]
    ) -> bool:
        """
        딕셔너리 리스트로부터 여러 행 동시 삽입.

        Args:
            table_name: 테이블 이름.
            data_list_of_dicts: 삽입할 데이터 딕셔너리 리스트.

        Returns:
            True: 성공 시.

        Raises:
            ValueError: `data_list_of_dicts` 리스트가 비었거나, 내부 딕셔너리 형식 오류 시.
            sqlite3.Error: DB 미연결 또는 SQL 실행 오류.
        """
        if not data_list_of_dicts:
            logger.warning("삽입할 딕셔너리 리스트가 비어있습니다.")
            raise ValueError("삽입할 데이터 딕셔너리 리스트가 비어있습니다.")

        if not self.conn or not self.cursor:
            logger.error("데이터베이스 미연결 상태에서 다중 딕셔너리 삽입 시도.")
            raise sqlite3.Error("데이터베이스에 연결되어 있지 않습니다.")

        try:
            # 첫 딕셔너리 기준으로 컬럼명/플레이스홀더 생성 (모든 딕셔너리 키 동일 가정).
            first_dict = data_list_of_dicts[0]
            if not isinstance(first_dict, dict):
                logger.error(
                    "다중 딕셔너리 삽입 시 첫 번째 항목이 딕셔너리가 아닙니다."
                )
                raise ValueError("데이터는 딕셔너리리의 리스트여야 합니다.")
            columns = ", ".join(first_dict.keys())
            placeholders = ", ".join(["?"] * len(first_dict))

        except (
            IndexError,
            AttributeError,
            TypeError,
        ) as e:  # AttributeError/TypeError 추가
            logger.error(
                f"다중 딕셔너리 삽입을 위한 컬럼 정보 추출 실패: {e}", exc_info=True
            )
            raise ValueError(
                "삽입할 딕셔너리 리스트가 비어있거나 첫 번째 딕셔너리의 형식이 잘못되었습니다."
            ) from e

        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        try:
            values_list = [tuple(data.values()) for data in data_list_of_dicts]

        except (AttributeError, TypeError) as e:  # TypeError 추가
            logger.error(f"다중 딕셔너리 삽입 중 값 추출 오류: {e}", exc_info=True)
            raise ValueError("삽입할 딕셔너리 중 일부가 잘못된 형식입니다.") from e

        try:
            self.cursor.executemany(sql, values_list)
            logger.info(
                f"테이블 '{table_name}'에 {self.cursor.rowcount}개 행 (딕셔너리 리스트로부터) 다중 삽입 성공."
            )
            return True

        except sqlite3.Error as e:
            logger.error(f"다중 딕셔너리 삽입 오류: {e}", exc_info=True)
            logger.error(
                f"실패한 쿼리 (일부): INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            )
            raise e
