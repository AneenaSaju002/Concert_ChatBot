# Concert_ChatBot
A context-aware FAQ chatbot built using LangChain, Google Gemini 1.5 Flash, FAISS, and HuggingFace embeddings. It answers real-time queries on Candlelight Concert FAQs.


Tools & Libraries:
   LLM: Google’s Gemini-1.5-Flash via langchain_google_genai
   Vector DB: FAISS
   Embeddings: BAAI/bge-small-en from HuggingFace
   Data Loader: CSVLoader from LangChain for structured FAQ ingestion
   LangChain Components:
     *ConversationalRetrievalChain
     *PromptTemplate
     *Retriever with score threshold for relevance
   API Key Management: .env with dotenv
   
Use Case:
 Perfect for any business looking to automate repetitive customer support with an intelligent, context-aware chatbot that leverages retrieval-augmented generation (RAG) to deliver accurate, real-time responses. 🚀
