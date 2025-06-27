from langchain_community.vectorstores import FAISS
from langchain.document_loaders.csv_loader import CSVLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv


load_dotenv()


llm = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-flash",
    google_api_key=os.environ["GOOGLE_API_KEY"],
    temperature=0.7
)


embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en")


vectordb_file_path = "faiss_index"


def create_vector_db():
    loader = CSVLoader(file_path='candlelight_faq.csv', source_column="prompt")
    data = loader.load()
    vectordb = FAISS.from_documents(documents=data, embedding=embeddings)
    vectordb.save_local(vectordb_file_path)


def get_qa_chain():
    vectordb = FAISS.load_local(
        vectordb_file_path,
        embeddings,
        allow_dangerous_deserialization=True
    )
    retriever = vectordb.as_retriever(score_threshold=0.7)


    condense_prompt = PromptTemplate.from_template(
        """Given the following chat history and a follow-up question, rephrase the question to be standalone.

Chat History:
{chat_history}

Follow-up question:
{question}"""
    )

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        condense_question_prompt=condense_prompt,
        return_source_documents=True
    )

    return chain

if __name__ == "__main__":
    create_vector_db()
    chain = get_qa_chain()
    result = chain({
        "question": "Do you have javascript course?",
        "chat_history": []
    })
    print(result["answer"])

