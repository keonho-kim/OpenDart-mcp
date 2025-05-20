from typing import Any

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from dart_mcp.db.schema import DartCorpList
from dart_mcp.settings.config import DB_INSTANCE


async def find_company_corp_code_by_name(
    corp_name: str, k: int = 10
) -> list[dict[str, Any]]:
    """
    회사명을 이용하여 가장 유사한 회사 정보를 우선적으로 정렬하여 조회합니다.

    Args:
        corp_name (str): 조회할 회사명
        k (int): 조회할 회사 수. 기본값은 10입니다.

    Returns:
        List[Dict[str, Any]]: 조회된 회사 정보를 유사도 순으로 정렬한 딕셔너리 리스트.
                               각 항목은 회사 정보를 담은 딕셔너리입니다.
                               결과가 없으면 빈 리스트를 반환합니다.
    """
    search_term = f"%{corp_name}%"
    sql_query = f"""
        SELECT corp_code, corp_name, corp_eng_name, stock_code
        FROM {DartCorpList.TABLE_NAME} 
        WHERE corp_name LIKE ?
    """

    with DB_INSTANCE as db:
        db_results = db.fetch_all(sql_query=sql_query, params=(search_term,))

    if not db_results:
        return []

    candidate_corp_names = [row["corp_name"] for row in db_results]

    all_names = [corp_name] + candidate_corp_names

    try:
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(all_names)
        cosine_sim_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])[0]

        scored_results = []
        for i, score in enumerate(cosine_sim_scores):
            scored_results.append((score, db_results[i]))

        scored_results.sort(key=lambda x: x[0], reverse=True)

        return [row for _, row in scored_results][:k]

    except Exception as e:
        print(f"Error during similarity calculation: {e}. Returning original order.")
        return db_results
