from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
)
from sqlalchemy import create_engine
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.core import SQLDatabase
import os


def persist_or_load(PERSIST_DIR, INPUT_FILES):
    if not os.path.exists(PERSIST_DIR):
        documents = SimpleDirectoryReader(input_files=INPUT_FILES).load_data()
        index = VectorStoreIndex.from_documents(documents, show_progress=True)
        index.storage_context.persist(persist_dir=PERSIST_DIR)
    else:
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        index = load_index_from_storage(storage_context)

    query_engine = index.as_query_engine()
    response = query_engine.query(
        "what are the names of the required documents and when are they due?"
    )
    return response


def query_db():
    database_file_path = "compliance/compliance.db"
    engine = create_engine(f"sqlite:///{database_file_path}")
    sql_database = SQLDatabase(engine, include_tables=["documents"])
    query_engine = NLSQLTableQueryEngine(
        sql_database=sql_database, tables=["documents"]
    )

    query_str = "Are all required documents present by their due date?"
    response = query_engine.query(query_str)
    return response
