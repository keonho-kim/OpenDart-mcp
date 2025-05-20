from dataclasses import dataclass

from dart_mcp.settings.config import Settings


@dataclass
class DartCorpList:
    TABLE_NAME = Settings.COMPANY_LIST_TABLE
    SCHEMA = {
        "corp_code": "TEXT",
        "corp_name": "TEXT",
        "corp_eng_name": "TEXT",
        "stock_code": "TEXT",
        "modify_date": "TEXT",
    }
