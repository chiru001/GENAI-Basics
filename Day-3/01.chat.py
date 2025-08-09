from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
# Vector embedding from indexing
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large",
)

vector_db = QdrantVectorStore.from_existing_collection(
    url="http://192.168.42.133:6333/",
    collection_name = "learning Vectors",
    embedding= embedding_model,  
)


# USER take query

query = input("> ")


# vector simularity Search in DB
search_result = vector_db.similarity_search(query=query, k=3)

# Prepare context string from search results
context = "\n\n".join([result.page_content for result in search_result])

client = OpenAI()

#One short prompting
with open('./prompt/prompt.md', 'r', encoding='utf-8') as file:
    prompt_template = file.read()

    # Replace placeholder with actual context
    prompt = prompt_template.replace("{context}", context)
    
    response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages= [
        {"role":"system", "content":prompt},
        {"role": "user", "content": query}
    ]
)

print(f"🤖: {response.choices[0].message.content}")