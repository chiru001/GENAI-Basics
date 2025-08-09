from openai import OpenAI
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()

# Load the pdf file 
file_path = "./Chiranjeevi_Dronamraju.pdf"
loader = PyPDFLoader(file_path)
docs = loader.load()

# CHUNCKING THE DDOCS
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=20,
)
split_docs = text_splitter.split_documents(documents=docs)

# Vector embedding
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large",
)

# using [embedding_model] create embedding of [split_docs] and store in DB

vector_store = QdrantVectorStore.from_documents(
    documents = split_docs,
    url="http://192.168.42.133:6333/",
    collection_name = "learning Vectors",
    embedding= embedding_model,   
)

print("Indexing of document is done.........")