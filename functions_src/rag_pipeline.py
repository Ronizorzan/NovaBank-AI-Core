# === Standard Library Imports ===
import os
import logging
from dotenv import load_dotenv
from asyncio import Lock


# === Langchain Imports ===
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.pdf import PyMuPDFLoader
from langchain_community.vectorstores.chroma import Chroma


load_dotenv()  # Load environment variables from .env file

    
class RagPipeline:
    def __init__(self, path, embedding_model):
        self.path = path
        self.vector_store = None
        self.embedding_model = embedding_model

    def load_documents(self):
        documents = []
        if os.path.isdir(self.path):
            for filename in os.listdir(self.path):
                file_path = os.path.join(self.path, filename)
                if os.path.isfile(file_path) and file_path.endswith("pdf"):
                    loader = PyMuPDFLoader(file_path)
                    documents.extend(loader.load())
                else:                
                    logging.info(f"O arquivo {file_path} não é um arquivo válido. Ignorando ...")
                    continue
                    #raise ValueError(f"O caminho {file_path} não contém um arquivo válido.")
        elif os.path.isfile(self.path):
            loader = PyMuPDFLoader(self.path)
            documents = loader.load()
        else:
            raise FileNotFoundError(f"O caminho {self.path} não existe.")
        
        logging.info(f"Total de documentos carregados: {len(documents)}")
        return documents

    def split_documents(self, documents, chunk_size=750, chunk_overlap=100):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            add_start_index=True,
            separators=["\n\n", "\n", " ", "."]
        )
        return self.text_splitter.split_documents(documents)
    
    def embed_chunks(self, chunks):
        """Get context from a vactorstore"""        
        self.vector_store = Chroma.from_documents(chunks, self.embedding_model)
        return self.vector_store

    def run(self, chunk_size=750, chunk_overlap=100):
        """Executa todo o pipeline"""
        documents = self.load_documents()
        chunks = self.split_documents(documents, chunk_size, chunk_overlap)
        vectorstore = self.embed_chunks(chunks)
        logging.info("Pipeline concluído com sucesso")
        return vectorstore
    

# --- Tempo Médio de Resposta da aplicação ---
class AppState:
    total_requests = 0
    total_duration_seconds = 0.0
    lock = Lock() # Para garantir atomicidade nas atualizações

    @classmethod
    async def update_state(cls, duration):
        async with cls.lock:
            cls.total_requests += 1
            cls.total_duration_seconds += duration

        
    @classmethod
    def get_average_ms(cls):
        if cls.total_requests == 0:
            return 0
    
        avg_seconds = cls.total_duration_seconds / cls.total_requests 
        return int(avg_seconds * 1000)  # O retorno é em milisegundos
        


        


    


