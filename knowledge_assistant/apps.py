from django.apps import AppConfig


class KnowledgeAssistantConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'knowledge_assistant'

    def ready(self):
        import knowledge_assistant.signals
        from knowledge_assistant.faiss_utils import build_faiss_index
        build_faiss_index()
