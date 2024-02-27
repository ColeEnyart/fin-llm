from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index.vector_stores.milvus import MilvusVectorStore
from llama_index.vector_stores.neo4jvector import Neo4jVectorStore
import pandas as pd


def create_vector_store(vector_db, dim, collection_name, *args):
    username, password, url = args
    dim = dim
    if vector_db == "milvus":
        return MilvusVectorStore(collection_name=collection_name, dim=dim)
    if vector_db == "neo4jvector":
        return Neo4jVectorStore(username, password, url, dim)


def save_index(vector_store, INPUT_DIR):
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    documents = SimpleDirectoryReader(INPUT_DIR).load_data()
    return VectorStoreIndex.from_documents(
        documents, storage_context, show_progress=True
    )


def load_index(vector_store):
    return VectorStoreIndex.from_vector_store(vector_store=vector_store)


def query_index(index, query):
    query_engine = index.as_query_engine()
    return query_engine.query(query)


def print_response(response):
    print(f"\n\n{response}\n\n")
    node_ids, page_labels, file_names, scores = [], [], [], []
    for source in response.source_nodes:
        node_ids.append(source.node.node_id)
        page_labels.append(source.node.metadata["page_label"])
        file_names.append(source.node.metadata["file_name"])
        scores.append(source.score)
    df = pd.DataFrame(
        {
            "node_id": node_ids,
            "page_label": page_labels,
            "file_name": file_names,
            "score": scores,
        }
    )
    print(df)
