from transformers import AutoTokenizer, AutoModel, pipeline

# Download embedding model
print('Downloading embedding model (sentence-transformers/all-MiniLM-L6-v2)...')
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
print('Embedding model downloaded.')

# Download LLM for answer generation
print('Downloading LLM (distilgpt2)...')
llm_pipe = pipeline('text-generation', model='distilgpt2')
print('LLM downloaded.')
