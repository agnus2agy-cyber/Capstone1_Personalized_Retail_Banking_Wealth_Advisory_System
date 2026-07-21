import re
import psycopg
import os
from core.db import get_vector_store
from psycopg.rows import dict_row


_raw_conn = os.getenv("PG_CONNECTION_STRING_FTS")


_KEYWORD_PATTERNS = [
    r"[A-Z]{2,}-\d{4}-\w+",  # policy/ticket codes: POL-2024-HR-007
    r"\b[A-Z]{2,5}\b",  # abbreviations: LTA, CTC, ESI
    r"\d{6,}",  # long numeric IDs / employee IDs
    r"\b[A-Z][A-Za-z]+\s+[A-Z]?\d+(?:-[A-Z0-9]+)?[A-Z]*\b",
]

_KEYWORD_RE = re.compile("|".join(_KEYWORD_PATTERNS))


def query_documents(query: str, k: int, collection_name: str = "personal_retail_banking"):
    print(query)

    # detect the search mode for the query
    mode = _detect_mode(query)
    if mode == "fts":
        # call _search_fts function
        print("FTS needed")
        return _search_fts(query, k, collection_name)

    if mode == "vector":
        # call _search_vector function
        print("Vector search needed")
        return _search_vector(query, k, collection_name)

    if mode == "hybrid":
        # call _search_hybrid function
        print("Hybrid search needed")
        return _search_hybrid(query, k, collection_name)


def _search_fts(query: str, k: int, collection_name: str):
    """Keyword search against the stored chunks using Postgres' tsvector/tsquery/ts_rank"""
    sql = """
        SELECT
            e.document                                               AS content,
            e.cmetadata                                              AS metadata,
            ts_rank(
                to_tsvector('english', e.document),
                plainto_tsquery('english', %(query)s)
            )                                                        AS fts_rank
        FROM  langchain_pg_embedding  e
        JOIN  langchain_pg_collection c ON c.uuid = e.collection_id
        WHERE c.name = %(collection)s
          AND to_tsvector('english', e.document)
              @@ plainto_tsquery('english', %(query)s)
        ORDER BY fts_rank DESC
        LIMIT %(k)s;
    """

    with psycopg.connect(_raw_conn, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, {"query": query, "collection": collection_name, "k": k})
            rows = cur.fetchall()

    output = [
        {
            "content": row["content"],
            "metadata": row["metadata"],
            "fts_rank": round(float(row["fts_rank"]), 4),
        }
        for row in rows
    ]


    return output


def _search_vector(query: str, k: int, collection_name: str):
    vector_store = get_vector_store(collection_name)
    docs = vector_store.similarity_search(query, k)

    output = [
        {
            "content": doc.page_content,
            "metadata": doc.metadata,
        }
        for doc in docs
    ]

    return output


def _search_hybrid(query: str, k: int, collection_name: str):
    """Merge vector and fts results using RRF (Reciprocal Rank Fusion)
    Chunks appearing in both search results will rank higher than those in only one
    The constant 60 prevents top-ranked outputs from dominating
    How RRF scores for a chunk = sum of 1/(rank + 60)
    """
    print("Running Hybrid Search")

    vector_search_results = _search_vector(query, 5, collection_name)
    fts_results = _search_fts(query, 5, collection_name)

    rrf_scores: dict[str, float] = {}
    chunk_map: dict[str, dict] = {}

   
    for rank, doc in enumerate(vector_search_results):
        
        key = doc["content"][:120]
        
        rrf_scores[key] = rrf_scores.get(key, 0) + 1 / (60 + rank + 1)
       
        chunk_map[key] = {"content": doc["content"], "metadata": doc["metadata"]}

   
    for rank, item in enumerate(fts_results):
        key = item["content"][:120]
        rrf_scores[key] = rrf_scores.get(key, 0) + 1 / (60 + rank + 1)
        chunk_map[key] = {"content": item["content"], "metadata": item["metadata"]}

  
    ranked = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
    print(ranked)
    return [chunk_map[key] for key, _ in ranked[:k]]


def _detect_mode(query: str):
    stripped_query = query.strip()
   
    if _KEYWORD_RE.search(stripped_query):
        return "fts"

  
    if len(stripped_query.split()) <= 3:
        return "hybrid"

   
    return "vector"


if __name__ == "__main__":
    
    query = "Balanced Advantage Fund "
    results = query_documents(query, k=5)

    print(f"\nTop {len(results)} results for: '{query}'\n{'=' * 60}")
    for i, item in enumerate(results, 1):
        metadata = item["metadata"]
        print(f"""\n[{i}] Source: {metadata.get('source')} | 
              Page: {metadata.get('page')}""")
        print(item["content"])


