from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
    Settings,
)
from llama_index.llms.mistralai import MistralAI
from llama_index.embeddings.mistralai import MistralAIEmbedding
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")
PERSIST_DIR = "./storage"
INPUT_DIR = "./data/10k"

Settings.llm = MistralAI(api_key=api_key, model="mistral-tiny")
Settings.embed_model = MistralAIEmbedding(model_name="mistral-embed", api_key=api_key)

if not os.path.exists(PERSIST_DIR):
    documents = SimpleDirectoryReader(INPUT_DIR).load_data()
    index = VectorStoreIndex.from_documents(documents, show_progress=True)
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)

query_engine = index.as_query_engine()
response = query_engine.query("how much revenue did Uber make vs lyft?")
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
