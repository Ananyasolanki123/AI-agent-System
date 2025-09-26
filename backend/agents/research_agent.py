import os
import fitz
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain.chains import ConversationalRetrievalChain
from pydantic import BaseModel, Field
from typing import List, Dict
from docx import Document
from langchain_core.prompts import ChatPromptTemplate 

load_dotenv()


class Keywords(BaseModel):
    """A list of important keywords extracted from a document."""
    keywords: List[str] = Field(
        description="A list of 5-10 of the most important keywords and terms from the text."
    )

class ResearchQueryType(BaseModel):
    """Classifies the user's query to determine the correct action."""
    category: str = Field(
        description="The type of query, must be one of 'summary', 'keywords', 'abstract', or 'question'.",
        enum=["summary", "keywords", "abstract", "question"]
    )

class ResearchAgent:
    """
    An intelligent agent for analyzing documents. It can ingest documents,
    summarize them, extract keywords, and answer questions.
    """
    def __init__(self):
        self.llm = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.1-8b-instant",
            temperature=0
        )
        self.vector_db = None
        persist_directory = "backend/vector_store"
        if os.path.exists(persist_directory):
            self.vector_db = Chroma(
                persist_directory=persist_directory,
                embedding_function=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            )
        self.docs = []

    def ingest_document(self, file_path: str, file_type: str) -> Dict[str, str]:
        """
        Loads a PDF or DOCX file, splits it into chunks, and stores
        it in a Chroma vector database.
        """
        try:
            full_text = ""
            if file_type == 'pdf':
                doc = fitz.open(file_path)
                full_text = "".join(page.get_text() for page in doc)
                doc.close()
            elif file_type == 'docx':
                doc = Document(file_path)
                full_text = "\n".join([para.text for para in doc.paragraphs])
            else:
                return {"type": "text", "message": "Unsupported file type."}

            if not full_text.strip():
                return {"type": "text", "message": "The document is empty."}

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            self.docs = text_splitter.create_documents([full_text])
            
            embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            persist_directory = "backend/vector_store"
            
            self.vector_db = Chroma.from_documents(
                documents=self.docs,
                embedding=embeddings_model,
                persist_directory=persist_directory
            )
            return {"type": "text", "message": "Document ingested and ready for analysis."}
        except Exception as e:
            print(f"Error during document ingestion: {e}")
            return {"type": "text", "message": f"Error ingesting the document: {e}"}

    def handle_query(self, query: str) -> Dict[str, str]:
        """
        Routes the user's query to the correct handler function based on its intent.
        This is a smart router powered by a structured output LLM call.
        """
        if self.vector_db is None:
            return {"type": "text", "message": "No document has been ingested yet."}

        structured_llm = self.llm.with_structured_output(ResearchQueryType)
        
        system_prompt = """You are an expert at classifying a user's query for a research agent.
Classify the query into one of the following categories:
- 'summary': If the user asks for a summary, overview, or main points of the entire document.
- 'abstract': If the user specifically asks for the abstract.
- 'keywords': If the user asks for keywords or key terms.
- 'question': If the user is asking a specific question about the document's content. This is a fallback if no other category matches.
"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "Classify the following user query: {query}"),
        ])
        
        chain = prompt | structured_llm
        
        try:
            query_type = chain.invoke({"query": query})
            
            if query_type.category == "summary":
                return self.summarize_paper()
            elif query_type.category == "keywords":
                return self.extract_keywords()
            elif query_type.category == "abstract":
                return self.summarize_abstract()
            else:
                return self.answer_question(query)
                
        except Exception as e:
            print(f"Error classifying research query: {e}. Defaulting to Q&A.")
            return self.answer_question(query)

    def summarize_paper(self) -> Dict[str, str]:
        """
        Summarizes the entire document using a map-reduce chain to handle
        documents of any size without exceeding token limits.
        """
        summarize_chain = load_summarize_chain(self.llm, chain_type="map_reduce")
        result = summarize_chain.invoke(self.docs)
        return {"type": "text", "message": result["output_text"]}

    def summarize_abstract(self) -> Dict[str, str]:
        """Summarizes just the first chunk, which usually contains the abstract."""
        if not self.docs:
            return {"type": "text", "message": "No document content available."}
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert summarizer. Provide a detailed summary of the abstract from the following text."),
            ("human", "Text: {text}")
        ])
        chain = prompt | self.llm
        result = chain.invoke({"text": self.docs[0].page_content})
        return {"type": "text", "message": result.content}

    def extract_keywords(self) -> Dict[str, str]:
        """Extracts keywords using a structured output call to guarantee a valid list."""
        if not self.docs:
            return {"type": "text", "message": "No document content available."}

        structured_llm = self.llm.with_structured_output(Keywords)
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert at extracting keywords from a research paper."),
            ("human", "Extract the most important keywords from the following text: {text}"),
        ])
        chain = prompt | structured_llm
        
        text_for_keywords = " ".join([doc.page_content for doc in self.docs[:4]])
        result = chain.invoke({"text": text_for_keywords})
        
        return {"type": "text", "message": ", ".join(result.keywords)}

    def answer_question(self, question: str) -> Dict[str, str]:
        """Answers a question using a retrieval chain and the vector database."""
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vector_db.as_retriever(),
            return_source_documents=True
        )
        result = qa_chain.invoke({"question": question, "chat_history": []})
        return {"type": "text", "message": result["answer"]}

