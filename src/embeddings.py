from langchain_huggingface import HuggingFaceEmbeddings
from functools import lru_cache

@lru_cache(maxsize = 1)
def get_embedding_model():
    """LOAD THE LOCAL SENTENCE TRANSFORMER'S EMBEDDING MODEL."""

    embeddings = HuggingFaceEmbeddings(

        model_name = "sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs = {"device" : "cpu"},
        encode_kwargs = {"normalize_embeddings" : True}
    )

    return embeddings