from langchain.chains import ConversationalRetrievalChain, StuffDocumentsChain, LLMChain
from langchain.vectorstores import VectorStore
from langchain.chat_models.base import BaseChatModel
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate


def build_conversation_chain(vector_store: VectorStore) -> ConversationalRetrievalChain:
    llm = ChatOpenAI(temperature=0)
    docs_chain = _build_docs_chain(llm)
    questions_chain = _build_question_generator_chain(llm)

    return ConversationalRetrievalChain(
        combine_docs_chain=docs_chain,
        question_generator=questions_chain,
        retriever=vector_store.as_retriever(),
    )


def _build_docs_chain(llm: BaseChatModel) -> StuffDocumentsChain:
    # Used for combining documents in a single context input
    document_prompt = PromptTemplate(
        input_variables=["page_content"],
        template="{page_content}"
    )

    d_combine_template = """Use the following pieces of context to answer the question at the end. Provide only the needed information without any preface. If you don't know the answer, just say that you don't know, don't try to make up an answer.
    \n\n{context}
    \n\nQuestion: {question}
    \nHelpful Answer:"""

    d_combine_prompt = PromptTemplate.from_template(d_combine_template)

    stuff_llm_chain = LLMChain(llm=llm, prompt=d_combine_prompt)
    return StuffDocumentsChain(
        llm_chain=stuff_llm_chain,
        document_prompt=document_prompt,
        document_variable_name='context'
    )


def _build_question_generator_chain(llm: BaseChatModel) -> LLMChain:
    # This controls how the standalone question is generated.
    # Should take `chat_history` and `question` as input variables.

    q_generator_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language.
    \n\nChat History:
    \n{chat_history}
    \nFollow Up Input: {question}
    \nStandalone question:"""

    q_generator_prompt = PromptTemplate.from_template(q_generator_template)
    return LLMChain(llm=llm, prompt=q_generator_prompt)
