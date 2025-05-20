from dart_mcp.api_clients.dart.helper import get_corp_list
from dart_mcp.db import ElasticSearchClient

INDEX_NAME = "test_index"

index_body = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "properties": {
            "corp_code": {"type": "text"},
            "stock_code": {"type": "text"},
            "corp_name": {"type": "keyword"},
            "corp_eng_name": {"type": "keyword"},
            "modify_date": {"type": "date"}
            
        }
    }
}

client = ElasticSearchClient()

client.create_index(index_name=INDEX_NAME, index_body=index_body)

company_list:list[dict[str, str]] = get_corp_list()

