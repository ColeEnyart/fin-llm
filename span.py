from span_marker import SpanMarkerModel
from llama_index.core import Settings, SimpleDirectoryReader

model = SpanMarkerModel.from_pretrained("tomaarsen/span-marker-mbert-base-multinerd")
# entities = model.predict("Amelia Earhart flew her single engine Lockheed Vega 5B across the Atlantic to Paris.")

documents = SimpleDirectoryReader(
    input_files=["./data/XYZ Corporation.pdf"]
).load_data()
doc_text = documents[0].__dict__['text']
text = doc_text.replace(" ", "").replace("\n", " ")
entities2 = model.predict(text)