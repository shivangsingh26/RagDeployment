#SUMMARY OF BELOW CODE 
# Loads PDF documents from a specified folder (data).
# Splits the documents into smaller chunks (1000 characters each).
# Generates embeddings for the document chunks using AWS Bedrock's Titan embedding model.
# Stores these embeddings in a FAISS vector database, saving the index locally for future use, like document similarity search or question answering over documents.


from langchain_community.document_loaders import PyPDFDirectoryLoader #FOR LOADING DATA
from langchain.text_splitter import RecursiveCharacterTextSplitter #FOR SPLITTING DATA INTO CHUNKS
from langchain_community.vectorstores import FAISS #FOR CREATING VECTOR DATABASE
from langchain_aws import BedrockEmbeddings #FOR CREATING EMBEDDINGS
from langchain.llms import Bedrock #FOR CREATING LLM

import boto3


#BOTO CLIENT FOR CONNECTING TO AWS BEDROCK
bedrock = boto3.client(service_name="bedrock-runtime")
bedrock_embeddings = BedrockEmbeddings(model_id = "amazon.titan-embed-text-v2:0", client= bedrock) #Embedding done using Titan Embedding Model

#FUNCTION TO LOAD DATA
def data_ingestion():
    loader = PyPDFDirectoryLoader("data")
    documents = loader.load()

    text_splitter =RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0) #each chunk is 1000 characters long
    text_splitter.split_documents(documents)

    docs = text_splitter.split_documents(documents)

    return docs

#FUNCTION TO STORE EMBEDDINGS IN VECTOR DATABASE
def get_vector_store(docs):
    vector_store_faiss = FAISS.from_documents(docs, bedrock_embeddings)
    vector_store_faiss.save_local("faiss_index")
    return vector_store_faiss

if __name__ == "__main__":
    docs = data_ingestion()
    get_vector_store(docs)
