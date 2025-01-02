from langchain_community.document_loaders import UnstructuredCSVLoader
from langchain_community.document_loaders import OnlinePDFLoader
doc_path = "data/small-list.csv"
model = "llama3.2"

if doc_path:
    loader = UnstructuredCSVLoader(file_path=doc_path)
    data = loader.load()
    print("done loading....")
else:
    print("Upload a PDF file")
    # Preview first page
content = data[0].page_content
#print(content[:100000])
#===END OF PDF INGESTION===

from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

# Split and chunk
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=300)
chunks = text_splitter.split_documents(data)
print("done splitting....")

# =======ADDING TO VECTOR DATABASE=====
import ollama
ollama.pull("nomic-embed-text")

vector_db = Chroma.from_documents(
    documents=chunks,
    embedding=OllamaEmbeddings(model="nomic-embed-text"),
    collection_name="simple-rag",
)
print("done adding to vector database....")

#====RETREIVING DATA====

from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_ollama import ChatOllama

from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers.multi_query import MultiQueryRetriever

llm = ChatOllama(model=model)

QUERY_PROMPT = PromptTemplate(
    input_variables=["question"],
    template="""You know in detail about construction equipment, 
    you have 35 years of experience identifying each equipment,
    you know product id very well.
    
}
    Original question: {question}""",
)

retriever = MultiQueryRetriever.from_llm(
    vector_db.as_retriever(), llm, prompt=QUERY_PROMPT
)
# RAG prompt
template = """Answer the question based ONLY on the following context:
{context}
Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)


res = chain.invoke(input=("""
Customer Order:

Ronark buildwell 

Site- alankar (sanand)

Safety Shoes x 7
Pawda no handle x 5
Damar x 5 box
Ply Wood 30x50m x 5
""",))


print(res)