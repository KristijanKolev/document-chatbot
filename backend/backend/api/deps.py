from typing import Generator, Annotated

from fastapi import Depends
from sqlalchemy.orm import Session
from langchain.vectorstores import VectorStore, Chroma
from langchain.embeddings import GPT4AllEmbeddings
from langchain.chains import ConversationalRetrievalChain
from chromadb import HttpClient as ChromaHttpClient

from backend import service
from backend.db.database import SessionLocal
from backend.config.settings import settings
from backend.util import llms as llm_utils


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_chat_session_service(db: Annotated[Session, Depends(get_db)]) -> service.ChatSessionService:
    return service.ChatSessionService(db)


def get_vector_store() -> Chroma:
    chroma_client = ChromaHttpClient(
        host=settings.CHROMA_HOST,
        port=settings.CHROMA_PORT
    )

    return Chroma(
        client=chroma_client,
        collection_name='punic_wars_local',
        embedding_function=GPT4AllEmbeddings()
    )


def get_llm_service(vector_store: Annotated[VectorStore, Depends(get_vector_store)]) -> ConversationalRetrievalChain:
    return llm_utils.build_conversation_chain(vector_store)
