from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from settings import MISTRAL_API_KEY
from llama_index.llms.mistralai import MistralAI
from llama_index.embeddings.mistralai import MistralAIEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.extractors.entity import EntityExtractor
from llama_index.core.ingestion import IngestionPipeline

# api_key = MISTRAL_API_KEY
# Settings.llm = MistralAI(api_key=api_key, model="mistral-tiny")
# Settings.embed_model = MistralAIEmbedding(model_name="mistral-embed", api_key=api_key)

entity_extractor = EntityExtractor(
    prediction_threshold=0.5,
    label_entities=False,  # include the entity label in the metadata (can be erroneous)
    device="cpu",  # set to "cuda" if you have a GPU
)

node_parser = SentenceSplitter()
transformations = [node_parser, entity_extractor]

documents = SimpleDirectoryReader(
    input_files=["./data/XYZ Corporation.pdf"]
).load_data()
text = documents[0].__dict__['text'].replace(" ", "").replace("\n", " ")
documents[0].__dict__['text'] = text
pipeline = IngestionPipeline(transformations=transformations)
nodes = pipeline.run(documents=documents)
entities = nodes[0].metadata['entities']
# index = VectorStoreIndex(nodes=nodes)

# https://docs.llamaindex.ai/en/stable/examples/metadata_extraction/EntityExtractionClimate.html
# https://cookbook.openai.com/examples/named_entity_recognition_to_enrich_text
# https://docs.llamaindex.ai/en/stable/examples/output_parsing/df_program.html