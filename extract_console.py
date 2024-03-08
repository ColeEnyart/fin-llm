from llama_index.core import Settings
from settings import MISTRAL_API_KEY
from llama_index.llms.mistralai import MistralAI
from llama_index.embeddings.mistralai import MistralAIEmbedding
import compliance.extract as extract

api_key = MISTRAL_API_KEY
Settings.llm = MistralAI(api_key=api_key, model="mistral-tiny")
Settings.embed_model = MistralAIEmbedding(model_name="mistral-embed", api_key=api_key)
PERSIST_DIR = "./compliance/storage"
INPUT_FILES = ["./compliance/data/test.txt"]

response = extract.persist_or_load(PERSIST_DIR, INPUT_FILES)
print(f"\n\n{response}\n\n")
response2 = extract.query_db()
print(f"\n\n{response2}\n\n")

# https://docs.llamaindex.ai/en/stable/examples/index_structs/struct_indices/SQLIndexDemo.html