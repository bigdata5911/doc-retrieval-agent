from langchain.tools import Tool
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from app.ai.utils import load_faq_documents
import os

def get_faq_tool():
    FAQ_DIR = os.path.join(os.path.dirname(__file__), '../../../data/faqs')
    faq_docs = load_faq_documents(FAQ_DIR)
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_texts = []
    metadatas = []
    for doc in faq_docs:
        for chunk in text_splitter.split_text(doc['content']):
            split_texts.append(chunk)
            metadatas.append({'source': doc['filename']})
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = FAISS.from_texts(split_texts, embeddings, metadatas=metadatas)
    def faq_search_func(q):
        results = vectorstore.similarity_search(q, k=2)
        return '\n'.join([f"{doc.metadata['source']}: {doc.page_content}" for doc in results])
    return Tool(
        name="faq_search",
        description="Useful for answering questions from the FAQ documents.",
        func=faq_search_func,
    ) 