from pymongo import MongoClient
#from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import MongoDBAtlasVectorSearch
from langchain.document_loaders import DirectoryLoader
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from PyPDF2 import PdfReader 
import os
#from pdfplumber import pdf
#import gradio as gr
#from gradio.themes.base import Base
#import key_param

openai_api_key = os.environ.get("OPENAI_API_KEY")
mongopasswd = os.getenv('CM_MONGO_PASS')

MONGO_URI = f'mongodb+srv://cmitchem:{mongopasswd}@cluster0.pshckj2.mongodb.net/?authSourse=admin&ssl=true&retryWrites=true&w=majority&appName=Cluster0'
client = MongoClient(MONGO_URI)

'''try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)'''

#print(client.list_database_names())
db = client["city_of_fort_worth_vector_db"]
collection = db["city_of_fort_worth_vector_collection"]
#print(collection.find_one())

loader = DirectoryLoader( './sample_files', glob="./*.txt", show_progress=True)
data = loader.load()

pdf_directory = './fwcodes' 
pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]

#Load and read the PDF
#pdf_loader = PdfReader("File-1.pdf")
#pdf_loader = PdfReader("File-2.pdf")
pdf_loader = PdfReader("File-3.pdf")
# pdf_loader = PdfReader("File-4.pdf") # too long!
#pdf_loader = PdfReader("File-5.pdf")
# pdf_loader = PdfReader("File-6.pdf") # too long
# pdf_loader = PdfReader("File-7.pdf") #empty: need to make OCR file to read
#pdf_loader = PdfReader("File-8.pdf")
#pdf_loader = PdfReader("File-9.pdf") # also long, did not embed
pdf_text = ""
for page_num in range(len(pdf_loader.pages)):
    pdf_page = pdf_loader.pages[page_num]
    pdf_text += pdf_page.extract_text()

embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
vectorStore = MongoDBAtlasVectorSearch.from_documents( data, embeddings, collection=collection )

query = "explain DDR5?"
query2 = "how long before inspection for sewer videos?"

def retriever_query(query):
    llm = OpenAI(openai_api_key=openai_api_key, temperature=0)
    retriever = vectorStore.as_retriever()
    qa = RetrievalQA.from_chain_type(llm, chain_type="stuff", retriever=retriever)
    retriever_output = qa.run(query)
    return(retriever_output)

def VS_query_data(query):
    # Convert question to vector using OpenAI embeddings
    # Perform Atlas Vector Search using Langchain's vectorStore
    # similarity_search returns MongoDB documents most similar to the query    

    docs = vectorStore.similarity_search(query, K=1)
    as_output = docs[0].page_content

    # Leveraging Atlas Vector Search paired with Langchain's QARetriever

# Define the LLM that we want to use -- note that this is the Language Generation Model and NOT an Embedding Model
# If it's not specified (for example like in the code below),
# then the default OpenAI model used in LangChain is OpenAI GPT-3.5-turbo, as of August 30, 2023

    llm = OpenAI(openai_api_key=openai_api_key, temperature=0)


# Get VectorStoreRetriever: Specifically, Retriever for MongoDB VectorStore.
# Implements _get_relevant_documents which retrieves documents relevant to a query.
    retriever = vectorStore.as_retriever()

# Load "stuff" documents chain. Stuff documents chain takes a list of documents,
# inserts them all into a prompt and passes that prompt to an LLM.

    qa = RetrievalQA.from_chain_type(llm, chain_type="stuff", retriever=retriever)

# Execute the chain

    retriever_output = qa.run(query)


# Return Atlas Vector Search output, and output generated using RAG Architecture
    return as_output, retriever_output