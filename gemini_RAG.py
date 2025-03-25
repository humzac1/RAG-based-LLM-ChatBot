import os
from chromadb import EmbeddingFunction
from langchain_core.prompts import SystemMessagePromptTemplate
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
import langchain.chains
import pandas as pd
from pathlib import Path
from langchain.chains import ConversationalRetrievalChain
from langchain_community.document_loaders import DataFrameLoader
from langchain.chains.conversation.memory import ConversationSummaryBufferMemory
from langchain_core.prompts import PromptTemplate
import google.generativeai as genai
import getpass

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = ("Your_Gemini_API_Key")

model = genai.GenerativeModel('gemini-1.5-pro-latest')


from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent


#using langchain for RAG

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = ("Your_Langchain_API_Key")

from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings


db = Chroma(persist_directory="vector_store_gemini", embedding_function= GoogleGenerativeAIEmbeddings(model="models/embedding-001"))

#retrieves relevants chunks

retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 6})

retrieved_docs = retriever.invoke("messages")


#creates memory

from langgraph.checkpoint.sqlite import SqliteSaver
from langchain.tools import Tool

# Define the tools (need to create for memory checkpointer)
tools = [
    Tool(
        name="Calculator",
        func=lambda x: eval(x),
        description="Useful for performing mathematical calculations"
    ),

    # Add other tools as needed
]


memory = SqliteSaver.from_conn_string(":memory:")

#creation of tools were needed to fill all perameters of agent_executor

agent_executor = create_react_agent(model, tools, checkpointer=memory)

config = {"configurable": {"thread_id": "abc123"}}

#setting up RAG

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

system_prompt = (
    "This variable is made for the sake of Langchain's framework, system prompting should be done in the RAG memory-enabled agent"
    "\n\n"
    "{context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(model, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

# Combine RAG and memory functions
# Define the function to get RAG response
def get_rag_response(input_text):
    response = rag_chain.invoke({"input": input_text})
    return response["answer"]

# Integrate RAG with memory-enabled agent executor
for chunk in agent_executor.stream(
    {
        "messages": [
            HumanMessage(content=""),
                SystemMessage(content="Here is where you can system prompt the model, should be noted that all prompts human or system use up tokens")
            ]}, config # type: ignore

):
    # Integrate the RAG response into the system message
    user_input = "Human input can be done through a variable like this or an input response from the terminal using a input function"
    rag_response = get_rag_response(user_input)
    combined_response = f"{chunk}\nRAG Response: {rag_response}"

    print(combined_response)
    print("----")


