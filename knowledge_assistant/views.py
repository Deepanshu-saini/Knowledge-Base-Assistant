from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import Document
from .serializers import DocumentSerializer
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .faiss_utils import faiss_index, EMBEDDING_DIM
from .models import Chunk
import numpy as np

# Create your views here.

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    parser_classes = (MultiPartParser, FormParser)

# Use the same embedding model as in signals.py
try:
    from transformers import AutoTokenizer, AutoModel
    import torch
    HF_MODEL = 'sentence-transformers/all-MiniLM-L6-v2'
    tokenizer = AutoTokenizer.from_pretrained(HF_MODEL)
    model = AutoModel.from_pretrained(HF_MODEL)
except ImportError:
    tokenizer = None
    model = None

class AskQuestionView(APIView):
    def post(self, request):
        question = request.data.get('question')
        if not question:
            return Response({'error': 'No question provided.'}, status=400)
        if not tokenizer or not model:
            return Response({'error': 'Embedding model not available.'}, status=500)
        # Generate embedding for the question
        inputs = tokenizer(question, return_tensors='pt', truncation=True, max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)
            query_emb = outputs.last_hidden_state.mean(dim=1).squeeze().cpu().numpy().astype(np.float32)
        # Search FAISS for top 5 chunks
        top_chunks = faiss_index.search(query_emb, top_k=5)
        results = []
        for chunk in top_chunks:
            source = f"{chunk.document.name}"
            if chunk.page_number:
                source += f" - Page {chunk.page_number}"
            results.append({
                'text': chunk.text,
                'source': source
            })
        return Response({'chunks': results})
