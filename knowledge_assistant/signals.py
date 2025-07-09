from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Document, Chunk
import os
import numpy as np
from .faiss_utils import faiss_index

# PDF parsing
try:
    import PyPDF2
except ImportError:
    PyPDF2 = None
# Markdown parsing
try:
    import markdown
except ImportError:
    markdown = None
# HuggingFace embedding
try:
    from transformers import AutoTokenizer, AutoModel
    import torch
    HF_MODEL = 'sentence-transformers/all-MiniLM-L6-v2'
    tokenizer = AutoTokenizer.from_pretrained(HF_MODEL)
    model = AutoModel.from_pretrained(HF_MODEL)
except ImportError:
    tokenizer = None
    model = None

def parse_pdf(file_path):
    if not PyPDF2:
        return []
    text_chunks = []
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                text_chunks.append((text, i+1))
    return text_chunks

def parse_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    # Simple chunking: split by paragraphs
    return [(chunk, None) for chunk in text.split('\n\n') if chunk.strip()]

def parse_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    # Simple chunking: split by headers
    chunks = text.split('\n# ')
    return [(chunk, None) for chunk in chunks if chunk.strip()]

def generate_embedding(text):
    if not tokenizer or not model:
        return b''
    inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().cpu().numpy().astype(np.float32)
    return embeddings.tobytes()

@receiver(post_save, sender=Document)
def process_document(sender, instance, created, **kwargs):
    if not created:
        return
    file_path = instance.file.path
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        chunks = parse_pdf(file_path)
    elif ext in ['.md', '.markdown']:
        chunks = parse_markdown(file_path)
    else:
        chunks = parse_text(file_path)
    for order, (chunk_text, page_number) in enumerate(chunks):
        embedding = generate_embedding(chunk_text)
        chunk = Chunk.objects.create(
            document=instance,
            text=chunk_text,
            embedding=embedding,
            page_number=page_number,
            order=order
        )
        faiss_index.add_chunk(chunk) 