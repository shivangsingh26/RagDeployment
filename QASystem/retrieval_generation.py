from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.llms.bedrock import Bedrock
import boto3
from langchain.prompts import PromptTemplate
from QASystem.ingestion import get_vector_store
from QASystem.ingestion import data_ingestion
from langchain_community.embeddings import BedrockEmbeddings

bedrock=boto3.client(service_name="bedrock-runtime")
bedrock_embeddings=BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0",client=bedrock)


prompt_template = """

Human: Use the following pieces of context to provide a 
concise answer to the question at the end but usse atleast summarize with 
250 words with detailed explaantions. If you don't know the answer, 
just say that you don't know, don't try to make up an answer.
<context>
{context}
</context>

Question: {question}

Assistant:"""

PROMPT=PromptTemplate(
    template=prompt_template,input_variables=["context","question"]
)


def get_llama3_llm():
    llm=Bedrock(model_id="meta.llama3-70b-instruct-v1:0",client=bedrock)
    # llm=Bedrock(model_id="us.meta.llama3-2-1b-instruct-v1:0",client=bedrock)

    
    return llm

def get_response_llm(llm,vectorstore_faiss,query):
    qa=RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore_faiss.as_retriever(
            search_type="similarity",
            search_kwargs={"k":3}
        ),
        return_source_documents=True,
        chain_type_kwargs={"prompt":PROMPT}
    
    )
    answer=qa({"query":query})
    return answer["result"]

# def get_llama3_llm():
#     llm = Bedrock(
#         model_id="meta.llama3-70b-instruct-v1:0",
#         client=bedrock,
#         model_kwargs={
#             "temperature": 0.7,
#             "max_tokens": 2000,
#             "inference_profile": "arn:aws:bedrock:ca-central-1::foundation-model/meta.llama3-70b-instruct-v1:0"  # Replace with your ARN
#         }
#     )
#     return llm

# def get_response_llm(llm, vectorstore_faiss, query):
#     try:
#         qa = RetrievalQA.from_chain_type(
#             llm=llm,
#             chain_type="stuff",
#             retriever=vectorstore_faiss.as_retriever(
#                 search_type="similarity",
#                 search_kwargs={"k": 3}
#             ),
#             return_source_documents=True,
#             chain_type_kwargs={"prompt": PROMPT}
#         )
#         answer = qa({"query": query})
#         return answer["result"]
#     except Exception as e:
#         print(f"Error during LLM inference: {str(e)}")
#         # You might want to return a default message or raise the error
#         raise e
    

if __name__=='__main__':
    #This is a main method
    #vectorstore_faiss=get_vector_store(docs)
    faiss_index=FAISS.load_local("faiss_index",bedrock_embeddings,allow_dangerous_deserialization=True)
    query="How to answer the question Tell me about yourself?"
    llm=get_llama3_llm()
    print(get_response_llm(llm,faiss_index,query))