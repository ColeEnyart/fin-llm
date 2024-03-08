from llama_index.core import Settings
from settings import MISTRAL_API_KEY
from llama_index.llms.mistralai import MistralAI
from llama_index.embeddings.mistralai import MistralAIEmbedding
import llamaindex.pipeline as pipeline

api_key = MISTRAL_API_KEY
INPUT_DIR = "./data/10k"
Settings.llm = MistralAI(api_key=api_key, model="mistral-tiny")
Settings.embed_model = MistralAIEmbedding(model_name="mistral-embed", api_key=api_key)

# select ->  milvus | neo4jvector
vector_db = "milvus"
collection_name = "llamalection"

# --env=NEO4J_AUTH=none auth is disabled from docker run
# but username and password are required for Neo4jVectorStore __init__
username = "neo4j"
password = "pleaseletmein"
url = "bolt://localhost:7687"
embedding_dimension = 1024

vector_store = pipeline.create_vector_store(
    vector_db, embedding_dimension, collection_name, username, password, url
)

# save_index first and then you can load_index from db
index = pipeline.save_index(vector_store, INPUT_DIR)
# index = pipeline.load_index(vector_store)

query = "how much revenue did Uber make vs lyft?"
response = pipeline.query_index(index, query)
pipeline.print_response(response)


# use docker desktop
# https://www.docker.com/products/docker-desktop/

# milvus db
# https://docs.llamaindex.ai/en/stable/examples/vector_stores/MilvusIndexDemo.html
# terminal -> fin-llm/llamaindex
# docker compose up -d

# neo4j db
# https://docs.llamaindex.ai/en/stable/examples/vector_stores/Neo4jVectorDemo.html
# https://hub.docker.com/_/neo4j/

# docker volume create neo4jdata
# docker run \
#     --name=neo4j \
#     --publish=7474:7474 --publish=7687:7687 \
#     --volume=neo4jdata:/data \
#     --env=NEO4J_AUTH=none \
#     neo4j

# http://localhost:7474
