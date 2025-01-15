from langchain_community.document_loaders import PyMuPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

loader = PyMuPDFLoader("data/DL-824_31-DIC-1974.pdf")
docs = loader.load_and_split()

embeddings = OpenAIEmbeddings()

chroma_db = Chroma.from_documents(
    documents=docs, 
    embedding=embeddings, 
    persist_directory="data", 
    collection_name="dl_824"
)
