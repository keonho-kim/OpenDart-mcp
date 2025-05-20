import logging

from dart_mcp.api_clients.dart.corp_list import get_corp_list
from dart_mcp.db.schema import DartCorpList
from dart_mcp.settings.config import DB_INSTANCE

logger = logging.getLogger(__name__)


def fetch_dart_corp_list():
    """
    Fetch Dart Corp List from DART API and save to SQLite DB
    """

    data = get_corp_list()
    logger.info(f"Fetching Company List: {len(data)}")

    with DB_INSTANCE as db:
        db.create_table(
            table_name=DartCorpList.TABLE_NAME,
            columns_schema=DartCorpList.SCHEMA,
            drop_if_exists=True,
        )

        db.insert_many_dicts(
            table_name=DartCorpList.TABLE_NAME, data_list_of_dicts=data
        )

        total_inserted = db.fetch_one(
            sql_query=f"SELECT COUNT(1) FROM {DartCorpList.TABLE_NAME}"
        )

        count_value = total_inserted["COUNT(1)"]
        logger.info(f"Total number of companies: {count_value}")

        if count_value != len(data):
            error_message = f"Total number of companies mismatch: DB count {count_value}, Fetched count {len(data)}"
            logger.error(error_message)
            raise Exception(error_message)

        logger.info("Fetching Company List: Success")
