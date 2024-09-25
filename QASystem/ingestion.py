from langchain_community.document_loaders import PyPDFDirectoryLoader #FOR LOADING DATA
from langchain.text_splitter import RecursiveCharacterTextSplitter #FOR SPLITTING DATA INTO CHUNKS
from langchain.vectorstores import FAISS #FOR CREATING VECTOR DATABASE
from langchain_community.embeddings import BedrockEmbeddings #FOR CREATING EMBEDDINGS
from langchain.llms.bedrock import Bedrock #FOR CREATING LLM

import boto3


#BOTO CLIENT FOR CONNECTING TO AWS BEDROCK
bedrock = boto3.client(service_name="bedrock-runtime")
bedrock_embeddings = BedrockEmbeddings(model_id = "amazon.titan-embed-text-v2:0", client= bedrock)

#FUNCTION TO LOAD DATA
def data_ingestion():
    loader = PyPDFDirectoryLoader("data")
    documents = loader.load()

    text_splitter =RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    text_splitter.split_documents(documents)

    docs = text_splitter.split_documents(documents)

    return docs

#FUNCTION TO STORE EMBEDDINGS IN VECTOR DATABASE
def get_vector_store(docs):
    vector_store_faiss = FAISS.from_documents(docs, bedrock_embeddings)
    vector_store_faiss.save_local("faiss_index")


if __name__ == "__main__":
    docs = data_ingestion()
    get_vector_store(docs)
    
