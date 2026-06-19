# functions_src/faq_engine.py
import os
import logging
from typing import Optional

from langchain_cohere import CohereEmbeddings
from langchain_chroma.vectorstores import Chroma
from langchain_core.documents import Document

# Importa os dados puros do FAQ diretamente do arquivo correspondente
from data.faq import novabank_faq

# Configurações do FAQ
CHROMA_FAQ_DIR = "./chroma_db_faq"          # Banco de dados FAQ
COLLECTION_FAQ_NAME = "faq_novabank_data"   # Nome da Coleção

# Limiar crítico: só aceita FAQ se a distância vetorial for pequena (similaridade alta)
# Para distância L2 (padrão do Chroma), menor score = mais similar. 

# Baseado em testes nessa base de dados chegamos ao valor de aproximadamente **0.5** de similaridade (Modelo embed-4.0 -> Cohere)
FAQ_THRESHOLD = 0.5

class FaqEngine:
    def __init__(self, embedding_model: CohereEmbeddings):
        self.embedding_model = embedding_model
        self.vector_store = self._get_or_create_store()

    def _get_or_create_store(self) -> Chroma:
        """Inicializa ou carrega o banco vetorial de FAQ persistente."""
        if os.path.exists(CHROMA_FAQ_DIR) and os.listdir(CHROMA_FAQ_DIR):
            logging.info("Carregando banco vetorial de FAQ existente...")
            return Chroma(
                persist_directory=CHROMA_FAQ_DIR,
                embedding_function=self.embedding_model,
                collection_name=COLLECTION_FAQ_NAME
                
            )
        else:
            logging.info("Criando novo banco vetorial de FAQ a partir de data/faq.py...")
            
            # Prepara os documentos LangChain a partir da lista de dicionários
            documents = []
            for item in novabank_faq:
                # O conteúdo da busca é a PERGUNTA
                content = item["pergunta"]
                # A RESPOSTA vai nos metadados para recuperação rápida
                metadata = {"pergunta": item["pergunta"], "resposta": item["resposta"]}
                documents.append(Document(page_content=content, metadata=metadata))
            
            # Cria e persiste o banco
            store = Chroma.from_documents(
                documents=documents,
                embedding=self.embedding_model,
                persist_directory=CHROMA_FAQ_DIR,
                collection_name=COLLECTION_FAQ_NAME
            )
            logging.info(f"Banco de FAQ criado com {len(novabank_faq)} Q&As.")
            return store

    def check_cache(self, query: str) -> Optional[str]:
        """
        Realiza busca semântica no banco de FAQ.
        Retorna a resposta se houver match forte (score < threshold), senão retorna None.
        """
        # Busca por similaridade com score (distância)
        results = self.vector_store.similarity_search_with_score(query, k=1)        
        
        if not results:            
            return None
        
        doc, score = results[0]
        
        # Log para calibração do threshold
        logging.info(f"FAQ Check - Query: '{query[:50]}...' - Best Match: '{doc.page_content[:50]}...' - Score: {score:.4f}")                
        # Se estiver dentro do limiar de segurança
        if score < FAQ_THRESHOLD:
            logging.info("Match de FAQ encontrado. Retornando resposta homologada.")
            return doc.metadata.get("resposta")
        
        return None        