from typing import Generator, Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from langchain.vectorstores import VectorStore, Chroma
from langchain.embeddings import GPT4AllEmbeddings
from langchain.chains import ConversationalRetrievalChain
from chromadb import HttpClient as ChromaHttpClient
from jose import JWTError, jwt

from backend import service, schemas, crud, models
from backend.db.database import SessionLocal
from backend.config.settings import settings
from backend.util import llms as llm_utils
from backend.security.oauth2_schemes import OAuth2Bearer


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_chat_session_service(db: Annotated[Session, Depends(get_db)]) -> service.ChatSessionService:
    return service.ChatSessionService(db)


def get_user_service(db: Annotated[Session, Depends(get_db)]) -> service.UserService:
    return service.UserService(db)


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


def get_conversation_chain(
        vector_store: Annotated[VectorStore, Depends(get_vector_store)]) -> ConversationalRetrievalChain:
    return llm_utils.build_conversation_chain(vector_store)


oauth2_scheme = OAuth2Bearer(auto_error=True)


async def get_current_user(db: Annotated[Session, Depends(get_db)],
                           token: Annotated[str, Depends(oauth2_scheme)]) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        token_data = schemas.TokenData.model_validate(payload, strict=False)
        if token_data.user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = crud.user.get(db=db, id=token_data.user_id)
    if user is None:
        raise credentials_exception
    return user
