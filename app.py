import json
import os 
import sys
import boto3
import streamlit as st


from langchain_community.embeddings import BedrockEmbeddings
from langchain.llms.bedrock import Bedrock

from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

from langchain.vectorstores import FAISS

from QASystem.ingestion import data_ingestion,get_vector_store

from QASystem.retrieval_generation import get_llama3_llm,get_response_llm

bedrock=boto3.client(service_name="bedrock-runtime")
bedrock_embeddings=BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0",client=bedrock)

def main():
    st.set_page_config("PDF-Q/A-Bot")
    st.header("Document Q/A Bot using AWS and Langchain")
    
    user_question=st.text_input("Ask any question from the pdf file")
    
    with st.sidebar:
        st.title("Update or Create the Vector Store")
        if st.button("Vectors Update"):
            with st.spinner("Processing..."):
                docs=data_ingestion()
                get_vector_store(docs)
                st.success("Done")
        st.title("Run LLM")

        if st.button("LLama Model"):
            with st.spinner("Processing..."):
                faiss_index=FAISS.load_local("faiss_index",bedrock_embeddings,allow_dangerous_deserialization=True)
                llm=get_llama3_llm()
                
                st.write(get_response_llm(llm,faiss_index,user_question))
                st.success("Done")
                
if __name__=="__main__":
    main()
    