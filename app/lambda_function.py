import json
import os

from dotenv import load_dotenv
from langchain_community.retrievers import WikipediaRetriever
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq


def format_docs(docs: list[Document]) -> str:
    f_docs = "\n\n".join(doc.page_content for doc in docs)
    print(f_docs)
    return f_docs


load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")


llm = ChatGroq(model="llama-3.1-70b-versatile", api_key=GROQ_API_KEY)


def base_chain():
    prompt = ChatPromptTemplate.from_template(
        """
        Responda à pergunta do usuário baseada exclusivamente no contexto fornecido. De forma sucinta em até 10 palavras.
        Caso os documentos retornados não tenham relação com a questão "{question}", responda: 'IIIH RAPAZ, deu RUIM!'
        
        Context: {context}
        
        Question: {question}
        """
    )

    retriever = WikipediaRetriever(lang="pt")

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain


def handler(event, context):
    """
    handler
    """
    question = event.get("question")

    if not question:
        return json.dumps({"statusCode": 400, "message": "Missing question parameter"})

    chain = base_chain()
    response = chain.invoke(question)

    return json.dumps({"statusCode": 200, "response": response})
