import re
import psycopg
import os
from core.db import get_vector_store
from psycopg.rows import dict_row
from langchain_core.tools import tool

_raw_conn = os.getenv("PG_CONNECTION_STRING_FTS")


def _search_fts(query: str, k: int, collection_name: str):
    """Search the retail banking knowledge base using full-text keyword search."""
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
    """Search the retail banking knowledge base using semantic similarity."""
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
    """Search the retail banking knowledge base using hybrid search
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

@tool
def search_vector(query: str):
    """Search the retail banking knowledge base using semantic similarity."""
    return _search_vector(
        query=query,
        k=5,
        collection_name="financial_advisor_support_desk"
    )

@tool
def search_fts(query: str):
    """Search the retail banking knowledge base using keyword search."""
    return _search_fts(
        query=query,
        k=5,
        collection_name="financial_advisor_support_desk"
    )


@tool
def search_hybrid(query: str):
    """Search the retail banking knowledge base using hybrid search."""
    return _search_hybrid(
        query=query,
        k=5,
        collection_name="financial_advisor_support_desk"
    )
