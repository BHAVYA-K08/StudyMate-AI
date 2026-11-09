from sentence_transformers import CrossEncoder
from functools import lru_cache

@lru_cache(maxsize = 1)
def get_reranker():
    """LOAD AND RETURN LOCAL CROSS-ENCODER MODEL"""

    model = CrossEncoder(
        "cross-encoder/ms-marco-MiniLM-L-6-v2",
        device = "cpu"
    )

    return model
