#https://medium.com/@yashashm77/querying-a-pdf-file-using-llm-models-and-sentence-transformer-b3d4d0b40f7d

from PyPDF2 import PdfReader 
from pdfplumber import pdf
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer, util

import time
import requests
import json


from numba import jit, cuda
import numpy as np  

pdf_loader = PdfReader("The Road Not Taken Poem.pdf")
pdf_text = ""
for page_num in range(len(pdf_loader.pages)):
    pdf_page = pdf_loader.pages[page_num]
    pdf_text += pdf_page.extract_text()

pdf_text

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2048,
    chunk_overlap=64
    )
split_texts = text_splitter.split_text(pdf_text)
paragraphs = []
for text in split_texts:
    paragraphs.extend(text.split('\n')) 

#paragraphs

model_name = "sentence-transformers/all-MiniLM-L6-v2"
embeddings = SentenceTransformer(model_name)

#embeddings

responses = []
for paragraph in paragraphs:
        response = embeddings.encode(paragraph, convert_to_tensor=False)
        responses.append((paragraph, response))
#responses 

temp_list = []
for idx, i in enumerate(responses):
    chunk_name, embedding_array = responses[idx]
    list_embedding_array = embedding_array.tolist()
    temp_list.append({"chunk_name":chunk_name,"embedding_array":list_embedding_array})
#temp_list   

#examples of how 1 pair of chunk_name and embedding_array generated
responses[0]

chunk_name, embedding_array = responses[0]
chunk_name
embedding_array

list_embedding_array = embedding_array.tolist()
list_embedding_array
result = {"chunk_name":chunk_name,"embedding":list_embedding_array}
result

payload2 = json.dumps({
    "collection":"Test",
    "database":"Test",
    "dataSource":"Cluster0",
    "documents": temp_list #put in list
})

headers = {
  'Content-Type': 'application/json',
  'Access-Control-Request-Headers': '*',
  'api-key': 'Phu3o72HM9itPsmX6e1Tb4S0aAuwyz8BrFmWPalg9HJs9vCRZ45YktglrKnrvIxg',
}

url_insert = "https://us-east-2.aws.data.mongodb-api.com/app/data-bvuiv/endpoint/data/v1/action/insertMany"

#response_2 = requests.post(url_insert, headers=headers, json=data_1)
response_2 = requests.request("POST", url_insert, headers=headers, data=payload2)
print(response_2.text)