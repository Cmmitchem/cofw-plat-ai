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

pdf_text = ""
paragraphs = []
responses = []
temp_list = []

# NEED TO CALL THIS FILE AND SEND THE plat name from the server.py flask api to the pdf_loader
# possibly create a function to accpet the PDF input 
def load_pdf(path):
    pdf_loader = PdfReader("The Road Not Taken Poem.pdf")
    #pdf_loader = PdfReader(path)
    pdf_text = ""
    #paragraphs = []
    #responses = []
   # temp_list = []
    
    for page_num in range(len(pdf_loader.pages)):
        pdf_page = pdf_loader.pages[page_num]
        pdf_text += pdf_page.extract_text()
    
    split_text()
    create_embeddings()
    send_chunks()
    #pdf_text

def split_text():
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2048,
        chunk_overlap=64
        )
    split_texts = text_splitter.split_text(pdf_text)
    for text in split_texts:
        paragraphs.extend(text.split('\n')) 


def create_embeddings():
    #paragraphs
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = SentenceTransformer(model_name)
    for paragraph in paragraphs:
            response = embeddings.encode(paragraph, convert_to_tensor=False)
            responses.append((paragraph, response))
    #responses 
    for idx, i in enumerate(responses):
        chunk_name, embedding_array = responses[idx]
        list_embedding_array = embedding_array.tolist()
        temp_list.append({"chunk_name":chunk_name,"embedding_array":list_embedding_array})
#temp_list   

#examples of how 1 pair of chunk_name and embedding_array generated
#responses[0]

def send_chunks():
    # fix the index out of range error that resuts from the responses[0] call (possibly add a for loop?)
    for i in range(len(responses)):
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
        file_path = 'embeddings.txt'   

        with open(file_path, 'w') as file: 
                file.write(response_2.text)
